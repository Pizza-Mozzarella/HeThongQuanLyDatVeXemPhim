import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os
import shutil

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_natural_report():
    doc = Document()

    # Căn lề chuẩn văn bản sinh viên: Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)

    # Style văn bản chuẩn
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # TRANG BÌA
    # -------------------------------------------------------------
    p_school = doc.add_paragraph()
    p_school.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_school.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC ...\nKHOA CÔNG NGHỆ THÔNG TIN\n")
    r.font.bold = True
    r.font.size = Pt(12)
    p_school.paragraph_format.space_after = Pt(24)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_title.add_run("BÁO CÁO TIỂU LUẬN MÔN HỌC\nCẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT\n\n")
    r_sub.font.bold = True
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    r_main = p_title.add_run("ĐỀ TÀI 9: HỆ THỐNG QUẢN LÝ ĐẶT VÉ XEM PHIM\n")
    r_main.font.bold = True
    r_main.font.size = Pt(18)
    r_main.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    r_desc = p_title.add_run("(Cấu trúc dữ liệu: Danh sách liên kết đơn & Ma trận phòng chiếu 30 ghế)\n")
    r_desc.font.italic = True
    r_desc.font.size = Pt(12)
    p_title.paragraph_format.space_after = Pt(36)

    # Hộp thông tin nhóm
    info_table = doc.add_table(rows=5, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "ThS. / TS. [Tên giảng viên]"),
        ("Lớp học phần:", "[Tên lớp học phần]"),
        ("Nhóm sinh viên thực hiện:", "Nhóm số [Điền số nhóm]"),
        ("Trưởng nhóm:", "Vương Quốc Khang - MSSV: [Điền MSSV]"),
        ("Thời gian thực hiện:", "Học kỳ ... - Năm học 202..."),
    ]
    for row_idx, (label, val) in enumerate(info_data):
        row = info_table.rows[row_idx]
        p_lbl = row.cells[0].paragraphs[0]
        r1 = p_lbl.add_run(label)
        r1.font.bold = True
        r1.font.size = Pt(12)
        p_lbl.paragraph_format.space_after = Pt(3)

        p_val = row.cells[1].paragraphs[0]
        r2 = p_val.add_run(val)
        r2.font.size = Pt(12)
        p_val.paragraph_format.space_after = Pt(3)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(40)

    doc.add_page_break()

    # -------------------------------------------------------------
    # HÀM BỔ TRỢ ĐỊNH DẠNG
    # -------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(15)
        r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(13.5)
        r.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(13)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "F2F4F7")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x11, 0x22, 0x44)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_note_box(note_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "FFF9E6")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("📌 Ghi chú: " + note_text)
        r.font.italic = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor(0x80, 0x40, 0x00)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_placeholder(title, desc=""):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "FAFAFA")
        set_cell_margins(cell, top=200, bottom=200, left=200, right=200)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(f"📷 [HÌNH ẢNH MINH HỌA: {title}]\n")
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        if desc:
            r2 = p.add_run(f"({desc})\n")
            r2.font.italic = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        r3 = p.add_run("(Dùng phím Windows + Shift + S chụp cửa sổ console và dán trực tiếp vào đây)")
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # MỤC IV: BẢNG PHÂN CHIA CÔNG VIỆC NHÓM
    # -------------------------------------------------------------
    add_h1("IV. BẢNG PHÂN CHIA CÔNG VIỆC NHÓM")
    add_note_box("Mục này phân định rõ ràng các phần việc của 3 bạn trong nhóm để cùng theo dõi tiến độ.")

    team_table = doc.add_table(rows=4, cols=5)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(team_table)
    headers = ["STT", "Họ và tên", "MSSV", "Nhiệm vụ đảm nhiệm trong dự án", "Mức độ HT"]

    hdr_cells = team_table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "D9E1F2")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(11)

    team_data = [
        ("1", "Vương Quốc Khang\n(Trưởng nhóm)", "[MSSV]",
         "• Phân chia cấu trúc file, thiết kế Struct và Danh sách liên kết đơn.\n"
         "• Viết bộ hàm validation nhập liệu an toàn (nhapChuoi, nhapSoNguyen, nhapSoThuc).\n"
         "• Quản lý tệp CSDL (cinema_db.txt), căn lề hiển thị bảng console 104 cột.\n"
         "• Phụ trách Chức năng 1 (Nhập phim) & Chức năng 2 (Xem danh sách phim).\n"
         "• Viết báo cáo: Phần 1 (Giới thiệu) & Phần 2 (Phân tích yêu cầu & Giải pháp).", "100%"),
        ("2", "[Tên Thành viên 2]", "[MSSV]",
         "• Viết hàm tìm kiếm mã phim timPhimTheoMa không phân biệt hoa thường.\n"
         "• Phụ trách Chức năng 3 (Tìm kiếm phim theo mã, tên, giá vé).\n"
         "• Phụ trách Chức năng 4 (Xóa phim an toàn, xử lý ca biên đầu/giữa/cuối).\n"
         "• Viết báo cáo: Phần 3 (Thiết kế CTDL) & Phần 4 (Mô tả nghiệp vụ & Code).", "100%"),
        ("3", "[Tên Thành viên 3]", "[MSSV]",
         "• Phụ trách Chức năng 5 (Cập nhật thông tin phim theo từng trường).\n"
         "• Phụ trách Chức năng 6 (Sắp xếp danh sách phim bằng Bubble Sort).\n"
         "• Phụ trách Chức năng 7 & 8 (Xem sơ đồ 30 ghế, Đặt vé cấp mã #1001, Hủy vé).\n"
         "• Viết báo cáo: Phần 5 (Chạy app & Chụp ảnh minh họa) & Phần 6 (Nhận xét).", "100%"),
    ]

    for row_idx, data in enumerate(team_data, start=1):
        row_cells = team_table.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(10.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # MỤC V: BÁO CÁO TIỂU LUẬN CHI TIẾT
    # -------------------------------------------------------------
    add_h1("V. BÁO CÁO TIỂU LUẬN CHI TIẾT")

    # 1. Giới thiệu đề tài
    add_h2("1. Giới thiệu đề tài")
    add_h3("1.1. Bối cảnh và lý do chọn đề tài")
    doc.add_paragraph(
        "Hiện nay, nhu cầu giải trí xem phim tại rạp của mọi người ngày càng tăng cao. Mỗi rạp chiếu phim hàng ngày "
        "đều có rất nhiều suất chiếu, nhiều bộ phim thuộc các thể loại khác nhau với mức giá vé và khung giờ chiếu riêng biệt. "
        "Cùng với đó, việc quản lý tình trạng ghế ngồi của từng phòng chiếu để tránh việc bán trùng ghế của khách hàng là một yêu cầu "
        "vô cùng quan trọng. Vì vậy, việc xây dựng một phần mềm quản lý đặt vé xem phim sẽ giúp cho nhân viên rạp thao tác nhanh chóng, "
        "chính xác và phục vụ khách hàng tốt hơn."
    )
    doc.add_paragraph(
        "Từ thực tế đó, nhóm chúng em đã chọn 'Đề tài 9: Hệ thống quản lý đặt vé xem phim' để áp dụng các kiến thức đã học "
        "trong môn Cấu trúc dữ liệu và Giải thuật, đặc biệt là danh sách liên kết đơn và mảng hai chiều, vào việc giải quyết bài toán quản lý này."
    )

    add_h3("1.2. Mục tiêu của đề tài")
    doc.add_paragraph(
        "- Về mặt học tập: Nắm vững và áp dụng thành thạo cấu trúc dữ liệu Danh sách liên kết đơn (Singly Linked List), "
        "biết cách quản lý con trỏ, cấp phát và giải phóng vùng nhớ động trên Heap để không bị rò rỉ bộ nhớ. Thực hiện được các thao tác "
        "cơ bản như thêm, sửa, xóa, tìm kiếm và sắp xếp trên danh sách liên kết.\n"
        "- Về mặt thực tế: Viết được một chương trình console hoàn chỉnh bằng C++, đáp ứng đầy đủ các chức năng quản lý phim và đặt vé, "
        "kiểm tra dữ liệu nhập vào cẩn thận để chương trình chạy mượt mà, không bị lỗi trôi lệnh cin hay crash, đồng thời tự động lưu trữ dữ liệu vào file text."
    )

    add_h3("1.3. Phạm vi đề tài")
    doc.add_paragraph(
        "- Đối tượng quản lý: Thông tin các bộ phim (Mã phim, Tên phim, Thể loại, Thời lượng, Giá vé) và sơ đồ 30 ghế ngồi (5 hàng x 6 cột) của mỗi phim.\n"
        "- Môi trường: Ứng dụng chạy trên màn hình dòng lệnh console (Terminal), dữ liệu được lưu bền vững vào file text cinema_db.txt."
    )

    # 2. Phân tích yêu cầu và giải pháp
    add_h2("2. Phân tích yêu cầu và giải pháp")
    add_h3("2.1. Yêu cầu chức năng của hệ thống")
    doc.add_paragraph(
        "Chương trình đáp ứng đầy đủ các chức năng sau:\n"
        "1. Thêm danh sách phim mới: Cho phép nhập liên tục nhiều bộ phim từ bàn phím. Kiểm tra mã phim không được trùng nhau, kiểm tra thời lượng và giá vé hợp lệ, tự động tạo 30 ghế trống cho phim mới.\n"
        "2. Xem danh sách phim: In toàn bộ phim ra màn hình dạng bảng rõ ràng, căn lề thẳng hàng, không bị lệch cột khi tên phim dài.\n"
        "3. Tìm kiếm phim: Tìm theo mã phim, tìm theo từ khóa tên phim (không phân biệt chữ hoa thường), tìm theo khoảng giá vé từ min đến max.\n"
        "4. Xóa phim: Xóa một bộ phim theo mã hoặc theo tên, có hỏi xác nhận trước khi xóa, xử lý tốt việc xóa ở đầu, ở giữa hoặc ở cuối danh sách liên kết.\n"
        "5. Cập nhật thông tin phim: Tra cứu phim theo mã rồi cho phép người dùng chọn sửa từng mục (Tên, Thể loại, Thời lượng, Giá vé) mà không cần phải nhập lại hết.\n"
        "6. Sắp xếp danh sách phim: Sắp xếp theo giá vé (tăng dần hoặc giảm dần) và theo thời lượng chiếu (ngắn đến dài hoặc dài đến ngắn) bằng thuật toán Bubble Sort.\n"
        "7. Xem sơ đồ ghế phòng chiếu: Vẽ trực quan sơ đồ 30 ghế dạng ma trận 5 hàng (A-E) x 6 cột (1-6), thể hiện rõ ghế nào còn trống, ghế nào đã được đặt.\n"
        "8. Đặt vé & Hủy vé xem phim: Khách chọn phim, xem ghế trống, chọn số ghế muốn đặt, nhập họ tên và số điện thoại, hệ thống tự cấp mã vé (từ #1001 trở đi). Hỗ trợ hủy vé đã đặt để trả ghế về trạng thái trống.\n"
        "9. Tự động đọc và lưu file: Khi mở chương trình thì tự động đọc dữ liệu từ file cinema_db.txt lên RAM. Mỗi khi có thao tác thêm, sửa, xóa, đặt vé hay hủy vé thì tự động lưu ngay lại vào file."
    )

    add_h3("2.2. Giải pháp kỹ thuật")
    doc.add_paragraph(
        "- Tổ chức mã nguồn gọn gàng, chia thành các phần rõ ràng: Khai báo thư viện -> Hằng số -> Struct -> Khai báo nguyên mẫu hàm -> "
        "Bộ hàm tiện ích nhập liệu an toàn -> Hàm đọc/ghi file -> Các hàm chức năng nghiệp vụ -> Hàm Menu và hàm main.\n"
        "- Dùng Danh sách liên kết đơn để lưu các bộ phim: Giúp chương trình có thể thêm bớt phim thoải mái trong khi chạy mà không sợ bị giới hạn kích thước như mảng tĩnh.\n"
        "- Dùng mảng 2 chiều 5x6 cho mỗi phim: Tương ứng với 30 ghế ngồi thực tế trong phòng chiếu, mỗi ô ghế lưu trạng thái đã đặt hay chưa và thông tin vé.\n"
        "- Dùng bộ hàm nhapChuoi, nhapSoNguyen, nhapSoThuc dùng getline và stringstream: Giúp ngăn chặn triệt để tình trạng trôi lệnh và người dùng lỡ nhập sai kiểu dữ liệu cũng không làm chương trình bị tắt đột ngột."
    )

    # 3. Thiết kế cấu trúc dữ liệu
    add_h2("3. Thiết kế cấu trúc dữ liệu và mô hình chương trình")
    add_h3("3.1. Các struct sử dụng trong chương trình")
    doc.add_paragraph("a) Struct thông tin vé (MaVe):")
    add_code_block("struct MaVe {\n    int    soVe;      // 0 = chưa đặt, >= 1001 = mã số vé đã đặt\n    string tenKhach;  // Họ và tên khách hàng\n    string sdt;       // Số điện thoại liên hệ\n};")

    doc.add_paragraph("b) Struct thông tin một ô ghế (ThongTinGhe):")
    add_code_block("struct ThongTinGhe {\n    bool  daDat;      // false = ghế còn trống, true = ghế đã đặt\n    MaVe  ve;         // Thông tin vé đi kèm khi ghế đã đặt\n};")

    doc.add_paragraph("c) Struct thông tin một bộ phim (Phim):")
    add_code_block("struct Phim {\n    string       ma;                    // Mã phim (VD: P01, P02)\n    string       ten;                   // Tên bộ phim\n    string       theLoai;               // Thể loại phim\n    int          thoiLuong;             // Thời lượng chiếu (phút)\n    double       giaVe;                 // Đơn giá vé (VND)\n    ThongTinGhe  ghe[SO_HANG][SO_COT]; // Ma trận ghế 5 hàng x 6 cột\n};")

    doc.add_paragraph("d) Struct một Node trong Danh sách liên kết đơn (NodePhim):")
    add_code_block("struct NodePhim {\n    Phim      data;   // Dữ liệu của bộ phim\n    NodePhim* next;   // Con trỏ trỏ tới bộ phim tiếp theo\n};")

    add_h3("3.2. Mô hình liên kết trên bộ nhớ RAM")
    doc.add_paragraph(
        "Chương trình quản lý toàn bộ các bộ phim thông qua con trỏ đầu danh sách 'headPhim'. "
        "Mỗi node phim được lưu trên vùng nhớ Heap và nối tiếp nhau qua con trỏ next, node cuối cùng sẽ trỏ vào nullptr:\n"
        "headPhim ──► [Phim 1: P01] ──► [Phim 2: P02] ──► ... ──► [Phim 10: P10] ──► nullptr\n"
        "Trong mỗi node phim đều chứa sẵn một ma trận 30 ghế ngồi độc lập của riêng bộ phim đó."
    )

    add_h3("3.3. Quy ước ánh xạ số ghế trong phòng chiếu")
    doc.add_paragraph(
        "Phòng chiếu có 30 ghế, đánh số từ 01 đến 30. Công thức quy đổi giữa số thứ tự của ghế 'so' và vị trí hàng r, cột c trong mảng ghe[r][c]:\n"
        "- Hàng r = (so - 1) / 6 (với r từ 0 đến 4, tương ứng các hàng A, B, C, D, E).\n"
        "- Cột c = (so - 1) % 6 (với c từ 0 đến 5, tương ứng các cột 1, 2, 3, 4, 5, 6).\n"
        "- Khi biết hàng r và cột c, số thứ tự ghế được tính lại bằng: so = r * 6 + c + 1."
    )

    add_h3("3.4. Mô hình luồng hoạt động tổng quan của hệ thống")
    doc.add_paragraph(
        "Toàn bộ chu trình vận hành từ lúc nạp dữ liệu ban đầu từ file cinema_db.txt, điều hướng menu, "
        "thực thi các nhóm chức năng nghiệp vụ, đồng bộ dữ liệu đĩa và thu hồi bộ nhớ Heap khi thoát được tóm lược bằng sơ đồ luồng tổng quan:"
    )
    add_code_block(
        "graph LR\n"
        "    subgraph KHOI_DONG [\"1. Khởi Động & Nạp CSDL\"]\n"
        "        A([Bắt đầu main]) --> B[Đọc file cinema_db.txt]\n"
        "        B --> C[Nạp vào DSLK & 30 ghế trên RAM]\n"
        "    end\n\n"
        "    subgraph DIEU_HUONG [\"2. Điều Hướng Menu Chính\"]\n"
        "        C --> D[Hiển thị Menu 8 chức năng]\n"
        "        D --> E{Chọn chức năng 1-8 hoặc 0}\n"
        "    end\n\n"
        "    subgraph XU_LY [\"3. Xử Lý Nghiệp Vụ\"]\n"
        "        E -- 1, 4, 5, 6 --> F[Quản lý phim: Thêm/Xóa/Sửa/Sắp xếp]\n"
        "        E -- 2, 3, 7 --> G[Tra cứu & Hiển thị: Bảng 104 cột / Sơ đồ ghế]\n"
        "        E -- 8 --> H[Phòng vé: Đặt vé / Hủy vé]\n"
        "    end\n\n"
        "    subgraph DONG_BO [\"4. Đồng Bộ & Lưu Trữ\"]\n"
        "        F --> I[Ghi đè cinema_db.txt]\n"
        "        H --> I\n"
        "        I --> D\n"
        "        G --> D\n"
        "    end\n\n"
        "    subgraph KET_THUC [\"5. Thoát & Giải Phóng\"]\n"
        "        E -- Chọn 0 --> J[Giải phóng bộ nhớ Heap]\n"
        "        J --> K([Kết thúc chương trình])\n"
        "    end"
    )

    # 4. MÔ TẢ NGHIỆP VỤ VÀ CÁC ĐOẠN MÃ QUAN TRỌNG
    add_h2("4. Mô tả nghiệp vụ chi tiết và các đoạn mã quan trọng")
    add_note_box(
        "Phân công nhiệm vụ nhóm: Nhóm trưởng đã viết mẫu chi tiết văn xuôi cho Chức năng 1, 2, 7, 8 và mục 4.9. "
        "Thành viên 2 chịu trách nhiệm hoàn thiện Chức năng 3 (Tìm kiếm) và Chức năng 4 (Xóa phim). "
        "Thành viên 3 chịu trách nhiệm hoàn thiện Chức năng 5 (Cập nhật) và Chức năng 6 (Sắp xếp). "
        "Các thành viên dựa theo dàn ý hướng dẫn từng bước để tự điền nội dung và dán mã nguồn vào các ô trống tương ứng."
    )

    # 4.1. CHỨC NĂNG 1
    add_h3("4.1. Chức năng 1: Nhập danh sách phim mới (nhapDanhSachPhim, nhapMotPhim, themPhim)")
    doc.add_paragraph(
        "Khi người dùng chọn chức năng 1 từ menu chính, chương trình sẽ gọi hàm nhapDanhSachPhim(). "
        "Hàm này cho phép nhập liên tục nhiều bộ phim cho đến khi nào người dùng không muốn nhập nữa thì dừng lại. "
        "Quá trình thực hiện diễn ra theo các bước cụ thể như sau:\n\n"
        "1. Bước 1: Nhập thông tin từng bộ phim (gọi hàm nhapMotPhim):\n"
        "   - Đầu tiên là nhập mã phim. Để đảm bảo tính duy nhất, chương trình cho người dùng nhập mã qua hàm nhapChuoi() "
        "rồi gọi kiemTraTrungMa() (hàm này dùng timPhimTheoMa()). Hàm sẽ so sánh mã vừa nhập với tất cả các phim đang có trong danh sách liên kết "
        "mà không phân biệt chữ hoa chữ thường. Nếu thấy mã đã tồn tại (ví dụ trong danh sách đã có 'P01' mà người dùng lại nhập 'p01' hay 'P01') "
        "thì chương trình sẽ xuất thông báo '[!] Ma phim DA TON TAI! Vui long dung ma khac.' và bắt buộc người dùng phải nhập lại mã khác. "
        "Chỉ khi nào nhập mã chưa từng có trong hệ thống thì mới được chuyển sang bước tiếp theo.\n"
        "   - Tiếp theo, người dùng nhập lần lượt: Tên phim, Thể loại, Thời lượng và Giá vé. Các trường này đều được nhập qua các hàm kiểm tra an toàn: "
        "nhapChuoi() kiểm tra bắt buộc không được để trống chuỗi; nhapSoNguyen() kiểm tra thời lượng phải là số nguyên trong khoảng từ 15 đến 360 phút; "
        "nhapSoThuc() kiểm tra giá vé phải là số thực từ 10.000 đến 1.000.000 VND. Nếu người dùng lỡ tay gõ chữ cái vào ô số, chương trình sẽ nhắc nhở và cho nhập lại chứ không bị crash.\n"
        "   - Sau khi nhập xong các thông tin cơ bản, chương trình tự động chạy 2 vòng lặp (5 hàng x 6 cột) để khởi tạo toàn bộ 30 ghế ngồi của phim này ở trạng thái ghế trống (daDat = false và ve = {0, '', ''}).\n\n"
        "2. Bước 2: Thêm phim vào danh sách liên kết (gọi hàm themPhim):\n"
        "   - Hàm themPhim() sẽ tạo một Node mới trên bộ nhớ Heap bằng lệnh new NodePhim{ p, nullptr }.\n"
        "   - Nếu danh sách ban đầu đang rỗng (head == nullptr) thì gán luôn head = node.\n"
        "   - Nếu danh sách đã có các phim từ trước thì dùng một con trỏ tạm duyệt từ đầu đến node cuối cùng (node có next == nullptr) rồi nối node mới vào sau.\n\n"
        "3. Bước 3: Hỏi người dùng có muốn nhập tiếp hay không:\n"
        "   - Chương trình in ra câu hỏi: 'Ban co muon nhap them phim nua khong? (y/n)'.\n"
        "   - Nếu người dùng nhập 'y' hoặc 'Y', chương trình tăng biến đếm số lượng phim lên 1 và tiếp tục lặp lại Bước 1 để nhập bộ phim tiếp theo.\n"
        "   - Nếu người dùng nhập ký tự khác, vòng lặp nhập phim sẽ dừng lại.\n\n"
        "4. Bước 4: Đồng bộ dữ liệu xuống file:\n"
        "   - Ngay sau khi kết thúc việc nhập, chương trình sẽ gọi hàm ghiToanBoFile(FILE_DB, head) để ghi đè toàn bộ danh sách phim từ bộ nhớ RAM xuống file text cinema_db.txt. "
        "Việc này đảm bảo dữ liệu mới nhập được lưu lại vĩnh viễn, kể cả khi tắt máy cũng không bị mất."
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) của chức năng 1:")
    add_code_block(
        "graph TD\n"
        "    A([Bắt đầu: nhapDanhSachPhim]) --> B[Khởi tạo dem = 0]\n"
        "    B --> C[Gọi nhapMotPhim: Nhập mã phim]\n"
        "    C --> D{kiemTraTrungMa?}\n"
        "    D -- Đúng: Đã có mã --> E[Báo lỗi: Mã phim đã tồn tại]\n"
        "    E --> C\n"
        "    D -- Sai: Mã hợp lệ --> F[Nhập Tên, Thể loại, Thời lượng, Giá vé]\n"
        "    F --> G[Vòng lặp 5x6: Khởi tạo 30 ghế trống daDat=false]\n"
        "    G --> H[Gọi themPhim: Cấp phát new NodePhim]\n"
        "    H --> I{head == nullptr?}\n"
        "    I -- Đúng --> J[Gán head = node]\n"
        "    I -- Sai --> K[Duyệt đến đuôi DSLK, nối node mới vào sau]\n"
        "    J --> L[Hỏi người dùng: Có nhập tiếp không? y/n]\n"
        "    K --> L\n"
        "    L -- Chọn y/Y --> C\n"
        "    L -- Chọn n/khác --> M[Gọi ghiToanBoFile ghi đè xuống cinema_db.txt]\n"
        "    M --> N([Kết thúc: Hoàn tất nhập phim])"
    )
    doc.add_paragraph("Đoạn mã nguồn của chức năng 1:")
    add_code_block(
        "Phim nhapMotPhim(NodePhim* head) {\n"
        "    Phim p{};\n"
        "    while (true) {\n"
        "        p.ma = nhapChuoi(\"  + Nhap ma phim (VD: P05): \");\n"
        "        if (kiemTraTrungMa(head, p.ma))\n"
        "            cout << \"  [!] Ma phim '\" << p.ma << \"' DA TON TAI! Vui long dung ma khac.\\n\";\n"
        "        else break;\n"
        "    }\n"
        "    p.ten       = nhapChuoi(\"  + Nhap ten phim: \");\n"
        "    p.theLoai   = nhapChuoi(\"  + Nhap the loai: \");\n"
        "    p.thoiLuong = nhapSoNguyen(\"  + Nhap thoi luong (15 - 360 phut): \", 15, 360);\n"
        "    p.giaVe     = nhapSoThuc(\"  + Nhap gia ve (10,000 - 1,000,000 VND): \", 10000, 1000000);\n"
        "    for (int r = 0; r < SO_HANG; r++)\n"
        "        for (int c = 0; c < SO_COT; c++) {\n"
        "            p.ghe[r][c].daDat = false;\n"
        "            p.ghe[r][c].ve = {0, \"\", \"\"};\n"
        "        }\n"
        "    return p;\n"
        "}\n\n"
        "void themPhim(NodePhim*& head, Phim p) {\n"
        "    NodePhim* node = new NodePhim{ p, nullptr };\n"
        "    if (head == nullptr) { head = node; return; }\n"
        "    NodePhim* t = head;\n"
        "    while (t->next != nullptr) t = t->next;\n"
        "    t->next = node;\n"
        "}"
    )

    # 4.2. CHỨC NĂNG 2
    add_h3("4.2. Chức năng 2: Hiển thị danh sách phim dạng bảng (xemDanhSachPhim, inTieuDeBang, inDongPhim)")
    doc.add_paragraph(
        "Chức năng xem danh sách phim được thực hiện qua hàm xemDanhSachPhim(). Mục đích là in toàn bộ danh mục phim "
        "ra màn hình dưới dạng bảng có kẻ ô rõ ràng, căn lề thẳng hàng để người xem dễ theo dõi. Luồng chạy cụ thể như sau:\n\n"
        "1. Kiểm tra danh sách rỗng:\n"
        "   - Tại menu chính, trước khi gọi hàm xem danh sách, chương trình sẽ kiểm tra con trỏ headPhim. "
        "Nếu headPhim == nullptr (nghĩa là trong hệ thống chưa có bộ phim nào) thì màn hình sẽ báo lỗi '[!] Danh sach hien dang trong, vui long nhap phim truoc!' "
        "và không in bảng ra, tránh việc in một cái bảng trống không có nội dung.\n\n"
        "2. In dòng tiêu đề bảng:\n"
        "   - Nếu có phim, chương trình gọi hàm inTieuDeBang(). Hàm này sẽ dùng lệnh printf để in ra dòng tiêu đề gồm 5 cột: "
        "Mã phim (rộng 8 ký tự), Tên Phim (rộng 40 ký tự), Thể loại (rộng 24 ký tự), Thời lượng (rộng 14 ký tự) và Giá vé (rộng 14 ký tự). "
        "Ngay sau đó, in ra một đường gạch ngang dài đúng 104 dấu gạch '-' để làm đường viền trên của bảng.\n"
        "   - Việc để cột Tên phim rộng 40 ký tự và Thể loại rộng 24 ký tự giúp cho những phim có tên rất dài (như 'Spider-Man: Across Spider-Verse' dài 31 ký tự) "
        "hoặc thể loại ghép (như 'Lich Su - Chinh Kich' dài 20 ký tự) vẫn nằm gọn gàng trong ô của nó, không bị tràn sang cột bên cạnh làm xô lệch bảng.\n\n"
        "3. Duyệt danh sách liên kết để in từng bộ phim:\n"
        "   - Chương trình gán con trỏ tạm NodePhim* p = headPhim, sau đó dùng vòng lặp while (p != nullptr) để đi qua từng node từ đầu đến cuối danh sách.\n"
        "   - Với mỗi node, chương trình gọi hàm inDongPhim(p->data). Trong hàm này, thời lượng được chuyển thành chuỗi '... phut' "
        "và giá vé được chuyển thành chuỗi '... VND', sau đó in ra khớp hoàn toàn với độ rộng của các cột đã định nghĩa ở phần tiêu đề.\n"
        "   - In xong một phim thì dời con trỏ sang node kế tiếp bằng lệnh p = p->next.\n\n"
        "4. Đóng bảng:\n"
        "   - Sau khi con trỏ p duyệt đến cuối danh sách (p == nullptr), chương trình in ra một đường kẻ kép gồm 104 dấu '=' "
        "để đóng lại bảng danh sách, giúp phần hiển thị kết thúc một cách rõ ràng và chuyên nghiệp."
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) của chức năng 2:")
    add_code_block(
        "graph TD\n"
        "    A([Bắt đầu: xemDanhSachPhim]) --> B{headPhim == nullptr?}\n"
        "    B -- Đúng: DS rỗng --> C[Thông báo: Danh sách hiện đang trống!]\n"
        "    C --> D([Kết thúc])\n"
        "    B -- Sai: Có phim --> E[Gọi inTieuDeBang: In 5 cột tiêu đề]\n"
        "    E --> F[In đường kẻ ngang 104 dấu '-']\n"
        "    F --> G[Gán con trỏ tạm: p = headPhim]\n"
        "    G --> H{p != nullptr?}\n"
        "    H -- Đúng: Còn phim --> I[Gọi inDongPhim: In căn lề chuẩn 104 ký tự]\n"
        "    I --> J[Chuyển sang node kế tiếp: p = p->next]\n"
        "    J --> H\n"
        "    H -- Sai: Hết danh sách --> K[In đường kẻ kép 104 dấu '=' đóng bảng]\n"
        "    K --> L([Kết thúc: Hoàn tất hiển thị])"
    )
    doc.add_paragraph("Đoạn mã nguồn của chức năng 2:")
    add_code_block(
        "void inTieuDeBang() {\n"
        "    printf(\"\\n%-8s %-40s %-24s %-14s %-14s\\n\", \"Ma\", \"Ten Phim\", \"The Loai\", \"Thoi Luong\", \"Gia Ve\");\n"
        "    printf(\"%s\\n\", string(104, '-').c_str());\n"
        "}\n\n"
        "void inDongPhim(const Phim& p) {\n"
        "    string thoiLuongStr = to_string(p.thoiLuong) + \" phut\";\n"
        "    string giaVeStr     = to_string((long long)p.giaVe) + \" VND\";\n"
        "    printf(\"%-8s %-40s %-24s %-14s %-14s\\n\",\n"
        "           p.ma.c_str(), p.ten.c_str(), p.theLoai.c_str(), thoiLuongStr.c_str(), giaVeStr.c_str());\n"
        "}\n\n"
        "void xemDanhSachPhim(NodePhim* headPhim) {\n"
        "    inTieuDeBang();\n"
        "    NodePhim* p = headPhim;\n"
        "    while (p != nullptr) {\n"
        "        inDongPhim(p->data);\n"
        "        p = p->next;\n"
        "    }\n"
        "    printf(\"%s\\n\", string(104, '=').c_str());\n"
        "}"
    )

    # 4.3. CHỨC NĂNG 3
    add_h3("4.3. Chức năng 3: Tìm kiếm phim đa tiêu chí (hienMenuTimKiem, timTheoMa, timTheoTen, timTheoGia, inDanhSachKetQua)")
    add_note_box(
        "✍️ [GIAO VIỆC CHO THÀNH VIÊN 2]: Dựa vào văn phong tự nhiên ở Chức năng 1 và 2 ở trên, bạn hãy tự viết mô tả nghiệp vụ chi tiết cho chức năng Tìm kiếm phim theo các gợi ý sau:\n"
        "- Bước 1: Giới thiệu menu con của chức năng tìm kiếm gồm các tiêu chí: 1. Tìm theo mã phim, 2. Tìm theo tên phim, 3. Tìm theo khoảng giá vé, 0. Quay lại menu chính.\n"
        "- Bước 2: Giải thích cơ chế kiểm tra khớp dữ liệu trong các hàm tìm kiếm: hàm chuyenChuThuong kết hợp hàm find() để tìm chuỗi con gần đúng không phân biệt chữ hoa thường (cho mã và tên phim); hàm timTheoGia kiểm tra giá vé nằm trong đoạn [giaMin, giaMax].\n"
        "- Bước 3: Duyệt danh sách liên kết đơn bằng con trỏ tạm, nếu khớp tiêu chí thì gọi inDongPhim(p->data) để in ra dạng bảng 104 cột, đồng thời tăng biến đếm số lượng phim tìm thấy.\n"
        "- Bước 4: Xử lý thông báo kết quả: nếu không tìm thấy phim nào thì báo lỗi, nếu tìm thấy thì in dòng gạch ngang đóng bảng và thông báo tổng số phim tìm được."
    )
    doc.add_paragraph("[VỊ TRÍ ĐỂ THÀNH VIÊN 2 TỰ GÕ BÀI VÀO ĐÂY]:\n(Thành viên 2 hãy xóa dòng này và tự gõ phần giải thích các bước theo hướng dẫn ở trên...)\n\n\n")
    doc.add_paragraph("Đoạn mã nguồn của chức năng 3:")
    add_code_block("// [Thành viên 2 dán đoạn code các hàm timTheoMa, timTheoTen, timTheoGia, inDanhSachKetQua, hienMenuTimKiem từ main_refactored.cpp vào đây]\n\n")

    # 4.4. CHỨC NĂNG 4
    add_h3("4.4. Chức năng 4: Xóa phim khỏi hệ thống (hienMenuXoaPhim, khopPhim, xoaPhim)")
    add_note_box(
        "✍️ [GIAO VIỆC CHO THÀNH VIÊN 2]: Dựa vào văn phong tự nhiên ở Chức năng 1 và 2 ở trên, bạn hãy tự viết mô tả nghiệp vụ chi tiết cho chức năng Xóa phim theo các gợi ý sau:\n"
        "- Bước 1: Kiểm tra danh sách rỗng (headPhim == nullptr). Nếu có phim, hiển thị menu chọn xóa: 1. Xóa theo mã phim, 2. Xóa theo tên phim, 0. Quay lại.\n"
        "- Bước 2: Duyệt danh sách tìm kiếm phim cần xóa bằng hàm khopPhim(). Nếu tìm thấy, in thông tin bộ phim đó ra màn hình để người dùng kiểm tra lại và hỏi xác nhận an toàn: 'Ban co CHAC CHAN muon xoa phim nay? (y/n)'. Nếu chọn 'n' thì hủy, giữ nguyên dữ liệu.\n"
        "- Bước 3: Giải thích thuật toán tách node trong hàm xoaPhim(): xử lý 2 trường hợp (Trường hợp 1: Node cần xóa ở ngay đầu danh sách thì dời head = head->next; Trường hợp 2: Node nằm ở giữa hoặc cuối thì dùng con trỏ p duyệt đến node trước đó rồi ngắt liên kết p->next = del->next). Sau đó dùng lệnh delete del để giải phóng vùng nhớ Heap.\n"
        "- Bước 4: Gọi ngay hàm ghiToanBoFile(FILE_DB, headPhim) để đồng bộ danh sách mới xuống file cinema_db.txt."
    )
    doc.add_paragraph("[VỊ TRÍ ĐỂ THÀNH VIÊN 2 TỰ GÕ BÀI VÀO ĐÂY]:\n(Thành viên 2 hãy xóa dòng này và tự gõ phần giải thích các bước theo hướng dẫn ở trên...)\n\n\n")
    doc.add_paragraph("Đoạn mã nguồn của chức năng 4:")
    add_code_block("// [Thành viên 2 dán đoạn code các hàm khopPhim, xoaPhim, hienMenuXoaPhim từ main_refactored.cpp vào đây]\n\n")

    # 4.5. CHỨC NĂNG 5
    add_h3("4.5. Chức năng 5: Cập nhật thông tin phim (capNhatThongTinPhim)")
    doc.add_paragraph(
        "Chức năng Cập nhật thông tin phim cho phép nhân viên rạp chỉnh sửa linh hoạt từng trường thông tin của một bộ phim "
        "(Tên phim, Thể loại, Thời lượng chiếu, Giá vé) mà không cần phải nhập lại toàn bộ từ đầu hay làm mất tình trạng 30 ghế ngồi đã đặt. "
        "Quy trình nghiệp vụ diễn ra theo 4 bước tuần tự như sau:\n\n"
        "1. Bước 1: Tra cứu phim cần cập nhật:\n"
        "   - Người dùng nhập mã phim cần sửa (ví dụ: P01, P02...). Để tạo sự thuận tiện, chương trình cho phép nhập '0' nếu muốn hủy bỏ thao tác ngay lập tức.\n"
        "   - Chương trình gọi hàm tiện ích timPhimTheoMa(headPhim, ma) để duyệt tìm trong danh sách liên kết (không phân biệt chữ hoa hay thường). "
        "Nếu trả về nullptr (không tồn tại mã này trong hệ thống), chương trình sẽ xuất cảnh báo '[!] Khong tim thay phim co ma...' và dừng xử lý.\n\n"
        "2. Bước 2: Hiển thị thông tin phim hiện tại:\n"
        "   - Khi tìm thấy node phim tương ứng, chương trình lập tức in toàn bộ thông tin hiện hữu của bộ phim lên màn hình "
        "(Tên phim, Thể loại, Thời lượng phút, Đơn giá vé VND) để nhân viên đối chiếu và xác nhận đúng phim cần sửa.\n\n"
        "3. Bước 3: Hỏi và cập nhật độc lập từng thuộc tính:\n"
        "   - Chương trình sử dụng biến cờ hiệu bool coThayDoi = false để ghi nhận biến động dữ liệu.\n"
        "   - Lần lượt hỏi người dùng có muốn thay đổi từng trường hay không (chọn y/n):\n"
        "     + Đổi tên phim mới? Nếu chọn 'y', yêu cầu nhập chuỗi qua hàm nhapChuoi() và gán lại cho p->data.ten.\n"
        "     + Đổi thể loại mới? Nếu chọn 'y', yêu cầu nhập chuỗi qua hàm nhapChuoi() và gán lại cho p->data.theLoai.\n"
        "     + Đổi thời lượng mới? Nếu chọn 'y', dùng nhapSoNguyen(15, 360) để kiểm tra hợp lệ và gán lại cho p->data.thoiLuong.\n"
        "     + Đổi giá vé mới? Nếu chọn 'y', dùng nhapSoThuc(10000, 1000000) để kiểm tra đơn giá vé và gán lại cho p->data.giaVe.\n"
        "     + Mỗi khi có trường được người dùng đồng ý đổi, cờ hiệu được bật coThayDoi = true.\n\n"
        "4. Bước 4: Đồng bộ dữ liệu xuống đĩa:\n"
        "   - Sau khi duyệt qua cả 4 trường, chương trình kiểm tra cờ coThayDoi. Nếu coThayDoi == true, hàm lập tức gọi "
        "ghiToanBoFile(FILE_DB, headPhim) để ghi đè toàn bộ dữ liệu mới nhất vào file cinema_db.txt, xuất thông báo cập nhật thành công. "
        "Nếu người dùng đều chọn 'n' (không đổi gì), chương trình thông báo 'Khong co thong tin nao bi thay doi' và giữ nguyên file."
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) của chức năng 5:")
    add_code_block(
        "graph LR\n"
        "    A([Bắt đầu]) --> B[Nhập mã phim cần sửa]\n"
        "    B --> C{ma == '0'?}\n"
        "    C -- Đúng --> D[Hủy thao tác] --> K([Kết thúc])\n"
        "    C -- Sai --> E{timPhimTheoMa?}\n"
        "    E -- Không thấy --> F[Báo lỗi: Phim không tồn tại] --> K\n"
        "    E -- Tìm thấy --> G[In thông tin hiện tại của phim]\n"
        "    G --> H[Hỏi sửa từng trường y/n: Tên, Thể loại, Thời lượng, Giá vé]\n"
        "    H --> I{coThayDoi == true?}\n"
        "    I -- Đúng --> J[Ghi đè file cinema_db.txt] --> K\n"
        "    I -- Sai --> K"
    )
    doc.add_paragraph("Đoạn mã nguồn của chức năng 5:")
    add_code_block(
        "void capNhatThongTinPhim(NodePhim* headPhim) {\n"
        "    cout << \"\\n--- CAP NHAT THONG TIN PHIM ---\\n\";\n"
        "    cout << \"Huong dan: Nhap '0' neu muon huy thao tac.\\n\";\n\n"
        "    string ma = nhapChuoi(\"Nhap ma phim can cap nhat (VD: P01): \");\n"
        "    if (ma == \"0\") {\n"
        "        cout << \"=> Da huy thao tac cap nhat.\\n\";\n"
        "        return;\n"
        "    }\n\n"
        "    NodePhim* p = timPhimTheoMa(headPhim, ma);\n"
        "    if (p == nullptr) {\n"
        "        cout << \"=> [!] Khong tim thay phim co ma: \" << ma << \"\\n\";\n"
        "        return;\n"
        "    }\n\n"
        "    cout << \"\\n[Thong tin phim hien tai]\\n\";\n"
        "    cout << \"- Ten phim     : \" << p->data.ten << \"\\n\";\n"
        "    cout << \"- The loai     : \" << p->data.theLoai << \"\\n\";\n"
        "    cout << \"- Thoi luong   : \" << p->data.thoiLuong << \" phut\\n\";\n"
        "    cout << \"- Gia ve       : \" << (long long)p->data.giaVe << \" VND\\n\";\n"
        "    cout << \"----------------------------------------\\n\";\n"
        "    cout << \"Ban co muon thay doi cac thong tin sau khong? (Nhap y/n)\\n\";\n\n"
        "    bool coThayDoi = false;\n"
        "    string traLoi;\n\n"
        "    traLoi = nhapChuoi(\"-> Doi ten phim moi? (y/n): \");\n"
        "    if (traLoi == \"y\" || traLoi == \"Y\") {\n"
        "        p->data.ten = nhapChuoi(\"   Nhap ten phim moi: \");\n"
        "        coThayDoi = true;\n"
        "    }\n\n"
        "    traLoi = nhapChuoi(\"-> Doi the loai moi? (y/n): \");\n"
        "    if (traLoi == \"y\" || traLoi == \"Y\") {\n"
        "        p->data.theLoai = nhapChuoi(\"   Nhap the loai moi: \");\n"
        "        coThayDoi = true;\n"
        "    }\n\n"
        "    traLoi = nhapChuoi(\"-> Doi thoi luong moi? (y/n): \");\n"
        "    if (traLoi == \"y\" || traLoi == \"Y\") {\n"
        "        p->data.thoiLuong = nhapSoNguyen(\"   Nhap thoi luong moi (15 - 360 phut): \", 15, 360);\n"
        "        coThayDoi = true;\n"
        "    }\n\n"
        "    traLoi = nhapChuoi(\"-> Doi gia ve moi? (y/n): \");\n"
        "    if (traLoi == \"y\" || traLoi == \"Y\") {\n"
        "        p->data.giaVe = nhapSoThuc(\"   Nhap gia ve moi (10,000 - 1,000,000 VND): \", 10000, 1000000);\n"
        "        coThayDoi = true;\n"
        "    }\n\n"
        "    if (coThayDoi) {\n"
        "        ghiToanBoFile(FILE_DB, headPhim);\n"
        "        cout << \"=> [Thanh cong] Cap nhat thong tin va DONG BO file thanh cong!\\n\";\n"
        "    } else {\n"
        "        cout << \"=> Khong co thong tin nao bi thay doi.\\n\";\n"
        "    }\n"
        "}"
    )

    # 4.6. CHỨC NĂNG 6
    add_h3("4.6. Chức năng 6: Sắp xếp danh sách phim (hienThiMenuSapXep, sapXepDanhSachPhim)")
    doc.add_paragraph(
        "Chức năng Sắp xếp cho phép người dùng tổ chức lại danh mục phim theo các tiêu chí quan trọng (Giá vé hoặc Thời lượng chiếu) "
        "theo thứ tự tăng dần hoặc giảm dần. Thuật toán được nhóm lựa chọn là Bubble Sort (Sắp xếp nổi bọt) cải tiến trực tiếp "
        "trên Danh sách liên kết đơn bằng cách hoán đổi vùng dữ liệu struct Phim giữa hai node kề nhau và sử dụng con trỏ biên lptr để tối ưu. "
        "Quy trình xử lý diễn ra như sau:\n\n"
        "1. Bước 1: Kiểm tra rỗng và điều hướng menu tiêu chí:\n"
        "   - Hàm hienThiMenuSapXep(headPhim) trước tiên kiểm tra xem headPhim == nullptr hay không. Nếu danh sách chưa có phim, thông báo lỗi và quay về.\n"
        "   - Nếu có phim, xuất menu con 4 tiêu chí sắp xếp: 1. Giá vé tăng dần, 2. Giá vé giảm dần, 3. Thời lượng tăng dần, 4. Thời lượng giảm dần, 0. Quay lại.\n"
        "   - Dựa vào lựa chọn, hàm sẽ truyền hai cờ hiệu giamDan (bool) và laGiaVe (bool) vào hàm xử lý thuật toán sapXepDanhSachPhim.\n\n"
        "2. Bước 2: Thuật toán Bubble Sort trên Danh sách liên kết đơn:\n"
        "   - Sử dụng vòng lặp do-while với cờ hiệu bool swapped. Đầu mỗi vòng lặp, gán swapped = false và con trỏ ptr1 = head.\n"
        "   - Duyệt ptr1 chạy từ đầu danh sách đến khi chạm con trỏ biên lptr (ban đầu lptr = nullptr):\n"
        "     + Lấy con trỏ kế tiếp ptr2 = ptr1->next.\n"
        "     + Trích xuất hai giá trị val1 và val2 tương ứng (nếu laGiaVe == true thì lấy giaVe, ngược lại lấy thoiLuong).\n"
        "     + Kiểm tra điều kiện nghịch thế: nếu giamDan == true thì điều kiện đổi là val1 < val2; nếu tăng dần thì val1 > val2.\n"
        "     + Nếu thỏa điều kiện nghịch thế, hoán đổi dữ liệu struct: Phim temp = ptr1->data; ptr1->data = ptr2->data; ptr2->data = temp; và bật swapped = true.\n"
        "     + Dời con trỏ ptr1 = ptr1->next.\n"
        "   - Kỹ thuật tối ưu hóa: Sau khi duyệt hết một lượt, gán lptr = ptr1. Điều này đảm bảo các vòng lặp sau không cần duyệt lại các node ở cuối danh sách đã nằm đúng vị trí.\n\n"
        "3. Bước 3: Đồng bộ thứ tự mới xuống đĩa và hiển thị kết quả:\n"
        "   - Khi vòng lặp kết thúc (swapped == false), danh sách đã hoàn toàn có thứ tự.\n"
        "   - Hàm lập tức gọi ghiToanBoFile(FILE_DB, headPhim) để ghi đè thứ tự phim mới xuống file cinema_db.txt.\n"
        "   - Cuối cùng, tự động gọi hàm xemDanhSachPhim(headPhim) xuất ngay bảng 104 cột ra màn hình để người dùng kiểm tra kết quả sắp xếp."
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) của chức năng 6:")
    add_code_block(
        "graph LR\n"
        "    A([Bắt đầu]) --> B{head == nullptr?}\n"
        "    B -- Đúng --> C[Báo danh sách trống] --> I([Kết thúc])\n"
        "    B -- Sai --> D[Chọn tiêu chí 1-4: Giá vé / Thời lượng]\n"
        "    D --> E[Vòng lặp Bubble Sort: So sánh cặp node ptr1 & ptr2]\n"
        "    E --> F{Nghịch thế?}\n"
        "    F -- Đúng --> G[Hoán đổi data: ptr1 <-> ptr2]\n"
        "    F -- Sai --> H[Duyệt tiếp con trỏ ptr1]\n"
        "    G --> H\n"
        "    H --> E\n"
        "    E -- Hoàn thành sắp xếp --> J[Ghi đè thứ tự mới vào cinema_db.txt]\n"
        "    J --> K[Gọi xemDanhSachPhim: In bảng 104 cột] --> I"
    )
    doc.add_paragraph("Đoạn mã nguồn của chức năng 6:")
    add_code_block(
        "void sapXepDanhSachPhim(NodePhim*& head, bool giamDan, bool laGiaVe) {\n"
        "    if (head == nullptr || head->next == nullptr) return;\n\n"
        "    bool swapped;\n"
        "    NodePhim* ptr1;\n"
        "    NodePhim* lptr = nullptr;\n\n"
        "    do {\n"
        "        swapped = false;\n"
        "        ptr1 = head;\n\n"
        "        while (ptr1->next != lptr) {\n"
        "            NodePhim* ptr2 = ptr1->next;\n\n"
        "            double val1 = laGiaVe ? ptr1->data.giaVe : ptr1->data.thoiLuong;\n"
        "            double val2 = laGiaVe ? ptr2->data.giaVe : ptr2->data.thoiLuong;\n\n"
        "            bool dieuKienDoi = giamDan ? (val1 < val2) : (val1 > val2);\n\n"
        "            if (dieuKienDoi) {\n"
        "                Phim temp = ptr1->data;\n"
        "                ptr1->data = ptr2->data;\n"
        "                ptr2->data = temp;\n"
        "                swapped = true;\n"
        "            }\n"
        "            ptr1 = ptr1->next;\n"
        "        }\n"
        "        lptr = ptr1;\n"
        "    } while (swapped);\n"
        "}\n\n"
        "void hienThiMenuSapXep(NodePhim* headPhim) {\n"
        "    if (headPhim == nullptr) {\n"
        "        cout << \"[!] Danh sach phim hien dang trong, chua co du lieu de sap xep!\\n\";\n"
        "        return;\n"
        "    }\n\n"
        "    cout << \"\\n--- CHON TIEU CHI SAP XEP ---\\n\";\n"
        "    cout << \"1. Gia ve tang dan\\n\";\n"
        "    cout << \"2. Gia ve giam dan\\n\";\n"
        "    cout << \"3. Thoi luong tang dan\\n\";\n"
        "    cout << \"4. Thoi luong giam dan\\n\";\n"
        "    cout << \"0. Quay lai\\n\";\n\n"
        "    string luaChon = nhapChuoi(\"Nhap lua chon cua ban: \");\n"
        "    bool daXuLy = true;\n"
        "    if (luaChon == \"0\") return;\n"
        "    else if (luaChon == \"1\") sapXepDanhSachPhim(headPhim, false, true);\n"
        "    else if (luaChon == \"2\") sapXepDanhSachPhim(headPhim, true, true);\n"
        "    else if (luaChon == \"3\") sapXepDanhSachPhim(headPhim, false, false);\n"
        "    else if (luaChon == \"4\") sapXepDanhSachPhim(headPhim, true, false);\n"
        "    else {\n"
        "        cout << \"=> [!] Tuy chon khong hop le!\\n\";\n"
        "        daXuLy = false;\n"
        "    }\n\n"
        "    if (daXuLy) {\n"
        "        ghiToanBoFile(FILE_DB, headPhim);\n"
        "        cout << \"=> Da sap xep va DONG BO file thanh cong!\\n\";\n"
        "        xemDanhSachPhim(headPhim);\n"
        "    }\n"
        "}"
    )

    # 4.7. CHỨC NĂNG 7
    add_h3("4.7. Chức năng 7: Xem sơ đồ ghế phòng chiếu (xemSoDoGhe)")
    doc.add_paragraph(
        "Chức năng này giúp nhân viên hoặc khách hàng xem được sơ đồ ghế thực tế của một phòng chiếu phim, "
        "biết được phòng chiếu đó có bao nhiêu ghế, vị trí các hàng ghế từ A đến E, ghế nào còn trống có thể đặt và ghế nào đã có người mua. "
        "Các bước xử lý diễn ra như sau:\n\n"
        "1. Nhập mã phim và tra cứu:\n"
        "   - Khi người dùng bấm chọn mục 7, chương trình yêu cầu nhập vào mã phim muốn xem (ví dụ: P01, P07...).\n"
        "   - Chương trình gọi hàm timPhimTheoMa(headPhim, maPhim) để tìm kiếm. Hàm này sẽ duyệt danh sách liên kết và so sánh mã "
        "dưới dạng chữ thường. Nhờ vậy, người dùng có gõ chữ thường 'p01' hay chữ hoa 'P01' thì chương trình đều tìm đúng phim.\n"
        "   - Nếu hàm trả về nullptr (nghĩa là mã phim không tồn tại trong hệ thống), chương trình sẽ thông báo '[!] Khong tim thay phim co ma: ...' và kết thúc thao tác.\n"
        "   - Nếu tìm thấy phim, chương trình lấy được con trỏ p trỏ tới bộ phim đó và truyền vào hàm xemSoDoGhe(p).\n\n"
        "2. Vẽ sơ đồ phòng chiếu ra màn hình (hàm xemSoDoGhe):\n"
        "   - Đầu tiên, in ra khung viền với tiêu đề tên phim, mã phim và dòng chữ '[ MAN HINH CHIEU (SCREEN) ]' ở phía trên "
        "để người nhìn biết được hướng nhìn của phòng chiếu.\n"
        "   - Tiếp theo là dòng tiêu đề hiển thị tên 6 cột từ 'Cot 1' đến 'Cot 6'.\n"
        "   - Sau đó, chương trình dùng 2 vòng lặp for lồng nhau để duyệt qua mảng 2 chiều ghe[SO_HANG][SO_COT] (5 hàng x 6 cột). "
        "Ở đầu mỗi hàng, in ra tên hàng ghế tương ứng: hàng thứ 0 là 'Hang A', hàng 1 là 'Hang B', cứ như vậy đến 'Hang E'.\n"
        "   - Tại mỗi vị trí ghế, chương trình tính ra số thứ tự của ghế bằng công thức: soGhe = r * 6 + c + 1 (từ 1 đến 30):\n"
        "     + Nếu ghế đó đã có người đặt rồi (ghe[r][c].daDat == true), chương trình sẽ in ra ký hiệu ' [ X]  '.\n"
        "     + Nếu ghế đó vẫn còn trống (ghe[r][c].daDat == false), chương trình sẽ in ra số thứ tự ghế dưới dạng 2 chữ số ' [%02d]  ' "
        "(ví dụ ghế 1 sẽ in là [01], ghế 9 in là [09], ghế 10 in là [10]). Việc in đủ 2 chữ số giúp các ô ghế có cùng độ rộng 4 ký tự, "
        "làm cho các hàng và các cột trong ma trận ghế luôn thẳng tắp, không bị lệch hàng.\n"
        "   - Cuối cùng, in ra dòng chú thích quy ước ký hiệu '[So]: Ghe con trong' và '[ X]: Ghe da dat', cùng với thông tin đơn giá vé của bộ phim đó."
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) của chức năng 7:")
    add_code_block(
        "graph TD\n"
        "    A([Bắt đầu: xemSoDoGhe]) --> B[Nhập mã phim cần xem sơ đồ]\n"
        "    B --> C[Gọi timPhimTheoMa headPhim, maPhim]\n"
        "    C --> D{p == nullptr?}\n"
        "    D -- Đúng: Không tìm thấy --> E[Thông báo: Không tìm thấy phim!]\n"
        "    E --> F([Kết thúc])\n"
        "    D -- Sai: Tìm thấy phim --> G[In tiêu đề phim & Màn hình SCREEN]\n"
        "    G --> H[In tiêu đề 6 cột: Cot 1 -> Cot 6]\n"
        "    H --> I[Vòng lặp hàng: r từ 0 đến 4 Hang A -> Hang E]\n"
        "    I --> J[Vòng lặp cột: c từ 0 đến 5]\n"
        "    J --> K[Tính số ghế: soGhe = r * 6 + c + 1]\n"
        "    K --> L{ghe[r][c].daDat == true?}\n"
        "    L -- Đúng: Đã đặt --> M[In ký hiệu: [ X] ]\n"
        "    L -- Sai: Còn trống --> N[In số 2 chữ số: [%02d] ]\n"
        "    M --> O{Hết 6 cột?}\n"
        "    N --> O\n"
        "    O -- Chưa hết cột --> J\n"
        "    O -- Hết 6 cột --> P{Hết 5 hàng?}\n"
        "    P -- Chưa hết hàng --> I\n"
        "    P -- Hết 5 hàng --> Q[In chú thích ký hiệu & Đơn giá vé]\n"
        "    Q --> R([Kết thúc: Hoàn tất vẽ sơ đồ])"
    )
    doc.add_paragraph("Đoạn mã nguồn của chức năng 7:")
    add_code_block(
        "void xemSoDoGhe(NodePhim* p) {\n"
        "    if (p == nullptr) return;\n"
        "    cout << \"\\n==================================================================\\n\";\n"
        "    cout << \"  SO DO PHONG CHIEU: \" << p->data.ten << \" (\" << p->data.ma << \")\\n\";\n"
        "    cout << \"==================================================================\\n\";\n"
        "    cout << \"                    [ MAN HINH CHIEU (SCREEN) ]                   \\n\";\n"
        "    cout << \"------------------------------------------------------------------\\n\";\n"
        "    cout << \"        Cot 1   Cot 2   Cot 3   Cot 4   Cot 5   Cot 6\\n\";\n"
        "    char tenHang = 'A';\n"
        "    for (int r = 0; r < SO_HANG; r++) {\n"
        "        cout << \"Hang \" << (char)(tenHang + r) << \"  \";\n"
        "        for (int c = 0; c < SO_COT; c++) {\n"
        "            int soGhe = r * SO_COT + c + 1;\n"
        "            if (p->data.ghe[r][c].daDat) cout << \" [ X]  \";\n"
        "            else printf(\" [%02d]  \", soGhe);\n"
        "        }\n"
        "        cout << \"\\n\\n\";\n"
        "    }\n"
        "    cout << \"Chu thich: [So]: Ghe con trong (co the dat)  |  [ X]: Ghe da dat\\n\";\n"
        "    cout << \"Gia ve   : \" << (long long)p->data.giaVe << \" VND / ghe\\n\";\n"
        "    cout << \"------------------------------------------------------------------\\n\";\n"
        "}"
    )

    # 4.8. CHỨC NĂNG 8
    add_h3("4.8. Chức năng 8: Nghiệp vụ Đặt vé và Hủy vé xem phim (hienMenuDatVeHuyVe, datVe, huyVe)")
    doc.add_paragraph(
        "Chức năng 8 được gom vào hàm hienMenuDatVeHuyVe() gồm một menu nhỏ với các lựa chọn: 1. Đặt vé, 2. Hủy vé, 3. Xem sơ đồ ghế, 0. Quay lại. "
        "Đây là nghiệp vụ cốt lõi của phần mềm rạp chiếu phim, kết nối trực tiếp giữa khách hàng, vị trí ghế và cơ sở dữ liệu. "
        "Chi tiết luồng chạy của từng nghiệp vụ như sau:\n\n"
        "A. QUY TRÌNH ĐẶT VÉ XEM PHIM (hàm datVe):\n"
        "1. Bước 1: Chọn phim muốn đặt vé:\n"
        "   - Người dùng nhập mã phim (ví dụ: P01). Chương trình gọi timPhimTheoMa() để tìm. Nếu không có phim thì báo lỗi và dừng thao tác.\n"
        "   - Nếu có phim, chương trình sẽ tự động gọi xemSoDoGhe(p) để vẽ sơ đồ 30 ghế ra màn hình, giúp người dùng nhìn thấy ngay ghế nào còn trống để chọn.\n\n"
        "2. Bước 2: Chọn ghế và kiểm tra trùng lặp (vòng lặp while true):\n"
        "   - Người dùng nhập số ghế muốn đặt từ 1 đến 30 qua hàm nhapSoNguyen(1, 30). Nếu nhập số âm hoặc số lớn hơn 30 sẽ bị bắt nhập lại.\n"
        "   - Chương trình quy đổi số ghế ra vị trí hàng và cột: r = (soGhe - 1) / 6 và c = (soGhe - 1) % 6.\n"
        "   - Kiểm tra ô ghế: Nếu p->data.ghe[r][c].daDat == true (nghĩa là ghế này đã có người đặt trước đó rồi), chương trình sẽ cảnh báo: "
        "'[!] Ghe so ... DA CO NGUOI DAT! Vui long chon ghe khac.' và bắt người dùng phải nhập lại số ghế khác. Vòng lặp chỉ kết thúc khi chọn được một ghế còn trống.\n\n"
        "3. Bước 3: Nhập thông tin khách hàng:\n"
        "   - Người dùng nhập Họ và tên khách hàng và Số điện thoại liên hệ qua hàm nhapChuoi() để đảm bảo thông tin không bị để trống.\n\n"
        "4. Bước 4: Cấp mã vé và cập nhật trạng thái ô ghế:\n"
        "   - Chương trình lấy mã số vé tự tăng từ biến veKeTiep (ví dụ bắt đầu từ số 1001, sau mỗi lần đặt thì veKeTiep tăng lên 1 đơn vị, đảm bảo không bao giờ trùng mã vé).\n"
        "   - Đánh dấu ô ghế đã được mua: p->data.ghe[r][c].daDat = true.\n"
        "   - Lưu thông tin vé vào ô ghế đó: p->data.ghe[r][c].ve = { maVeMoi, tenKhach, sdt }.\n\n"
        "5. Bước 5: Lưu vào file và in biên lai:\n"
        "   - Chương trình lập tức gọi ghiToanBoFile(FILE_DB, headPhim) để ghi đè trạng thái ghế mới xuống file cinema_db.txt.\n"
        "   - In ra màn hình hóa đơn đặt vé thành công gồm: Mã số vé (#1001), Tên phim, Vị trí ghế (Hàng A-E, Cột 1-6), Tên khách, SĐT và Giá tiền.\n\n"
        "B. QUY TRÌNH HỦY VÉ XEM PHIM (hàm huyVe):\n"
        "1. Bước 1: Người dùng nhập mã số vé muốn hủy (ví dụ: 1001). Nếu người dùng đổi ý không muốn hủy nữa thì có thể nhập số 0 để thoát ra ngoài.\n\n"
        "2. Bước 2: Tìm kiếm vé trong hệ thống:\n"
        "   - Chương trình dùng 2 vòng lặp: duyệt qua từng bộ phim trong danh sách liên kết, và với mỗi phim thì duyệt qua toàn bộ 30 ghế ngồi.\n"
        "   - Điều kiện kiểm tra là: nếu ghế đó đang có người đặt (daDat == true) và mã số vé trùng khớp với mã cần hủy (ve.soVe == maVeCanHuy).\n\n"
        "3. Bước 3: Xử lý kết quả tìm kiếm:\n"
        "   - Trường hợp không tìm thấy: Nếu duyệt hết tất cả các phim mà không có vé nào khớp, chương trình xuất thông báo '[!] Khong tim thay ve co ma #... trong he thong!'.\n"
        "   - Trường hợp tìm thấy vé: Chương trình sẽ in chi tiết thông tin vé tìm được ra màn hình (Mã vé, Tên phim, Vị trí hàng ghế, Tên khách hàng, Số điện thoại) "
        "và hỏi xác nhận: 'Ban co CHAC CHAN muon huy ve nay? (y/n)'.\n"
        "     + Nếu người dùng gõ 'n' hoặc 'N', chương trình báo hủy thao tác và giữ nguyên vé như cũ, không thay đổi gì cả.\n"
        "     + Nếu người dùng gõ 'y' hoặc 'Y', chương trình sẽ trả ô ghế đó về trạng thái trống (daDat = false và ve = {0, '', ''}), "
        "sau đó gọi hàm ghiToanBoFile(FILE_DB, headPhim) để cập nhật lại file database và in thông báo đã hủy vé thành công, trả lại ghế trống cho phòng chiếu."
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) Quy trình Đặt vé (datVe):")
    add_code_block(
        "graph TD\n"
        "    A([Bắt đầu: datVe]) --> B[Nhập mã phim muốn đặt vé]\n"
        "    B --> C[Gọi timPhimTheoMa headPhim, maPhim]\n"
        "    C --> D{p == nullptr?}\n"
        "    D -- Không thấy --> E[Thông báo: Không tìm thấy phim!]\n"
        "    E --> F([Kết thúc])\n"
        "    D -- Tìm thấy --> G[Gọi xemSoDoGhe: Vẽ sơ đồ 30 ghế]\n"
        "    G --> H[Nhập số ghế muốn đặt 1 - 30]\n"
        "    H --> I[Quy đổi: r = soGhe-1 / 6, c = soGhe-1 % 6]\n"
        "    I --> J{ghe[r][c].daDat == true?}\n"
        "    J -- Đã có người mua --> K[Cảnh báo: Ghế đã có người đặt! Bắt chọn lại]\n"
        "    K --> H\n"
        "    J -- Còn trống --> L[Nhập Họ tên khách hàng & Số điện thoại]\n"
        "    L --> M[Cấp mã vé tự tăng: maVeMoi = veKeTiep++]\n"
        "    M --> N[Đánh dấu: daDat = true & Lưu thông tin vé]\n"
        "    N --> O[Gọi ghiToanBoFile lưu ngay cinema_db.txt]\n"
        "    O --> P[In biên lai vé thành công]\n"
        "    P --> Q([Kết thúc])"
    )
    doc.add_paragraph("Sơ đồ luồng hoạt động (Flowchart) Quy trình Hủy vé (huyVe):")
    add_code_block(
        "graph TD\n"
        "    A([Bắt đầu: huyVe]) --> B[Nhập mã số vé cần hủy]\n"
        "    B --> C{maVeCanHuy == 0?}\n"
        "    C -- Đúng --> D[Thoát thao tác]\n"
        "    D --> E([Kết thúc])\n"
        "    C -- Sai --> F[Duyệt danh sách phim: p = headPhim]\n"
        "    F --> G[Duyệt 30 ghế của phim p: hàng r 0..4, cột c 0..5]\n"
        "    G --> H{daDat == true && ve.soVe == maVeCanHuy?}\n"
        "    H -- Khớp vé --> I[In chi tiết thông tin vé]\n"
        "    I --> J{Xác nhận chắc chắn hủy? y/n}\n"
        "    J -- Chọn n --> K[Thông báo hủy thao tác, giữ nguyên vé]\n"
        "    K --> E\n"
        "    J -- Chọn y --> L[Trả ghế trống: daDat = false & ve rỗng]\n"
        "    L --> M[Gọi ghiToanBoFile cập nhật cinema_db.txt]\n"
        "    M --> N[Thông báo: Đã hủy vé thành công!]\n"
        "    N --> E\n"
        "    H -- Chưa khớp --> O{Hết 30 ghế & Hết phim?}\n"
        "    O -- Chưa hết --> G\n"
        "    O -- Đã duyệt hết --> P[Thông báo: Không tìm thấy vé trong hệ thống!]\n"
        "    P --> E"
    )
    doc.add_paragraph("Đoạn mã nguồn của chức năng 8:")
    add_code_block(
        "void datVe(NodePhim* headPhim, int& veKeTiep) {\n"
        "    string maPhim = nhapChuoi(\"Nhap ma phim ban muon dat ve (VD: P01): \");\n"
        "    NodePhim* p = timPhimTheoMa(headPhim, maPhim);\n"
        "    if (p == nullptr) { cout << \"  [!] Khong tim thay phim!\\n\"; return; }\n"
        "    xemSoDoGhe(p);\n"
        "    int soGhe, r, c;\n"
        "    while (true) {\n"
        "        soGhe = nhapSoNguyen(\"Nhap so ghe ban muon dat (1 - 30): \", 1, TONG_GHE);\n"
        "        r = (soGhe - 1) / SO_COT;\n"
        "        c = (soGhe - 1) % SO_COT;\n"
        "        if (p->data.ghe[r][c].daDat) cout << \"  [!] Ghe so \" << soGhe << \" DA CO NGUOI DAT! Vui long chon ghe khac.\\n\";\n"
        "        else break;\n"
        "    }\n"
        "    string tenKhach = nhapChuoi(\"  + Ho ten khach hang: \");\n"
        "    string sdt      = nhapChuoi(\"  + So dien thoai: \");\n"
        "    int maVeMoi = veKeTiep++;\n"
        "    p->data.ghe[r][c].daDat = true;\n"
        "    p->data.ghe[r][c].ve    = { maVeMoi, tenKhach, sdt };\n"
        "    ghiToanBoFile(FILE_DB, headPhim);\n"
        "    cout << \"=> [Thanh cong] Da dat ve #\" << maVeMoi << \" cho khach \" << tenKhach << \"!\\n\";\n"
        "}\n\n"
        "void huyVe(NodePhim* headPhim) {\n"
        "    int maVeCanHuy = nhapSoNguyen(\"Nhap ma so ve can huy (0 de thoat): \", 0, 9999999);\n"
        "    if (maVeCanHuy == 0) return;\n"
        "    NodePhim* p = headPhim;\n"
        "    while (p != nullptr) {\n"
        "        for (int r = 0; r < SO_HANG; r++)\n"
        "            for (int c = 0; c < SO_COT; c++)\n"
        "                if (p->data.ghe[r][c].daDat && p->data.ghe[r][c].ve.soVe == maVeCanHuy) {\n"
        "                    string xn = nhapChuoi(\"Ban co CHAC CHAN muon huy ve nay? (y/n): \");\n"
        "                    if (xn == \"y\" || xn == \"Y\") {\n"
        "                        p->data.ghe[r][c].daDat = false;\n"
        "                        p->data.ghe[r][c].ve = { 0, \"\", \"\" };\n"
        "                        ghiToanBoFile(FILE_DB, headPhim);\n"
        "                        cout << \"=> [Thanh cong] Da huy ve #\" << maVeCanHuy << \"!\\n\";\n"
        "                    }\n"
        "                    return;\n"
        "                }\n"
        "        p = p->next;\n"
        "    }\n"
        "    cout << \"  [!] Khong tim thay ve co ma #\" << maVeCanHuy << \"!\\n\";\n"
        "}"
    )

    # 4.9. CÁC HÀM TIỆN ÍCH DÙNG CHUNG VÀ CƠ CHẾ LƯU TRỮ FILE
    add_h3("4.9. Các hàm tiện ích dùng chung và cơ chế lưu trữ file (timPhimTheoMa, ghiToanBoFile)")
    doc.add_paragraph(
        "- Hàm timPhimTheoMa: Đây là một hàm tiện ích rất quan trọng được dùng chung cho nhiều chức năng trong chương trình "
        "(dùng trong Chức năng 1 để kiểm tra trùng mã, Chức năng 5 để cập nhật thông tin, Chức năng 7 để xem sơ đồ ghế và Chức năng 8 để đặt vé). "
        "Hàm này duyệt qua danh sách liên kết và so sánh mã phim dưới dạng chữ thường (lowercase). Nhờ vậy, người dùng có nhập chữ hoa hay chữ thường thì hệ thống vẫn tìm thấy chính xác bộ phim."
    )
    add_code_block(
        "NodePhim* timPhimTheoMa(NodePhim* head, string ma) {\n"
        "    if (ma.empty()) return nullptr;\n"
        "    string maTim = chuyenChuThuong(ma);\n"
        "    NodePhim* p = head;\n"
        "    while (p != nullptr) {\n"
        "        if (chuyenChuThuong(p->data.ma) == maTim) return p;\n"
        "        p = p->next;\n"
        "    }\n"
        "    return nullptr;\n"
        "}"
    )
    doc.add_paragraph(
        "- Hàm ghiToanBoFile: Đảm bảo tính lưu trữ bền vững cho phần mềm. Mỗi khi dữ liệu trên RAM bị thay đổi, "
        "hàm này sẽ mở file cinema_db.txt ở chế độ ghi đè toàn bộ (ofstream). Sau đó, duyệt qua từng bộ phim để ghi dòng header (bắt đầu bằng dấu #) "
        "và ghi lần lượt 30 dòng trạng thái ghế của phim đó xuống file."
    )
    add_code_block(
        "void ghiToanBoFile(const string& file, NodePhim* head) {\n"
        "    ofstream f(file);\n"
        "    NodePhim* p = head;\n"
        "    while (p) {\n"
        "        f << \"#\" << p->data.ma << \"|\" << p->data.ten  << \"|\"\n"
        "                 << p->data.theLoai  << \"|\" << p->data.thoiLuong << \"|\"\n"
        "                 << p->data.giaVe << \"\\n\";\n"
        "        for (int r = 0; r < SO_HANG; r++)\n"
        "            for (int c = 0; c < SO_COT; c++) {\n"
        "                int so = r * SO_COT + c + 1;\n"
        "                f << taoGheDong(so, p->data.ghe[r][c]) << \"\\n\";\n"
        "            }\n"
        "        p = p->next;\n"
        "    }\n"
        "    f.close();\n"
        "}"
    )

    # -------------------------------------------------------------
    # MỤC 5: HÌNH ẢNH MINH HỌA
    # -------------------------------------------------------------
    add_h2("5. Hình ảnh minh họa (Chạy chương trình thực tế)")
    add_note_box("Thành viên 3 chạy chương trình ./main_app (hoặc main_refactored.exe), dùng phím Windows + Shift + S chụp lại màn hình console thực tế và dán trực tiếp vào các khung dưới đây:")

    add_h3("5.1. Màn hình khởi động hệ thống & Menu chính (Nạp 10 phim)")
    add_image_placeholder("Khởi động hệ thống & Menu chính", "Chụp thông báo nạp thành công 10 phim từ database và menu chính 8 chức năng")

    add_h3("5.2. Chức năng 2: Xem danh sách phim dạng bảng (Căn lề 104 cột)")
    add_image_placeholder("Bảng danh sách phim căn lề 104 cột", "Chụp bảng danh sách 10 bộ phim với các cột căn lề thẳng tắp, không bị lệch hàng")

    add_h3("5.3. Chức năng 1: Thêm phim mới & Cảnh báo trùng mã phim")
    add_image_placeholder("Thêm phim mới & Bắt lỗi trùng mã", "Chụp lúc nhập mã P01 bị hệ thống báo trùng và bắt nhập lại")

    add_h3("5.4. Chức năng 3: Tìm kiếm phim theo tiêu chí")
    add_image_placeholder("Kết quả tìm kiếm phim", "Chụp kết quả tìm kiếm phim theo tên hoặc theo khoảng giá vé")

    add_h3("5.5. Chức năng 4: Xóa phim khỏi hệ thống")
    add_image_placeholder("Xóa phim thành công", "Chụp bước hỏi xác nhận y/n trước khi xóa và thông báo xóa thành công")

    add_h3("5.6. Chức năng 5: Cập nhật thông tin phim")
    add_image_placeholder("Cập nhật thông tin phim", "Chụp giao diện cho phép chọn sửa Tên, Thể loại, Thời lượng, Giá vé")

    add_h3("5.7. Chức năng 6: Sắp xếp danh sách phim")
    add_image_placeholder("Bảng phim sau khi sắp xếp", "Chụp bảng phim sau khi sắp xếp giá vé giảm dần hoặc thời lượng tăng dần")

    add_h3("5.8. Chức năng 7: Sơ đồ ghế phòng chiếu trực quan")
    add_image_placeholder("Sơ đồ phòng chiếu 30 ghế", "Chụp ma trận ghế 5 hàng x 6 cột với màn hình chiếu SCREEN, ghế trống [01]..[30] và ghế đã đặt [ X]")

    add_h3("5.9. Chức năng 8: Nghiệp vụ Đặt vé & Hủy vé xem phim")
    add_image_placeholder("Đặt vé & Hủy vé thành công", "Chụp thông báo đặt vé thành công có mã vé #1001 và quy trình hủy vé")

    # -------------------------------------------------------------
    # MỤC 6: NHẬN XÉT VÀ HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------
    add_h2("6. Nhận xét và hướng phát triển thêm")
    add_h3("6.1. Đánh giá ưu điểm của chương trình")
    doc.add_paragraph(
        "1. Vận dụng đúng cấu trúc dữ liệu: Nhóm đã sử dụng thành thạo Danh sách liên kết đơn trong việc quản lý danh sách phim động, "
        "thao tác con trỏ chính xác và có hàm giải phóng toàn bộ bộ nhớ RAM trước khi tắt chương trình để không bị lãng phí bộ nhớ.\n"
        "2. Kiểm soát nhập liệu chặt chẽ: Chương trình sử dụng bộ hàm nhập an toàn với stringstream, không bao giờ bị lỗi trôi lệnh cin "
        "và nếu người dùng lỡ nhập sai định dạng (nhập chữ vào ô số, bỏ trống chuỗi) thì chương trình đều nhắc nhở nhập lại chứ không bị tắt đột ngột.\n"
        "3. Hiển thị bảng console đẹp mắt: Bảng danh sách phim được căn lề rộng 104 cột, giải quyết triệt để lỗi tràn dòng khi tên phim quá dài.\n"
        "4. Bố cục mã nguồn gọn gàng, dễ hiểu: Code được chia thành các phần chức năng rõ ràng, có đầy đủ nguyên mẫu hàm và tái sử dụng hàm rất tốt.\n"
        "5. Dữ liệu được lưu trữ tự động: Mọi thay đổi về phim hay vé đều được tự động lưu ngay vào file cinema_db.txt."
    )

    add_h3("6.2. Những điểm còn hạn chế")
    doc.add_paragraph(
        "1. Giao diện: Chương trình vẫn chạy trên màn hình console dòng lệnh, chưa có giao diện đồ họa chuột (GUI) với hình ảnh poster phim.\n"
        "2. Cấu hình phòng chiếu: Số lượng ghế hiện đang cố định là 30 ghế (5 hàng x 6 cột) cho mỗi phim, chưa cho phép người dùng tự thiết lập số hàng và số cột theo từng phòng thực tế.\n"
        "3. Phân quyền: Chương trình chưa chia tài khoản đăng nhập giữa Quản trị viên (được thêm, sửa, xóa phim) và Khách hàng (chỉ được xem phim và đặt vé)."
    )

    add_h3("6.3. Hướng phát triển trong tương lai")
    doc.add_paragraph(
        "- Làm giao diện đồ họa GUI bằng thư viện Qt C++ để người dùng có thể dùng chuột chọn ghế trực quan hơn.\n"
        "- Áp dụng thêm cấu trúc dữ liệu Ngăn xếp (Stack) để làm tính năng Hoàn tác (Undo), giúp phục hồi lại phim nếu lỡ tay xóa nhầm.\n"
        "- Áp dụng Hàng đợi (Queue) để xếp hàng khách đặt vé online vào những giờ cao điểm.\n"
        "- Áp dụng Cây nhị phân tìm kiếm (Binary Search Tree) để tăng tốc độ tìm kiếm khi rạp có hàng nghìn bộ phim.\n"
        "- Bổ sung thêm tính năng thống kê tổng doanh thu bán vé theo ngày."
    )

    # Lưu an toàn vào file chính và file bản chuẩn
    primary_path = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Tieu_Luan_MovieBooking.docx"
    ban_chuan_path = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Tieu_Luan_MovieBooking_BanChuan.docx"
    alt_path = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Tieu_Luan_MovieBooking_ChiTietNghiepVu.docx"
    
    # 1. Lưu bản chuẩn mới
    try:
        doc.save(ban_chuan_path)
        print(f"[OK] Successfully saved: {ban_chuan_path}")
    except Exception as e:
        print(f"[NOTE] Ban chuan file is locked: {e}")

    # 2. Lưu file chính
    try:
        doc.save(primary_path)
        print(f"[OK] Successfully updated primary file: {primary_path}")
    except Exception as e:
        print(f"[NOTE] Primary file is locked: {e}")

    # 3. Thử lưu alt nếu không bị khóa
    try:
        doc.save(alt_path)
        print(f"[OK] Successfully updated alt file: {alt_path}")
    except Exception as e:
        print(f"[NOTE] Alt file is locked: {e}")

if __name__ == "__main__":
    build_natural_report()
