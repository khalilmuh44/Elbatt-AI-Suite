# =========================================================
# Imports
# استدعاء المكتبات والموديولات المستخدمة في التطبيق
# =========================================================

import re

import streamlit as st

from media_plan import generate_media_plan
from blueprint import generate_blueprint
from sales_funnel import generate_sales_funnel

from styles.app_style import APP_STYLE


# =========================================================
# Page Configuration
# إعدادات صفحة Streamlit
# يجب أن تكون قبل أي عنصر Streamlit آخر
# =========================================================

st.set_page_config(
    page_title="Elbatt AI Suite",
    page_icon="🦆",
    layout="wide"
)


# =========================================================
# Application Style
# تصميم واجهة التطبيق
# للتعديل على الألوان أو التنسيق:
# styles/app_style.py
# =========================================================

st.markdown(
    APP_STYLE,
    unsafe_allow_html=True
)


# =========================================================
# WhatsApp Country Codes
# الدول المتاحة لاختيار مفتاح رقم مسؤول المبيعات
# يمكن إضافة دول جديدة لاحقًا بسهولة
# =========================================================

WHATSAPP_COUNTRY_CODES = {
    "Saudi Arabia (+966)": "966",
    "Egypt (+20)": "20",
    "United Arab Emirates (+971)": "971",
    "Kuwait (+965)": "965",
    "Qatar (+974)": "974",
    "Bahrain (+973)": "973",
    "Oman (+968)": "968"
}


# =========================================================
# WhatsApp Number Normalization
# تحويل رقم الهاتف إلى الصيغة المناسبة لرابط WhatsApp
# =========================================================

def normalize_whatsapp_number(
    phone_number: str,
    country_code: str
) -> str:
    """
    Convert a local or international phone number
    into digits-only international WhatsApp format.

    Examples:

    Saudi Arabia:
    0508976543 -> 966508976543

    Egypt:
    01095351127 -> 201095351127

    International formats are also accepted:
    +966 50 897 6543 -> 966508976543
    00201095351127 -> 201095351127
    """

    # حذف كل شيء عدا الأرقام
    digits = re.sub(
        r"\D",
        "",
        phone_number or ""
    )

    if not digits:
        return ""

    # تحويل صيغة 00 الدولية:
    # 00966... تصبح 966...
    if digits.startswith("00"):
        digits = digits[2:]

    # لو المستخدم كتب الرقم كاملًا بمفتاح الدولة المختار
    # نتركه كما هو
    if digits.startswith(country_code):
        return digits

    # لو المستخدم كتب رقمًا محليًا يبدأ بصفر
    # نحذف الصفر المحلي ثم نضيف مفتاح الدولة
    local_number = digits.lstrip("0")

    if not local_number:
        return ""

    return f"{country_code}{local_number}"


# =========================================================
# Header
# لوجو التطبيق والعنوان الرئيسي
# =========================================================

logo_left, logo_center, logo_right = st.columns([4, 1, 4])

with logo_center:

    st.image(
        "assets/logo.png",
        use_container_width=True
    )

