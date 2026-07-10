

import os
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import markdown
from dotenv import load_dotenv  
load_dotenv()  

from styles.report_style import REPORT_CSS
from styles.components import WHATSAPP_CTA

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

################################################################

#                     Scraping and Brand Asset Extraction


################################################################


def is_valid_hex(color):
    return bool(re.match(r"^#[0-9A-Fa-f]{6}$", color))


def extract_brand_assets(soup, base_url):
    theme_color = None

    meta_theme = soup.find("meta", attrs={"name": "theme-color"})
    if meta_theme and meta_theme.get("content"):
        color = meta_theme.get("content").strip()
        if is_valid_hex(color):
            theme_color = color

    html_text = str(soup)
    hex_colors = re.findall(r"#[0-9A-Fa-f]{6}", html_text)

    ignored_colors = {
        "#ffffff", "#000000", "#f5f5f5", "#eeeeee", "#e5e5e5",
        "#cccccc", "#dddddd", "#f9f9f9", "#111111", "#222222"
    }

    filtered_colors = [
        c for c in hex_colors
        if c.lower() not in ignored_colors
    ]

    primary_color = theme_color or (filtered_colors[0] if filtered_colors else "#4f46e5")
    secondary_color = filtered_colors[1] if len(filtered_colors) > 1 else "#111827"

    logo_url = None
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        logo_url = og_image.get("content")

    if not logo_url:
        logo_img = soup.find("img", attrs={"alt": re.compile("logo|شعار", re.I)})
        if logo_img and logo_img.get("src"):
            logo_url = logo_img.get("src")

    if logo_url and logo_url.startswith("/"):
        logo_url = base_url.rstrip("/") + logo_url

    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "logo_url": logo_url
    }



def fetch_store_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    brand_assets = extract_brand_assets(soup, url)

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""

    meta_description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_description = meta.get("content", "")

    headings = [
        h.get_text(" ", strip=True)
        for h in soup.find_all(["h1", "h2", "h3"])
        if h.get_text(strip=True)
    ]

    links_ctas = [
        a.get_text(" ", strip=True)
        for a in soup.find_all(["a", "button"])
        if a.get_text(strip=True)
    ]

    page_text = soup.get_text(" ", strip=True)

    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings[:50],
        "links_ctas": links_ctas[:80],
        "page_text": page_text[:12000],
        "brand_assets": brand_assets
    }


####################################################################
#                       Paid Media Blueprint Generator
##################################################################


def generate_sales_funnel(
    store_name,
    store_url="",
    store_category="Other",
    monthly_budget=10000,
    biggest_challenge="",
    winning_channels=None,
    report_language="Arabic",
    report_theme=None,
    **kwargs
):
    """
    Generate a Paid Media Blueprint for a Saudi e-commerce store.
    """

    if winning_channels is None:
        winning_channels = []

    if report_theme is None:
        report_theme = {
            "agency_name": "البط",
            "bg_color": "#3B4757",
            "text_color": "#FFFFFF",
            "secondary_text_color": "#FEC000",
            "accent_color": "#FE5500",
        }

    # ==============================
    # Optional website scraping
    # ==============================
    store_data = None
    logo_url = None

    if store_url and store_url.strip():
        try:
            store_data = fetch_store_page(store_url.strip())
            logo_url = store_data["brand_assets"].get("logo_url")
        except Exception:
            store_data = None

    # Format winning channels for prompt
    channels_text = ", ".join(winning_channels) if winning_channels else "None selected"
    has_sales = "No Sales Yet" not in winning_channels
    budget_sar = f"{monthly_budget:,} SAR"


#############################################################

#                     OpenAI Prompt — Paid Media Blueprint


