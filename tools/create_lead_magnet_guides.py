from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf"
ASSETS = ROOT / "assets"

WIDTH, HEIGHT = letter
NAVY = colors.HexColor("#0B1F3A")
NAVY_2 = colors.HexColor("#15395F")
GOLD = colors.HexColor("#C99A3A")
GOLD_2 = colors.HexColor("#E4BD68")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#D9E2EC")
SOFT = colors.HexColor("#F5F8FB")
SOFT_BLUE = colors.HexColor("#EAF1F8")
WHITE = colors.white

PHONE = "(402) 237-6592"
WEBSITE = "helmsretirement.com"
BOOK_URL = "https://calendly.com/helmsretirement"
LOGO = ASSETS / "helms-logo.png"
HEADSHOT = ASSETS / "headshot_1.jpg"
TMP = ROOT / "tmp"
PROFILE_IMAGE = TMP / "guide-profile-headshot.png"


GUIDES = [
    {
        "id": "medicare",
        "title": "The Medicare Timeline Guide",
        "short_title": "Medicare Timeline Guide",
        "filename": "medicare-timeline-guide-helms-retirement-solutions.pdf",
        "hook": "A 10-minute workbook to organize your Medicare enrollment timeline, doctors, prescriptions, and coverage questions before deadlines sneak up on you.",
        "inside": [
            ("Timeline Worksheet", "Mark what needs attention 12 months, 6 months, and 3 months out."),
            ("Coverage Checklist", "Doctors, prescriptions, pharmacy preference, and open questions in one place."),
        ],
        "mistake": "Waiting too long on Medicare.",
        "mistake_body": "Enrollment windows, drug coverage, and carrier choices deserve a timeline - not a scramble. Missing a deadline can mean permanent penalties or gaps in coverage. This guide gives you a simple way to get ahead of it.",
        "worksheet_title": "What Is My Medicare Timeline?",
        "worksheet_intro": "Use this page to mark what needs attention before, during, and after Medicare enrollment.",
        "timeline": [
            ("12 months", "Gather doctors, medications, and current coverage."),
            ("6 months", "Compare Medicare paths and prescription needs."),
            ("3 months", "Confirm enrollment timing and plan details."),
            ("Annual review", "Review changes in plans, drugs, doctors, and costs."),
        ],
        "lines": ["Doctors I want to keep", "Prescriptions I take", "Pharmacy preference", "Coverage questions"],
        "readiness_title": "How Ready Am I on Medicare?",
        "readiness": [
            "I understand my Medicare timeline.",
            "I have reviewed prescription and doctor needs.",
            "I know my enrollment window dates.",
            "I understand the difference between my coverage options.",
            "I know who to ask when questions come up.",
        ],
        "review_steps": [
            ("Medicare Review", "Review doctors, prescriptions, timing, and coverage questions."),
            ("Timeline Mapping", "Know exactly which dates matter for your situation."),
            ("Recommendations", "Leave with clear next steps and options that fit you."),
        ],
        "cta_title": "Claim Your Medicare Timeline Review",
        "cta_items": ["Medicare enrollment timing", "Doctor and prescription coverage", "Plan comparison questions", "Costs and what to expect"],
        "disclaimer": "Not affiliated with or endorsed by the U.S. government or the federal Medicare program. We do not offer every plan available in your area.",
    },
    {
        "id": "social-security",
        "title": "The Social Security & Income Guide",
        "short_title": "Social Security & Income Guide",
        "filename": "social-security-income-guide-helms-retirement-solutions.pdf",
        "hook": "A 10-minute workbook to organize your retirement income sources and compare Social Security claiming questions before the decision is made for you.",
        "inside": [
            ("Income Worksheet", "List each income source and see your estimated monthly total."),
            ("Claiming Age Comparison", "Compare claiming at 62, full retirement age, and 70."),
        ],
        "mistake": "Guessing at monthly income.",
        "mistake_body": "Retirement gets easier when every income source has a job. Most people estimate, and estimates are how gaps happen. This guide gives you a simple way to see the real number.",
        "worksheet_title": "Do I Have Enough Income?",
        "worksheet_intro": "List your expected monthly income. The goal is not perfection - it is clarity.",
        "income_rows": ["Social Security", "Pension", "IRA/401(k) withdrawals", "Annuity income", "Part-time work", "Other", "Total estimated monthly income"],
        "second_title": "When Should I Claim Social Security?",
        "second_intro": "Social Security decisions can affect monthly income for life. Use this worksheet to compare three claiming ages.",
        "claim_rows": ["62", "Full retirement age", "70"],
        "readiness_title": "Income Planning Check",
        "readiness": [
            "I have listed my expected monthly income sources.",
            "I know my estimated monthly spending need.",
            "I have compared Social Security claiming ages.",
            "I understand which questions need a second opinion.",
        ],
        "review_steps": [
            ("Income Review", "Look at your expected retirement income and monthly spending needs."),
            ("Social Security Timing", "Talk through claiming strategies that fit your situation."),
            ("Recommendations", "Leave with clear next steps and options that fit you."),
        ],
        "cta_title": "Claim Your Income & Social Security Review",
        "cta_items": ["Retirement income sources", "Social Security claiming timing", "Monthly income vs. expenses", "Gaps or open questions"],
        "disclaimer": "Not affiliated with or endorsed by the U.S. government or the federal Medicare program. We do not offer every plan available in your area.",
    },
    {
        "id": "tax",
        "title": "The Retirement Tax Guide",
        "short_title": "Retirement Tax Guide",
        "filename": "retirement-tax-guide-helms-retirement-solutions.pdf",
        "hook": "A 10-minute workbook to spot tax surprises that catch retirees off guard - before withdrawals begin, not after.",
        "inside": [
            ("Budget Worksheet", "Estimate what retirement may actually cost each month."),
            ("Tax Checklist", "Seven questions to answer before pulling from accounts."),
        ],
        "mistake": "Ignoring taxes.",
        "mistake_body": "Withdrawals, Social Security, and account types can change the tax picture in ways people do not see coming until the bill arrives. This guide helps you spot questions worth asking a tax professional.",
        "worksheet_title": "What Will Retirement Cost Each Month?",
        "worksheet_intro": "Estimate the expenses that continue into retirement.",
        "budget_rows": [("Housing", "Utilities"), ("Groceries", "Transportation"), ("Health care", "Insurance"), ("Debt", "Travel/fun"), ("Giving", "Other")],
        "readiness_title": "What Could Surprise Me at Tax Time?",
        "readiness": [
            "I know which accounts are taxable, tax-deferred, and tax-free.",
            "I have discussed whether Social Security may be taxable.",
            "I understand required minimum distribution timing.",
            "I have reviewed Roth conversion questions with a tax professional.",
            "I know how pension, annuity, or IRA income may be withheld.",
            "I have a plan for charitable giving or beneficiary tax questions.",
            "I know which tax records to keep for health and insurance costs.",
        ],
        "review_steps": [
            ("Budget Review", "Compare your expected costs against your expected income."),
            ("Tax Discussion", "Identify tax questions to bring to your tax professional before decisions are made."),
            ("Recommendations", "Leave with clear next steps and options that fit you."),
        ],
        "cta_title": "Claim Your Tax Readiness Review",
        "cta_items": ["Monthly retirement budget", "Tax questions on withdrawals", "Account types and timing", "Records to keep"],
        "disclaimer": "Not affiliated with or endorsed by the U.S. government or the federal Medicare program. This is not tax advice - consult a qualified tax professional.",
    },
    {
        "id": "family-protection",
        "title": "The Family Protection Guide",
        "short_title": "Family Protection Guide",
        "filename": "family-protection-guide-helms-retirement-solutions.pdf",
        "hook": "A 10-minute workbook to get your beneficiaries, documents, and family plan organized so nothing is left vague for the people you love.",
        "inside": [
            ("Protection Checklist", "Seven items to confirm beneficiaries, documents, and directives are in order."),
            ("Readiness Score", "See where you stand and what to tackle first."),
        ],
        "mistake": "Leaving family protection vague.",
        "mistake_body": "Life insurance, final expense, beneficiaries, and documents should line up, but most families never sit down and check. This guide gives you a simple way to see what is handled and what is not.",
        "worksheet_title": "Is My Family Protection Organized?",
        "worksheet_intro": "This is not legal advice. Use the checklist to decide what to review with qualified professionals.",
        "readiness_title": "How Ready Am I?",
        "readiness": [
            "Beneficiaries are current on life insurance, retirement accounts, and annuities.",
            "My spouse or family knows where important documents are stored.",
            "I have reviewed final expense needs and funeral preferences.",
            "I have considered power of attorney and health care directive documents.",
            "My will or trust has been reviewed recently.",
            "My emergency contacts and account list are updated.",
            "I know who should be involved in a family planning conversation.",
        ],
        "score_items": [
            "My beneficiary information is current.",
            "My spouse or family understands the plan.",
            "I have a 90-day action plan for what is left.",
        ],
        "review_steps": [
            ("Protection Review", "Talk through beneficiaries, documents, and coverage gaps."),
            ("Risk Analysis", "Talk through health cost concerns and protection gaps."),
            ("Recommendations", "Leave with clear next steps and options that fit you."),
        ],
        "cta_title": "Claim Your Family Protection Review",
        "cta_items": ["Beneficiaries and documents", "Estate planning", "Legacy planning", "Final expense needs"],
        "disclaimer": "Not affiliated with or endorsed by the U.S. government or the federal Medicare program. This is not legal advice - consult qualified professionals.",
    },
]


