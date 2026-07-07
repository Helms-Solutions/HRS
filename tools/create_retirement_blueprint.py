from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf"
ASSETS = ROOT / "assets"
PDF_PATH = OUTPUT / "the-retirement-blueprint-helms-retirement-solutions.pdf"
PUBLIC_PDF_PATH = ASSETS / "the-retirement-blueprint-helms-retirement-solutions.pdf"

WIDTH, HEIGHT = letter
NAVY = colors.HexColor("#0B1F3A")
NAVY_2 = colors.HexColor("#102D52")
GOLD = colors.HexColor("#C99A3A")
GOLD_2 = colors.HexColor("#E4BD68")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#D9E2EC")
SOFT = colors.HexColor("#F5F8FB")
WHITE = colors.white

PHONE = "(402) 237-6592"
EMAIL = "helmsretirement@gmail.com"
WEBSITE = "helmsretirement.com"
BOOK_URL = "https://calendly.com/helmsretirement"
LOGO = ASSETS / "helms-logo.png"
HEADSHOT = ASSETS / "headshot_1.jpg"


def draw_paragraph(c, text, x, y, width, size=10, leading=None, color=INK, bold=False, align="LEFT"):
    style = ParagraphStyle(
        "body",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment={"LEFT": 0, "CENTER": 1, "RIGHT": 2}[align],
        spaceAfter=0,
    )
    paragraph = Paragraph(text, style)
    _, h = paragraph.wrap(width, 600)
    paragraph.drawOn(c, x, y - h)
    return y - h


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=10, leading=14, color=INK):
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


def footer(c, page_num):
    c.setStrokeColor(LINE)
    c.line(42, 42, WIDTH - 42, 42)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(42, 29, "Helping Families Retire With Confidence")
    c.drawString(42, 17, f"Helms Retirement Solutions | {PHONE} | {WEBSITE}")
    c.drawRightString(WIDTH - 42, 26, f"Page {page_num}")


def header(c, eyebrow, title, page_num):
    c.setFillColor(NAVY)
    c.rect(0, HEIGHT - 96, WIDTH, 96, fill=1, stroke=0)
    c.setFillColor(GOLD_2)
    c.rect(0, HEIGHT - 100, WIDTH, 4, fill=1, stroke=0)
    if LOGO.exists():
        c.drawImage(str(LOGO), 42, HEIGHT - 88, width=200, height=58, preserveAspectRatio=True, mask="auto")
    c.setFillColor(GOLD_2)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(WIDTH - 42, HEIGHT - 66, eyebrow.upper())
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawRightString(WIDTH - 42, HEIGHT - 42, title)
    footer(c, page_num)


def section_label(c, x, y, text):
    c.setFillColor(GOLD)
    c.roundRect(x, y - 20, 130, 22, 5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + 65, y - 14, text.upper())


def card(c, x, y, w, h, title=None, fill=WHITE, stroke=LINE):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y - h, w, h, 8, fill=1, stroke=1)
    if title:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 16, y - 24, title)


def checkbox(c, x, y, label, width=440, checked=False):
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.rect(x, y - 11, 11, 11, fill=0, stroke=1)
    if checked:
        c.line(x + 2, y - 6, x + 5, y - 10)
        c.line(x + 5, y - 10, x + 11, y)
    draw_wrapped(c, label, x + 20, y - 1, width, font="Helvetica", size=9.5, leading=12, color=INK)


def answer_line(c, x, y, label, width=190):
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y + 5, label.upper())
    c.setStrokeColor(LINE)
    c.line(x, y - 8, x + width, y - 8)


def score_box(c, x, y, label, max_score=5):
    card(c, x, y, 154, 54, fill=SOFT)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x + 12, y - 18, label)
    c.setStrokeColor(GOLD)
    for i in range(max_score):
        c.circle(x + 18 + i * 24, y - 38, 6, fill=0, stroke=1)


def draw_qr(c, x, y, size, value):
    code = qr.QrCodeWidget(value)
    bounds = code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = code
    from reportlab.graphics.shapes import Drawing

    d = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    d.add(drawing)
    renderPDF.draw(d, c, x, y - size)


def cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    c.setFillColor(NAVY_2)
    c.circle(WIDTH - 70, HEIGHT - 80, 180, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, HEIGHT - 152, WIDTH, 7, fill=1, stroke=0)
    if LOGO.exists():
        c.drawImage(str(LOGO), 48, HEIGHT - 118, width=275, height=82, preserveAspectRatio=True, mask="auto")

    section_label(c, 48, HEIGHT - 185, "Free Workbook")
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 48)
    c.drawString(48, HEIGHT - 260, "The Retirement")
    c.drawString(48, HEIGHT - 315, "Blueprint")
    draw_paragraph(
        c,
        "A 10-minute workbook to organize income, Medicare, taxes, estate planning, and next steps before retirement decisions pile up.",
        50,
        HEIGHT - 352,
        440,
        size=15,
        leading=21,
        color=colors.HexColor("#E8EEF6"),
    )

    card(c, 48, 290, 230, 112, fill=colors.HexColor("#F8FBFF"), stroke=colors.HexColor("#F8FBFF"))
    card(c, 304, 290, 230, 112, fill=colors.HexColor("#F8FBFF"), stroke=colors.HexColor("#F8FBFF"))
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(70, 242, "Worksheets")
    c.drawString(326, 242, "Checklists")
    draw_wrapped(c, "Fill in your income, budget, Social Security, and readiness score.", 70, 218, 180, size=10.5, leading=14, color=MUTED)
    draw_wrapped(c, "Review Medicare, tax, estate, and 90-day planning action items.", 326, 218, 180, size=10.5, leading=14, color=MUTED)

    c.setFillColor(GOLD_2)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(48, 104, "Helms Retirement Solutions")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    c.drawString(48, 82, f"{PHONE} | {WEBSITE} | {EMAIL}")
    c.setFont("Helvetica", 8.5)
    c.drawString(48, 54, "Not affiliated with or endorsed by the U.S. government or the federal Medicare program.")


