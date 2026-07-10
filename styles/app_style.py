APP_STYLE = """
<style>

/* =========================
   GLOBAL APP BACKGROUND
   ========================= */
.stApp {
    background: radial-gradient(
        circle at top left,
        #15596A 0%,
        #0F263C 35%,
        #071729 100%
    );
}

/* =========================
   MAIN TITLES
   ========================= */
.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #F1F3F4;
    margin-bottom: 6px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #2BB3BC;
    margin-bottom: 35px;
}

.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #F1F3F4;
    margin: 20px 0 28px 0;
}

/* =========================
   MAIN FORM LABELS
   ========================= */
main div[data-testid="stWidgetLabel"] p {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* =========================
   MAIN INPUTS
   ========================= */
main .stTextInput input,
main .stNumberInput input,
main .stTextArea textarea,
main div[data-baseweb="select"] > div {
    background: #16364D !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid rgba(43,179,188,.20) !important;
    border-radius: 14px !important;
    transition: all .25s ease;
}

main .stTextInput input::placeholder,
main .stTextArea textarea::placeholder {
    color: #A8BCC9 !important;
    opacity: 1 !important;
}

main div[data-baseweb="select"] span,
main div[data-baseweb="select"] div {
    color: #FFFFFF !important;
}

main .stTextInput input:focus,
main .stNumberInput input:focus,
main .stTextArea textarea:focus,
main div[data-baseweb="select"] > div:focus-within {
    border-color: #2BB3BC !important;
    box-shadow: 0 0 0 3px rgba(43,179,188,.25);
}

/* =========================
   MAIN BUTTONS
   ========================= */
div.stButton > button {
    background: linear-gradient(
        90deg,
        #2BB3BC 0%,
        #38C6D4 100%
    ) !important;

    color: #071729 !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 15px 24px !important;
    font-weight: 800 !important;
    transition: all .25s ease;
    box-shadow: 0 10px 24px rgba(43,179,188,.25);
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #38C6D4 0%,
        #52DCE5 100%
    ) !important;

    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(43,179,188,.35);
}

/* =========================
   HERO IMAGE
   ========================= */
.hero-image-wrap {
    width: min(100%, 1100px);
    height: 300px;
    margin: 25px auto 28px auto;
    overflow: hidden;
    border-radius: 22px;
    background: #0F263C;
    border: 1px solid rgba(43,179,188,.18);
    box-shadow:
        0 12px 30px rgba(7,23,41,.35),
        0 0 30px rgba(43,179,188,.08);
}

.hero-image-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    display: block;
}

.brand-header {
    text-align: center;
    margin: 0 auto 32px auto;
}

.brand-logo {
    width: 92px;
    height: 92px;
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid #2BB3BC;
    box-shadow:
        0 8px 22px rgba(7,23,41,.35),
        0 0 24px rgba(43,179,188,.18);
    margin-bottom: 14px;
}

/* =========================
   TABS
   ========================= */
main button[data-baseweb="tab"],
main button[data-baseweb="tab"] *,
main div[data-baseweb="tab-list"] button,
main div[data-baseweb="tab-list"] button * {
    color: #A8BCC9 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

main button[data-baseweb="tab"][aria-selected="true"],
main button[data-baseweb="tab"][aria-selected="true"] *,
main div[data-baseweb="tab-list"] button[aria-selected="true"],
main div[data-baseweb="tab-list"] button[aria-selected="true"] * {
    color: #2BB3BC !important;
    font-weight: 800 !important;
}

main div[data-baseweb="tab-highlight"] {
    background-color: #2BB3BC !important;
    height: 3px !important;
    border-radius: 20px !important;
}

/* =========================
   MARKDOWN PREVIEW
   ========================= */
.markdown-preview {
    background: #0F263C;
    border: 1px solid rgba(43,179,188,.15);
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 10px 28px rgba(7,23,41,.25);
}

.markdown-preview,
.markdown-preview * {
    color: #F8FAFC !important;
}

.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3 {
    color: #2BB3BC !important;
}

.markdown-preview table {
    width: 100%;
    border-collapse: collapse;
}

.markdown-preview th {
    background: #2BB3BC !important;
    color: #071729 !important;
    padding: 12px;
}

.markdown-preview td {
    background: rgba(255,255,255,.03);
    color: #F8FAFC !important;
    padding: 12px;
    border: 1px solid rgba(255,255,255,.08);
}

/* =========================
   ALERTS
   ========================= */
div[data-testid="stAlert"] {
    border-radius: 18px !important;
    border: 1px solid rgba(43,179,188,.15) !important;
    box-shadow: 0 8px 22px rgba(7,23,41,.12);
}

/* =========================
   SIDEBAR
   ========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F263C 0%,
        #0A1D2E 45%,
        #071729 100%
    ) !important;

    border-right: 1px solid rgba(43,179,188,.15);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] div[role="radiogroup"] p {
    color: #D6E3EA !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #16364D !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid rgba(43,179,188,.22) !important;
    border-radius: 14px !important;
}

section[data-testid="stSidebar"] input::placeholder,
section[data-testid="stSidebar"] textarea::placeholder {
    color: #A8BCC9 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover p {
    color: #2BB3BC !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.08) !important;
}

/* =========================
   SPINNER
   ========================= */
.stSpinner {
    padding: 18px 24px;
    border-radius: 16px;
    background: rgba(15,38,60,.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(43,179,188,.15);
}

/* =========================
   MOBILE
   ========================= */
@media (max-width: 768px) {
    main {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    section[data-testid="stSidebar"] {
        width: 82vw !important;
        min-width: 82vw !important;
        max-width: 82vw !important;
    }

    .main-title {
        font-size: 28px !important;
    }

    .sub-title {
        font-size: 14px !important;
        padding: 0 12px !important;
    }

    .section-title {
        font-size: 26px !important;
    }

    main .stTextInput input,
    main .stNumberInput input,
    main .stTextArea textarea,
    main div[data-baseweb="select"] > div {
        min-height: 48px !important;
        font-size: 15px !important;
    }

    div.stButton > button {
        min-height: 50px !important;
        font-size: 15px !important;
    }

    .markdown-preview {
        padding: 18px !important;
        overflow-x: auto !important;
    }
}
.hero-image-wrap {
    height: 190px !important;
    margin: 15px auto 22px auto !important;
    border-radius: 16px !important;
}

.brand-logo {
    width: 72px !important;
    height: 72px !important;
}
</style>
"""