def style(size=10, color=INK, bold=False, leading=None, align="LEFT"):
    return ParagraphStyle(
        "p",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment={"LEFT": 0, "CENTER": 1, "RIGHT": 2}[align],
        spaceAfter=0,
    )


def para(c, text, x, y, width, size=10, color=INK, bold=False, leading=None, align="LEFT"):
    p = Paragraph(text, style(size=size, color=color, bold=bold, leading=leading, align=align))
    _, h = p.wrap(width, 700)
    p.drawOn(c, x, y - h)
    return y - h


def wrapped(c, text, x, y, width, font="Helvetica", size=10, leading=14, color=INK):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def footer(c, guide, page_num):
    c.setStrokeColor(LINE)
    c.line(42, 42, WIDTH - 42, 42)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(42, 29, "Helping Families Retire With Confidence")
    c.drawString(42, 17, f"Helms Retirement Solutions | {PHONE} | {WEBSITE}")
    c.drawRightString(WIDTH - 42, 26, f"{guide['short_title']} | Page {page_num}")


def header(c, guide, eyebrow, page_title, page_num):
    c.setFillColor(NAVY)
    c.rect(0, HEIGHT - 94, WIDTH, 94, fill=1, stroke=0)
    c.setFillColor(GOLD_2)
    c.rect(0, HEIGHT - 98, WIDTH, 4, fill=1, stroke=0)
    if LOGO.exists():
        c.drawImage(str(LOGO), 42, HEIGHT - 84, width=190, height=54, preserveAspectRatio=True, mask="auto")
    c.setFillColor(GOLD_2)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(WIDTH - 42, HEIGHT - 66, eyebrow.upper())
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawRightString(WIDTH - 42, HEIGHT - 42, page_title)
    footer(c, guide, page_num)


