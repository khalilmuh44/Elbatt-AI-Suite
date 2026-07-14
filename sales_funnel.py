# =========================================================
# Imports
# استدعاء المكتبات والملفات المستخدمة
# =========================================================

import os
import re
from urllib.parse import urljoin

import markdown
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

from prompts.sales_funnel import build_sales_funnel_messages
from styles.components import build_whatsapp_cta
from styles.report_style import REPORT_CSS


# =========================================================
# Environment and OpenAI Client
# تحميل متغيرات البيئة وإنشاء OpenAI Client
# =========================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================================================
# Brand Assets Extraction
# استخراج شعار المتجر وبعض بيانات الهوية
# =========================================================

def is_valid_hex(color: str) -> bool:
    """
    التحقق من أن اللون HEX صحيح.

    مثال صحيح:
    #0F75CA
    """

    return bool(
        re.match(
            r"^#[0-9A-Fa-f]{6}$",
            color or ""
        )
    )


def extract_brand_assets(
    soup: BeautifulSoup,
    base_url: str
) -> dict:
    """
    استخراج بيانات الهوية الأساسية من صفحة المتجر.

    حاليًا نستخدم:
    - رابط شعار المتجر.

    الألوان محفوظة لاستخدامها مستقبلًا.
    """

    theme_color = None

    # محاولة استخراج اللون الأساسي من meta theme-color
    meta_theme = soup.find(
        "meta",
        attrs={"name": "theme-color"}
    )

    if meta_theme and meta_theme.get("content"):

        color = meta_theme.get(
            "content",
            ""
        ).strip()

        if is_valid_hex(color):
            theme_color = color


    # البحث عن ألوان HEX داخل الصفحة
    html_text = str(soup)

    hex_colors = re.findall(
        r"#[0-9A-Fa-f]{6}",
        html_text
    )


    # ألوان عامة لا نريد اعتمادها كلون للهوية
    ignored_colors = {
        "#ffffff",
        "#000000",
        "#f5f5f5",
        "#eeeeee",
        "#e5e5e5",
        "#cccccc",
        "#dddddd",
        "#f9f9f9",
        "#111111",
        "#222222"
    }


    filtered_colors = [
        color
        for color in hex_colors
        if color.lower() not in ignored_colors
    ]


    primary_color = (
        theme_color
        or (
            filtered_colors[0]
            if filtered_colors
            else "#4f46e5"
        )
    )


    secondary_color = (
        filtered_colors[1]
        if len(filtered_colors) > 1
        else "#111827"
    )


    # -----------------------------------------------------
    # استخراج شعار المتجر
    # -----------------------------------------------------

    logo_url = None


    # الأولوية الأولى:
    # صورة تحتوي كلمة logo أو شعار في alt
    logo_img = soup.find(
        "img",
        attrs={
            "alt": re.compile(
                r"logo|شعار",
                re.I
            )
        }
    )

    if logo_img and logo_img.get("src"):
        logo_url = logo_img.get("src")


    # بديل:
    # استخدام og:image لو لم نجد شعارًا واضحًا
    if not logo_url:

        og_image = soup.find(
            "meta",
            property="og:image"
        )

        if og_image and og_image.get("content"):
            logo_url = og_image.get("content")


    # تحويل الرابط النسبي إلى رابط كامل
    if logo_url:

        logo_url = urljoin(
            base_url,
            logo_url
        )


    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "logo_url": logo_url
    }


# =========================================================
# Website Scraping
# قراءة الصفحة الرئيسية وتجهيز بياناتها للتحليل
# =========================================================

