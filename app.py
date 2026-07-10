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
# تطبيق CSS الخاص بواجهة التطبيق
# للتعديل على شكل الواجهة:
# styles/app_style.py
# =========================================================

st.markdown(
    APP_STYLE,
    unsafe_allow_html=True
)


# =========================================================
# Header
# اللوجو واسم التطبيق
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
# اختيار الموديول وإعدادات التقرير
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


# ربط اسم الموديول الظاهر بالقيمة المستخدمة داخل الكود
module_map = {
    "📈 Media Plan": "media",
    "🚀 Business Growth Blueprint": "blueprint",
    "💰 Sales Funnel": "sales_funnel"
}

service = module_map[selected_module]


st.sidebar.divider()


# لغة التقرير
# حاليًا يتم تمريرها إلى Sales Funnel.
# لاحقًا نربطها بباقي الموديولات.
report_language = st.sidebar.selectbox(
    "Report Language / لغة التقرير",
    [
        "Arabic",
        "English"
    ]
)


# =========================================================
# Active Module Message
# الرسالة التي توضح نوع التقرير المختار
# =========================================================

if service == "media":
    st.info("📈 You are generating an AI Media Plan")

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
# البيانات المشتركة بين جميع الموديولات
# =========================================================

st.markdown(
    '<div class="section-title">Business Information</div>',
    unsafe_allow_html=True
)

form_col1, form_col2 = st.columns(2)


# العمود الأول
with form_col1:

    store_name = st.text_input(
        "Business / Store Name",
        placeholder="Example: Elbatt Store"
    )

    store_url = st.text_input(
        "Website / Store URL",
        placeholder="https://example.com"
    )

    niche = st.text_input(
        "Business Niche",
        placeholder=(
            "Example: Perfumes, Fashion, Auto Parts"
        )
    )


# العمود الثاني
with form_col2:

    budget = st.text_input(
        "Monthly Budget",
        value="10000 SAR",
        placeholder="Example: 10000 SAR"
    )

    country = st.selectbox(
        "Target Country",
        [
            "Saudi Arabia",
            "UAE",
            "Qatar",
            "Kuwait"
        ]
    )


# =========================================================
# Default Variables
# قيم افتراضية للمدخلات الخاصة بالموديولات
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
# تظهر فقط عند اختيار Business Growth Blueprint
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
# =========================================================

if service == "sales_funnel":

    st.markdown(
        '<div class="section-title">'
        'Sales Funnel Settings'
        '</div>',
        unsafe_allow_html=True
    )

    sales_biggest_challenge = st.text_area(
        "Biggest Growth Challenge",
        placeholder=(
            "Example: We have traffic but low sales, "
            "high CPA, or no sales yet..."
        ),
        height=140
    )

    winning_channels = st.multiselect(
        "Current Winning Channels",
        [
            "No Sales Yet",
            "Google Ads",
            "Snapchat Ads",
            "TikTok Ads",
            "Instagram / Meta Ads",
            "SEO",
            "Influencers",
            "Email / WhatsApp",
            "Other"
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
# Budget Cleaning Function
# تحويل الميزانية من نص مثل:
# 10,000 SAR
# إلى رقم:
# 10000
# =========================================================

def parse_budget(budget_text):
    """
    Convert a budget string into an integer.

    Examples:
    10000 SAR -> 10000
    10,000 -> 10000
    SAR 15000 -> 15000
    """

    cleaned_budget = re.sub(
        r"[^0-9.]",
        "",
        str(budget_text)
    )

    if not cleaned_budget:
        raise ValueError("Invalid budget")

    return int(float(cleaned_budget))


# =========================================================
# Report Generation
# تشغيل الموديول المختار وإنشاء التقرير
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

    elif not budget.strip():
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
                # =========================================

                elif service == "sales_funnel":

                    monthly_budget = parse_budget(
                        budget
                    )

                    html_report, markdown_report = (
                        generate_sales_funnel(
                            store_name=store_name.strip(),
                            store_url=store_url.strip(),
                            store_category=niche.strip(),
                            monthly_budget=monthly_budget,
                            biggest_challenge=(
                                sales_biggest_challenge.strip()
                            ),
                            winning_channels=winning_channels,
                            report_language=report_language
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


            # التقرير المنسق HTML
            with formatted_tab:

                st.components.v1.html(
                    html_report,
                    height=5000,
                    scrolling=True
                )


            # التقرير الخام Markdown
            with markdown_tab:

                st.markdown(
                    f"""
                    <div class="markdown-preview">
                        {markdown_report}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # تحميل التقرير
            with download_tab:

                st.download_button(
                    label="Download HTML Report",
                    data=html_report,
                    file_name=file_name,
                    mime="text/html",
                    use_container_width=True
                )


        # -----------------------------------------------------
        # Invalid Budget Error
        # -----------------------------------------------------

        except ValueError:

            st.error(
                "Monthly Budget must contain "
                "a valid number. Example: 10000 SAR"
            )


        # -----------------------------------------------------
        # General Error
        # -----------------------------------------------------

        except Exception as error:

            st.error(
                f"Report generation failed: {error}"
            )