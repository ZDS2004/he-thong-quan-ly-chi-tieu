from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'word' / 'Bao_cao_He_thong_quan_ly_chi_tieu.docx'
ASSETS = ROOT / 'reports' / 'assets'


def set_cell_fill(cell, fill='F2F2F2'):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=80, start=100, bottom=80, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in('w:tcMar')
    if margins is None:
        margins = OxmlElement('w:tcMar')
        tc_pr.append(margins)
    for m, v in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = margins.find(qn('w:' + m))
        if node is None:
            node = OxmlElement('w:' + m)
            margins.append(node)
        node.set(qn('w:w'), str(v))
        node.set(qn('w:type'), 'dxa')


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    repeat = OxmlElement('w:tblHeader')
    repeat.set(qn('w:val'), 'true')
    tr_pr.append(repeat)


def set_no_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement('w:cantSplit')
    tr_pr.append(el)


def configure_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.top_margin = Inches(1)
    sec.bottom_margin = Inches(1)
    sec.left_margin = Inches(1)
    sec.right_margin = Inches(1)
    sec.different_first_page_header_footer = True
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor(26, 26, 26)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.space_after = Pt(4)
    for style_name, size, before, after in [('Heading 1', 15, 2, 8), ('Heading 2', 11.5, 6, 3), ('Heading 3', 10.5, 4, 2)]:
        style = doc.styles[style_name]
        style.font.name = 'Times New Roman'
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(20, 20, 20)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    run._r.addnext(fld)
    return doc


def add_para(doc, text, style=None, align=None, italic=False, bold=False, after=None):
    para = doc.add_paragraph(style=style)
    if align is not None:
        para.alignment = align
    run = para.add_run(text)
    run.font.name = 'Times New Roman'
    if italic:
        run.italic = True
    if bold:
        run.bold = True
    if after is not None:
        para.paragraph_format.space_after = Pt(after)
    return para


def add_heading(doc, text, level=1, align=None):
    para = doc.add_paragraph(style=f'Heading {level}')
    if align is not None:
        para.alignment = align
    run = para.add_run(text)
    run.font.name = 'Times New Roman'
    return para


def add_table(doc, rows, widths=None, header=True, font_size=9.2):
    cols = len(rows[0])
    table = doc.add_table(rows=0, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for r_index, values in enumerate(rows):
        row = table.add_row()
        set_no_split(row)
        if r_index == 0 and header:
            set_repeat_table_header(row)
        for c_index, value in enumerate(values):
            cell = row.cells[c_index]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            set_cell_margins(cell)
            if widths:
                cell.width = Inches(widths[c_index])
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(str(value))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.bold = bool(header and r_index == 0)
            if header and r_index == 0:
                set_cell_fill(cell)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def add_image(doc, name, width=6.25, height=None):
    path = ASSETS / name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    run = p.add_run()
    if height is None:
        run.add_picture(str(path), width=Inches(width))
    else:
        run.add_picture(str(path), width=Inches(width), height=Inches(height))
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)
    r.italic = True