st.markdown(
    '<div class="main-title">Elbatt AI Suite</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'AI Powered Growth Reports Platform'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# Sidebar Navigation
# اختيار نوع التقرير ولغة التقرير
# =========================================================

st.sidebar.title("⚙️ Report Settings")

selected_module = st.sidebar.radio(
    "Choose Module",
    [
        "📈 Media Plan",
        "🚀 Business Growth Blueprint",
        "💰 Sales Funnel"
    ]
)

module_map = {
    "📈 Media Plan": "media",
    "🚀 Business Growth Blueprint": "blueprint",
    "💰 Sales Funnel": "sales_funnel"
}

service = module_map[selected_module]

st.sidebar.divider()


# =========================================================
# Report Language
# تحديد لغة التقرير
# =========================================================

report_language = st.sidebar.selectbox(
    "Report Language / لغة التقرير",
    [
        "Arabic",
        "English"
    ]
)


# =========================================================
# Report Contact Settings
# بيانات مسؤول المبيعات الذي سيظهر في نهاية التقرير
# =========================================================

st.sidebar.divider()

st.sidebar.subheader(
    "📞 Report Contact"
)

sales_contact_name = st.sidebar.text_input(
    "Sales Representative Name",
    placeholder="Example: Khalil"
)

selected_phone_country = st.sidebar.selectbox(
    "WhatsApp Number Country",
    list(WHATSAPP_COUNTRY_CODES.keys()),
    index=0
)

sales_whatsapp_number = st.sidebar.text_input(
    "WhatsApp Number",
    placeholder="Example: 0501234567"
)

st.sidebar.caption(
    "اكتب الرقم بصيغته المحلية أو الدولية، "
    "وسيتم تجهيزه تلقائيًا لرابط WhatsApp."
)

# الحصول على مفتاح الدولة المختارة
selected_country_code = WHATSAPP_COUNTRY_CODES[
    selected_phone_country
]

# تجهيز رقم واتساب النهائي
clean_sales_whatsapp = normalize_whatsapp_number(
    phone_number=sales_whatsapp_number,
    country_code=selected_country_code
)


# =========================================================
# Active Module Message
# توضيح نوع التقرير المختار
# =========================================================

if service == "media":

    st.info(
        "📈 You are generating an AI Media Plan"
    )

elif service == "blueprint":

    st.info(
        "🚀 You are generating a full "
        "Business Growth Blueprint"
    )

elif service == "sales_funnel":

    st.info(
        "💰 You are generating a Sales Funnel Blueprint"
    )


# =========================================================
# Shared Business Inputs
# البيانات الأساسية المشتركة بين الموديولات الحالية
# =========================================================

st.markdown(
    '<div class="section-title">Business Information</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# تقسيم بيانات المتجر إلى 3 أعمدة متساوية
# ---------------------------------------------------------

business_col1, business_col2, business_col3 = st.columns(3)

with business_col1:

    store_name = st.text_input(
        "Business / Store Name",
        placeholder="Example: Elbatt Store"
    )

with business_col2:

    store_url = st.text_input(
        "Website / Store URL",
        placeholder="https://example.com"
    )

with business_col3:

    niche = st.text_input(
        "Business Niche",
        placeholder=(
            "Example: Perfumes, Fashion, Auto Parts"
        )
    )


# =========================================================
# Shared Fixed Values
# المشروع مخصص للسوق السعودي فقط
# =========================================================

country = "Saudi Arabia"

# الميزانية تستخدم فقط في Media Plan وBlueprint
# لا تستخدم نهائيًا داخل Sales Funnel
budget = None


# =========================================================
# Budget Input
# يظهر فقط عند اختيار Media Plan أو Blueprint
# =========================================================

if service in ["media", "blueprint"]:

    budget_col1, budget_col2 = st.columns([1, 2])

    with budget_col1:

        budget = st.text_input(
            "Monthly Budget",
            value="10000 SAR",
            placeholder="Example: 10000 SAR"
        )

    with budget_col2:

        st.markdown(
            """
            <div style="
                padding: 17px 20px;
                margin-top: 28px;
                border-radius: 14px;
                background: rgba(255,255,255,.03);
                border: 1px solid rgba(255,255,255,.08);
                line-height: 1.8;
            ">
                <strong>Target Market</strong><br>
                Kingdom of Saudi Arabia
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# Default Variables
# قيم افتراضية للحقول الخاصة بكل موديول
# =========================================================

# Business Blueprint variables
business_type = None
focus_areas = []
current_problem = None

# Sales Funnel variables
sales_biggest_challenge = None
winning_channels = []


# =========================================================
# Business Growth Blueprint Inputs
# تظهر فقط عند اختيار Blueprint
# =========================================================

if service == "blueprint":

    st.markdown(
        '<div class="section-title">'
        'Blueprint Settings'
        '</div>',
        unsafe_allow_html=True
    )

    blueprint_col1, blueprint_col2 = st.columns(2)

    with blueprint_col1:

        business_type = st.selectbox(
            "Business Type",
            [
                "E-commerce Store",
                "Service Business",
                "Restaurant",
                "Clinic",
                "Real Estate",
                "Other"
            ]
        )

    with blueprint_col2:

        focus_areas = st.multiselect(
            "Blueprint Focus Areas",
            [
                "CRO Audit",
                "SEO Audit",
                "Media Plan",
                "Competitor Analysis",
                "Growth Opportunities",
                "90-Day Roadmap"
            ],
            default=[
                "CRO Audit",
                "SEO Audit",
                "Media Plan",
                "Competitor Analysis",
                "Growth Opportunities",
                "90-Day Roadmap"
            ]
        )

    current_problem = st.text_area(
        "Current Main Problem",
        placeholder=(
            "Example: We get traffic, "
            "but sales are still low..."
        ),
        height=140
    )


# =========================================================
# Sales Funnel Inputs
# تظهر فقط عند اختيار Sales Funnel
# الميزانية غير موجودة في هذا الموديول
# =========================================================

if service == "sales_funnel":

    st.markdown(
        '<div class="section-title">'
        'Sales Funnel Settings'
        '</div>',
        unsafe_allow_html=True
    )

    funnel_col1, funnel_col2 = st.columns(2)

    # -----------------------------------------------------
    # العمود الأول
    # أكبر تحدٍ يواجه المتجر
    # -----------------------------------------------------

    with funnel_col1:

        sales_biggest_challenge = st.text_area(
            "Biggest Growth Challenge",
            placeholder=(
                "Example: We have traffic but low sales, "
                "customers abandon the cart, or repeat "
                "purchases are low..."
            ),
            height=155
        )

    # -----------------------------------------------------
    # العمود الثاني
    # القنوات التسويقية المستخدمة حاليًا
    # -----------------------------------------------------

    with funnel_col2:

        winning_channels = st.multiselect(
            "Current Marketing Channels",
            [
                "No Marketing Yet",
                "Google Ads",
                "Snapchat Ads",
                "TikTok Ads",
                "Instagram / Meta Ads",
                "SEO",
                "Influencers",
                "Email Marketing",
                "WhatsApp Marketing",
                "SMS Marketing"
            ]
        )


# =========================================================
# Generate Button
# زر إنشاء التقرير
# =========================================================

generate = st.button(
    "✨ Generate Report",
    use_container_width=True
)


# =========================================================
# Report Generation
# التحقق من المدخلات وتشغيل الموديول المختار
# =========================================================

if generate:

    # -----------------------------------------------------
    # Shared Validation
    # التحقق من البيانات الأساسية
    # -----------------------------------------------------

    if not store_name.strip():

        st.error(
            "Please enter the Business / Store Name."
        )

    elif not store_url.strip():

        st.error(
            "Please enter the Website / Store URL."
        )

    elif not niche.strip():

        st.error(
            "Please enter the Business Niche."
        )


    # -----------------------------------------------------
    # Report Contact Validation
    # التحقق من بيانات مسؤول المبيعات
    # -----------------------------------------------------

    elif not sales_whatsapp_number.strip():

        st.error(
            "Please enter the WhatsApp number "
            "that should appear in the report."
        )

    elif not clean_sales_whatsapp:

        st.error(
            "Please enter a valid WhatsApp number."
        )

    elif not (
        8 <= len(clean_sales_whatsapp) <= 15
    ):

        st.error(
            "The WhatsApp number does not appear valid. "
            "Please check the selected country and number."
        )


    # -----------------------------------------------------
    # Budget Validation
    # الميزانية مطلوبة فقط في Media Plan وBlueprint
    # -----------------------------------------------------

    elif (
        service in ["media", "blueprint"]
        and (
            budget is None
            or not budget.strip()
        )
    ):

        st.error(
            "Please enter the Monthly Budget."
        )


    # -----------------------------------------------------
    # Blueprint Validation
    # -----------------------------------------------------

    elif (
        service == "blueprint"
        and not current_problem
    ):

        st.error(
            "Please describe the current main problem."
        )

    elif (
        service == "blueprint"
        and not focus_areas
    ):

        st.error(
            "Please select at least one focus area."
        )


    # -----------------------------------------------------
    # Sales Funnel Validation
    # -----------------------------------------------------

    elif (
        service == "sales_funnel"
        and not sales_biggest_challenge
    ):

        st.error(
            "Please describe the biggest growth challenge."
        )


    # -----------------------------------------------------
    # Generate Selected Report
    # -----------------------------------------------------

    else:

        try:

            with st.spinner(
                "Analyzing the business "
                "and generating the report..."
            ):

                # =========================================
                # Media Plan Module
                # =========================================

                if service == "media":

                    html_report, markdown_report = (
                        generate_media_plan(
                            store_name=store_name.strip(),
                            store_url=store_url.strip(),
                            niche=niche.strip(),
                            budget=budget.strip(),
                            country=country
                        )
                    )

                    file_name = (
                        f"{store_name.strip()}_"
                        f"media_plan.html"
                    )


                # =========================================
                # Business Growth Blueprint Module
                # =========================================

                elif service == "blueprint":

                    html_report, markdown_report = (
                        generate_blueprint(
                            store_name=store_name.strip(),
                            store_url=store_url.strip(),
                            niche=niche.strip(),
                            budget=budget.strip(),
                            country=country,
                            business_type=business_type,
                            main_goal=", ".join(
                                focus_areas
                            ),
                            current_problem=(
                                current_problem.strip()
                            )
                        )
                    )

                    file_name = (
                        f"{store_name.strip()}_"
                        f"business_blueprint.html"
                    )


                # =========================================
                # Sales Funnel Module
                # لا يستخدم أو يستقبل أي ميزانية
                # يتم إرسال بيانات مسؤول المبيعات
                # =========================================

                elif service == "sales_funnel":

                    html_report, markdown_report = (
                        generate_sales_funnel(
                            store_name=store_name.strip(),
                            store_url=store_url.strip(),
                            store_category=niche.strip(),
                            biggest_challenge=(
                                sales_biggest_challenge.strip()
                            ),
                            winning_channels=winning_channels,
                            report_language=report_language,
                            whatsapp_number=clean_sales_whatsapp,
                            sales_contact_name=(
                                sales_contact_name.strip()
                            )
                        )
                    )

                    file_name = (
                        f"{store_name.strip()}_"
                        f"sales_funnel.html"
                    )


                # =========================================
                # Unknown Module Protection
                # =========================================

                else:

                    st.error(
                        "Invalid report service selected."
                    )

                    st.stop()


            # =================================================
            # Report Output
            # عرض التقرير بعد إنشائه
            # =================================================

            st.success(
                "Report generated successfully!"
            )

            formatted_tab, markdown_tab, download_tab = (
                st.tabs(
                    [
                        "Formatted Report",
                        "Raw Markdown",
                        "Download"
                    ]
                )
            )


            # -------------------------------------------------
            # التقرير المنسق HTML
            # -------------------------------------------------

            with formatted_tab:

                st.components.v1.html(
                    html_report,
                    height=5000,
                    scrolling=True
                )


            # -------------------------------------------------
            # التقرير الخام Markdown
            # -------------------------------------------------

            with markdown_tab:

                st.markdown(
                    f"""
                    <div class="markdown-preview">
                        {markdown_report}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -------------------------------------------------
            # تحميل التقرير
            # -------------------------------------------------

            with download_tab:

                st.download_button(
                    label="Download HTML Report",
                    data=html_report,
                    file_name=file_name,
                    mime="text/html",
                    use_container_width=True
                )


        # -----------------------------------------------------
        # General Error
        # -----------------------------------------------------

        except Exception as error:

            st.error(
                f"Report generation failed: {error}"
            )