def card(c, x, y, w, h, fill=WHITE, stroke=LINE):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y - h, w, h, 8, fill=1, stroke=1)


def section_label(c, x, y, text, w=146):
    c.setFillColor(GOLD)
    c.roundRect(x, y - 22, w, 24, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w / 2, y - 15, text.upper())


def checkbox(c, x, y, label, width=440):
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.rect(x, y - 11, 11, 11, fill=0, stroke=1)
    wrapped(c, label, x + 20, y - 1, width, size=9.4, leading=12, color=INK)


def answer_line(c, x, y, label, width=480):
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y + 5, label.upper())
    c.setStrokeColor(LINE)
    c.line(x, y - 8, x + width, y - 8)


def qr_code(c, x, y, size, value):
    code = qr.QrCodeWidget(value)
    bounds = code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    d.add(code)
    renderPDF.draw(d, c, x, y - size)


def prepare_profile_image():
    if not HEADSHOT.exists():
        return None

    TMP.mkdir(parents=True, exist_ok=True)
    image = Image.open(HEADSHOT).convert("RGBA")
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = max(0, int((height - side) * 0.38))
    image = image.crop((left, top, left + side, top + side)).resize((320, 320), Image.LANCZOS)

    mask = Image.new("L", (320, 320), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 319, 319), fill=255)

    output = Image.new("RGBA", (320, 320), (255, 255, 255, 0))
    output.paste(image, (0, 0), mask)
    output.save(PROFILE_IMAGE)
    return PROFILE_IMAGE


