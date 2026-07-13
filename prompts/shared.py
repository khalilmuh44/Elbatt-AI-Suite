def get_language_rules(report_language: str) -> str:
    if report_language == "Arabic":
        return """
==========================================================
قواعد اللغة العربية — إلزامية
==========================================================

- اكتب التقرير بالكامل بالعربية المهنية الواضحة المناسبة لصاحب متجر سعودي.
- استخدم العربية في جميع العناوين والجداول والتوصيات وأسماء الحقول.
- لا تستخدم الإنجليزية إلا لأسماء المنصات والمنتجات والمصطلحات التي لا يوجد لها بديل عربي عملي، مثل:
  Google Ads, TikTok, Snapchat, Meta Ads, WhatsApp, Apple Pay, Tabby, Tamara.
- عند استخدام مقياس تسويقي لأول مرة، اكتبه بالعربية ثم الإنجليزية بين قوسين، مثل:
  معدل التحويل (Conversion Rate).
- بعد ذلك استخدم المصطلح العربي فقط.
- لا تكتب عناوين مثل Audience أو Objective أو Landing Page Recommendation بالإنجليزية.
- استخدم بدلًا منها:
  الجمهور المستهدف، الهدف، توصية صفحة الهبوط، زاوية الرسالة، مؤشر الأداء.
- لا تخلط العربية والإنجليزية داخل الجملة إلا عند الضرورة.
- لا تستخدم كلمات معرّبة مثل كمبين أو كريتيف أو أودينس.
- اجعل كل توصية في سطر مستقل.
- ضع سطرًا فارغًا بين الفقرات والأقسام.
"""
    
    return """
==========================================================
ENGLISH LANGUAGE RULES
==========================================================

- Write the entire report in professional business English.
- Use clear headings and field labels.
- Put every recommendation on a separate line.
- Add blank lines between paragraphs and sections.
- Avoid dense paragraphs containing multiple labeled items.
"""


FACTUALITY_RULES = """
==========================================================
FACTUALITY RULES
==========================================================

- Never fabricate store information.
- Never claim that an element exists on the website unless it appears in the supplied website data.
- If information is unavailable, state clearly that it could not be confirmed.
- Clearly distinguish between:
  1. Confirmed observations.
  2. Reasonable assumptions.
  3. Recommendations requiring verification.
- Never invent conversion rates, sales figures, order values, benchmarks, customer behavior, or campaign performance.
"""


MARKDOWN_RULES = """
==========================================================
MARKDOWN FORMATTING RULES
==========================================================

- Output pure Markdown only.
- Do not use Markdown code fences.
- Use Markdown tables only for comparisons and structured plans.
- Use bullet lists for recommendations.
- Never write several labeled fields in one paragraph separated by hyphens.
- Do not create excessively wide tables.
- Keep table columns concise.
- Every section must have a clear Markdown heading.
- Add one blank line before and after every table.
"""