def fetch_store_page(url: str) -> dict:
    """
    قراءة الصفحة الرئيسية للمتجر واستخراج
    البيانات المفيدة لتحليل Sales Funnel.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": (
            "ar-SA,ar;q=0.9,en;q=0.7"
        )
    }


    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    brand_assets = extract_brand_assets(
        soup=soup,
        base_url=url
    )


    # حذف العناصر التي لا تفيد التحليل
    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg"
        ]
    ):
        tag.decompose()


    title = (
        soup.title.get_text(
            " ",
            strip=True
        )
        if soup.title
        else ""
    )


    meta_description = ""

    meta = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta:

        meta_description = meta.get(
            "content",
            ""
        ).strip()


    headings = [
        heading.get_text(
            " ",
            strip=True
        )
        for heading in soup.find_all(
            ["h1", "h2", "h3"]
        )
        if heading.get_text(strip=True)
    ]


    links_ctas = [
        element.get_text(
            " ",
            strip=True
        )
        for element in soup.find_all(
            ["a", "button"]
        )
        if element.get_text(strip=True)
    ]


    page_text = soup.get_text(
        " ",
        strip=True
    )


    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings[:50],
        "links_ctas": links_ctas[:80],
        "page_text": page_text[:12000],
        "brand_assets": brand_assets
    }


# =========================================================
# Website Context Builder
# تحويل بيانات الموقع إلى نص منظم للـ Prompt
# =========================================================

def build_website_context(
    store_data: dict | None
) -> str:
    """
    تجهيز بيانات الموقع في شكل واضح
    لإرسالها إلى الـ Prompt.
    """

    if not store_data:

        return (
            "تعذر جلب بيانات الموقع أو لم تتوفر "
            "بيانات كافية للتحليل."
        )


    return f"""
عنوان الصفحة:
{store_data.get("title") or "لم يظهر من البيانات المتاحة"}

الوصف التعريفي:
{store_data.get("meta_description") or "لم يظهر من البيانات المتاحة"}

العناوين الرئيسية:
{store_data.get("headings") or "لم يظهر من البيانات المتاحة"}

الأزرار والدعوات لاتخاذ إجراء:
{store_data.get("links_ctas") or "لم يظهر من البيانات المتاحة"}