def next_page(doc):
    doc.add_page_break()


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = configure_document()

    add_para(doc, 'HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, after=1)
    add_para(doc, 'KHOA CÔNG NGHỆ THÔNG TIN 1', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, after=38)
    add_para(doc, 'BÁO CÁO ĐỒ ÁN CÁ NHÂN', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, after=18)
    add_para(doc, 'ĐỀ TÀI', align=WD_ALIGN_PARAGRAPH.CENTER, after=7)
    add_para(doc, 'HỆ THỐNG QUẢN LÝ CHI TIÊU', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, after=40)
    add_para(doc, 'Môn học: Lập trình Python\nGiảng viên hướng dẫn: [Điền tên giảng viên]\nSinh viên thực hiện: Hoàng Bình Minh – B22DCCN530', after=0)
    for _ in range(7):
        add_para(doc, '')
    add_para(doc, 'Hà Nội, năm 2026', align=WD_ALIGN_PARAGRAPH.CENTER)

    next_page(doc)
    add_heading(doc, 'LỜI MỞ ĐẦU')
    for text in [
        'Trong đời sống hằng ngày, các khoản thu và chi thường phát sinh ở nhiều thời điểm, từ tiền ăn uống, đi lại đến học tập và sinh hoạt. Khi không được ghi chép tập trung, người dùng khó theo dõi tổng chi trong tháng, so sánh các khoản và nhớ những việc cần xử lý.',
        'Đề tài “Hệ thống quản lý chi tiêu” được thực hiện nhằm tạo một công cụ đơn giản để ghi nhận thu nhập, chi tiêu và ghi chú theo ngày. Hệ thống cho phép người dùng quản lý danh mục, lọc giao dịch theo tháng, xem số liệu tổng hợp và trực quan hóa một số thông tin trên trang tổng quan.',
        'Ứng dụng được xây dựng bằng Python và Django, sử dụng SQLite để lưu trữ dữ liệu. Trong quá trình thực hiện, em tìm hiểu cách tổ chức ứng dụng web theo mô hình MTV, thiết kế các bảng dữ liệu, kiểm tra biểu mẫu, phân quyền truy cập theo tài khoản và viết kiểm thử cho những luồng chính.',
        'Báo cáo trình bày lần lượt lý do chọn đề tài và công nghệ sử dụng; yêu cầu, quy trình nghiệp vụ và thiết kế hệ thống; cuối cùng là môi trường cài đặt, kết quả triển khai, kiểm thử và hướng phát triển. Do phạm vi đồ án có giới hạn, sản phẩm chưa kết nối ngân hàng hoặc cung cấp các tính năng tài chính chuyên sâu.',
        'Em xin cảm ơn giảng viên hướng dẫn đã hỗ trợ trong quá trình thực hiện. Em mong nhận được góp ý để tiếp tục hoàn thiện sản phẩm.'
    ]:
        add_para(doc, text)

    next_page(doc)
    add_heading(doc, 'BẢNG PHÂN CHIA CÔNG VIỆC')
    add_table(doc, [['Thành viên', 'Phần chính', 'Nhiệm vụ cụ thể'], ['Hoàng Bình Minh\nB22DCCN530', 'Toàn bộ đồ án cá nhân', 'Khảo sát yêu cầu; phân tích, thiết kế; xây dựng hệ thống Django; kiểm thử và viết báo cáo.']], [1.4, 1.6, 3.5])

    next_page(doc)
    add_heading(doc, 'MỤC LỤC')
    toc = [
        ('LỜI MỞ ĐẦU', 2, False), ('BẢNG PHÂN CHIA CÔNG VIỆC', 3, False),
        ('CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ', 5, True), ('1.1. Giới thiệu đề tài', 5, False), ('1.2. Lựa chọn công nghệ sử dụng', 6, False), ('1.3. Kết luận chương 1', 6, False),
        ('CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG', 7, True), ('2.1. Khảo sát yêu cầu hệ thống', 7, False), ('2.2. Biểu đồ Use Case', 8, False), ('2.3. Xây dựng kịch bản', 9, False), ('2.4. Biểu đồ lớp thực thể', 11, False), ('2.5. Biểu đồ tuần tự', 12, False), ('2.6. Thiết kế cơ sở dữ liệu', 13, False), ('2.7. Kết luận chương 2', 13, False),
        ('CHƯƠNG 3: KẾT QUẢ XÂY DỰNG ỨNG DỤNG', 14, True), ('3.1. Môi trường cài đặt', 14, False), ('3.2.1. Giao diện tổng quan', 15, False), ('3.2.2. Giao diện giao dịch và ghi chú', 16, False), ('3.2.3. Kiểm thử chức năng', 17, False), ('3.3. Kết luận chương 3', 17, False), ('KẾT LUẬN', 18, False), ('HƯỚNG PHÁT TRIỂN TƯƠNG LAI', 19, False)
    ]
    for title, page, bold in toc:
        para = doc.add_paragraph()
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.tab_stops.add_tab_stop(Inches(6.35), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        run = para.add_run(f'{title}\t{page}')
        run.bold = bold
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)

    next_page(doc)
    add_heading(doc, 'CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI VÀ LỰA CHỌN CÔNG NGHỆ')
    add_heading(doc, '1.1. Giới thiệu đề tài', 2)
    add_para(doc, 'Hệ thống quản lý chi tiêu hỗ trợ cá nhân ghi nhận các khoản thu, chi và xem tổng hợp theo tháng. Mỗi người dùng có danh mục và dữ liệu riêng; ngoài giao dịch, người dùng có thể lưu ghi chú gắn với một ngày để tra cứu.')
    add_heading(doc, '1.1.1. Lý do chọn đề tài', 3)
    add_para(doc, 'Việc tự theo dõi chi tiêu thường được thực hiện rời rạc bằng trí nhớ, giấy ghi chú hoặc nhiều ứng dụng khác nhau. Một website nhỏ có thể tập trung dữ liệu, giúp người dùng xem lại lịch sử và nhận biết nhóm chi tiêu chính mà không phải sử dụng các chức năng tài chính phức tạp.')
    add_heading(doc, '1.1.2. Mục tiêu xây dựng ứng dụng', 3)
    add_para(doc, 'Xây dựng hệ thống có đăng ký, đăng nhập; quản lý danh mục thu và chi; tạo, sửa, xóa và lọc giao dịch; hiển thị số liệu tổng hợp theo tháng; lưu ghi chú theo ngày; và bảo đảm người dùng chỉ truy cập dữ liệu của tài khoản mình.')
    add_heading(doc, '1.1.3. Kết quả dự kiến đạt được', 3)
    add_para(doc, 'Sản phẩm gồm website Django dùng được trên máy cá nhân, cơ sở dữ liệu quan hệ, biểu mẫu kiểm tra dữ liệu đầu vào, giao diện tiếng Việt, trang tổng quan có biểu đồ và bộ kiểm thử tự động cho những luồng nghiệp vụ chính.')
    add_heading(doc, 'Giới hạn đề tài', 2)
    add_para(doc, 'Phiên bản hiện tại không kết nối ngân hàng, không tự nhập giao dịch, không hỗ trợ nhiều loại tiền tệ, chia sẻ tài khoản hay xuất dữ liệu từ giao diện. Hệ thống được xây dựng phục vụ học tập và trình diễn.')

    next_page(doc)
    add_heading(doc, '1.2. LỰA CHỌN CÔNG NGHỆ SỬ DỤNG')
    add_table(doc, [['Thành phần', 'Công nghệ', 'Lý do sử dụng'], ['Ngôn ngữ', 'Python 3.12', 'Cú pháp dễ đọc, phù hợp học tập và có hệ sinh thái thư viện web.'], ['Backend', 'Django 5.2', 'Có sẵn định tuyến, ORM, biểu mẫu, xác thực và trang quản trị.'], ['Cơ sở dữ liệu', 'SQLite', 'Không cần cài dịch vụ riêng, thuận tiện chạy demo và kiểm thử.'], ['Giao diện', 'HTML, CSS, JavaScript', 'Dựng trang và tương tác cơ bản mà không cần thêm framework frontend.'], ['Biểu đồ', 'Chart.js', 'Hiển thị số liệu tổng hợp theo ngày và danh mục.'], ['Kiểm thử', 'Django TestCase', 'Kiểm tra nghiệp vụ và quyền truy cập bằng bộ công cụ tích hợp.']], [1.2, 1.6, 3.7])
    add_heading(doc, 'Kiến trúc triển khai', 2)
    add_image(doc, 'diagrams/architecture.png', width=6.25)
    caption(doc, 'Luồng chính: trình duyệt gửi yêu cầu đến URL, view kiểm tra biểu mẫu hoặc gọi service, ORM đọc/ghi SQLite và template trả kết quả cho người dùng.')
    add_heading(doc, '1.3. Kết luận chương 1', 2)
    add_para(doc, 'Python và Django giúp hoàn thiện nhanh các chức năng quản lý dữ liệu. SQLite phù hợp với phạm vi cá nhân; cấu trúc tách app hỗ trợ đọc và bảo trì mã nguồn. Các công nghệ này là nền tảng để phân tích và thiết kế các luồng ở chương tiếp theo.')

    next_page(doc)
    add_heading(doc, 'CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG')
    add_heading(doc, '2.1. Khảo sát yêu cầu hệ thống', 2)
    add_para(doc, 'Hệ thống hướng đến cá nhân muốn ghi chép thủ công thu, chi và ghi chú. Các chức năng nghiệp vụ yêu cầu đăng nhập; dữ liệu trong danh mục, giao dịch và ghi chú phải được giới hạn theo chủ sở hữu.')
    add_table(doc, [['Mã', 'Chức năng', 'Mô tả'], ['F1', 'Tài khoản', 'Đăng ký, đăng nhập, đăng xuất; tạo danh mục mặc định khi đăng ký.'], ['F2', 'Danh mục', 'Thêm, xem, sửa, xóa danh mục thu hoặc chi.'], ['F3', 'Giao dịch', 'Lưu số tiền, ngày, danh mục; lọc theo tháng, loại và danh mục.'], ['F4', 'Ghi chú', 'Tạo, xem dạng bảng, sửa và xóa ghi chú có ngày.'], ['F5', 'Tổng quan', 'Tổng hợp thu, chi, số dư và hiển thị biểu đồ.'], ['F6', 'Quản trị', 'Quản lý dữ liệu qua Django Admin theo quyền quản trị.']], [0.45, 1.1, 4.95])
    add_heading(doc, '2.1.1. Yêu cầu phi chức năng', 3)
    add_para(doc, 'Giao diện tiếng Việt; biểu mẫu báo lỗi khi dữ liệu không hợp lệ; dữ liệu số tiền dùng DecimalField; thao tác POST có CSRF; truy vấn theo tài khoản hiện tại; có thể khởi động cục bộ bằng SQLite.')
    add_heading(doc, '2.1.2. Quy trình nghiệp vụ', 3)
    add_para(doc, 'Người dùng đăng ký hoặc đăng nhập, chọn tháng trên trang tổng quan, tạo danh mục nếu cần, ghi giao dịch, xem lịch sử và tổng hợp. Khi cần ghi việc cần nhớ, người dùng nhập ngày cùng nội dung rồi theo dõi trong bảng Ghi chú.')

    next_page(doc)
    add_heading(doc, '2.2. BIỂU ĐỒ USE CASE')
    add_heading(doc, '2.2.1. Các tác nhân và Use Case tổng quát', 2)
    add_para(doc, 'Người dùng là một tác nhân xuyên suốt sơ đồ, gồm cả thao tác đăng ký/đăng nhập và nghiệp vụ sau khi xác thực. Các chức năng giao dịch, danh mục, ghi chú, tổng quan yêu cầu đăng nhập. Người có quyền staff hoặc superuser sử dụng thêm Django Admin.')
    add_table(doc, [['Tác nhân', 'Use Case chính'], ['Người dùng', 'Đăng ký / đăng nhập / đăng xuất; quản lý giao dịch, danh mục và ghi chú; xem tổng quan.'], ['Quản trị viên', 'Quản lý Category, Transaction, Note qua Django Admin.']], [1.3, 5.2])
    add_heading(doc, '2.2.2. Biểu đồ Use Case tổng quát', 2)
    add_image(doc, 'diagrams/usecase.png', width=6.15)
    caption(doc, 'Sơ đồ tác nhân và các chức năng chính của Hệ thống quản lý chi tiêu.')

    next_page(doc)
    add_heading(doc, '2.3. XÂY DỰNG KỊCH BẢN')
    add_heading(doc, 'Kịch bản đăng ký tài khoản', 2)
    add_table(doc, [['Mục', 'Nội dung'], ['Tác nhân', 'Người dùng chưa đăng nhập.'], ['Điều kiện', 'Tên đăng nhập chưa được sử dụng; thông tin mật khẩu hợp lệ.'], ['Luồng chính', 'Người dùng mở trang đăng ký, nhập thông tin và gửi biểu mẫu. View kiểm tra biểu mẫu, tạo tài khoản; tín hiệu tạo danh mục mặc định.'], ['Kết quả', 'Tài khoản được tạo, người dùng được đăng nhập tự động và chuyển đến trang tổng quan.'], ['Ngoại lệ', 'Nếu tên đăng nhập đã tồn tại hoặc dữ liệu không hợp lệ, biểu mẫu hiển thị lỗi để người dùng sửa.']], [1.15, 5.35], font_size=9)
    add_heading(doc, 'Kịch bản thêm giao dịch', 2)
    add_table(doc, [['Mục', 'Nội dung'], ['Tác nhân', 'Người dùng đã đăng nhập.'], ['Điều kiện', 'Danh mục thuộc tài khoản hiện tại; số tiền lớn hơn 0.'], ['Luồng chính', 'Chọn thêm giao dịch, nhập loại, danh mục, ngày, số tiền và nội dung tùy chọn; gửi biểu mẫu để lưu.'], ['Kết quả', 'Giao dịch gắn với người dùng hiện tại và xuất hiện trong danh sách.'], ['Ngoại lệ', 'Form giữ lại nội dung và báo lỗi nếu dữ liệu thiếu hoặc không đúng.']], [1.15, 5.35], font_size=9)

    next_page(doc)
    add_heading(doc, '2.3. XÂY DỰNG KỊCH BẢN (TIẾP THEO)')
    add_heading(doc, 'Kịch bản thêm ghi chú', 2)
    add_table(doc, [['Mục', 'Nội dung'], ['Tác nhân', 'Người dùng đã đăng nhập.'], ['Điều kiện', 'Người dùng mở chức năng Ghi chú.'], ['Luồng chính', 'Chọn Thêm ghi chú, nhập ngày và nội dung, gửi biểu mẫu. Hệ thống gắn ghi chú với tài khoản, lưu bản ghi và hiển thị lại trong bảng.'], ['Kết quả', 'Ghi chú xuất hiện cùng ngày, nội dung và thao tác sửa/xóa.'], ['Ngoại lệ', 'Nếu nội dung không hợp lệ, hệ thống báo lỗi và không lưu bản ghi.']], [1.15, 5.35], font_size=9)
    add_heading(doc, 'Sơ đồ hoạt động thêm ghi chú', 2)
    add_image(doc, 'diagrams/note_activity.png', width=4.6)
    caption(doc, 'Nhánh Không báo lỗi và cho nhập lại; nhánh Có lưu ghi chú rồi cập nhật bảng.')

    next_page(doc)
    add_heading(doc, '2.4. BIỂU ĐỒ LỚP THỰC THỂ')
    add_para(doc, 'Mô hình dữ liệu gồm tài khoản, danh mục, giao dịch và ghi chú. Category phân biệt danh mục thu/chi; Transaction giữ số tiền cùng ngày phát sinh; Note lưu ngày ghi chú và nội dung.')
    add_image(doc, 'diagrams/classes.png', width=6.2)
    caption(doc, 'Biểu đồ lớp khái quát các thực thể; ký hiệu 1–* biểu thị quan hệ một-nhiều.')
    add_table(doc, [['Lớp', 'Trách nhiệm'], ['User', 'Tài khoản đăng nhập và chủ sở hữu dữ liệu.'], ['Category', 'Tên, loại thu/chi và màu hiển thị; thuộc về một User.'], ['Transaction', 'Số tiền, ngày, loại danh mục; liên kết User và Category.'], ['Note', 'Ngày ghi chú, nội dung, thời gian tạo/cập nhật; thuộc về một User.']], [1.4, 5.1])

    next_page(doc)
    add_heading(doc, '2.5. BIỂU ĐỒ TUẦN TỰ')
    add_para(doc, 'Các sơ đồ thể hiện trao đổi giữa người dùng, view, form và cơ sở dữ liệu trong ba luồng tiêu biểu.')
    add_image(doc, 'diagrams/sequences.png', width=6.15)
    caption(doc, 'Các luồng đăng ký tài khoản, thêm giao dịch và thêm ghi chú.')

    next_page(doc)
    add_heading(doc, '2.6. THIẾT KẾ CƠ SỞ DỮ LIỆU')
    add_heading(doc, '2.6.1. Mô tả các bảng', 2)
    add_table(doc, [['Bảng', 'Thuộc tính chính', 'Ràng buộc / mô tả'], ['User', 'username, email, password', 'Django Authentication; chủ sở hữu dữ liệu cá nhân.'], ['Category', 'user, name, kind, color', 'Khóa ngoại User; tên danh mục duy nhất theo người dùng và loại.'], ['Transaction', 'user, category, amount, occurred_on, note', 'Số tiền DecimalField nguyên VNĐ; ngày là DateField; liên kết danh mục.'], ['Note', 'user, note_date, content, created_at, updated_at', 'Ghi chú có ngày; dữ liệu được lọc theo chủ sở hữu.']], [1.1, 2.25, 3.15], font_size=8.8)
    add_heading(doc, '2.6.2. Lược đồ cơ sở dữ liệu', 2)
    add_table(doc, [['Quan hệ', 'Ý nghĩa'], ['User 1 — N Category', 'Một tài khoản sở hữu nhiều danh mục.'], ['User 1 — N Transaction', 'Một tài khoản sở hữu nhiều giao dịch.'], ['Category 1 — N Transaction', 'Một danh mục phân loại nhiều giao dịch.'], ['User 1 — N Note', 'Một tài khoản sở hữu nhiều ghi chú.'], ['Category — Transaction', 'Form kiểm tra danh mục phải thuộc cùng User.']], [2.0, 4.5], font_size=9)
    add_heading(doc, 'Toàn vẹn dữ liệu', 2)
    add_para(doc, 'Các khóa ngoại duy trì quan hệ giữa bản ghi. Form kiểm tra dữ liệu trước khi lưu; queryset nghiệp vụ giới hạn theo User hiện tại để ngăn truy cập chéo tài khoản.')
    add_heading(doc, '2.7. Kết luận chương 2', 2)
    add_para(doc, 'Chương 2 đã xác định tác nhân, yêu cầu chức năng và quy trình nghiệp vụ của Hệ thống quản lý chi tiêu. Use Case, kịch bản, biểu đồ tuần tự, mô hình lớp và lược đồ dữ liệu tạo cơ sở cho triển khai Django, ORM và SQLite ở chương tiếp theo.')

    next_page(doc)
    add_heading(doc, 'CHƯƠNG 3: KẾT QUẢ XÂY DỰNG ỨNG DỤNG')
    add_heading(doc, '3.1. Môi trường cài đặt', 2)
    add_table(doc, [['Thành phần', 'Yêu cầu / sử dụng'], ['Hệ điều hành', 'Windows; thực hiện lệnh bằng PowerShell.'], ['Ngôn ngữ và framework', 'Python 3.12, Django 5.2.'], ['Cơ sở dữ liệu', 'SQLite; không cần dịch vụ database riêng.'], ['Frontend', 'HTML, CSS, JavaScript; Chart.js tải từ CDN để vẽ biểu đồ.'], ['Công cụ', 'Visual Studio Code hoặc editor tương đương; Git; trình duyệt web.']], [1.7, 4.8])
    add_heading(doc, 'Các bước cài đặt', 2)
    add_para(doc, 'Tạo môi trường ảo; cài requirements.txt; sao chép .env.example thành .env; chạy migrate; chạy lệnh seed_demo nếu cần dữ liệu mẫu; sau đó khởi động bằng python manage.py runserver.')
    add_para(doc, 'Tài khoản demo: demo / demo12345. Địa chỉ mặc định: http://127.0.0.1:8000/. Lệnh seed_demo tạo lại dữ liệu giao dịch demo; không tạo hoặc xóa ghi chú.')
    add_heading(doc, '3.2. Kết quả cài đặt', 2)
    add_para(doc, 'Các chức năng chính đã được triển khai gồm tài khoản, danh mục, giao dịch, bảng ghi chú có ngày, trang tổng quan và giao diện quản trị. Các trang nghiệp vụ yêu cầu đăng nhập và truy vấn dữ liệu theo tài khoản hiện tại.')

    next_page(doc)
    add_heading(doc, '3.2. KẾT QUẢ CÀI ĐẶT')
    add_heading(doc, '3.2.1. Giao diện tổng quan', 2)
    add_para(doc, 'Trang tổng quan cho phép chọn tháng, xem tổng thu, chi, số dư và theo dõi biểu đồ chi theo ngày hoặc danh mục.')
    add_image(doc, 'giao-dien-tong-quan.png', width=6.15)
    caption(doc, 'Hình 3.1. Giao diện tổng quan với dữ liệu demo.')
    add_para(doc, 'Số dư thể hiện chênh lệch thu và chi trong tháng đang xem; đây không phải số dư tài khoản ngân hàng.', italic=True)

    next_page(doc)
    add_heading(doc, '3.2.2. GIAO DỊCH VÀ GHI CHÚ')
    add_heading(doc, '3.2.2. Giao diện giao dịch và ghi chú', 2)
    add_para(doc, 'Danh sách giao dịch hiển thị ngày, danh mục, số tiền và nội dung; người dùng có thể lọc theo tháng, loại và danh mục. Bảng Ghi chú lưu ngày riêng cùng nội dung, hỗ trợ sửa và xóa.')
    add_image(doc, 'giao-dien-giao-dich.png', width=6.15)
    caption(doc, 'Hình 3.2. Danh sách giao dịch của tài khoản demo.')
    add_image(doc, 'giao-dien-ghi-chu.png', width=6.15)
    caption(doc, 'Hình 3.3. Bảng ghi chú hiển thị ngày, nội dung và thao tác.')

    next_page(doc)
    add_heading(doc, '3.2.3. KIỂM THỬ CHỨC NĂNG')
    add_table(doc, [['Nội dung kiểm thử', 'Kết quả'], ['Tạo tài khoản và danh mục mặc định', 'Đạt trong bộ test tự động.'], ['Tạo / sửa / xóa giao dịch', 'Đạt trong bộ test tự động.'], ['Tạo / sửa / xóa ghi chú có ngày', 'Đạt trong bộ test tự động.'], ['Phân quyền dữ liệu theo tài khoản', 'Đạt trong bộ test tự động.'], ['Kiểm tra tổng hợp và danh mục', 'Đạt trong bộ test tự động.'], ['Toàn bộ kiểm thử Django', '9 test chạy thành công; 0 lỗi.']], [3.8, 2.7])
    add_para(doc, 'Lệnh kiểm tra: python manage.py test. Kết quả ghi nhận gần nhất: Ran 9 tests; OK. Kiểm tra migration: makemigrations --check --dry-run báo không có thay đổi.', italic=True)
    add_heading(doc, '3.3. Kết luận chương 3', 2)
    add_para(doc, 'Ứng dụng đã triển khai được các luồng quản lý thu, chi và ghi chú theo ngày trên Django với SQLite. Trang tổng quan tính dữ liệu theo tháng; quyền truy cập bản ghi được giới hạn theo tài khoản. Các kiểm thử tự động hiện có đều đạt.')

    next_page(doc)
    add_heading(doc, 'KẾT LUẬN')
    add_para(doc, 'Đề tài xây dựng được ứng dụng web hỗ trợ ghi nhận thu nhập, chi tiêu và ghi chú cá nhân. Sản phẩm có đăng ký/đăng nhập, danh mục, giao dịch có lọc, bảng ghi chú theo ngày, tổng hợp tháng và biểu đồ. Thiết kế dữ liệu gắn với tài khoản, biểu mẫu kiểm tra đầu vào và 9 bài kiểm thử tự động tạo cơ sở cho việc sử dụng và tiếp tục phát triển.')
    add_para(doc, 'Hạn chế hiện tại gồm chưa kết nối ngân hàng, chưa xuất CSV/Excel, chưa có tìm kiếm ghi chú và chưa kiểm tra toàn diện giao diện trên nhiều thiết bị. SQLite phù hợp cho đồ án và demo, chưa hướng tới tải đồng thời lớn.')

    next_page(doc)
    add_heading(doc, 'HƯỚNG PHÁT TRIỂN TƯƠNG LAI')
    add_para(doc, 'Các hướng tiếp theo ưu tiên độ tin cậy, khả năng tra cứu và bảo vệ dữ liệu trước khi mở rộng tích hợp bên ngoài.')
    add_table(doc, [['Ưu tiên', 'Nội dung'], ['1', 'Mở rộng kiểm thử biên, kiểm thử biểu mẫu và giao diện.'], ['2', 'Thêm tìm kiếm, lọc ngày tùy chọn và xuất CSV/Excel.'], ['3', 'Bổ sung xác thực email, đặt lại mật khẩu và giới hạn đăng nhập.'], ['4', 'Chuyển sang PostgreSQL, bổ sung backup và logging khi triển khai.'], ['5', 'Hoàn thiện giao diện di động và khả năng tiếp cận.']], [0.8, 5.7])
    add_para(doc, 'Các tính năng cần được triển khai theo nhu cầu sử dụng thực tế và kèm kiểm thử tương ứng.')

    doc.core_properties.title = 'Báo cáo đồ án Hệ thống quản lý chi tiêu'
    doc.core_properties.author = 'Hoàng Bình Minh'
    doc.save(OUT)
    print(OUT)


if __name__ == '__main__':
    build()
