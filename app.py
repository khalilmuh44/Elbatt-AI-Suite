import streamlit as st
from media_plan import generate_media_plan
from blueprint import generate_blueprint
from sales_funnel import generate_sales_funnel
st.set_page_config(
    page_title="Elbatt AI Suite",
    layout="wide"
)

st.image("assets/hero.png", use_container_width=True)

col1, col2 = st.columns([1, 6])

with col1:
    st.image("assets/logo.png", width=80)

with col2:
    st.title("Elbatt AI Suite")
    st.caption("AI Growth Reports Generator")

if "service" not in st.session_state:
    st.session_state.service = "media"

btn1, btn2, btn3 = st.columns(3)

with btn1:
    if st.button("📈 Media Plan", use_container_width=True):
        st.session_state.service = "media"

with btn2:
    if st.button("🚀 Business Growth Blueprint", use_container_width=True):
        st.session_state.service = "blueprint"


with btn3:
    if st.button("💰 Sales Funnel", use_container_width=True):
        st.session_state.service = "sales_funnel"

st.divider()

if st.session_state.service == "media":
    st.info("📈 You are generating an AI Media Plan")
elif st.session_state.service == "blueprint":
    st.info("🚀 You are generating a full Business Growth Blueprint")
else:
    st.info("💰 You are generating a Sales Funnel Blueprint")

store_name = st.text_input("Business / Store Name")
store_url = st.text_input("Website / Store URL")
niche = st.text_input("Business Niche")
budget = st.text_input("Monthly Budget", value="10000 SAR")

country = st.selectbox(
    "Target Country",
    ["Saudi Arabia", "UAE", "Qatar", "Kuwait"]
)

business_type = None
focus_areas = []
current_problem = None
sales_biggest_challenge = None
winning_channels = []

if st.session_state.service == "blueprint":
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
        placeholder="Example: We get traffic, but sales are still low..."
    )


if st.session_state.service == "sales_funnel":
    sales_biggest_challenge = st.text_area(
        "Biggest Growth Challenge",
        placeholder="Example: We have traffic but low sales / High CPA / No sales yet..."
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


generate = st.button("Generate Report", use_container_width=True)

if generate:
    if not store_name or not store_url or not niche or not budget:
        st.error("Please fill all required fields.")

    elif st.session_state.service == "blueprint" and not current_problem:
        st.error("Please describe the current main problem.")

    elif st.session_state.service == "blueprint" and not focus_areas:
        st.error("Please select at least one focus area.")

    elif (
        st.session_state.service == "sales_funnel"
        and not sales_biggest_challenge
    ):
        st.error("Please describe the biggest growth challenge.")

    else:
        try:
            with st.spinner("Generating report..."):

                if st.session_state.service == "media":
                    html_report, markdown_report = generate_media_plan(
                        store_name=store_name,
                        store_url=store_url,
                        niche=niche,
                        budget=budget,
                        country=country
                    )

                    file_name = "media_plan.html"

                elif st.session_state.service == "blueprint":
                    html_report, markdown_report = generate_blueprint(
                        store_name=store_name,
                        store_url=store_url,
                        niche=niche,
                        budget=budget,
                        country=country,
                        business_type=business_type,
                        main_goal=", ".join(focus_areas),
                        current_problem=current_problem
                    )

                    file_name = "business_growth_blueprint.html"

                elif st.session_state.service == "sales_funnel":

                    clean_budget = (
                        budget
                        .upper()
                        .replace("SAR", "")
                        .replace(",", "")
                        .strip()
                    )

                    monthly_budget = int(clean_budget)

                    html_report, markdown_report = generate_sales_funnel(
                        store_name=store_name,
                        store_url=store_url,
                        store_category=niche,
                        monthly_budget=monthly_budget,
                        biggest_challenge=sales_biggest_challenge,
                        winning_channels=winning_channels,
                        report_language="Arabic"
                    )

                    file_name = "sales_funnel.html"

                else:
                    st.error("Invalid report service selected.")
                    st.stop()

            st.success("Report generated successfully!")

            st.markdown(markdown_report)

            st.download_button(
                label="Download HTML Presentation",
                data=html_report,
                file_name=file_name,
                mime="text/html",
                use_container_width=True
            )

        except ValueError:
            st.error(
                "Monthly Budget must contain a valid number, "
                "for example: 10000 SAR"
            )

        except Exception as error:
            st.error(f"Report generation failed: {error}")