محتوى الصفحة:
{store_data.get("page_text") or "لم يظهر من البيانات المتاحة"}
"""


# =========================================================
# Sales Funnel Generator
# الدالة الرئيسية الخاصة بالموديول
# =========================================================

def generate_sales_funnel(
    store_name: str,
    store_url: str = "",
    store_category: str = "Other",
    biggest_challenge: str = "",
    winning_channels: list[str] | None = None,
    report_language: str = "Arabic",
    whatsapp_number: str = "",
    sales_contact_name: str = "",
    **kwargs
):
    """
    إنشاء تقرير Sales Funnel لمتجر إلكتروني سعودي.

    هذا الموديول لا يستخدم الميزانية نهائيًا.

    Parameters
    ----------
    store_name:
        اسم المتجر.

    store_url:
        رابط المتجر.

    store_category:
        مجال المتجر.

    biggest_challenge:
        أكبر تحدٍ يواجه المتجر.

    winning_channels:
        القنوات التسويقية المستخدمة حاليًا.

    report_language:
        لغة التقرير: Arabic أو English.

    whatsapp_number:
        رقم واتساب بصيغة دولية بدون علامة +.

    sales_contact_name:
        اسم مسؤول المبيعات الذي سيظهر في نهاية التقرير.
    """

    if winning_channels is None:
        winning_channels = []


    # -----------------------------------------------------
    # Website Scraping
    # -----------------------------------------------------

    store_data = None
    logo_url = None


    if store_url and store_url.strip():

        try:

            store_data = fetch_store_page(
                store_url.strip()
            )

            logo_url = (
                store_data
                .get("brand_assets", {})
                .get("logo_url")
            )

        except requests.RequestException:

            store_data = None

        except Exception:

            store_data = None


    website_context = build_website_context(
        store_data
    )


    # -----------------------------------------------------
    # Build Prompt Messages
    # لا يتم إرسال أي ميزانية
    # -----------------------------------------------------

    messages = build_sales_funnel_messages(
        store_name=store_name,
        store_url=store_url,
        store_category=store_category,
        biggest_challenge=biggest_challenge,
        marketing_channels=winning_channels,
        report_language=report_language,
        website_context=website_context
    )


    # -----------------------------------------------------
    # OpenAI Request
    # -----------------------------------------------------

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.2
    )


    report_markdown = (
        response
        .choices[0]
        .message
        .content
        or ""
    ).strip()


    if not report_markdown:

        raise ValueError(
            "The model returned an empty report."
        )


    # -----------------------------------------------------
    # Convert Markdown to HTML
    # -----------------------------------------------------

    report_html_body = markdown.markdown(
        report_markdown,
        extensions=[
            "tables",
            "sane_lists",
            "nl2br"
        ]
    )
    
    # =========================================================
# Print Page Breaks
# إجبار الأقسام الطويلة على البدء في صفحة جديدة
# =========================================================

    report_soup = BeautifulSoup(
        report_html_body,
        "html.parser"
    )

    for heading in report_soup.find_all("h2"):

        heading_text = heading.get_text(
            " ",
            strip=True
        )

        # القسم الرابع بالعربية أو الإنجليزية
        if (
            "خريطة رحلة العميل" in heading_text
            or "Customer Journey Map" in heading_text
        ):
            current_classes = heading.get(
                "class",
                []
            )

            heading["class"] = (
                current_classes
                + ["start-new-page"]
            )

    report_html_body = str(report_soup)







    # تغليف الجداول لتكون Responsive
    report_html_body = report_html_body.replace(
        "<table>",
        '<div class="table-wrapper"><table>'
    )

    report_html_body = report_html_body.replace(
        "</table>",
        "</table></div>"
    )


    # -----------------------------------------------------
    # Store Logo
    # -----------------------------------------------------

    logo_html = (
        f'<img src="{logo_url}" '
        f'class="logo" '
        f'alt="Store Logo">'
        if logo_url
        else ""
    )


    # -----------------------------------------------------
    # Dynamic WhatsApp CTA
    # إنشاء زر واتساب بالرقم واسم مسؤول المبيعات
    # -----------------------------------------------------

    whatsapp_cta_html = build_whatsapp_cta(
        whatsapp_number=whatsapp_number,
        sales_name=sales_contact_name
    )


    # -----------------------------------------------------
    # Language and Direction
    # -----------------------------------------------------

    is_arabic = (
        report_language == "Arabic"
    )

    html_dir = (
        "rtl"
        if is_arabic
        else "ltr"
    )

    html_lang = (
        "ar"
        if is_arabic
        else "en"
    )


    if is_arabic:

        report_title = (
            "مخطط قمع المبيعات"
        )

        report_subtitle = (
            f"خطة مخصصة لتحسين رحلة العميل "
            f"وزيادة مبيعات متجر {store_name}"
        )

        store_category_label = (
            f"المجال: {store_category}"
        )

        market_label = (
            "السوق المستهدف: "
            "المملكة العربية السعودية"
        )

        prepared_by = (
            "تم إعداد التقرير بواسطة Elbatt Group. "
            "جميع الحقوق محفوظة © 2026"
        )

    else:

        report_title = (
            "Sales Funnel Blueprint"
        )

        report_subtitle = (
            f"A practical customer journey and "
            f"conversion growth plan for {store_name}"
        )

        store_category_label = (
            f"Store Category: {store_category}"
        )

        market_label = (
            "Target Market: "
            "Kingdom of Saudi Arabia"
        )

        prepared_by = (
            "Prepared by Elbatt Group. "
            "All rights reserved © 2026"
        )


    # -----------------------------------------------------
    # Final HTML Template
    # -----------------------------------------------------

    html_template = f"""
<!DOCTYPE html>
<html lang="{html_lang}" dir="{html_dir}">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        {report_title} - {store_name}
    </title>

    <link
        rel="preconnect"
        href="https://fonts.googleapis.com"
    >

    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin
    >

    <link
        href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap"
        rel="stylesheet"
    >

    {REPORT_CSS}

</head>

<body>

    <div class="report">

        <div class="cover">

            {logo_html}

            <h1>
                {report_title}
            </h1>

            <p>
                {report_subtitle}
            </p>

            <p>
                {store_category_label}
            </p>

            <p>
                {market_label}
            </p>

        </div>

        <div class="content">

            {report_html_body}

            {whatsapp_cta_html}

            <div class="footer">
                {prepared_by}
            </div>

        </div>

    </div>

</body>

</html>
"""


    # -----------------------------------------------------
    # Save Local HTML Copy
    # -----------------------------------------------------

    with open(
        "sales_funnel.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            html_template
        )


    return (
        html_template,
        report_markdown
    )