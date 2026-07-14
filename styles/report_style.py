# =========================================================
# Report Style
# التنسيق العام للتقارير وتنسيق الطباعة إلى PDF
# =========================================================

from styles.theme import *


REPORT_CSS = f"""
<style>

/* =======================================================
   Global Document Settings
   الإعدادات العامة للتقرير
   ======================================================= */

* {{
    box-sizing: border-box;
}}

html,
body {{
    margin: 0;
    padding: 0;
    font-family: Tahoma, Arial, sans-serif;
    direction: rtl;
    background: {DARK};
    color: {LIGHT};
}}

body {{
    overflow-x: hidden;
}}

.report {{
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    background: {DARK};
    color: {LIGHT};
}}


/* =======================================================
   Cover
   غلاف التقرير
   ======================================================= */

.cover {{
    padding: 46px 50px;
    background: linear-gradient(
        135deg,
        {DARK},
        {SURFACE}
    );
    border-bottom: 6px solid {PRIMARY};
    text-align: center;
}}

.logo {{
    display: block;
    width: auto;
    height: auto;
    max-width: 190px;
    max-height: 90px;
    object-fit: contain;
    background: {LIGHT};
    padding: 12px;
    border-radius: 18px;
    margin: 0 auto 22px;
}}


/* =======================================================
   Headings
   العناوين
   ======================================================= */

h1 {{
    margin: 0 0 12px;
    color: {LIGHT};
    font-size: 36px;
    line-height: 1.35;
}}

h2 {{
    margin-top: 36px;
    margin-bottom: 18px;
    padding-right: 14px;
    border-right: 6px solid {PRIMARY};
    color: {PRIMARY};
    line-height: 1.45;
}}

h3 {{
    margin-top: 26px;
    margin-bottom: 12px;
    color: {SECONDARY};
    line-height: 1.5;
}}

h4 {{
    margin-top: 22px;
    margin-bottom: 10px;
    line-height: 1.5;
}}


/* =======================================================
   Text
   النصوص والقوائم
   ======================================================= */

p,
li {{
    font-size: 17px;
    line-height: 1.85;
}}

p {{
    margin-top: 10px;
    margin-bottom: 14px;
}}

ul,
ol {{
    padding-right: 28px;
    padding-left: 0;
}}

li {{
    margin-bottom: 7px;
}}

strong {{
    font-weight: 700;
}}


/* =======================================================
   Report Content
   محتوى التقرير
   ======================================================= */

.content {{
    padding: 36px 45px 24px;
}}


/* =======================================================
   Tables
   الجداول
   ======================================================= */

.table-wrapper {{
    width: 100%;
    margin: 22px 0;
    overflow-x: auto;
    overflow-y: visible;
}}

table {{
    width: 100%;
    margin: 0;
    border-collapse: collapse;
    border-spacing: 0;
    table-layout: auto;
    font-size: 16px;
}}

thead {{
    display: table-header-group;
}}

tbody {{
    display: table-row-group;
}}

tfoot {{
    display: table-footer-group;
}}

tr {{
    page-break-inside: avoid;
    break-inside: avoid;
}}

th {{
    padding: 12px 10px;
    border: 1px solid {BORDER};
    background: {PRIMARY};
    color: #000000;
    text-align: center;
    vertical-align: middle;
    font-weight: 700;
    line-height: 1.45;
    overflow-wrap: anywhere;
    word-break: normal;
}}

td {{
    padding: 12px 10px;
    border: 1px solid {BORDER};
    background: rgba(255,255,255,.07);
    color: {LIGHT};
    text-align: right;
    vertical-align: middle;
    line-height: 1.55;
    overflow-wrap: anywhere;
    word-break: normal;
}}

tr:nth-child(even) td {{
    background: rgba(255,255,255,.11);
}}


/* =======================================================
   Score Boxes
   صناديق التقييم
   ======================================================= */

.score,
.score-box {{
    max-width: 380px;
    margin: 30px auto;
    padding: 26px;
    border-radius: 18px;
    background: {PRIMARY};
    color: #000000;
    text-align: center;
    font-size: 46px;
    font-weight: bold;
}}

.score-number {{
    color: #000000;
    font-size: 58px;
    font-weight: 700;
}}

.score-label {{
    margin-top: 8px;
    color: #000000;
    font-size: 20px;
}}


/* =======================================================
   WhatsApp CTA
   صندوق التواصل
   ======================================================= */

.cta-box {{
    margin-top: 50px;
    padding: 30px;
    border: 2px solid {PRIMARY};
    border-radius: 18px;
    background: rgba(255,255,255,.05);
    text-align: center;
}}

.cta-box h2 {{
    margin-top: 0;
    padding-right: 0;
    border-right: 0;
    text-align: center;
}}

.cta-box p {{
    margin-top: 15px;
    margin-bottom: 20px;
}}

.whatsapp-btn {{
    display: inline-block;
    margin-top: 18px;
    padding: 14px 30px;
    border-radius: 12px;
    background: #25D366;
    color: #FFFFFF;
    text-decoration: none;
    font-size: 18px;
    font-weight: bold;
    transition: .3s;
}}

.whatsapp-btn:hover {{
    background: #1EBE5D;
}}


/* =======================================================
   Footer
   تذييل التقرير
   ======================================================= */

.footer {{
    margin-top: 35px;
    padding-top: 20px;
    border-top: 1px solid {BORDER};
    color: {TEXT_MUTED};
    text-align: center;
    font-size: 14px;
}}


/* =======================================================
   A4 Page Settings
   إعداد صفحة PDF
   ======================================================= */

@page {{
    size: A4 portrait;
    margin: 12mm 10mm 14mm;
}}


/* =======================================================
   Print Styles
   تنسيقات الطباعة من Chrome إلى PDF
   ======================================================= */

@media print {{

    html,
    body {{
        width: 100%;
        min-height: 100%;
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
        background: {DARK} !important;
        color: {LIGHT} !important;

        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

    .report {{
        width: 100% !important;
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
        background: {DARK} !important;
    }}

    .content {{
        padding: 9mm 8mm 8mm !important;
        overflow: visible !important;
    }}


    /* ===================================================
       Cover Print Settings
       تنسيق الغلاف في الطباعة
       =================================================== */

    .cover {{
        padding: 18mm 10mm !important;
        background: linear-gradient(
            135deg,
            {DARK},
            {SURFACE}
        ) !important;

        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

    .logo {{
        max-width: 170px !important;
        max-height: 72px !important;
    }}

    h1 {{
        font-size: 30px !important;
    }}


    /* ===================================================
       Heading Page-Break Protection
       منع ظهور عنوان القسم منفصلًا عن محتواه
       =================================================== */

    h2 {{
        font-size: 23px !important;

        page-break-inside: avoid !important;
        break-inside: avoid-page !important;

        page-break-after: avoid !important;
        break-after: avoid-page !important;
    }}

    h3,
    h4 {{
        page-break-inside: avoid !important;
        break-inside: avoid-page !important;

        page-break-after: avoid !important;
        break-after: avoid-page !important;
    }}

    /*
    ربط العنوان بأول فقرة أو قائمة أو جدول بعده.
    يمنع ظهور عنوان القسم وحده في نهاية الصفحة.
    */

    h2 + p,
    h2 + ul,
    h2 + ol,
    h2 + .table-wrapper,
    h2 + table,
    h3 + p,
    h3 + ul,
    h3 + ol,
    h3 + .table-wrapper,
    h3 + table {{
        page-break-before: avoid !important;
        break-before: avoid-page !important;
    }}

    /*
    منع انفصال الفقرة الأولى بعد عنوان القسم.
    */

    h2 + p,
    h3 + p {{
        page-break-inside: avoid !important;
        break-inside: avoid-page !important;
    }}


    /* ===================================================
       Text Print Settings
       إعدادات النصوص في الطباعة
       =================================================== */

    p,
    li {{
        font-size: 13.5px !important;
        line-height: 1.7 !important;
        orphans: 3;
        widows: 3;
    }}


    /* ===================================================
       Table Print Settings
       إعدادات الجداول في الطباعة
       =================================================== */

    /*
    لا نمنع الجدول الطويل بالكامل من الانقسام؛
    لأن بعض الجداول أطول من صفحة A4.

    نسمح للجدول بالاستمرار في الصفحة التالية،
    مع منع انقسام الصف الواحد وتكرار رأس الجدول.
    */

    .table-wrapper {{
        display: block !important;
        width: 100% !important;
        margin: 14px 0 20px !important;
        overflow: visible !important;

        page-break-inside: auto !important;
        break-inside: auto !important;
    }}

    /*
    إذا جاء الجدول مباشرة بعد العنوان،
    احتفظ بالعنوان مع بداية الجدول قدر الإمكان.
    */

    h2 + .table-wrapper,
    h3 + .table-wrapper {{
        page-break-before: avoid !important;
        break-before: avoid-page !important;
    }}

    table {{
        width: 100% !important;
        margin: 0 !important;
        table-layout: auto !important;
        font-size: 12px !important;

        page-break-inside: auto !important;
        break-inside: auto !important;

        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

    /*
    تكرار رأس الجدول في كل صفحة جديدة.
    */

    thead {{
        display: table-header-group !important;
    }}

    tbody {{
        display: table-row-group !important;
    }}

    tfoot {{
        display: table-footer-group !important;
    }}

    /*
    منع انقسام الصف الواحد بين صفحتين.
    */

    tr {{
        page-break-inside: avoid !important;
        break-inside: avoid-page !important;
    }}

    th,
    td {{
        padding: 7px 6px !important;
        font-size: 12px !important;
        line-height: 1.4 !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;

        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}


    /* ===================================================
       Component Page-Break Protection
       منع تقسيم المكونات المهمة
       =================================================== */

    .score,
    .score-box,
    .cta-box,
    .footer {{
        page-break-inside: avoid !important;
        break-inside: avoid-page !important;

        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

    .score,
    .score-box {{
        margin: 20px auto !important;
        padding: 18px !important;
    }}

    .cta-box {{
        margin-top: 28px !important;
        padding: 22px !important;
    }}

    .whatsapp-btn {{
        background: #25D366 !important;
        color: #FFFFFF !important;

        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}


    /* ===================================================
       Link Print Settings
       منع ظهور رابط الزر كنص في PDF
       =================================================== */

    a[href]::after {{
        content: none !important;
    }}


    /* ===================================================
       Hidden Print Elements
       إخفاء العناصر غير المطلوبة في PDF
       =================================================== */

    button,
    .no-print {{
        display: none !important;
    }}


    .start-new-page {{
    page-break-before: always !important;
    break-before: page !important;

}}

</style>
"""