def cover(c, guide):
    c.setFillColor(NAVY)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    c.setFillColor(NAVY_2)
    c.circle(WIDTH - 70, HEIGHT - 80, 175, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, HEIGHT - 150, WIDTH, 7, fill=1, stroke=0)
    if LOGO.exists():
        c.drawImage(str(LOGO), 48, HEIGHT - 116, width=280, height=82, preserveAspectRatio=True, mask="auto")

    section_label(c, 48, HEIGHT - 185, "Free Workbook")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 43)
    title_lines = guide["title"].replace("The ", "The|").replace(" & ", " &|").split("|")
    y = HEIGHT - 254
    for line in [line.strip() for line in title_lines if line.strip()]:
        c.drawString(48, y, line)
        y -= 50
    para(c, guide["hook"], 50, y - 12, 440, size=14, leading=20, color=colors.HexColor("#E8EEF6"))

    y = 288
    for idx, (title, body) in enumerate(guide["inside"]):
        x = 48 + idx * 256
        card(c, x, y, 230, 116, fill=colors.HexColor("#F8FBFF"), stroke=colors.HexColor("#F8FBFF"))
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x + 22, y - 38, title)
        wrapped(c, body, x + 22, y - 64, 178, size=10.3, leading=14, color=MUTED)

    c.setFillColor(GOLD_2)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48, 104, "Helms Retirement Solutions")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    c.drawString(48, 82, f"{PHONE} | {WEBSITE}")
    c.setFont("Helvetica", 8.5)
    c.drawString(48, 54, "Educational information only. Not affiliated with or endorsed by the U.S. government or the federal Medicare program.")


def mistake_page(c, guide):
    header(c, guide, "Start Here", "The #1 Mistake", 2)
    section_label(c, 58, 660, "Start Here", 118)
    para(c, guide["mistake"], 58, 600, 496, size=26, leading=31, color=NAVY, bold=True)
    para(c, guide["mistake_body"], 58, 500, 496, size=13.5, leading=20, color=INK)
    card(c, 58, 342, 496, 116, fill=SOFT_BLUE)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(82, 300, "Use this guide to answer one question at a time.")
    wrapped(c, "No walls of text. No pressure. Just the facts, checklists, and notes you need for a better retirement conversation.", 82, 274, 430, size=11, leading=16, color=MUTED)
    answer_line(c, 58, 168, "The biggest question I want answered", 496)


def table(c, x, y, widths, row_h, rows, header_labels=None):
    if header_labels:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8.5)
        xx = x
        for label, w in zip(header_labels, widths):
            c.drawString(xx + 8, y - 16, label.upper())
            xx += w
        y -= 28
    for row in rows:
        h = row_h
        card(c, x, y, sum(widths), h, fill=WHITE)
        xx = x
        for i, w in enumerate(widths):
            if i:
                c.setStrokeColor(LINE)
                c.line(xx, y, xx, y - h)
            text = row[i] if i < len(row) else ""
            if text:
                wrapped(c, text, xx + 8, y - 18, w - 16, size=8.6, leading=11, color=INK)
            xx += w
        y -= h
    return y


def worksheet_page(c, guide):
    header(c, guide, "Question", guide["worksheet_title"], 3)
    para(c, guide["worksheet_intro"], 58, 650, 496, size=12.5, leading=18, color=MUTED)
    y = 595

    if "timeline" in guide:
        rows = [[title, body] for title, body in guide["timeline"]]
        y = table(c, 58, y, [120, 376], 58, rows, ["Timing", "What to organize"])
        y -= 16
        for label in guide["lines"]:
            answer_line(c, 58, y, label, 496)
            y -= 54
    elif "income_rows" in guide:
        rows = [[row, ""] for row in guide["income_rows"]]
        y = table(c, 58, y, [310, 186], 42, rows, ["Income source", "Monthly amount"])
        answer_line(c, 58, 94, "One income question I need answered", 496)
    elif "budget_rows" in guide:
        rows = [[left, "", right, ""] for left, right in guide["budget_rows"]]
        y = table(c, 58, y, [132, 110, 132, 122], 48, rows, ["Expense", "Amount", "Expense", "Amount"])
        answer_line(c, 58, 180, "Estimated monthly retirement budget", 496)
        answer_line(c, 58, 116, "Tax professional I should talk with", 496)
    else:
        y = 585
        for item in guide["readiness"]:
            checkbox(c, 70, y, item, 448)
            y -= 45
        answer_line(c, 58, 128, "One family protection task to finish first", 496)


