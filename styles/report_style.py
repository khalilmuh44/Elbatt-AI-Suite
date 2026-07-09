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

p, li {{
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
    color: #000000;
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

.score, .score-box {{
    background: {PRIMARY};
    color: #000000;
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
    color: #000000;
}}

.score-label {{
    font-size: 20px;
    color: #000000;
    margin-top: 8px;
}}

.content {{
    padding: 36px 45px 24px;
}}

.footer {{
    margin-top: 35px;
    padding-top: 20px;
    border-top: 1px solid {BORDER};
    text-align: center;
    color: {TEXT_MUTED};
    font-size: 14px;
}}
</style>
"""