#############################################################

    # ==============================
    # Language Instructions
    # ==============================
    if report_language == "Arabic":
        language_instruction = """
        Write the entire report in professional Saudi Arabic.
        Use tables whenever possible.
        Use a business-friendly tone suitable for Saudi e-commerce store owners.
        """
    else:
        language_instruction = """
        Write the entire report in professional English.
        Use tables whenever possible.
        Use a business-friendly tone suitable for Saudi e-commerce store owners.
        """

    ############################                 System Prompt Start 
    system_prompt = f"""
You are a world-class Paid Media Strategist specializing in Saudi Arabian e-commerce.

You ONLY work with Saudi e-commerce stores.
You do NOT work with B2B companies, SaaS products, service businesses, lead generation websites, or consultation-based businesses.

{language_instruction}

==========================================================
YOUR ROLE
==========================================================

You are a senior paid media consultant creating a premium Paid Media Blueprint for a Saudi e-commerce store owner.

Your report should feel like a premium consulting playbook — not a generic media plan.

The store owner should finish reading your report and feel:
"I know exactly where to put my money next month."

==========================================================
TERMINOLOGY RULES — STRICT
==========================================================

You MUST use e-commerce terminology ONLY:
- orders, sales, revenue
- CPA (Cost Per Acquisition)
- ROAS (Return On Ad Spend)
- AOV (Average Order Value)
- cart abandonment, checkout, product pages
- repeat purchases, retention, catalog
- product feed, purchase event
- conversion rate, add to cart rate

You MUST NOT use or mention:
- B2B
- SaaS
- lead generation
- consultation requests
- client acquisition
- LinkedIn
- service pages
- qualified leads
- booking rate
- sales pipeline
- demos, trials, signups

==========================================================
CONSULTING MINDSET
==========================================================

Never write generic advice.

Every recommendation must be specific to:
- The store category
- The monthly budget
- The biggest growth challenge
- The current winning channels
- Whether the store has sales or not yet

Always explain WHY for every recommendation.

==========================================================
QUALITY RULES
==========================================================

Do not repeat ideas.
Do not contradict yourself.
Do not create filler paragraphs.
Avoid vague recommendations.
Avoid generic marketing clichés.
Make every paragraph actionable.
Keep the report short, premium, and practical.

==========================================================
ASSUMPTIONS
==========================================================

Never fabricate information.
If website information is insufficient, clearly state that it is an assumption.
Never present assumptions as facts.

==========================================================
OUTPUT STYLE
==========================================================

Write in a professional consulting style.
Write for Saudi e-commerce store owners.
Use clear business language.
Use tables whenever they improve clarity.
Output only Markdown.
Do NOT wrap the output inside markdown code blocks.
Return only the final report.
"""

    ############################                 System Prompt End 

    # ==============================
    # Build website context block (only if URL was provided and scraped)
    # ==============================
    website_context = ""
    if store_data:
        website_context = f"""
==========================================================
WEBSITE AUDIT DATA
==========================================================

Page Title:
{store_data["title"]}

Meta Description:
{store_data["meta_description"]}

Main Headings:
{store_data["headings"]}

Buttons & Calls To Action:
{store_data["links_ctas"]}

Website Content:
{store_data["page_text"]}
"""

    #####################################   Start User Prompt 
    user_prompt = f"""
==========================================================
STORE INFORMATION
==========================================================

Store Name:
{store_name}

Website URL:
{store_url if store_url else "Not provided"}

Store Category:
{store_category}

Country:
Saudi Arabia

Business Type:
E-commerce Store

Goal:
Generate more profitable sales

Monthly Growth Budget:
{budget_sar}

Biggest Growth Challenge:
{biggest_challenge}

Current Winning Channels:
{channels_text}

Store Currently Has Sales:
{"Yes" if has_sales else "No — store has no sales yet"}

{website_context}

==========================================================
REPORT STRUCTURE — STRICT
==========================================================

You MUST produce exactly 6 sections. No more, no less.
Do NOT add extra sections. Do NOT merge sections.

## 1. Executive Sales Opportunity Summary

Explain:
- Store context
- Biggest growth challenge
- What is likely blocking more sales
- Top 3 paid media priorities
- What to do first

## 2. Saudi E-commerce Funnel Blueprint

Build a paid media funnel for the store:
- TOFU (Top of Funnel)
- MOFU (Middle of Funnel)
- BOFU (Bottom of Funnel)
- Retargeting
- Retention

For each funnel stage, explain:
- Funnel stage
- Objective
- Recommended channel
- Audience
- Message angle
- KPI

Use a table format.

## 3. Budget Allocation Plan

Allocate the Monthly Growth Budget of {budget_sar} across channels.

Rules:
- Do NOT split the budget equally.
- Justify every percentage.
- Budget should depend on: store category, monthly budget, biggest challenge, current winning channels, and whether the store has sales or not.
- If no sales yet, focus more on testing and learning.
- If existing winning channels exist, build around them first.

Output as a table with columns:
Channel | Funnel Stage | Budget % | Budget SAR | Objective | Reason

## 4. Campaign Structure Blueprint

Create campaign structure by channel.

For each recommended channel include:
- Campaign name
- Campaign objective
- Ad set / ad group structure
- Audience
- Creative angle
- Optimization event
- Landing page recommendation

For Google Search / Shopping / Performance Max:
include suggested campaign/ad group logic.

For Meta / TikTok / Snapchat:
include prospecting, retargeting, and creative testing logic.

## 5. Creative & Offer Strategy

Create practical creative recommendations for Saudi e-commerce.

Include:
- 6 TOFU creative ideas (specific to the store category)
- 6 MOFU creative ideas (specific to the store category)
- 6 BOFU creative ideas (specific to the store category)
- Offer recommendations
- Messaging angles
- CTA recommendations

Do NOT write generic advice. Make ideas fit the store category "{store_category}".

## 6. 30-Day Paid Media Action Plan

Create a simple execution plan:
- Week 1
- Week 2
- Week 3
- Week 4

Each week must include:
- Actions
- Expected outcome
- KPI to watch
- Decision to make

Use a table format.

==========================================================
WRITING RULES
==========================================================

Use tables whenever they improve readability.
Never fabricate information.
Do not write generic recommendations.
Use a positive advisory tone.
Do NOT wrap the response inside markdown code blocks.
Return pure Markdown only.
"""
 
    ##################################### End User Prompt 




