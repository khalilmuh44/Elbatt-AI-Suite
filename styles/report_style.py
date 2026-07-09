from styles.theme import *

REPORT_CSS = f"""
<style>

html, body {{
    margin: 0;
    padding: 0;
    font-family: Tahoma, Arial, sans-serif;
    direction: rtl;
    background: {DARK};
    color: {LIGHT};
}}

.report {{
    max-width: 1100px;
    margin: auto;
    background: {DARK};
    color: {LIGHT};
}}

.cover {{
    padding: 46px 50px;
    background: linear-gradient(135deg, {DARK}, {SURFACE});
    border-bottom: 6px solid {PRIMARY};
    text-align: center;
}}

.logo {{
    max-height: 90px;
    max-width: 190px;
    object-fit: contain;
    background: {LIGHT};
    padding: 12px;
    border-radius: 18px;
    margin-bottom: 22px;
}}

h1 {{
    font-size: 36px;
    color: {LIGHT};
    margin: 0 0 12px;
}}

h2 {{
    color: {PRIMARY};
    border-right: 6px solid {PRIMARY};
    padding-right: 14px;
    margin-top: 32px;
}}

h3 {{
    color: {SECONDARY};
}}

p,
li {{
    font-size: 17px;
    line-height: 1.85;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 22px 0;
    font-size: 16px;
}}

th {{
    background: {PRIMARY};
    color: #000;
    padding: 12px;
}}

td {{
    background: rgba(255,255,255,.07);
    border: 1px solid {BORDER};
    padding: 12px;
}}

tr:nth-child(even) td {{
    background: rgba(255,255,255,.11);
}}

.score,
.score-box {{
    background: {PRIMARY};
    color: #000;
    text-align: center;
    padding: 26px;
    font-size: 46px;
    font-weight: bold;
    margin: 30px auto;
    max-width: 380px;
    border-radius: 18px;
}}

.score-number {{
    font-size: 58px;
    font-weight: 700;
    color: #000;
}}

.score-label {{
    font-size: 20px;
    color: #000;
    margin-top: 8px;
}}

.content {{
    padding: 36px 45px 24px;
}}

.cta-box {{
    margin-top: 50px;
    background: rgba(255,255,255,.05);
    border: 2px solid {PRIMARY};
    border-radius: 18px;
    padding: 30px;
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
    background: #25D366;
    color: #FFFFFF;
    text-decoration: none;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    transition: .3s;
}}

.whatsapp-btn:hover {{
    background: #1EBE5D;
}}

.footer {{
    margin-top: 35px;
    padding-top: 20px;
    border-top: 1px solid {BORDER};
    text-align: center;
    color: {TEXT_MUTED};
    font-size: 14px;
}}

@page {{
    size: A4;
    margin: 0;
}}

@media print {{

    html,
    body {{
        background: {DARK} !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

    .cover,
    .score-box,
    .cta-box,
    table,
    th,
    td {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}

}}

</style>
"""