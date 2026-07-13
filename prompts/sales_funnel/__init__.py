# =========================================================
# Imports
# استدعاء أجزاء Prompt الخاصة بموديول Sales Funnel
# =========================================================

from prompts.sales_funnel.example import get_output_example
from prompts.sales_funnel.system import build_system_prompt
from prompts.sales_funnel.user import build_user_prompt


# =========================================================
# Sales Funnel Messages Builder
# تجميع System Prompt + Example + User Prompt
# =========================================================

def build_sales_funnel_messages(
    store_name: str,
    store_url: str,
    store_category: str,
    biggest_challenge: str,
    marketing_channels: list[str],
    report_language: str,
    website_context: str
) -> list[dict]:
    """
    Build the complete message list for the Sales Funnel module.

    This module does not use any budget input.
    """

    # -----------------------------------------------------
    # System Prompt
    # شخصية النموذج وقواعد التحليل
    # -----------------------------------------------------

    system_prompt = build_system_prompt(
        report_language=report_language
    )


    # -----------------------------------------------------
    # Assistant Example
    # مثال قصير يوضح شكل التقرير فقط
    # -----------------------------------------------------

    output_example = get_output_example(
        report_language=report_language
    )


    # -----------------------------------------------------
    # User Prompt
    # بيانات المتجر وهيكل التقرير المطلوب
    # -----------------------------------------------------

    user_prompt = build_user_prompt(
        store_name=store_name,
        store_url=store_url,
        store_category=store_category,
        biggest_challenge=biggest_challenge,
        marketing_channels=marketing_channels,
        report_language=report_language,
        website_context=website_context
    )


    # -----------------------------------------------------
    # Final Messages
    # الرسائل التي سيتم إرسالها إلى OpenAI
    # -----------------------------------------------------

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "assistant",
            "content": output_example
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]