def second_question_page(c, guide):
    title = guide.get("second_title", guide["readiness_title"])
    header(c, guide, "Question", title, 4)
    y = 650
    if "claim_rows" in guide:
        para(c, guide["second_intro"], 58, y, 496, size=12.5, leading=18, color=MUTED)
        y = 590
        rows = [[age, "", "", ""] for age in guide["claim_rows"]]
        table(c, 58, y, [92, 132, 156, 116], 76, rows, ["Claim age", "Estimated benefit", "Why it might fit", "Concerns"])
        answer_line(c, 58, 142, "My best next question", 496)
    else:
        para(c, "Check each item that feels mostly handled. Your score is a starting point for the next conversation.", 58, y, 496, size=12.5, leading=18, color=MUTED)
        y = 590
        items = guide.get("score_items", guide["readiness"])
        for item in items:
            checkbox(c, 70, y, item, 448)
            y -= 41
        max_score = len(items)
        card(c, 58, 150, 496, 64, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(76, 112, f"Readiness score: _____ out of {max_score}")


def review_page(c, guide):
    header(c, guide, "Next Step", "What Happens During Your Review?", 5)
    para(c, "People often delay appointments because they are not sure what will happen. Your review is a simple, no-pressure conversation built around your questions.", 58, 650, 496, size=12.5, leading=18, color=MUTED)
    y = 570
    for idx, (title, body) in enumerate(guide["review_steps"], start=1):
        card(c, 58, y, 496, 86, fill=WHITE)
        c.setFillColor(GOLD)
        c.circle(88, y - 43, 20, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(88, y - 48, str(idx))
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(124, y - 32, title)
        wrapped(c, body, 124, y - 55, 374, size=10.4, leading=14, color=MUTED)
        y -= 100
    card(c, 58, 166, 496, 58, fill=SOFT_BLUE)
    para(c, "No obligation. Just clarity around your next best step.", 82, 130, 440, size=14, color=NAVY, bold=True, align="CENTER")


def cta_page(c, guide):
    header(c, guide, "Complimentary", guide["cta_title"], 6)
    para(c, "Bring your guide notes to a no-pressure appointment. We will review the major moving pieces together and help you decide what deserves attention first.", 58, 650, 496, size=12.5, leading=18, color=MUTED)

    card(c, 58, 562, 250, 210, fill=WHITE)
    para(c, "During your appointment we will review:", 78, 532, 210, size=12.2, leading=15, color=NAVY, bold=True)
    y = 492
    for item in guide["cta_items"]:
        checkbox(c, 78, y, item, 190)
        y -= 34

    card(c, 326, 562, 228, 210, fill=SOFT_BLUE)
    c.setFillColor(NAVY)
    c.roundRect(326, 562, 228, -56, 8, fill=1, stroke=0)
    c.setFillColor(GOLD_2)
    c.circle(440, 502, 48, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.circle(440, 502, 43, fill=1, stroke=0)
    if PROFILE_IMAGE.exists():
        c.drawImage(str(PROFILE_IMAGE), 399, 461, width=82, height=82, mask="auto")
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(440, 438, "Meet Travis Helms")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(440, 420, "INDEPENDENT RETIREMENT STRATEGIST")
    para(c, "Helping families retire with confidence through education, not pressure.", 352, 396, 176, size=9.3, leading=12, color=MUTED, align="CENTER")

    card(c, 58, 322, 306, 94, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    para(c, '"Travis made Medicare easy to understand and helped us avoid an expensive mistake."', 78, 284, 266, size=11, leading=15, color=NAVY, bold=True)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(78, 244, "Sue and Jim H., Omaha")

    card(c, 386, 322, 168, 168, fill=WHITE)
    qr_code(c, 417, 294, 106, BOOK_URL)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(470, 174, "Scan to book")

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(58, 162, "Estimated value: $250")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(58, 138, f"No obligation. Call {PHONE} or visit {WEBSITE}.")
    para(c, guide["disclaimer"], 58, 96, 496, size=8.2, leading=11, color=MUTED)


def build_guide(guide):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT / guide["filename"]
    public_path = ASSETS / guide["filename"]
    c = canvas.Canvas(str(output_path), pagesize=letter)
    for page in [cover, mistake_page, worksheet_page, second_question_page, review_page, cta_page]:
        page(c, guide)
        c.showPage()
    c.save()
    public_path.write_bytes(output_path.read_bytes())
    return output_path, public_path


def main():
    prepare_profile_image()
    for guide in GUIDES:
        output_path, public_path = build_guide(guide)
        print(f"Created {output_path}")
        print(f"Copied {public_path}")


if __name__ == "__main__":
    main()
