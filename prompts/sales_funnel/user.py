# =========================================================
# Imports
# =========================================================

from prompts.sales_funnel.sections import get_report_sections


# =========================================================
# User Prompt Builder
# إنشاء User Prompt الخاص بموديول Sales Funnel
# =========================================================

def build_user_prompt(
    store_name: str,
    store_url: str,
    store_category: str,
    biggest_challenge: str,
    marketing_channels: list[str],
    report_language: str,
    website_context: str
) -> str:
    """
    Build the user prompt for the Sales Funnel report.

    This module focuses on:
    - Customer Journey
    - Conversion
    - Funnel Leaks
    - Retention

    It does NOT use advertising budgets.
    """

    # -----------------------------------------------------
    # Marketing Channels
    # -----------------------------------------------------

    channels_text = (
        ", ".join(marketing_channels)
        if marketing_channels
        else "No current marketing channels were selected."
    )


    # -----------------------------------------------------
    # Report Structure
    # -----------------------------------------------------

    report_sections = get_report_sections(
        report_language
    )


    # -----------------------------------------------------
    # Final Prompt
    # -----------------------------------------------------

    return f"""
==========================================================
STORE INFORMATION
==========================================================

Store Name:
{store_name}

Website URL:
{store_url or "Not provided"}

Store Category:
{store_category}

Target Market:
Kingdom of Saudi Arabia

Business Type:
E-commerce Store Selling Physical Products

Primary Goal:
Increase profitable online sales through customer journey optimization.

Biggest Growth Challenge:
{biggest_challenge}

Current Marketing Channels:
{channels_text}

==========================================================
AVAILABLE WEBSITE DATA
==========================================================

{website_context if website_context else "No website data was successfully retrieved."}

==========================================================
ANALYSIS INSTRUCTIONS
==========================================================

Analyze the actual website before making recommendations.

Separate:

- Confirmed observations
- Assumptions
- Opportunities

Never present an assumption as a confirmed fact.

Focus on:

- Customer Journey
- Conversion Optimization
- Funnel Leaks
- Trust
- Product Experience
- Checkout Experience
- Retention
- Repeat Purchases

Recommend only the marketing channels that truly fit the store.

Do NOT recommend every platform.

Do NOT generate:

- Media Budget Allocation
- Campaign Budgets
- ROAS Forecasts
- Media Buying Plans

Those belong to the Media Plan module.

Avoid duplicate recommendations.

Keep the report practical, concise, and suitable for Saudi e-commerce store owners.

{report_sections}
"""