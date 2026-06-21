import os
import re
from openai import OpenAI
import markdown
from dotenv import load_dotenv
from media_plan import fetch_store_page

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_blueprint(store_name, store_url, niche, budget, country, business_type, main_goal, current_problem):
    store_data = fetch_store_page(store_url)
    logo_url = store_data.get("brand_assets", {}).get("logo_url")
    logo_html = f'<img src="{logo_url}" class="logo" alt="Store Logo">' if logo_url else ""
    system_prompt = """
    You are a senior Saudi growth consultant.
    Create a Business Growth Blueprint in professional Saudi Arabic.

    Important:
    The selected Focus Areas do NOT replace the report sections.
    You must always include all Blueprint sections:
    - CRO Audit
    - SEO Audit
    - Media Plan
    - Competitor Analysis
    - Growth Opportunities
    - 90-Day Roadmap

    Use the selected Focus Areas only to decide which sections deserve deeper analysis.
    The report must be customized, practical, and business-friendly.

    Include:
    - الملخص التنفيذي
    - CRO Audit
    - SEO Audit
    - Media Plan
    - Competitor Analysis
    - Growth Opportunities
    - 90-Day Roadmap
    - Quick Wins
    - Final Recommendations

    Avoid harsh criticism.
    Use advisory tone.
    Output in Markdown.
    Use tables where useful.

    When the target country is Saudi Arabia, prioritize Snapchat, Google Ads, Instagram and TikTok. Do not recommend Facebook as a primary acquisition channel unless there is a specific reason.
    Very important for the 90-Day Roadmap:
    - Do not delay ads until the second or third month.
    - The client should start running controlled ads from day 1.
    - The roadmap must run in parallel tracks:
      1. Conversion and website improvements
      2. Paid ads testing and optimization
      3. Retargeting
      4. SEO and content improvements
    - First 30 days should include launching test campaigns with controlled budget, not waiting.
    - Month 2 should focus on optimization and scaling winning campaigns.
    - Month 3 should focus on growth, automation, and expanding profitable channels.
    At the very end of the response, write this machine-readable line exactly:
    FINAL_SCORE: [number from 1 to 10]

    Important:
    - Do not mention the final score anywhere else in the report.
    - Do not write "التقييم النهائي للنمو هو" anywhere in the report.
    - The FINAL_SCORE line is only for code parsing and must not be part of the client-facing report.
    - The score can include decimals, مثل 6.5 أو 7.2.

     يجب أن تكون خطة 90 يوم واقعية وعملية. 
    لا تؤخر الإعلانات إلى الشهر الثاني أو الثالث.
    يجب أن تبدأ الحملات الإعلانية بشكل تجريبي من أول شهر بالتوازي مع تحسين الموقع.
    يجب أن تعمل التحسينات والإعلانات وإعادة الاستهداف وSEO بالتوازي وليس بشكل متسلسل.
    """
    
    example_user = """
    Business Name: متجر لوازم السيارات
    Website URL: https://example.com
    Niche: مستلزمات سيارات
    Business Type: E-commerce Store
    Monthly Budget: 20000 SAR
    Country: Saudi Arabia
    Main Goal: Increase Sales
    Current Problem: لدينا زيارات على المتجر ولكن معدل الطلبات ضعيف.
    Create a complete Business Growth Blueprint.
    """

    example_assistant = """
    # Business Growth Blueprint لمتجر لوازم السيارات

    ## 1. الملخص التنفيذي
    بعد مراجعة بيانات المتجر، يظهر أن لدى متجر لوازم السيارات فرصة جيدة للنمو داخل السوق السعودي، خصوصاً إذا تم تحسين تجربة الشراء، وضبط الرسائل الإعلانية، وربط الحملات بعروض واضحة ومقنعة.

    الهدف من هذا التقرير هو تحديد أهم فرص النمو التي يمكن العمل عليها خلال أول 90 يوم، مع ترتيب الأولويات حسب الأثر المتوقع على المبيعات.

    ---

    ## 2. تقييم النمو الحالي من 10

    | العنصر | التقييم | الملاحظة |
    |---|---:|---|
    | تجربة المستخدم داخل الموقع | 7/10 | التجربة جيدة، لكن تحتاج إلى إبراز العروض والثقة بشكل أوضح. |
    | وضوح العرض التجاري | 6/10 | العميل يحتاج أن يفهم بسرعة لماذا يشتري الآن. |
    | جاهزية الموقع للإعلانات | 7/10 | الموقع مناسب كبداية، لكن يحتاج تحسينات قبل التوسع في الإنفاق. |
    | فرص الظهور في Google | 6/10 | توجد فرص لتحسين صفحات المنتجات والمحتوى. |
    | فرص النمو خلال 90 يوم | 8/10 | توجد فرص واضحة لتحسين التحويل وزيادة المبيعات. |

   FINAL_SCORE: 7

    ---

    ## 3. CRO Audit
    أهم فرصة حالياً هي تحسين معدل التحويل داخل المتجر. الزائر قد يصل إلى الموقع، لكنه يحتاج إلى أسباب أوضح لاتخاذ قرار الشراء.

    | الملاحظة | الأثر التجاري | التوصية |
    |---|---|---|
    | العروض غير بارزة بشكل كافٍ | يقلل قرار الشراء السريع | إبراز عرض واضح أعلى الصفحة. |
    | عناصر الثقة محدودة | يقلل اطمئنان العميل | إضافة تقييمات، سياسة استبدال، وضمانات. |
    | صفحات المنتجات تحتاج تحسين | يقلل الإضافة للسلة | تحسين الصور، الوصف، والفوائد. |

    ---

    ## 4. SEO Audit
    يوجد مجال لتحسين الظهور في Google من خلال تحسين عناوين الصفحات، وصف المنتجات، وإنشاء محتوى يستهدف نية البحث الشرائية.

    | الفرصة | التوصية |
    |---|---|
    | صفحات المنتجات | تحسين العنوان والوصف والكلمات المفتاحية. |
    | التصنيفات | كتابة وصف واضح لكل تصنيف. |
    | المحتوى | إنشاء مقالات قصيرة عن أفضل المنتجات والاستخدامات. |

    ---

    ## 5. Media Plan
    بناءً على طبيعة النشاط والسوق السعودي، الأنسب هو البدء بقنوات تساعد على الطلب المباشر وإعادة الاستهداف.

    | القناة | الدور | التوصية |
    |---|---|---|
    | Snapchat | جذب زيارات مهتمة | مناسب للوصول السريع داخل السعودية. |
    | Google Search | التقاط نية الشراء | مهم جداً للمنتجات التي يبحث عنها العميل مباشرة. |
    | Instagram | بناء الثقة والظهور | مناسب للمحتوى والعروض وإعادة الاستهداف. |

    ---

    ## 6. Competitor Analysis
    المنافسة في مستلزمات السيارات تعتمد غالباً على السعر، سرعة التوصيل، وضوح جودة المنتج. لذلك يجب أن يوضح المتجر سبب اختياره مقارنة بالبدائل.

    | محور المقارنة | فرصة التحسين |
    |---|---|
    | السعر والعروض | إنشاء عروض واضحة ومحددة المدة. |
    | الثقة | إبراز تقييمات العملاء وتجارب الاستخدام. |
    | تجربة الشراء | تقليل الخطوات حتى إتمام الطلب. |

    ---

    ## 7. Growth Opportunities
    | الفرصة | الأولوية | السبب |
    |---|---|---|
    | تحسين صفحة المنتج | عالية | تؤثر مباشرة على التحويل. |
    | إطلاق حملة إعادة استهداف | عالية | تستعيد الزوار الذين لم يشتروا. |
    | تحسين Google SEO | متوسطة | يبني مصدر زيارات مستمر. |
    | عروض Bundles | عالية | تساعد في زيادة قيمة السلة. |

    ---

    ## 8. 90-Day Roadmap

    | الفترة | الهدف | الإجراءات |
    |---|---|---|
    | أول 30 يوم | تحسين التحويل + إطلاق حملات اختبار | تحسين الصفحات الأساسية، إطلاق حملات Snapchat وGoogle بميزانية اختبار، إعداد Retargeting. |
    | من 31 إلى 60 يوم | تحسين الحملات ورفع النتائج | تحليل الأداء، إيقاف الحملات الضعيفة، تحسين الإعلانات، رفع الميزانية على الحملات الرابحة. |
    | من 61 إلى 90 يوم | التوسع والنمو | توسيع القنوات الناجحة، تحسين SEO، بناء محتوى، وأتمتة المتابعة مع العملاء. |

    ---

    ## 9. Quick Wins
    - إضافة عرض واضح في أول الصفحة.
    - تحسين وصف أفضل المنتجات.
    - إضافة تقييمات العملاء.
    - إنشاء حملة Retargeting للزوار.
    - اختبار عرض Bundle لزيادة قيمة السلة.

    ---

    ## 10. التوصيات النهائية
    نوصي بالبدء بتحسين تجربة الشراء قبل زيادة الميزانية الإعلانية. بعد تنفيذ التحسينات الأساسية، يمكن توسيع الحملات تدريجياً بناءً على النتائج الفعلية.

    إذا أعجبتك هذه الرؤية، يمكن لفريق Ameen مساعدتك في تنفيذ الخطة أو عقد جلسة استراتيجية متخصصة.
    """



    user_prompt = f"""
    Business Name: {store_name}
    Website URL: {store_url}
    Niche: {niche}
    Business Type: {business_type}
    Monthly Budget: {budget}
    Country: {country}
    Selected Focus Areas: {main_goal}
    Current Problem: {current_problem}

    Website Data:
    Title: {store_data["title"]}
    Meta Description: {store_data["meta_description"]}
    Headings: {store_data["headings"]}
    CTAs: {store_data["links_ctas"]}
    Page Text: {store_data["page_text"]}

    Create a complete Business Growth Blueprint.
    """

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": example_user},
        {"role": "assistant", "content": example_assistant},
        {"role": "user", "content": user_prompt},
    ],
    temperature=0.3,
)

    report_markdown = response.choices[0].message.content

    match = re.search(
        r"FINAL_SCORE:\s*(\d+(?:\.\d+)?)",
        report_markdown
    )
    final_score = match.group(1) if match else "8"

    report_markdown = re.sub(r"FINAL_SCORE:\s*\d+(?:\.\d+)?", "", report_markdown)
    report_markdown = re.sub(r"التقييم النهائي للنمو هو:\s*\d+(?:\.\d+)?", "", report_markdown)
    report_markdown = report_markdown.strip()

    report_html_body = markdown.markdown(
        report_markdown,
        extensions=["tables"]
    )

    html_template = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="UTF-8">
    <title>Business Growth Blueprint - {store_name}</title>
    <style>
    html, body {{
        margin:0;
        padding:0;
        font-family: Tahoma, Arial, sans-serif;
        direction:rtl;
        background:#061A45;
        color:white;
    }}

    .report {{
        max-width:1100px;
        margin:auto;
        background:#061A45;
        padding-bottom:25px;
    }}

    .cover {{
        padding:42px 50px;
        background:linear-gradient(135deg,#061A45,#0B255F);
        border-bottom:5px solid #FF6A00;
        text-align:center;
    }}

    .logo {{
        max-height:80px;
        max-width:180px;
        object-fit:contain;
        background:white;
        padding:12px;
        border-radius:16px;
        margin-bottom:20px;
    }}

    h1 {{
        font-size:36px;
        color:white;
        margin:0 0 12px;
    }}

    h2 {{
        color:#FF6A00;
        border-right:6px solid #FF6A00;
        padding-right:14px;
        margin-top:28px;
        margin-bottom:14px;
    }}

    p, li {{
        font-size:17px;
        line-height:1.75;
    }}

    table {{
        width:100%;
        border-collapse:collapse;
        margin:16px 0;
    }}

    th {{
        background:#FF6A00;
        color:#061A45;
        padding:10px;
    }}

    td {{
        background:rgba(255,255,255,.07);
        border:1px solid rgba(255,255,255,.15);
        padding:10px;
    }}

    .score {{
        background:#FF6A00;
        color:#061A45;
        text-align:center;
        padding:24px;
        font-size:46px;
        font-weight:bold;
        margin:30px auto;
        max-width:350px;
        border-radius:18px;
    }}

    .content {{
        padding:30px 45px 20px;
    }}

    .footer {{
        margin-top:25px;
        padding-top:18px;
        border-top:1px solid rgba(255,255,255,.18);
        text-align:center;
        color:rgba(255,255,255,.75);
        font-size:14px;
    }}
</style>
    


    </head>
    <body>
    <div class="report">
    <div class="cover">
    {logo_html}
    <h1>🚀 Business Growth Blueprint</h1>
    <p>تقرير نمو مخصص لمشروع {store_name}</p>
     </div>
        <div class="content">
            <div class="score">{final_score}/10</div>
            {report_html_body}
            <div class="footer">
         تم إعداد هذا التقرير بواسطة شركة أمين للحلول التسويقية والنمو الرقمي
           </div>
        </div>
    </div>
    </body>
    </html>
    """

    return html_template, report_markdown