def page_mistakes(c):
    header(c, "Start Here", "The 5 Biggest Retirement Mistakes", 2)
    y = 640
    items = [
        ("1", "Guessing at monthly income", "Retirement gets easier when every income source has a job."),
        ("2", "Waiting too long on Medicare", "Enrollment windows, drug coverage, and carrier choices deserve a timeline."),
        ("3", "Ignoring taxes", "Withdrawals, Social Security, and account types can change the tax picture."),
        ("4", "Leaving family protection vague", "Life insurance, final expense, beneficiaries, and documents should line up."),
        ("5", "Having no 90-day plan", "The best retirement plan is broken into practical next actions."),
    ]
    for number, title, body in items:
        card(c, 58, y, 496, 78, fill=WHITE)
        c.setFillColor(GOLD)
        c.circle(88, y - 39, 18, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(88, y - 44, number)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(124, y - 28, title)
        draw_wrapped(c, body, 124, y - 49, 380, size=10.5, leading=14, color=MUTED)
        y -= 88


def page_income(c):
    header(c, "Question", "Do I Have Enough Income?", 3)
    draw_paragraph(c, "List your expected monthly income. The goal is not perfection - it is clarity.", 58, 648, 496, size=13, leading=18, color=MUTED)
    y = 590
    rows = ["Social Security", "Pension", "IRA/401(k) withdrawals", "Annuity income", "Part-time work", "Other"]
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(NAVY)
    c.drawString(62, y, "INCOME SOURCE")
    c.drawRightString(505, y, "MONTHLY AMOUNT")
    y -= 12
    for row in rows:
        card(c, 58, y, 496, 48, fill=WHITE)
        c.setFillColor(INK)
        c.setFont("Helvetica", 11)
        c.drawString(76, y - 29, row)
        c.setStrokeColor(LINE)
        c.line(365, y - 30, 520, y - 30)
        y -= 56
    card(c, 58, y - 4, 496, 58, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(76, y - 39, "Total estimated monthly income")
    c.setStrokeColor(GOLD)
    c.line(365, y - 39, 520, y - 39)
    answer_line(c, 58, 104, "One income question I need answered", 496)


def page_medicare(c):
    header(c, "Question", "What Is My Medicare Timeline?", 4)
    draw_paragraph(c, "Use this page to mark what needs attention before, during, and after Medicare enrollment.", 58, 648, 496, size=13, leading=18, color=MUTED)
    x_positions = [74, 204, 334, 464]
    labels = ["12 months", "6 months", "3 months", "Annual review"]
    marker_labels = ["12", "6", "3", "YR"]
    captions = [
        "Gather doctors, medications, and current coverage.",
        "Compare Medicare paths and prescription needs.",
        "Confirm enrollment timing and plan details.",
        "Review changes in plans, drugs, doctors, and costs.",
    ]
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.line(88, 500, 478, 500)
    for x, label, marker_label, caption in zip(x_positions, labels, marker_labels, captions):
        c.setFillColor(GOLD)
        c.circle(x + 14, 500, 16, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + 14, 496, marker_label)
        card(c, x - 10, 458, 108, 134, fill=WHITE)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + 44, 430, label)
        draw_paragraph(c, caption, x + 2, 405, 84, size=8.7, leading=11, color=MUTED, align="CENTER")
    y = 260
    for item in ["Doctors I want to keep", "Prescriptions I take", "Pharmacy preference", "Coverage questions"]:
        answer_line(c, 58, y, item, 496)
        y -= 54


def page_social_security(c):
    header(c, "Question", "When Should I Claim Social Security?", 5)
    draw_paragraph(c, "Social Security decisions can affect monthly income for life. Use this worksheet to compare three claiming ages.", 58, 648, 496, size=13, leading=18, color=MUTED)
    headers = ["Claim age", "Estimated monthly benefit", "Why this age might fit", "Concerns"]
    x = [58, 156, 310, 440]
    widths = [88, 140, 120, 114]
    y = 584
    for i, h in enumerate(headers):
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x[i], y, h.upper())
    y -= 10
    for age in ["62", "Full retirement age", "70"]:
        card(c, 52, y, 508, 82, fill=WHITE)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(66, y - 45, age)
        for i in range(1, 4):
            c.setStrokeColor(LINE)
            c.line(x[i], y - 46, x[i] + widths[i] - 10, y - 46)
        y -= 92
    card(c, 58, 215, 496, 98, "My best next question", fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    answer_line(c, 78, 151, "Question", 440)


def page_budget(c):
    header(c, "Question", "What Will Retirement Cost Each Month?", 6)
    draw_paragraph(c, "Estimate the expenses that continue into retirement. Then compare the total with your income worksheet.", 58, 648, 496, size=13, leading=18, color=MUTED)
    categories = ["Housing", "Utilities", "Groceries", "Transportation", "Health care", "Insurance", "Debt", "Travel/fun", "Giving", "Other"]
    y = 590
    for i, category in enumerate(categories):
        x = 58 if i % 2 == 0 else 316
        if i % 2 == 0 and i > 0:
            y -= 58
        card(c, x, y, 238, 48, fill=WHITE)
        c.setFillColor(INK)
        c.setFont("Helvetica", 10.5)
        c.drawString(x + 14, y - 29, category)
        c.setStrokeColor(LINE)
        c.line(x + 128, y - 30, x + 220, y - 30)
    card(c, 58, 178, 496, 62, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(76, 137, "Estimated monthly retirement budget")
    c.setStrokeColor(GOLD)
    c.line(365, 137, 520, 137)


def page_tax(c):
    header(c, "Question", "What Could Surprise Me at Tax Time?", 7)
    draw_paragraph(c, "Use this checklist to spot tax conversations to have before retirement withdrawals begin.", 58, 648, 496, size=13, leading=18, color=MUTED)
    items = [
        "I know which accounts are taxable, tax-deferred, and tax-free.",
        "I have discussed whether Social Security may be taxable.",
        "I understand required minimum distribution timing.",
        "I have reviewed Roth conversion questions with a tax professional.",
        "I know how pension, annuity, or IRA income may be withheld.",
        "I have a plan for charitable giving or beneficiary tax questions.",
        "I know which tax records to keep for health and insurance costs.",
    ]
    y = 575
    for item in items:
        checkbox(c, 68, y, item, 450)
        y -= 48
    answer_line(c, 58, 110, "Tax professional I should talk with", 496)


def page_estate(c):
    header(c, "Question", "Is My Family Protection Organized?", 8)
    draw_paragraph(c, "This is not legal advice. Use the checklist to decide what to review with qualified professionals.", 58, 648, 496, size=13, leading=18, color=MUTED)
    items = [
        "Beneficiaries are current on life insurance, retirement accounts, and annuities.",
        "My spouse or family knows where important documents are stored.",
        "I have reviewed final expense needs and funeral preferences.",
        "I have considered power of attorney and health care directive documents.",
        "My will or trust has been reviewed recently.",
        "My emergency contacts and account list are updated.",
        "I know who should be involved in a family planning conversation.",
    ]
    y = 575
    for item in items:
        checkbox(c, 68, y, item, 450)
        y -= 48
    answer_line(c, 58, 110, "One family protection task to finish first", 496)


def page_risk(c):
    header(c, "Question", "How Much Risk Am I Comfortable With?", 9)
    draw_paragraph(c, "Circle a score from 1 to 5 for each statement. 1 means low confidence or low comfort. 5 means high confidence or high comfort.", 58, 648, 496, size=13, leading=18, color=MUTED)
    labels = [
        "Income stability",
        "Market volatility comfort",
        "Emergency reserves",
        "Health cost preparedness",
        "Legacy confidence",
        "Withdrawal plan clarity",
    ]
    y = 575
    for i, label in enumerate(labels):
        x = 58 if i % 2 == 0 else 322
        if i % 2 == 0 and i > 0:
            y -= 76
        score_box(c, x, y, label)
    card(c, 58, 242, 496, 92, "My score notes", fill=WHITE)
    for yy in [190, 166, 142]:
        c.setStrokeColor(LINE)
        c.line(78, yy, 532, yy)


def page_quiz(c):
    header(c, "Question", "How Ready Am I?", 10)
    draw_paragraph(c, "Check each item that feels mostly handled. Your score is a starting point for the next conversation.", 58, 648, 496, size=13, leading=18, color=MUTED)
    items = [
        "I know my expected retirement income.",
        "I know my expected monthly expenses.",
        "I understand my Medicare timeline.",
        "I have reviewed prescription and doctor needs.",
        "I know when I may claim Social Security.",
        "I have reviewed tax questions.",
        "My beneficiary information is current.",
        "My spouse or family understands the plan.",
        "I have a 90-day action plan.",
    ]
    y = 575
    for item in items:
        checkbox(c, 68, y, item, 450)
        y -= 38
    card(c, 58, 155, 496, 62, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(76, 116, "Readiness score")
    c.setStrokeColor(GOLD)
    c.line(210, 116, 280, 116)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(288, 116, "out of 9")


def page_action(c):
    header(c, "Question", "What Should I Do in the Next 90 Days?", 11)
    draw_paragraph(c, "Choose a few small actions. A simple plan usually beats a perfect plan that never starts.", 58, 648, 496, size=13, leading=18, color=MUTED)
    columns = [("Next 30 days", 58), ("Days 31-60", 224), ("Days 61-90", 390)]
    for title, x in columns:
        card(c, x, 580, 150, 360, title, fill=WHITE)
        y = 515
        for _ in range(6):
            c.setStrokeColor(LINE)
            c.line(x + 18, y, x + 132, y)
            y -= 45
    card(c, 58, 172, 496, 58, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(76, 136, "The first call or appointment I need to make")
    c.setStrokeColor(GOLD)
    c.line(346, 136, 520, 136)


def page_review_process(c):
    header(c, "Next Step", "What Happens During Your Review?", 12)
    draw_paragraph(
        c,
        "People often delay appointments because they are not sure what will happen. Your review is a simple, no-pressure conversation built around your questions.",
        58,
        648,
        496,
        size=14,
        leading=20,
        color=MUTED,
    )
    steps = [
        ("1", "Income Review", "Look at your expected retirement income and monthly spending needs."),
        ("2", "Medicare Review", "Review doctors, prescriptions, timing, and coverage questions."),
        ("3", "Tax Discussion", "Identify tax questions to bring to your tax professional before decisions are made."),
        ("4", "Risk Analysis", "Talk through market comfort, health cost concerns, and protection gaps."),
        ("5", "Recommendations", "Leave with clear next steps and options that fit your situation."),
    ]
    y = 548
    for number, title, body in steps:
        card(c, 70, y, 472, 70, fill=WHITE)
        c.setFillColor(GOLD)
        c.circle(98, y - 35, 16, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(98, y - 40, number)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12.5)
        c.drawString(132, y - 27, title)
        draw_wrapped(c, body, 132, y - 48, 360, size=9.5, leading=12, color=MUTED)
        y -= 82
    card(c, 58, 134, 496, 58, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(76, 98, "No obligation. Just clarity around your next best step.")


def page_schedule(c):
    header(c, "Complimentary", "Claim Your Blueprint Review", 13)
    draw_paragraph(
        c,
        "Bring your workbook notes to a no-pressure appointment. We will review the major moving pieces together and help you decide what deserves attention first.",
        58,
        640,
        496,
        size=13,
        leading=18,
        color=MUTED,
    )

    card(c, 58, 552, 496, 122, fill=colors.HexColor("#FFF8EA"), stroke=GOLD_2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(82, 516, "During your appointment we'll review:")
    c.setFont("Helvetica", 10.5)
    items = ["Medicare", "Retirement income", "Tax questions", "Social Security", "Estate planning", "Legacy planning"]
    x = 82
    y = 492
    for i, item in enumerate(items):
        if i == 3:
            x = 320
            y = 492
        c.setStrokeColor(GOLD)
        c.rect(x, y - 8, 10, 10, fill=0, stroke=1)
        c.setFillColor(INK)
        c.drawString(x + 18, y - 6, item)
        y -= 20

    if HEADSHOT.exists():
        c.drawImage(str(HEADSHOT), 58, 276, width=116, height=130, preserveAspectRatio=True, mask="auto")
    card(c, 190, 406, 364, 130, fill=WHITE)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(214, 362, "Meet Travis Helms")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(214, 340, "INDEPENDENT RETIREMENT STRATEGIST")
    draw_paragraph(
        c,
        "Helping families retire with confidence through education - not pressure.",
        214,
        316,
        300,
        size=12,
        leading=16,
        color=MUTED,
    )

    card(c, 58, 258, 496, 66, fill=SOFT)
    draw_paragraph(
        c,
        '"Travis made Medicare easy to understand and helped us avoid an expensive mistake."',
        82,
        234,
        430,
        size=11,
        leading=14,
        color=NAVY,
        bold=True,
    )
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(82, 198, "- Sue and Jim H., Omaha")

    card(c, 58, 166, 238, 70, fill=WHITE)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(82, 134, "Estimated value: $250")
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(82, 110, "No obligation.")

    card(c, 316, 166, 238, 70, fill=WHITE)
    draw_qr(c, 334, 156, 50, BOOK_URL)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(398, 132, "Scan to book")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(398, 116, PHONE)
    c.drawString(398, 102, WEBSITE)
    draw_paragraph(c, "Not affiliated with or endorsed by the U.S. government or the federal Medicare program. We do not offer every plan available in your area.", 58, 78, 496, size=8, leading=10, color=MUTED)


def build_pdf(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    pages = [
        cover,
        page_mistakes,
        page_income,
        page_medicare,
        page_social_security,
        page_budget,
        page_tax,
        page_estate,
        page_risk,
        page_quiz,
        page_action,
        page_review_process,
        page_schedule,
    ]
    for page in pages:
        page(c)
        c.showPage()
    c.save()


if __name__ == "__main__":
    build_pdf(PDF_PATH)
    build_pdf(PUBLIC_PDF_PATH)
    print(PDF_PATH)
    print(PUBLIC_PDF_PATH)
