from pathlib import Path
from math import atan2, cos, sin, pi

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable,
    Image,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Bao_cao_He_thong_quan_ly_chi_tieu.pdf"
FONT = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
FONT_ITALIC = Path("C:/Windows/Fonts/ariali.ttf")
FONT_TIMES = Path("C:/Windows/Fonts/times.ttf")
FONT_TIMES_BOLD = Path("C:/Windows/Fonts/timesbd.ttf")
FONT_TIMES_ITALIC = Path("C:/Windows/Fonts/timesi.ttf")

pdfmetrics.registerFont(TTFont("Arial", str(FONT)))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_BOLD)))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_ITALIC)))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")
pdfmetrics.registerFont(TTFont("TimesNewRoman", str(FONT_TIMES)))
pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", str(FONT_TIMES_BOLD)))
pdfmetrics.registerFont(TTFont("TimesNewRoman-Italic", str(FONT_TIMES_ITALIC)))
pdfmetrics.registerFontFamily("TimesNewRoman", normal="TimesNewRoman", bold="TimesNewRoman-Bold", italic="TimesNewRoman-Italic", boldItalic="TimesNewRoman-Bold")

INK = colors.HexColor("#1A1A1A")
FOREST = colors.HexColor("#1A1A1A")
MOSS = colors.HexColor("#555555")
CLAY = colors.HexColor("#444444")
PAPER = colors.HexColor("#F4F4F4")
PALE = colors.HexColor("#F0F0F0")
LINE = colors.HexColor("#B5B5B5")
MUTED = colors.HexColor("#555555")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyVi", fontName="TimesNewRoman", fontSize=10.5, leading=15, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="SmallVi", fontName="TimesNewRoman", fontSize=9, leading=12, textColor=MUTED, spaceAfter=5))
styles.add(ParagraphStyle(name="H1Vi", fontName="TimesNewRoman-Bold", fontSize=16, leading=20, textColor=FOREST, spaceAfter=10))
styles.add(ParagraphStyle(name="H2Vi", fontName="TimesNewRoman-Bold", fontSize=12, leading=16, textColor=FOREST, spaceBefore=5, spaceAfter=5))
styles.add(ParagraphStyle(name="CoverTitle", fontName="TimesNewRoman-Bold", fontSize=23, leading=29, textColor=FOREST, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CoverSub", fontName="TimesNewRoman", fontSize=12, leading=17, textColor=INK, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Cell", fontName="TimesNewRoman", fontSize=9, leading=12, textColor=INK))
styles.add(ParagraphStyle(name="CellHead", fontName="TimesNewRoman-Bold", fontSize=9, leading=12, textColor=INK))
styles.add(ParagraphStyle(name="Quote", fontName="TimesNewRoman-Italic", fontSize=10.5, leading=15, textColor=INK, leftIndent=12, rightIndent=12, spaceBefore=5, spaceAfter=7))
styles.add(ParagraphStyle(name="CodeVi", fontName="TimesNewRoman", fontSize=8.5, leading=11, textColor=INK, backColor=PALE, borderPadding=8, spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="CaptionVi", fontName="TimesNewRoman-Italic", fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=6))


def P(text, style="BodyVi"):
    return Paragraph(text, styles[style])


def bullet(text):
    return P("•&nbsp;&nbsp;" + text)


def section(title, text):
    return [P(title, "H2Vi"), P(text)]


