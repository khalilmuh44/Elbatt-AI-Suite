# ==========================================================
# Components.py
# Reusable HTML Components
# تستخدم داخل جميع التقارير
# ==========================================================


# ==========================================================
# Dynamic WhatsApp CTA
# يستخدم في التقارير الجديدة
# ==========================================================

def build_whatsapp_cta(
    whatsapp_number: str,
    sales_name: str = ""
):
    """
    Builds a dynamic WhatsApp CTA.

    Parameters
    ----------
    whatsapp_number
        رقم واتساب بصيغة دولية

        مثال:
        966501234567

    sales_name
        اسم مسؤول المبيعات (اختياري)
    """

    # ------------------------------------------------------
    # Subtitle
    # ------------------------------------------------------

    if sales_name.strip():

        subtitle = (
            f"إذا رغبت في مناقشة هذا التقرير أو تنفيذ الخطة، "
            f"يمكنك التواصل مباشرة مع <strong>{sales_name}</strong>."
        )

    else:

        subtitle = (
            "إذا رغبت في مناقشة هذا التقرير أو تنفيذ خطة النمو، "
            "يسعد فريق شركة البط بمساعدتك."
        )

    # ------------------------------------------------------
    # WhatsApp Message
    # ------------------------------------------------------

    message = (
        "السلام عليكم، "
        "استلمت تقرير Elbatt AI Suite "
        "وأرغب في مناقشته."
    )

    return f"""
    <div class="cta-box">

        <h2>
            🚀 الخطوة التالية
        </h2>

        <p>
            {subtitle}
        </p>

        <a
            class="whatsapp-btn"
            href="https://wa.me/{whatsapp_number}?text={message}"
            target="_blank">

            💬 تواصل عبر WhatsApp

        </a>

    </div>

    """


# ==========================================================
# TEMPORARY LEGACY COMPONENT
# ==========================================================
#
# ⚠️ IMPORTANT
#
# هذا المتغير موجود فقط للحفاظ على توافق
# Media Plan و Blueprint مع النظام القديم.
#
# بعد الانتهاء من تحويل جميع الـ Modules لاستخدام:
#
#     build_whatsapp_cta(...)
#
# يجب حذف هذا الجزء بالكامل.
#
# Files currently depending on this:
#
# - media_plan.py
# - blueprint.py
#
# REMOVE AFTER ALL MODULES ARE MIGRATED.
# ==========================================================

WHATSAPP_CTA = build_whatsapp_cta(
    whatsapp_number="966541571968",
    sales_name=""
)