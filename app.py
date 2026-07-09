import streamlit as st
from media_plan import generate_media_plan
from blueprint import generate_blueprint

st.set_page_config(
    page_title="Elbatt AI Suite",
    layout="wide"
)

st.image(
    "assets/hero.png",
    use_container_width=True
)

col1, col2 = st.columns([1,6])

with col1:
    st.image("assets/logo.png", width=80)

with col2:
    st.title("Elbatt AI Suite")
    st.caption("AI Growth Reports Generator")

st.divider()

if st.session_state.service == "media":
    st.info("📈 You are generating an AI Media Plan")
else:
    st.info("🚀 You are generating a full Business Growth Blueprint")

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

generate = st.button("Generate Report", use_container_width=True)

if generate:
    if not store_name or not store_url or not niche or not budget:
        st.error("Please fill all required fields.")

    elif st.session_state.service == "blueprint" and not current_problem:
        st.error("Please describe the current main problem.")

    elif st.session_state.service == "blueprint" and not focus_areas:
        st.error("Please select at least one focus area.")

    else:
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

            else:
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

        st.success("Report generated successfully!")
        st.markdown(markdown_report)

        st.download_button(
            label="Download HTML Presentation",
            data=html_report,
            file_name=file_name,
            mime="text/html",
            use_container_width=True
        )