##############################################################
    # Send request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    # Extract the report markdown from OpenAI response
    report_markdown = response.choices[0].message.content

    # Convert Markdown tables and content to HTML
    report_html_body = markdown.markdown(
        report_markdown,
        extensions=["tables"]
    )
    
    # Wrap tables for responsive/print styling
    report_html_body = report_html_body.replace('<table>', '<div class="table-wrapper"><table>')
    report_html_body = report_html_body.replace('</table>', '</table></div>')


    # Get agency/report theme settings
    agency_name = report_theme.get("agency_name", "Ameen")
    bg_color = report_theme.get("bg_color", "#3B4757")
    text_color = report_theme.get("text_color", "#FFFFFF")
    secondary_text_color = report_theme.get("secondary_text_color", "#FEC000")
    accent_color = report_theme.get("accent_color", "#FE5500")

    # Store logo from website if available
    logo_html = (
        f'<img src="{logo_url}" class="logo" alt="Store Logo">'
        if logo_url
        else ""
    )

    html_dir = "rtl" if report_language == "Arabic" else "ltr"
    html_lang = "ar" if report_language == "Arabic" else "en"

    section_border_side = "right" if report_language == "Arabic" else "left"
    section_padding_side = "right" if report_language == "Arabic" else "left"

    # Report HTML Template
    html_template = f"""
<!DOCTYPE html>
<html lang="{html_lang}" dir="{html_dir}">
<head>
<meta charset="UTF-8">
<title>Paid Media Blueprint - {{store_name}}</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">

# <style>
# :root {{
#     --bg: {bg_color};
#     --text: {text_color};
#     --secondary-text: {secondary_text_color};
#     --accent: {accent_color};
#     --white: #FFFFFF;
#     --border: rgba(255,255,255,0.18);
# }}

# html {{
#     background: var(--bg);
#     direction: {html_dir};
# }}

# body {{
#     font-family: 'Cairo', Tahoma, Arial, sans-serif;
#     direction: {html_dir};
#     background: var(--bg);
#     color: var(--text);
#     margin: 0;
#     padding: 0;
#     text-align: {'right' if html_dir == 'rtl' else 'left'};
# }}

# .report {{
#     width: 100%;
#     max-width: 1100px;
#     margin: 0 auto;
#     background: var(--bg);
#     color: var(--text);
#     overflow: visible;
# }}

# .cover {{
#     padding: 54px 50px 36px 50px;
#     background: var(--bg);
#     color: var(--text);
#     border-bottom: 6px solid var(--accent);
# }}

# .logo {{
#     max-height: 82px;
#     max-width: 190px;
#     background: var(--white);
#     padding: 12px;
#     border-radius: 14px;
#     margin-bottom: 26px;
# }}

# .cover h1 {{
#     margin: 0;
#     font-size: 38px;
#     line-height: 1.55;
#     color: var(--text);
#     border: none;
#     padding: 0;
# }}

# .cover p {{
#     margin-top: 14px;
#     font-size: 17px;
#     color: var(--secondary-text);
# }}

# .content {{
#     padding: 45px;
#     background: var(--bg);
# }}

# h1 {{
#     color: var(--text);
#     font-size: 34px;
#     padding-bottom: 18px;
#     border-bottom: 4px solid var(--accent);
#     width: 100%;
# }}

# h2 {{
#     color: var(--secondary-text);
#     margin-top: 42px;
#     font-size: 30px;
#     border-{section_border_side}: 7px solid var(--accent);
#     padding-{section_padding_side}: 14px;
#     width: 100%;
# }}

# h3 {{
#     color: var(--text);
#     margin-top: 30px;
#     font-size: 23px;
# }}

# p, li {{
#     font-size: 18px;
#     line-height: 2;
#     color: var(--text);
# }}

# ul {{
#     padding-right: 28px;
# }}

# .table-wrapper {{
#     width: 100%;
#     overflow: visible;
#     margin: 28px 0;
# }}

# table {{
#     width: 100%;
#     table-layout: fixed;
#     border-collapse: collapse;
#     font-size: 16px;
# }}

# th {{
#     background: var(--accent);
#     color: #000000;
#     padding: 14px;
#     border: 1px solid var(--accent);
#     font-weight: 700;
#     white-space: normal;
#     overflow-wrap: break-word;
#     word-break: break-word;
# }}

# td {{
#     padding: 14px;
#     border: 1px solid var(--border);
#     background: rgba(255,255,255,0.06);
#     color: var(--text);
#     white-space: normal;
#     overflow-wrap: break-word;
#     word-break: break-word;
# }}

# tr:nth-child(even) td {{
#     background: rgba(255,255,255,0.10);
# }}

# strong {{
#     color: var(--text);
#     font-weight: 700;
# }}

# .footer {{
#     margin-top: 55px;
#     padding-top: 24px;
#     border-top: 1px solid var(--border);
#     text-align: center;
#     color: var(--secondary-text);
#     font-size: 14px;
# }}

# @page {{
#     size: A4 landscape;
#     margin: 10mm 12mm;
# }}

# @media print {{
#     html, body {{
#         width: 100%;
#         margin: 0 !important;
#         padding: 0 !important;
#         background: var(--bg) !important;
#         -webkit-print-color-adjust: exact !important;
#         print-color-adjust: exact !important;
#     }}

#     .report {{
#         width: 100% !important;
#         max-width: none !important;
#         margin: 0 !important;
#         background: var(--bg) !important;
#         overflow: visible !important;
#     }}

#     .cover {{
#         page-break-after: always !important;
#         break-after: page !important;
#     }}
    
#     h2, h3, .logo {{
#         page-break-inside: avoid !important;
#         break-inside: avoid !important;
#         page-break-after: avoid !important;
#         break-after: avoid !important;
#     }}
    
#     .table-wrapper {{
#         width: 100% !important;
#         overflow: visible !important;
#         page-break-inside: auto !important;
#         break-inside: auto !important;
#     }}
    
#     table {{
#         width: 100% !important;
#         table-layout: fixed !important;
#         page-break-inside: auto !important;
#         break-inside: auto !important;
#     }}
    
#     tr {{
#         page-break-inside: avoid !important;
#         break-inside: avoid !important;
#     }}
    
#     thead {{
#         display: table-header-group !important;
#     }}

#     table, th, td {{
#         font-size: 10px !important;
#         padding: 8px !important;
#     }}

#     .cover,
#     .content,
#     th,
#     td {{
#         -webkit-print-color-adjust: exact !important;
#         print-color-adjust: exact !important;
#     }}
    
#     * {{
#         transition: none !important;
#         animation: none !important;
#     }}
# }}
# </style>

{REPORT_CSS}
</head>

<body>
<div class="report">
    <div class="cover">
        {logo_html}
        <h1>{agency_name} — Paid Media Blueprint</h1>
        <p>Paid media growth playbook for {store_name} | {store_category} | {budget_sar}</p>
    </div>

    <div class="content">
        {report_html_body}
        {WHATSAPP_CTA}
        <div class="footer">
            Prepared by {agency_name}
        </div>
    </div>
</div>
</body>
</html>
"""

    # Save HTML locally

    with open("sales_funnel.html", "w", encoding="utf-8") as file:
        file.write(html_template)

    return html_template, report_markdown