class ProjectDiagram(Flowable):
    def __init__(self, kind, height):
        super().__init__()
        self.kind = kind
        self.width = 440
        self.height = height

    def wrap(self, available_width, available_height):
        self.width = min(440, available_width)
        return self.width, self.height

    def box(self, x, y, width, height, lines, title=False):
        canvas = self.canv
        canvas.setFillColor(PALE if title else colors.white)
        canvas.setStrokeColor(MOSS)
        canvas.roundRect(x, y, width, height, 5, fill=1, stroke=1)
        canvas.setFillColor(FOREST if title else INK)
        line_height = 10
        total = len(lines) * line_height
        first_y = y + (height + total) / 2 - line_height + 2
        canvas.setFont("Arial-Bold" if title else "Arial", 7.5 if title else 6.8)
        for index, line in enumerate(lines):
            canvas.drawCentredString(x + width / 2, first_y - index * line_height, line)

    def arrow(self, x1, y1, x2, y2, label="", dashed=False, head=True):
        canvas = self.canv
        canvas.setStrokeColor(MUTED)
        canvas.setFillColor(MUTED)
        if dashed:
            canvas.setDash(3, 2)
        canvas.line(x1, y1, x2, y2)
        canvas.setDash()
        if head:
            angle = atan2(y2 - y1, x2 - x1)
            size = 6
            spread = pi / 7
            path = canvas.beginPath()
            path.moveTo(x2, y2)
            path.lineTo(x2 - size * cos(angle - spread), y2 - size * sin(angle - spread))
            path.lineTo(x2 - size * cos(angle + spread), y2 - size * sin(angle + spread))
            path.close()
            canvas.drawPath(path, fill=1, stroke=0)
        if label:
            canvas.setFont("Arial", 6.6)
            canvas.setFillColor(INK)
            label_x = (x1 + x2) / 2
            label_y = (y1 + y2) / 2 + 4
            width = pdfmetrics.stringWidth(label, "Arial", 6.6)
            canvas.setFillColor(colors.white)
            canvas.rect(label_x - width / 2 - 2, label_y - 1, width + 4, 9, fill=1, stroke=0)
            canvas.setFillColor(INK)
            canvas.drawCentredString(label_x, label_y + 1, label)

    def relationship(self, x1, y1, x2, y2, label):
        self.arrow(x1, y1, x2, y2, head=False)
        canvas = self.canv
        canvas.setFillColor(INK)
        canvas.setFont("Arial", 6.3)
        canvas.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 4, label)

    def actor(self, x, y, label):
        canvas = self.canv
        canvas.setStrokeColor(INK)
        canvas.setFillColor(INK)
        canvas.circle(x, y + 18, 6, fill=0, stroke=1)
        canvas.line(x, y + 12, x, y - 5)
        canvas.line(x - 8, y + 5, x + 8, y + 5)
        canvas.line(x, y - 5, x - 7, y - 15)
        canvas.line(x, y - 5, x + 7, y - 15)
        canvas.setFont("Arial", 6.7)
        canvas.drawCentredString(x, y - 26, label)

    def draw_use_cases(self):
        canvas = self.canv
        canvas.setStrokeColor(MUTED)
        canvas.roundRect(100, 18, 260, 188, 6, fill=0, stroke=1)
        canvas.setFont("Arial-Bold", 8)
        canvas.setFillColor(FOREST)
        canvas.drawCentredString(230, 194, "HỆ THỐNG QUẢN LÝ CHI TIÊU")
        self.actor(35, 112, "Người dùng")
        self.actor(420, 55, "Quản trị viên")
        cases = [
            (230, 166, "Tài khoản"), (230, 140, "Giao dịch"),
            (230, 114, "Danh mục"), (230, 88, "Ghi chú theo ngày"),
            (230, 62, "Tổng quan"), (230, 36, "Django Admin"),
        ]
        for x, y, label in cases:
            canvas.setFillColor(colors.white)
            canvas.setStrokeColor(MOSS)
            canvas.ellipse(x - 48, y - 14, x + 48, y + 14, fill=1, stroke=1)
            canvas.setFillColor(INK)
            canvas.setFont("Arial", 7)
            canvas.drawCentredString(x, y - 2, label)
        for x, y, label in cases[:-1]:
            self.arrow(46, 109, x - 50, y, "", head=False)
        self.arrow(410, 55, 280, 36, "", head=False)

    def draw_architecture(self):
        canvas = self.canv
        nodes = [
            (2, ["Trình duyệt", "HTML / CSS / JS"]),
            (75, ["URLconf", "Định tuyến"]),
            (148, ["Views", "Django"]),
            (221, ["Forms + Services", "Kiểm tra / tổng hợp"]),
            (294, ["Django ORM", "Đọc / ghi dữ liệu"]),
            (367, ["SQLite", "Cơ sở dữ liệu"]),
        ]
        for x, lines in nodes:
            self.box(x, 38, 62, 60, lines, title=True)
        for x in [64, 137, 210, 283, 356]:
            self.arrow(x, 68, x + 11, 68)
        canvas.setFont("Arial", 7)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(220, 18, "Yêu cầu đi qua URL và View; phản hồi được trả về trình duyệt qua Django.")

    def draw_classes(self):
        canvas = self.canv
        self.box(5, 112, 128, 72, ["User", "id, username, email, is_staff"], title=True)
        self.box(155, 112, 128, 72, ["Category", "name, kind, color, user_id"], title=True)
        self.box(305, 112, 128, 72, ["Note", "note_date, content, user_id"], title=True)
        self.box(155, 15, 128, 72, ["Transaction", "amount, occurred_on, note", "category_id, user_id"], title=True)
        self.relationship(133, 148, 155, 148, "1       *")
        self.relationship(45, 112, 155, 55, "1       *")
        self.canv.setStrokeColor(MUTED)
        self.canv.line(100, 184, 100, 202)
        self.canv.line(100, 202, 369, 202)
        self.canv.line(369, 202, 369, 184)
        self.canv.setFont("Arial", 6.3)
        self.canv.setFillColor(INK)
        self.canv.drawCentredString(100, 205, "1")
        self.canv.drawCentredString(369, 205, "*")
        self.relationship(219, 112, 219, 87, "1       *")

    def draw_sequence(self, participants, messages):
        canvas = self.canv
        usable_width = self.width - 20
        step = usable_width / len(participants)
        centers = [10 + step * (i + 0.5) for i in range(len(participants))]
        for center, label in zip(centers, participants):
            self.box(center - 42, self.height - 36, 84, 24, [label], title=True)
            canvas.setStrokeColor(LINE)
            canvas.setDash(2, 2)
            canvas.line(center, self.height - 38, center, 7)
            canvas.setDash()
        y = self.height - 52
        for index, (source, target, label) in enumerate(messages):
            reverse = target < source
            self.arrow(centers[source], y, centers[target], y, label, dashed=reverse)
            y -= 16

    def draw_activity(self):
        canvas = self.canv
        x = self.width / 2
        self.box(x - 69, 165, 138, 22, ["Mở Ghi chú"])
        self.box(x - 82, 126, 164, 24, ["Nhập ngày và nội dung"])
        canvas.setStrokeColor(MOSS)
        canvas.setFillColor(colors.white)
        path = canvas.beginPath()
        path.moveTo(x, 111)
        path.lineTo(x + 40, 91)
        path.lineTo(x, 71)
        path.lineTo(x - 40, 91)
        path.close()
        canvas.drawPath(path, fill=1, stroke=1)
        canvas.setFillColor(INK)
        canvas.setFont("Arial", 6.8)
        canvas.drawCentredString(x, 89, "Form hợp lệ?")
        self.box(x + 82, 81, 96, 21, ["Lưu ghi chú"])
        self.box(x - 178, 81, 96, 21, ["Hiển thị lỗi"])
        self.box(x - 80, 31, 160, 22, ["Hiển thị bảng"])
        canvas.setFillColor(MOSS)
        canvas.circle(x, 201, 4, fill=1, stroke=0)
        self.arrow(x, 197, x, 187)
        self.arrow(x, 165, x, 150)
        self.arrow(x, 126, x, 111)
        self.arrow(x + 40, 91, x + 82, 91, "Có")
        self.arrow(x - 40, 91, x - 82, 91, "Không")
        canvas.line(x - 178, 91, x - 193, 91)
        canvas.line(x - 193, 91, x - 193, 138)
        canvas.line(x - 193, 138, x - 82, 138)
        self.arrow(x - 193, 138, x - 82, 138, "Nhập lại")
        self.arrow(x + 82, 81, x + 72, 64)
        canvas.line(x + 72, 64, x, 64)
        self.arrow(x, 64, x, 53)
        self.arrow(x, 31, x, 15)
        canvas.circle(x, 8, 6, fill=0, stroke=1)
        canvas.circle(x, 8, 3, fill=1, stroke=0)

    def draw(self):
        self.canv.saveState()
        if self.kind == "use_cases":
            self.draw_use_cases()
        elif self.kind == "architecture":
            self.draw_architecture()
        elif self.kind == "classes":
            self.draw_classes()
        elif self.kind == "registration_sequence":
            self.draw_sequence(
                ["Người dùng", "RegisterView", "RegisterForm", "Data/DB"],
                [(0, 1, "POST đăng ký"), (1, 2, "validate"), (2, 1, "form hợp lệ"), (1, 3, "Tạo User"), (3, 1, "User + danh mục mặc định"), (1, 0, "tự đăng nhập; mở tổng quan")],
            )
        elif self.kind == "transaction_sequence":
            self.draw_sequence(
                ["Người dùng", "TransactionView", "TransactionForm", "ORM / DB"],
                [(0, 1, "POST giao dịch"), (1, 2, "kiểm tra dữ liệu"), (2, 1, "form hợp lệ"), (1, 3, "form.save()"), (3, 1, "giao dịch đã lưu"), (1, 0, "chuyển về danh sách")],
            )
        elif self.kind == "note_sequence":
            self.draw_sequence(
                ["Người dùng", "NoteView", "NoteForm", "ORM / DB"],
                [(0, 1, "POST ngày + nội dung"), (1, 2, "kiểm tra dữ liệu"), (2, 1, "form hợp lệ"), (1, 3, "form.save()"), (3, 1, "ghi chú đã lưu"), (1, 0, "chuyển về bảng ghi chú")],
            )
        elif self.kind == "note_activity":
            self.draw_activity()
        self.canv.restoreState()


def grid(rows, widths, header=True):
    data = []
    for row_index, row in enumerate(rows):
        sty = "CellHead" if header and row_index == 0 else "Cell"
        data.append([P(str(cell), sty) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (-1, 0), PAPER),
    ]
    if header:
        cmds.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]))
    table.setStyle(TableStyle(cmds))
    return table


class ReportDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(str(filename), pagesize=LETTER, leftMargin=25.4 * mm, rightMargin=25.4 * mm, topMargin=25.4 * mm, bottomMargin=25.4 * mm, title="Báo cáo đồ án Hệ thống quản lý chi tiêu", author="Hoàng Bình Minh")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="report", frames=frame, onPage=self.decorate)])

    def decorate(self, canvas, doc):
        canvas.saveState()
        w, h = LETTER
        if doc.page > 1:
            canvas.setFont("Arial", 9)
            canvas.setFillColor(INK)
            canvas.drawCentredString(w / 2, 11 * mm, str(doc.page))
        canvas.restoreState()


def add_page(story, title, content):
    story.append(P(title, "H1Vi"))
    story.extend(content)
    story.append(PageBreak())


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    story = []

    story += [Spacer(1, 10 * mm), P("<b>HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG</b>", "CoverSub"), P("<b>KHOA CÔNG NGHỆ THÔNG TIN 1</b>", "CoverSub"), Spacer(1, 31 * mm)]
    story += [P("BÁO CÁO ĐỒ ÁN CÁ NHÂN", "CoverTitle"), Spacer(1, 7 * mm), P("ĐỀ TÀI", "CoverSub"), Spacer(1, 5 * mm), P("HỆ THỐNG QUẢN LÝ CHI TIÊU", "CoverTitle"), Spacer(1, 19 * mm)]
    story.append(P("Môn học: Lập trình Python<br/>Giảng viên hướng dẫn: [Điền tên giảng viên]<br/>Sinh viên thực hiện: Hoàng Bình Minh – B22DCCN530", "BodyVi"))
    story += [Spacer(1, 50 * mm), P("Hà Nội, năm 2026", "CoverSub"), PageBreak()]

    add_page(story, "LỜI MỞ ĐẦU", [
        P("Trong đời sống hằng ngày, các khoản thu và chi thường phát sinh ở nhiều thời điểm, từ tiền ăn uống, đi lại đến học tập và sinh hoạt. Khi không được ghi chép tập trung, người dùng khó theo dõi tổng chi trong tháng, so sánh các khoản và nhớ những việc cần xử lý."),
        P("Đề tài “Hệ thống quản lý chi tiêu” được thực hiện nhằm tạo một công cụ đơn giản để ghi nhận thu nhập, chi tiêu và ghi chú theo ngày. Hệ thống cho phép người dùng quản lý danh mục, lọc giao dịch theo tháng, xem số liệu tổng hợp và trực quan hóa một số thông tin trên trang tổng quan."),
        P("Ứng dụng được xây dựng bằng Python và Django, sử dụng SQLite để lưu trữ dữ liệu. Trong quá trình thực hiện, em tìm hiểu cách tổ chức ứng dụng web theo mô hình MTV, thiết kế các bảng dữ liệu, kiểm tra biểu mẫu, phân quyền truy cập theo tài khoản và viết kiểm thử cho những luồng chính."),
        P("Báo cáo trình bày lần lượt lý do chọn đề tài và công nghệ sử dụng; yêu cầu, quy trình nghiệp vụ và thiết kế hệ thống; cuối cùng là môi trường cài đặt, kết quả triển khai, kiểm thử và hướng phát triển. Do phạm vi đồ án có giới hạn, sản phẩm chưa kết nối ngân hàng hoặc cung cấp các tính năng kế toán chuyên sâu."),
        P("Em xin cảm ơn giảng viên hướng dẫn đã hỗ trợ trong quá trình thực hiện. Em mong nhận được góp ý để tiếp tục hoàn thiện sản phẩm.")
    ])

    add_page(story, "BẢNG PHÂN CHIA CÔNG VIỆC", [
        grid([["Thành viên", "Phần chính", "Nhiệm vụ cụ thể"], ["Hoàng Bình Minh\nB22DCCN530", "Toàn bộ đồ án cá nhân", "Khảo sát; phân tích, thiết kế; xây dựng hệ thống Django; kiểm thử và viết báo cáo."]], [35 * mm, 42 * mm, 83 * mm]),
    ])

    class TocLine(Flowable):
        def __init__(self, title, page, bold=False):
            super().__init__()
            self.title, self.page, self.bold = title, str(page), bold
            self.height = 15
        def wrap(self, available_width, available_height):
            self.width = available_width
            return available_width, self.height
        def draw(self):
            font = "TimesNewRoman-Bold" if self.bold else "TimesNewRoman"
            size = 8.6
            self.canv.setFont(font, size)
            self.canv.setFillColor(INK)
            title_width = pdfmetrics.stringWidth(self.title, font, size)
            page_width = pdfmetrics.stringWidth(self.page, font, size)
            dot_width = pdfmetrics.stringWidth(".", font, size)
            count = max(2, int((self.width - title_width - page_width - 10) / dot_width))
            self.canv.drawString(0, 2, self.title)
            self.canv.drawString(title_width + 5, 2, "." * count)
            self.canv.drawRightString(self.width, 2, self.page)

    toc = [
        ("LỜI MỞ ĐẦU", 2, False), ("BẢNG PHÂN CHIA CÔNG VIỆC", 3, False),
        ("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ", 5, True), ("1.1. Giới thiệu đề tài", 5, False), ("1.2. Lựa chọn công nghệ sử dụng", 6, False), ("1.3. Kết luận chương 1", 6, False),
        ("CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 7, True), ("2.1. Khảo sát yêu cầu hệ thống", 7, False), ("2.2. Biểu đồ Use Case", 8, False), ("2.3. Xây dựng kịch bản", 9, False), ("2.4. Biểu đồ lớp thực thể", 11, False), ("2.5. Biểu đồ tuần tự", 12, False), ("2.6. Thiết kế cơ sở dữ liệu", 13, False), ("2.7. Kết luận chương 2", 13, False),
        ("CHƯƠNG 3: KẾT QUẢ XÂY DỰNG ỨNG DỤNG", 14, True), ("3.1. Môi trường cài đặt", 14, False), ("3.2.1. Giao diện tổng quan", 15, False), ("3.2.2. Giao diện giao dịch và ghi chú", 16, False), ("3.2.3. Kiểm thử chức năng", 17, False), ("3.3. Kết luận chương 3", 17, False), ("KẾT LUẬN", 18, False), ("HƯỚNG PHÁT TRIỂN TƯƠNG LAI", 19, False),
    ]
    add_page(story, "MỤC LỤC", [TocLine(*row) for row in toc])

    add_page(story, "CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ", [
        *section("1.1. Giới thiệu đề tài", "Hệ thống quản lý chi tiêu hỗ trợ cá nhân ghi nhận các khoản thu, chi và xem tổng hợp theo tháng. Mỗi người dùng có danh mục và dữ liệu riêng; ngoài giao dịch, người dùng có thể lưu ghi chú gắn với một ngày để tra cứu."),
        *section("1.1.1. Lý do chọn đề tài", "Việc tự theo dõi chi tiêu thường được thực hiện rời rạc bằng trí nhớ, giấy ghi chú hoặc nhiều ứng dụng khác nhau. Một website nhỏ có thể tập trung dữ liệu, giúp người dùng xem lại lịch sử và nhận biết nhóm chi tiêu chính mà không phải sử dụng các chức năng tài chính phức tạp."),
        *section("1.1.2. Mục tiêu xây dựng ứng dụng", "Xây dựng hệ thống có đăng ký, đăng nhập; quản lý danh mục thu và chi; tạo, sửa, xóa và lọc giao dịch; hiển thị số liệu tổng hợp theo tháng; lưu ghi chú theo ngày; và bảo đảm người dùng chỉ truy cập dữ liệu của tài khoản mình."),
        *section("1.1.3. Kết quả dự kiến đạt được", "Sản phẩm gồm website Django dùng được trên máy cá nhân, cơ sở dữ liệu quan hệ, biểu mẫu kiểm tra dữ liệu đầu vào, giao diện tiếng Việt, trang tổng quan có biểu đồ và bộ kiểm thử tự động cho các luồng nghiệp vụ chính."),
        *section("Giới hạn đề tài", "Phiên bản hiện tại không kết nối ngân hàng, không tự nhập giao dịch, không hỗ trợ nhiều loại tiền tệ, chia sẻ tài khoản hay xuất dữ liệu từ giao diện. Hệ thống được xây dựng phục vụ học tập và trình diễn.")
    ])

    add_page(story, "1.2. LỰA CHỌN CÔNG NGHỆ SỬ DỤNG", [
        grid([["Thành phần", "Công nghệ", "Lý do sử dụng"], ["Ngôn ngữ", "Python 3.12", "Cú pháp dễ đọc, phù hợp học tập và có hệ sinh thái thư viện web."], ["Backend", "Django 5.2", "Có sẵn định tuyến, ORM, biểu mẫu, xác thực và trang quản trị."], ["Cơ sở dữ liệu", "SQLite", "Không cần cài dịch vụ riêng, thuận tiện chạy demo và kiểm thử."], ["Giao diện", "HTML, CSS, JavaScript", "Dựng trang và tương tác cơ bản mà không cần thêm framework frontend."], ["Biểu đồ", "Chart.js", "Hiển thị số liệu tổng hợp theo ngày và danh mục."], ["Kiểm thử", "Django TestCase", "Kiểm tra nghiệp vụ và quyền truy cập bằng bộ công cụ tích hợp."]], [31 * mm, 42 * mm, 87 * mm]),
        P("Kiến trúc triển khai", "H2Vi"),
        ProjectDiagram("architecture", 125),
        P("Luồng chính: trình duyệt gửi yêu cầu đến URL, view kiểm tra biểu mẫu hoặc gọi service, ORM đọc/ghi SQLite và template trả kết quả cho người dùng.", "CaptionVi"),
        *section("1.3. Kết luận chương 1", "Python và Django giúp hoàn thiện nhanh các chức năng quản lý dữ liệu. SQLite phù hợp với phạm vi cá nhân; cấu trúc tách app hỗ trợ đọc và bảo trì mã nguồn. Các công nghệ này là nền tảng để phân tích và thiết kế các luồng ở chương tiếp theo.")
    ])

    add_page(story, "CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", [
        *section("2.1. Khảo sát yêu cầu hệ thống", "Hệ thống hướng đến cá nhân muốn ghi chép thủ công thu, chi và ghi chú. Các chức năng nghiệp vụ yêu cầu đăng nhập; dữ liệu trong danh mục, giao dịch và ghi chú phải được giới hạn theo chủ sở hữu."),
        grid([["Mã", "Chức năng", "Mô tả"], ["F1", "Tài khoản", "Người dùng đăng ký, đăng nhập, đăng xuất; hệ thống tạo danh mục mặc định khi đăng ký."], ["F2", "Danh mục", "Thêm, xem, sửa, xóa danh mục thu hoặc chi."], ["F3", "Giao dịch", "Lưu số tiền, ngày, danh mục; lọc theo tháng, loại và danh mục."], ["F4", "Ghi chú", "Tạo, xem dạng bảng, sửa và xóa ghi chú có ngày."], ["F5", "Tổng quan", "Tổng hợp thu, chi, số dư và hiển thị biểu đồ."], ["F6", "Quản trị", "Quản lý dữ liệu qua Django Admin theo quyền quản trị."]], [15 * mm, 33 * mm, 112 * mm]),
        *section("2.1.1. Yêu cầu phi chức năng", "Giao diện tiếng Việt; biểu mẫu báo lỗi khi dữ liệu không hợp lệ; dữ liệu số tiền dùng DecimalField; thao tác POST có CSRF; truy vấn theo tài khoản hiện tại; có thể khởi động cục bộ bằng SQLite."),
        *section("2.1.2. Quy trình nghiệp vụ", "Người dùng đăng ký hoặc đăng nhập, chọn tháng trên trang tổng quan, tạo danh mục nếu cần, ghi giao dịch, xem lịch sử và tổng hợp. Khi cần ghi việc cần nhớ, người dùng nhập ngày cùng nội dung rồi theo dõi trong bảng Ghi chú.")
    ])

    add_page(story, "2.2. BIỂU ĐỒ USE CASE", [
        *section("2.2.1. Các tác nhân và Use Case tổng quát", "Người dùng là một tác nhân xuyên suốt sơ đồ, gồm cả thao tác đăng ký/đăng nhập và nghiệp vụ sau khi xác thực. Các chức năng giao dịch, danh mục, ghi chú, tổng quan yêu cầu đăng nhập. Người có quyền staff hoặc superuser sử dụng thêm Django Admin."),
        grid([["Tác nhân", "Use Case chính"], ["Người dùng", "Đăng ký / đăng nhập / đăng xuất; quản lý giao dịch, danh mục và ghi chú; xem tổng quan."], ["Quản trị viên", "Quản lý Category, Transaction, Note qua Django Admin."]], [40 * mm, 120 * mm]),
        P("2.2.2. Biểu đồ Use Case tổng quát", "H2Vi"),
        ProjectDiagram("use_cases", 220),
        P("Sơ đồ tác nhân và các chức năng chính của Hệ thống quản lý chi tiêu.", "CaptionVi")
    ])

    add_page(story, "2.3. XÂY DỰNG KỊCH BẢN", [
        P("Kịch bản đăng ký tài khoản", "H2Vi"),
        grid([["Mục", "Nội dung"], ["Tác nhân", "Người dùng chưa đăng nhập."], ["Điều kiện", "Tên đăng nhập chưa được sử dụng; thông tin mật khẩu hợp lệ."], ["Luồng chính", "Người dùng mở trang đăng ký, nhập thông tin và gửi biểu mẫu. View kiểm tra biểu mẫu, tạo tài khoản; tín hiệu tạo danh mục mặc định."], ["Kết quả", "Tài khoản được tạo, người dùng được đăng nhập tự động và chuyển đến trang tổng quan."], ["Ngoại lệ", "Nếu tên đăng nhập đã tồn tại hoặc dữ liệu không hợp lệ, biểu mẫu hiển thị lỗi để người dùng sửa."]], [35 * mm, 125 * mm]),
        Spacer(1, 8),
        P("Kịch bản thêm giao dịch", "H2Vi"),
        grid([["Mục", "Nội dung"], ["Tác nhân", "Người dùng đã đăng nhập."], ["Điều kiện", "Danh mục thuộc tài khoản hiện tại; số tiền lớn hơn 0."], ["Luồng chính", "Chọn thêm giao dịch, nhập loại, danh mục, ngày, số tiền và nội dung tùy chọn; gửi biểu mẫu để lưu."], ["Kết quả", "Giao dịch gắn với người dùng hiện tại và xuất hiện trong danh sách."], ["Ngoại lệ", "Form giữ lại nội dung và báo lỗi nếu dữ liệu thiếu hoặc không đúng."]], [35 * mm, 125 * mm])
    ])

    add_page(story, "2.3. XÂY DỰNG KỊCH BẢN (TIẾP THEO)", [
        P("Kịch bản thêm ghi chú", "H2Vi"),
        grid([["Mục", "Nội dung"], ["Tác nhân", "Người dùng đã đăng nhập."], ["Điều kiện", "Người dùng mở chức năng Ghi chú."], ["Luồng chính", "Chọn Thêm ghi chú, nhập ngày và nội dung, gửi biểu mẫu. Hệ thống gắn ghi chú với tài khoản, lưu bản ghi và hiển thị lại trong bảng."], ["Kết quả", "Ghi chú xuất hiện cùng ngày, nội dung và thao tác sửa/xóa."], ["Ngoại lệ", "Nếu nội dung không hợp lệ, hệ thống báo lỗi và không lưu bản ghi."]], [35 * mm, 125 * mm]),
        P("Sơ đồ hoạt động thêm ghi chú", "H2Vi"),
        ProjectDiagram("note_activity", 205),
        P("Quy trình kết thúc khi dữ liệu hợp lệ được lưu và bảng ghi chú được cập nhật.", "CaptionVi")
    ])

    add_page(story, "2.4. BIỂU ĐỒ LỚP THỰC THỂ", [
        P("Mô hình dữ liệu gồm tài khoản, danh mục, giao dịch và ghi chú. Category phân biệt danh mục thu/chi; Transaction giữ số tiền cùng ngày phát sinh; Note lưu ngày ghi chú và nội dung."),
        ProjectDiagram("classes", 220),
        P("Biểu đồ lớp khái quát các thực thể; ký hiệu 1–* biểu thị quan hệ một-nhiều.", "CaptionVi"),
        grid([["Lớp", "Trách nhiệm"], ["User", "Tài khoản đăng nhập và chủ sở hữu dữ liệu."], ["Category", "Tên, loại thu/chi và màu hiển thị; thuộc về một User."], ["Transaction", "Số tiền, ngày, loại danh mục; liên kết User và Category."], ["Note", "Ngày ghi chú, nội dung, thời gian tạo/cập nhật; thuộc về một User."]], [38 * mm, 122 * mm])
    ])

    add_page(story, "2.5. BIỂU ĐỒ TUẦN TỰ", [
        P("Các sơ đồ thể hiện trao đổi giữa người dùng, view, form và cơ sở dữ liệu trong ba luồng tiêu biểu.", "BodyVi"),
        P("2.5.1. Đăng ký tài khoản", "H2Vi"),
        ProjectDiagram("registration_sequence", 118),
        P("Dữ liệu được xác thực trước khi tài khoản cùng danh mục mặc định được tạo.", "CaptionVi"),
        P("2.5.2. Thêm giao dịch", "H2Vi"),
        ProjectDiagram("transaction_sequence", 118),
        P("Giao dịch chỉ được lưu sau khi form kiểm tra dữ liệu và danh mục thuộc đúng tài khoản.", "CaptionVi"),
        P("2.5.3. Thêm ghi chú", "H2Vi"),
        ProjectDiagram("note_sequence", 118),
        P("Ngày và nội dung được gắn với người dùng đang đăng nhập.", "CaptionVi")
    ])

    add_page(story, "2.6. THIẾT KẾ CƠ SỞ DỮ LIỆU", [
        P("2.6.1. Mô tả các bảng", "H2Vi"),
        grid([["Bảng", "Thuộc tính chính", "Ràng buộc / mô tả"], ["User", "username, email, password", "Django Authentication; chủ sở hữu dữ liệu cá nhân."], ["Category", "user, name, kind, color", "Khóa ngoại User; tên danh mục duy nhất theo người dùng và loại."], ["Transaction", "user, category, amount, occurred_on, note", "Số tiền DecimalField nguyên VNĐ; ngày là DateField; liên kết danh mục."], ["Note", "user, note_date, content, created_at, updated_at", "Ghi chú có ngày; dữ liệu được lọc theo chủ sở hữu."]], [29 * mm, 62 * mm, 69 * mm]),
        P("2.6.2. Lược đồ cơ sở dữ liệu", "H2Vi"),
        grid([["Quan hệ", "Ý nghĩa"], ["User 1 — N Category", "Một tài khoản sở hữu nhiều danh mục."], ["User 1 — N Transaction", "Một tài khoản sở hữu nhiều giao dịch."], ["Category 1 — N Transaction", "Một danh mục phân loại nhiều giao dịch."], ["User 1 — N Note", "Một tài khoản sở hữu nhiều ghi chú."], ["Category — Transaction", "Form kiểm tra danh mục phải thuộc cùng User."]], [50 * mm, 110 * mm]),
        *section("Toàn vẹn dữ liệu", "Các khóa ngoại duy trì quan hệ giữa bản ghi. Form kiểm tra dữ liệu trước khi lưu; queryset nghiệp vụ giới hạn theo User hiện tại để ngăn truy cập chéo tài khoản."),
        P("2.7. Kết luận chương 2", "H2Vi"),
        P("Chương 2 đã xác định tác nhân, yêu cầu chức năng và quy trình nghiệp vụ của Hệ thống quản lý chi tiêu. Use Case, kịch bản, biểu đồ tuần tự, mô hình lớp và lược đồ dữ liệu tạo cơ sở cho triển khai Django, ORM và SQLite ở chương tiếp theo.")
    ])

    add_page(story, "CHƯƠNG 3: KẾT QUẢ XÂY DỰNG ỨNG DỤNG", [
        P("3.1. Môi trường cài đặt", "H2Vi"),
        grid([["Thành phần", "Yêu cầu / sử dụng"], ["Hệ điều hành", "Windows; thực hiện lệnh bằng PowerShell."], ["Ngôn ngữ và framework", "Python 3.12, Django 5.2."], ["Cơ sở dữ liệu", "SQLite; không cần dịch vụ database riêng."], ["Frontend", "HTML, CSS, JavaScript; Chart.js tải từ CDN để vẽ biểu đồ."], ["Công cụ", "Visual Studio Code hoặc editor tương đương; Git; trình duyệt web."]], [45 * mm, 115 * mm]),
        P("Các bước cài đặt", "H2Vi"),
        P("Tạo môi trường ảo; cài requirements.txt; sao chép .env.example thành .env; chạy migrate; chạy lệnh seed_demo nếu cần dữ liệu mẫu; sau đó khởi động bằng python manage.py runserver.", "BodyVi"),
        P("Tài khoản demo: demo / demo12345. Địa chỉ mặc định: http://127.0.0.1:8000/. Lệnh seed_demo tạo lại dữ liệu giao dịch demo; không tạo hoặc xóa ghi chú.", "SmallVi"),
        *section("3.2. Kết quả cài đặt", "Các chức năng chính đã được triển khai gồm tài khoản, danh mục, giao dịch, bảng ghi chú có ngày, trang tổng quan và giao diện quản trị. Các trang nghiệp vụ yêu cầu đăng nhập và truy vấn dữ liệu theo tài khoản hiện tại.")
    ])

    add_page(story, "3.2. KẾT QUẢ CÀI ĐẶT", [
        P("3.2.1. Giao diện tổng quan", "H2Vi"),
        P("Trang tổng quan cho phép chọn tháng, xem tổng thu, chi, số dư và theo dõi biểu đồ chi theo ngày hoặc danh mục."),
        Image(str(ROOT / "reports" / "assets" / "giao-dien-tong-quan.png"), width=160 * mm, height=125 * mm, kind="proportional"),
        P("Hình 3.1. Giao diện tổng quan với dữ liệu demo.", "CaptionVi"),
        P("Số dư thể hiện chênh lệch thu và chi trong tháng đang xem; đây không phải số dư tài khoản ngân hàng.", "SmallVi")
    ])

    add_page(story, "3.2.2. GIAO DỊCH VÀ GHI CHÚ", [
        P("3.2.2. Giao diện giao dịch và ghi chú", "H2Vi"),
        P("Danh sách giao dịch hiển thị ngày, danh mục, số tiền và nội dung; người dùng có thể lọc theo tháng, loại và danh mục. Bảng Ghi chú lưu ngày riêng cùng nội dung, hỗ trợ sửa và xóa."),
        Image(str(ROOT / "reports" / "assets" / "giao-dien-giao-dich.png"), width=160 * mm, height=88 * mm, kind="proportional"),
        P("Hình 3.2. Danh sách giao dịch của tài khoản demo.", "CaptionVi"),
        Image(str(ROOT / "reports" / "assets" / "giao-dien-ghi-chu.png"), width=160 * mm, height=48 * mm, kind="proportional"),
        P("Hình 3.3. Bảng ghi chú hiển thị ngày, nội dung và thao tác.", "CaptionVi")
    ])

    add_page(story, "3.2.3. KIỂM THỬ CHỨC NĂNG", [
        grid([["Nội dung kiểm thử", "Kết quả"], ["Tạo tài khoản và danh mục mặc định", "Đạt trong bộ test tự động."], ["Tạo / sửa / xóa giao dịch", "Đạt trong bộ test tự động."], ["Tạo / sửa / xóa ghi chú có ngày", "Đạt trong bộ test tự động."], ["Phân quyền dữ liệu theo tài khoản", "Đạt trong bộ test tự động."], ["Kiểm tra tổng hợp và danh mục", "Đạt trong bộ test tự động."], ["Toàn bộ kiểm thử Django", "9 test chạy thành công; 0 lỗi."]], [92 * mm, 68 * mm]),
        P("Lệnh kiểm tra: python manage.py test. Kết quả ghi nhận gần nhất: Ran 9 tests; OK. Kiểm tra migration: makemigrations --check --dry-run báo không có thay đổi.", "Quote"),
        P("3.3. Kết luận chương 3", "H2Vi"),
        P("Ứng dụng đã triển khai được các luồng quản lý thu, chi và ghi chú theo ngày trên Django với SQLite. Trang tổng quan tính dữ liệu theo tháng; quyền truy cập bản ghi được giới hạn theo tài khoản. Các kiểm thử tự động hiện có đều đạt.")
    ])

    add_page(story, "KẾT LUẬN", [
        P("Đề tài xây dựng được ứng dụng web hỗ trợ ghi nhận thu nhập, chi tiêu và ghi chú cá nhân. Sản phẩm có đăng ký/đăng nhập, danh mục, giao dịch có lọc, bảng ghi chú theo ngày, tổng hợp tháng và biểu đồ. Thiết kế dữ liệu gắn với tài khoản, biểu mẫu kiểm tra đầu vào và 9 bài kiểm thử tự động tạo cơ sở cho việc sử dụng và tiếp tục phát triển."),
        P("Hạn chế hiện tại gồm chưa kết nối ngân hàng, chưa xuất CSV/Excel, chưa có tìm kiếm ghi chú và chưa kiểm tra toàn diện giao diện trên nhiều thiết bị. SQLite phù hợp cho đồ án và demo, chưa hướng tới tải đồng thời lớn."),
    ])

    add_page(story, "HƯỚNG PHÁT TRIỂN TƯƠNG LAI", [
        P("Các hướng tiếp theo ưu tiên độ tin cậy, khả năng tra cứu và bảo vệ dữ liệu trước khi mở rộng tích hợp bên ngoài."),
        grid([["Ưu tiên", "Nội dung"], ["1", "Mở rộng kiểm thử biên, kiểm thử biểu mẫu và giao diện."], ["2", "Thêm tìm kiếm, lọc ngày tùy chọn và xuất CSV/Excel."], ["3", "Bổ sung xác thực email, đặt lại mật khẩu và giới hạn đăng nhập."], ["4", "Chuyển sang PostgreSQL, bổ sung backup và logging khi triển khai."], ["5", "Hoàn thiện giao diện di động và khả năng tiếp cận."]], [23 * mm, 137 * mm]),
        P("Các tính năng cần được triển khai theo nhu cầu sử dụng thực tế và kèm kiểm thử tương ứng.")
    ])


    if story and isinstance(story[-1], PageBreak):
        story.pop()
    ReportDoc(OUTPUT).build(story)
    print(OUTPUT)

if __name__ == "__main__":
    build()
