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

def build_full_report():
    doc = Document()

    # Căn lề chuẩn A4 học thuật Việt Nam: Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)

    # Style mặc định
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # TRANG BÌA (COVER PAGE)
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

    r_desc = p_title.add_run("(Kiến trúc phân lớp chuẩn mực - Phân tích chi tiết luồng nghiệp vụ & Giải thuật)\n")
    r_desc.font.italic = True
    r_desc.font.size = Pt(12)
    p_title.paragraph_format.space_after = Pt(36)

    # Hộp thông tin đề tài
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
    # HÀM ĐỊNH DẠNG VĂN BẢN
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

    def add_flow_box(flow_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "EBF2F7") # Light soft blue
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(flow_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x0C, 0x2D, 0x48)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_note_box(note_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "FFF9E6")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("📌 " + note_text)
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
        r = p.add_run(f"📷 [CHÈN HÌNH ẢNH MINH HỌA: {title}]\n")
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        if desc:
            r2 = p.add_run(f"({desc})\n")
            r2.font.italic = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        r3 = p.add_run("(Dùng Windows + Shift + S chụp cửa sổ console và dán trực tiếp vào khung này)")
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # MỤC IV: BẢNG PHÂN CHIA CÔNG VIỆC NHÓM
    # -------------------------------------------------------------
    add_h1("IV. BẢNG PHÂN CHIA CÔNG VIỆC NHÓM")
    add_note_box("Mục này được xây dựng chuẩn theo đề cương tiểu luận, phân định rõ ràng trách nhiệm kỹ thuật và trách nhiệm viết báo cáo của 3 thành viên.")

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
         "• Thiết kế kiến trúc phân lớp mã nguồn (8 tầng), Structs và Danh sách liên kết đơn.\n"
         "• Xây dựng bộ hàm Validation an toàn (nhapChuoi, nhapSoNguyen, nhapSoThuc).\n"
         "• Quản lý CSDL (cinema_db.txt), định dạng bảng Console 104 cột chuẩn mực.\n"
         "• Chức năng: Nhập danh sách phim, Thêm phim mới, Hiển thị danh sách.\n"
         "• Viết báo cáo: Phần 1 (Giới thiệu đề tài) & Phần 2 (Phân tích & Giải pháp).", "100%"),
        ("2", "[Tên Thành viên 2]", "[MSSV]",
         "• Chuẩn hóa hàm tìm kiếm mã phim không phân biệt hoa thường (timPhimTheoMa).\n"
         "• Thuật toán Tìm kiếm phim đa tiêu chí (mã phim, tên phim, khoảng giá vé).\n"
         "• Thuật toán Xóa phim an toàn: so khớp chính xác mã, xử lý ca biên, giải phóng RAM.\n"
         "• Viết báo cáo: Phần 3 (Thiết kế CTDL & Sơ đồ) & Phần 4 (Đoạn mã quan trọng).", "100%"),
        ("3", "[Tên Thành viên 3]", "[MSSV]",
         "• Chức năng Cập nhật thông tin phim (cho phép sửa từng trường dữ liệu riêng lẻ).\n"
         "• Thuật toán Sắp xếp danh sách (Bubble sort theo giá vé và thời lượng chiếu).\n"
         "• Nghiệp vụ phòng vé: Xem sơ đồ 30 ghế, Đặt vé (cấp mã #1001), Hủy vé.\n"
         "• Viết báo cáo: Phần 5 (Chạy chương trình & Chụp ảnh minh họa) & Phần 6 (Đánh giá).", "100%"),
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
        "Trong thời đại công nghệ số hóa, ngành công nghiệp điện ảnh và dịch vụ giải trí chiếu phim phát triển "
        "vượt bậc. Các cụm rạp chiếu phim hiện đại phải liên tục xử lý khối lượng lớn thông tin biến động theo từng khung giờ: "
        "danh mục các phim đang công chiếu, thời lượng từng suất, mức giá vé từng hạng và đặc biệt là tình trạng vị trí "
        "ghế ngồi của từng phòng chiếu. Việc ứng dụng giải pháp công nghệ thông tin giúp tự động hóa khâu quản trị, "
        "hạn chế tối đa tình trạng nhầm lẫn hay trùng lặp ghế, đồng thời tăng tốc độ phục vụ khách hàng."
    )
    doc.add_paragraph(
        "Xuất phát từ bài toán thực tế đó, nhóm đã lựa chọn 'Đề tài 9: Hệ thống quản lý đặt vé xem phim' nhằm vận dụng "
        "các kiến thức nền tảng của môn Cấu trúc dữ liệu và Giải thuật vào việc xây dựng một hệ thống phần mềm hoàn chỉnh, "
        "vừa đảm bảo tính hàn lâm khoa học về mặt thuật toán, vừa đáp ứng trọn vẹn nghiệp vụ thực tiễn."
    )

    add_h3("1.2. Mục tiêu đề tài")
    p = doc.add_paragraph()
    p.add_run("• Về mặt học thuật: ").bold = True
    p.add_run(
        "Làm chủ kỹ thuật lập trình với Danh sách liên kết đơn (Singly Linked List), quản trị con trỏ bộ nhớ động, "
        "chủ động cấp phát và giải phóng triệt để bộ nhớ trên vùng nhớ Heap, hiện thực hóa các giải thuật tìm kiếm chuỗi con "
        "và thuật toán sắp xếp nổi bọt (Bubble Sort) trực tiếp trên danh sách liên kết.\n"
    )
    p.add_run("• Về mặt ứng dụng: ").bold = True
    p.add_run(
        "Xây dựng ứng dụng Console hoàn chỉnh bằng C++, cung cấp trọn vẹn 8 chức năng CRUD và nghiệp vụ phòng vé chuyên sâu, "
        "sở hữu cơ chế kiểm soát nhập liệu an toàn chống sập chương trình (Validation Layer), giao diện bảng dữ liệu căn lề "
        "rộng rãi chuẩn 104 ký tự và cơ chế đồng bộ dữ liệu tự động 100% vào tệp tin văn bản (cinema_db.txt)."
    )

    add_h3("1.3. Phạm vi đề tài")
    doc.add_paragraph(
        "• Đối tượng quản lý: Quản lý danh mục các bộ phim (Mã định danh duy nhất, Tên phim, Thể loại, Thời lượng chiếu, Đơn giá vé) "
        "và sơ đồ phòng chiếu 30 ghế ngồi (5 hàng A-E x 6 cột 1-6) cùng thông tin vé đặt kèm theo mỗi phim.\n"
        "• Môi trường triển khai: Ứng dụng chạy trên nền tảng Console C++ (tương thích cả Windows Command Prompt / PowerShell và Linux Terminal), "
        "lưu trữ dữ liệu bền vững trên tệp tin phẳng cinema_db.txt."
    )

    # 2. Phân tích yêu cầu và mô tả giải pháp
    add_h2("2. Phân tích yêu cầu và mô tả giải pháp")
    add_h3("2.1. Phân tích yêu cầu chức năng hệ thống")
    doc.add_paragraph(
        "Hệ thống đáp ứng đầy đủ và vượt mức 8 yêu cầu cơ bản trong đề cương môn học:\n"
        "1. Nhập danh sách phim: Hỗ trợ nhập thông tin liên tiếp nhiều bộ phim từ bàn phím. Kiểm tra tính hợp lệ dữ liệu "
        "(thời lượng 15-360 phút, giá vé 10.000-1.000.000 VND, chuỗi không để trống), tự động khởi tạo ma trận 30 ghế trống cho mỗi phim mới.\n"
        "2. Thêm phim mới: Chèn một node phim mới vào cuối danh sách liên kết. Bắt buộc kiểm tra tính duy nhất của mã phim "
        "(khóa chính - Primary Key) trước khi lưu.\n"
        "3. Xem danh sách phim: Xuất toàn bộ phim ra màn hình dạng bảng chuẩn mực, căn lề 104 cột rộng rãi, thẳng tắp, không bị xô lệch cột "
        "khi tên phim hoặc thể loại quá dài.\n"
        "4. Tìm kiếm đa tiêu chí: Hỗ trợ 3 phương thức tra cứu: (1) Theo mã phim, (2) Theo từ khóa tên phim (không phân biệt hoa/thường, tìm chuỗi con), "
        "(3) Theo khoảng giá vé [GiaMin - GiaMax].\n"
        "5. Xóa phim an toàn: Xóa phim theo mã (so khớp chính xác mã) hoặc theo tên. Xử lý triệt để các ca biên đầu, giữa, cuối danh sách, "
        "yêu cầu xác nhận (y/n) trước khi thực hiện và gọi delete thu hồi RAM.\n"
        "6. Cập nhật thông tin: Tra cứu phim qua mã bằng hàm timPhimTheoMa, cho phép nhân viên lựa chọn sửa từng trường riêng lẻ (Tên, Thể loại, Thời lượng, Giá vé) "
        "mà không cần nhập lại các thông tin còn lại.\n"
        "7. Sắp xếp danh sách: Sắp xếp theo Giá vé (Tăng/Giảm dần) và Thời lượng chiếu (Tăng/Giảm dần) bằng thuật toán Bubble Sort.\n"
        "8. Nghiệp vụ phòng vé (Đặt vé & Hủy vé): Hiển thị trực quan sơ đồ 30 ghế ngồi, khách chọn ghế, nhập thông tin liên hệ (Họ tên, SĐT), "
        "hệ thống cấp mã số vé tự tăng từ #1001. Hỗ trợ hủy vé theo mã số vé và hoàn trả ghế về trạng thái trống.\n"
        "9. Đọc / Ghi cơ sở dữ liệu: Tự động nạp dữ liệu từ cinema_db.txt lên RAM khi bật ứng dụng và tự động ghi đè đồng bộ xuống tệp ngay sau mỗi thao tác."
    )

    add_h3("2.2. Mô tả kiến trúc phân tầng (Clean Architecture)")
    doc.add_paragraph(
        "Mã nguồn được tái cấu trúc (Refactor) thành 8 tầng rõ ràng theo thứ tự chuẩn mực:\n"
        "• Tầng 1 & 2: Khai báo Thư viện (Libraries) và Hằng số hệ thống (Constants: SO_HANG=5, SO_COT=6, TONG_GHE=30, FILE_DB='cinema_db.txt').\n"
        "• Tầng 3: Cấu trúc dữ liệu lồng nhau (Structs: MaVe, ThongTinGhe, Phim, NodePhim).\n"
        "• Tầng 4: Danh mục nguyên mẫu hàm (Function Prototypes) giúp trình biên dịch nắm bắt toàn bộ chữ ký hàm trước khi định nghĩa chi tiết.\n"
        "• Tầng 5: Bộ hàm tiện ích cơ bản nhất (Atomic Helpers & Validation: chuyenChuThuong, nhapChuoi, nhapSoNguyen, nhapSoThuc, timPhimTheoMa, kiemTraTrungMa, inTieuDeBang, inDongPhim, giaiPhong).\n"
        "• Tầng 6: Thao tác tệp tin CSDL (Database File I/O: kiemTraDBTrong, taoGheDong, docDanhSachPhim, ghiToanBoFile).\n"
        "• Tầng 7: Nghiệp vụ CRUD & Phòng vé (7.1 Thêm phim, 7.2 Xem danh sách, 7.3 Tìm kiếm, 7.4 Xóa phim, 7.5 Cập nhật, 7.6 Sắp xếp, 7.7 Đặt vé & Hủy vé).\n"
        "• Tầng 8: Menu điều phối & Luồng thực thi chính (hienThiMenu, khoiTaoHeThong, main)."
    )

    # 3. Thiết kế cấu trúc dữ liệu và mô hình chương trình
    add_h2("3. Thiết kế cấu trúc dữ liệu và mô hình chương trình")
    add_h3("3.1. Thiết kế các Cấu trúc dữ liệu (Struct)")
    
    doc.add_paragraph("a) Cấu trúc vé xem phim (MaVe):")
    add_code_block("struct MaVe {\n    int    soVe;      // 0 = chưa đặt, >= 1001 = mã số vé đã đặt\n    string tenKhach;  // Họ và tên khách hàng\n    string sdt;       // Số điện thoại liên hệ\n};")

    doc.add_paragraph("b) Cấu trúc một ô ghế (ThongTinGhe):")
    add_code_block("struct ThongTinGhe {\n    bool  daDat;      // false = ghế trống, true = ghế đã có người đặt\n    MaVe  ve;         // Dữ liệu vé đi kèm (chỉ có nghĩa khi daDat == true)\n};")

    doc.add_paragraph("c) Cấu trúc một bộ phim (Phim):")
    add_code_block("struct Phim {\n    string       ma;                    // Mã phim định danh duy nhất (VD: 'P01')\n    string       ten;                   // Tên bộ phim\n    string       theLoai;               // Thể loại phim\n    int          thoiLuong;             // Thời lượng chiếu (phút)\n    double       giaVe;                 // Đơn vị giá vé (VND)\n    ThongTinGhe  ghe[SO_HANG][SO_COT]; // Ma trận ghế 5 hàng (A-E) x 6 cột (1-6)\n};")

    doc.add_paragraph("d) Cấu trúc một Node trong Danh sách liên kết đơn (NodePhim):")
    add_code_block("struct NodePhim {\n    Phim      data;   // Dữ liệu bộ phim chứa trong node\n    NodePhim* next;   // Con trỏ liên kết trỏ tới node kế tiếp\n};")

    add_h3("3.2. Mô hình tổ chức bộ nhớ RAM")
    doc.add_paragraph(
        "Hệ thống quản lý toàn bộ dữ liệu thông qua con trỏ đầu danh sách 'headPhim'. "
        "Mỗi node được cấp phát động trên Heap, chứa dữ liệu phim và trỏ đến node kế tiếp:\n"
        "headPhim ──► [NodePhim: P01] ──► [NodePhim: P02] ──► ... ──► [NodePhim: P10] ──► nullptr\n"
        "Mỗi NodePhim bao hàm trọn vẹn một ma trận ghế 30 phần tử độc lập của riêng bộ phim đó."
    )

    add_h3("3.3. Quy ước ánh xạ tọa độ ghế trong phòng chiếu")
    doc.add_paragraph(
        "Phòng chiếu có 30 ghế, đánh số từ 01 đến 30. Công thức chuyển đổi 2 chiều giữa số thứ tự 'so' và chỉ số mảng ghe[r][c]:\n"
        "• Chỉ số hàng: r = (so - 1) / SO_COT    (r = 0..4 tương ứng hàng A, B, C, D, E)\n"
        "• Chỉ số cột:  c = (so - 1) % SO_COT    (c = 0..5 tương ứng cột 1, 2, 3, 4, 5, 6)\n"
        "• Ngược lại:   so = r * SO_COT + c + 1"
    )

    add_h3("3.4. Sơ đồ luồng hoạt động tổng thể của ứng dụng (Workflow)")
    doc.add_paragraph(
        "1. Khởi động (khoiTaoHeThong): Đọc file cinema_db.txt. Nạp toàn bộ 10 phim cùng trạng thái các ghế đã đặt lên RAM. Khởi tạo bộ đếm mã vé tiếp theo (veKeTiep).\n"
        "2. Vòng lặp Menu (while true): Nhận lựa chọn từ người dùng (1 đến 8).\n"
        "3. Thực thi nghiệp vụ: Gọi hàm chức năng tương ứng trên RAM.\n"
        "4. Tự động đồng bộ: Mọi thao tác Thêm, Sửa, Xóa, Sắp xếp, Đặt vé, Hủy vé đều tự động gọi ghiToanBoFile để ghi đè dữ liệu xuống đĩa cứng.\n"
        "5. Thoát chương trình (Lựa chọn 0): Ghi file lần cuối và gọi giaiPhong để delete toàn bộ các node trên Heap, trả lại RAM cho hệ điều hành."
    )

    # -------------------------------------------------------------
    # MỤC 4: MÔ TẢ NGHIỆP VỤ CHI TIẾT & CÁC ĐOẠN MÃ QUAN TRỌNG
    # -------------------------------------------------------------
    add_h2("4. Mô tả nghiệp vụ chi tiết & Phân tích các đoạn mã quan trọng")
    add_note_box("Phần này phân tích chuyên sâu luồng nghiệp vụ (Execution Flow) của các chức năng trọng tâm trên Menu, làm rõ từng trường hợp rẽ nhánh, kiểm tra điều kiện dữ liệu và cơ chế đồng bộ CSDL.")

    # 4.1. CHỨC NĂNG 1: THÊM DANH SÁCH PHIM MỚI
    add_h3("4.1. Chức năng 1: Nhập danh sách phim mới & Thêm phim (nhapDanhSachPhim, nhapMotPhim, themPhim)")
    doc.add_paragraph(
        "• Mục tiêu nghiệp vụ: Cho phép nhân viên nhập liên tiếp nhiều bộ phim mới từ bàn phím, đảm bảo tính toàn vẹn của mã khóa chính (Primary Key), "
        "ràng buộc miền giá trị hợp lệ, tự động khởi tạo ma trận 30 ghế trống cho mỗi phim và đồng bộ toàn bộ dữ liệu xuống tệp cinema_db.txt."
    )
    
    doc.add_paragraph("• Sơ đồ luồng thực thi chi tiết (Execution Flow Diagram):")
    add_flow_box(
        "[Bắt đầu nhapDanhSachPhim]\n"
        "    │\n"
        "    ▼\n"
        "Vòng lặp nhập từng phim (while true, biến đếm dem = 0):\n"
        "    │\n"
        "    ├──> B1: Gọi nhapMotPhim(head)\n"
        "    │      ├──> B1.1: Nhập Mã phim (p.ma) qua nhapChuoi()\n"
        "    │      │      ├──> Gọi kiemTraTrungMa(head, p.ma) -> gọi timPhimTheoMa(head, p.ma)\n"
        "    │      │      ├──> [Trường hợp A - TRÙNG MÃ]: Mã đã tồn tại (không phân biệt hoa/thường)\n"
        "    │      │      │      └──> Báo lỗi: '[!] Ma phim DA TON TAI! Vui long dung ma khac.' -> Bắt nhập lại.\n"
        "    │      │      └──> [Trường hợp B - MÃ HỢP LỆ]: Mã chưa có trong CSDL -> Chấp nhận mã.\n"
        "    │      │\n"
        "    │      ├──> B1.2: Nhập thông tin chi tiết qua bộ hàm Validation:\n"
        "    │      │      ├──> Tên phim: nhapChuoi() (chống trôi dòng cin, bắt buộc không rỗng).\n"
        "    │      │      ├──> Thể loại: nhapChuoi() (không để trống).\n"
        "    │      │      ├──> Thời lượng: nhapSoNguyen(15, 360) (bắt buộc nằm trong [15 - 360] phút).\n"
        "    │      │      └──> Giá vé: nhapSoThuc(10000, 1000000) (bắt buộc trong [10.000 - 1.000.000] VND).\n"
        "    │      │\n"
        "    │      └──> B1.3: Khởi tạo 30 ô ghế trống cho phòng chiếu:\n"
        "    │             └──> Quét ma trận 5x6: gán daDat = false và ve = {0, \"\", \"\"}.\n"
        "    │\n"
        "    ├──> B2: Gọi themPhim(head, p) để nối node vào đuôi Danh sách liên kết:\n"
        "    │      ├──> Cấp phát động: NodePhim* node = new NodePhim{ p, nullptr }.\n"
        "    │      ├──> [Trường hợp 1 - Danh sách rỗng (head == nullptr)]: Gán head = node.\n"
        "    │      └──> [Trường hợp 2 - Danh sách có node]: Duyệt tới node cuối (t->next == nullptr), gán t->next = node.\n"
        "    │\n"
        "    ├──> B3: Thông báo đã thêm tạm thời vào RAM và hỏi: 'Ban co muon nhap them nua khong? (y/n)':\n"
        "    │      ├──> [Nếu chọn y / Y]: Tăng biến đếm dem++, quay lại B1 nhập phim tiếp theo.\n"
        "    │      └──> [Nếu chọn khác y/Y]: Thoát vòng lặp nhập phim.\n"
        "    │\n"
        "    └──> B4: Đồng bộ dữ liệu xuống đĩa cứng:\n"
        "           └──> Gọi ghiToanBoFile(FILE_DB, head) -> Ghi đè toàn bộ dữ liệu xuống cinema_db.txt -> Hoàn tất."
    )

    doc.add_paragraph("• Phân tích các trường hợp rẽ nhánh & Ca biên:")
    doc.add_paragraph(
        "1. Trùng mã phim: Người dùng nhập 'p01' hay 'P01' khi hệ thống đã có 'P01' đều bị hàm kiemTraTrungMa chặn lại nhờ cơ chế so sánh chữ thường của timPhimTheoMa. Người dùng bắt buộc phải nhập mã mới duy nhất mới được đi tiếp.\n"
        "2. Nhập sai định dạng: Nếu người dùng cố tình nhập chữ cái vào ô Thời lượng hoặc Giá vé, hoặc nhập số âm, hàm nhapSoNguyen và nhapSoThuc sẽ bắt lỗi thông qua stringstream, hiển thị thông báo lỗi và yêu cầu nhập lại mà chương trình không bao giờ bị crash.\n"
        "3. Danh sách ban đầu rỗng vs đã có dữ liệu: Hàm themPhim xử lý an toàn cả trường hợp con trỏ head đang là nullptr (gán trực tiếp) và trường hợp đã có hàng nghìn node (duyệt tới đuôi rồi nối con trỏ next)."
    )

    doc.add_paragraph("• Đoạn mã nguồn then chốt:")
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

    # 4.2. CHỨC NĂNG 2: XEM DANH SÁCH PHIM
    add_h3("4.2. Chức năng 2: Hiển thị danh sách phim dạng bảng 104 cột (xemDanhSachPhim, inTieuDeBang, inDongPhim)")
    doc.add_paragraph(
        "• Mục tiêu nghiệp vụ: Xuất toàn bộ danh mục phim ra console dưới dạng bảng chuẩn hóa 104 cột, căn lề thẳng hàng tuyệt đối, "
        "tự động co giãn không gian để ngay cả các tựa phim dài đến 40 ký tự và thể loại ghép 24 ký tự cũng không gây tràn dòng hay xô lệch cột."
    )

    doc.add_paragraph("• Sơ đồ luồng thực thi chi tiết (Execution Flow Diagram):")
    add_flow_box(
        "[Bắt đầu xemDanhSachPhim(headPhim)]\n"
        "    │\n"
        "    ├──> B1: Kiểm tra danh sách phim trên RAM (tại Menu chính):\n"
        "    │      ├──> [Trường hợp A - Danh sách rỗng (headPhim == nullptr)]:\n"
        "    │      │      └──> Báo: '[!] Danh sach hien dang trong, vui long nhap phim truoc!' -> Quay về Menu.\n"
        "    │      └──> [Trường hợp B - Danh sách có phim]: Tiếp tục B2.\n"
        "    │\n"
        "    ├──> B2: In tiêu đề bảng (inTieuDeBang()):\n"
        "    │      ├──> In Header: printf(\"%-8s %-40s %-24s %-14s %-14s\\n\", ...)\n"
        "    │      └──> In đường kẻ ngang trên: string(104, '-').\n"
        "    │\n"
        "    ├──> B3: Duyệt tuần tự danh sách liên kết đơn (while p != nullptr):\n"
        "    │      ├──> Tại mỗi node, gọi inDongPhim(p->data):\n"
        "    │      │      ├──> Định dạng chuỗi thời lượng: to_string(p.thoiLuong) + \" phut\".\n"
        "    │      │      ├──> Định dạng chuỗi giá vé: to_string((long long)p.giaVe) + \" VND\".\n"
        "    │      │      └──> Xuất dòng dữ liệu khớp 104 cột: printf(\"%-8s %-40s %-24s %-14s %-14s\\n\", ...).\n"
        "    │      └──> Dời con trỏ: p = p->next.\n"
        "    │\n"
        "    └──> B4: In đường kẻ kép đóng bảng: string(104, '=')."
    )

    doc.add_paragraph("• Phân tích các trường hợp rẽ nhánh & Kỹ thuật định dạng:")
    doc.add_paragraph(
        "1. Tối ưu hóa độ rộng cột: Trước đây khi dùng %-30s cho tên phim, phim 'Spider-Man: Across Spider-Verse' (31 ký tự) "
        "bị tràn 1 ký tự đẩy cột Thể loại sang phải. Nhóm đã nâng lên %-40s cho tên phim và %-24s cho thể loại ('Lich Su - Chinh Kich' dài 20 ký tự), "
        "đảm bảo 100% phim mẫu hiển thị thẳng tắp.\n"
        "2. Đồng nhất kiểu dữ liệu in: Thay vì in số nguyên kèm chữ 'phut' rời rạc gây lệch tab, hàm inDongPhim đóng gói sẵn thành chuỗi "
        "'192 phut' và '95000 VND' rồi in đồng bộ qua định dạng %-14s."
    )

    doc.add_paragraph("• Đoạn mã nguồn then chốt:")
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

    # 4.3. CHỨC NĂNG 7: XEM SƠ ĐỒ GHẾ PHÒNG CHIẾU
    add_h3("4.3. Chức năng 7: Xem sơ đồ ghế phòng chiếu trực quan (xemSoDoGhe)")
    doc.add_paragraph(
        "• Mục tiêu nghiệp vụ: Cung cấp giao diện trực quan mô phỏng phòng chiếu thực tế gồm màn hình Screen và ma trận 30 ghế ngồi "
        "(5 hàng A-E x 6 cột 1-6), hiển thị rõ ràng tình trạng ghế còn trống [Số] hay đã đặt [ X], hỗ trợ khách hàng chọn chỗ ngồi ưng ý."
    )

    doc.add_paragraph("• Sơ đồ luồng thực thi chi tiết (Execution Flow Diagram):")
    add_flow_box(
        "[Bắt đầu Chức năng 7 / Xem sơ đồ ghế]\n"
        "    │\n"
        "    ├──> B1: Kiểm tra danh sách: Nếu headPhim == nullptr -> Thông báo trống, quay về Menu.\n"
        "    │\n"
        "    ├──> B2: Nhập mã phim cần xem sơ đồ (maPhim) qua nhapChuoi() (VD: 'P01', 'p07').\n"
        "    │\n"
        "    ├──> B3: Tra cứu con trỏ phim qua hàm timPhimTheoMa(headPhim, maPhim):\n"
        "    │      ├──> [Trường hợp A - Không tìm thấy (p == nullptr)]:\n"
        "    │      │      └──> Báo lỗi: '[!] Khong tim thay phim co ma: ...' -> Dừng thao tác.\n"
        "    │      └──> [Trường hợp B - Tìm thấy phim (p != nullptr)]:\n"
        "    │             └──> Chuyển tiếp con trỏ p tới hàm xemSoDoGhe(p).\n"
        "    │\n"
        "    └──> B4: Vẽ trực quan sơ đồ phòng chiếu (xemSoDoGhe):\n"
        "           ├──> In khung tiêu đề: Tên phim, Mã phim và khung [ MAN HINH CHIEU (SCREEN) ].\n"
        "           ├──> In thanh tiêu đề cột: 'Cot 1   Cot 2   Cot 3   Cot 4   Cot 5   Cot 6'.\n"
        "           ├──> Quét 2 vòng lặp lồng nhau ma trận ghe[r][c] (r = 0..4 tương ứng Hàng A..E, c = 0..5):\n"
        "           │      ├──> Tính số ghế thứ tự: soGhe = r * 6 + c + 1 (từ 01 đến 30).\n"
        "           │      ├──> [Nhánh 1 - Ghế ĐÃ ĐẶT (daDat == true)]: In ký hiệu ' [ X]  '.\n"
        "           │      └──> [Nhánh 2 - Ghế CÒN TRỐNG (daDat == false)]: In số ghế dạng ' [%02d]  ' (VD: [01], [15]).\n"
        "           └──> In phần chú thích và đơn giá vé: '[So]: Ghe trong | [ X]: Ghe da dat' và 'Gia ve: ... VND / ghe'."
    )

    doc.add_paragraph("• Phân tích các trường hợp rẽ nhánh:")
    doc.add_paragraph(
        "1. Tra cứu không phân biệt hoa thường: Khách gõ 'p07' hay 'P07' đều tìm thấy phim Spider-Man nhờ hàm timPhimTheoMa chuyển chuỗi về lowercase trước khi so sánh.\n"
        "2. Hiển thị ghế hai chữ số đồng bộ: Dùng định dạng [%02d] giúp các ghế từ 1 đến 9 hiển thị thành [01]..[09], có cùng độ rộng 4 ký tự như các ghế từ [10] đến [30], "
        "giữ cho toàn bộ ma trận 5x6 luôn vuông vắn, không bị lệch hàng ngang hay hàng dọc."
    )

    doc.add_paragraph("• Đoạn mã nguồn then chốt:")
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

    # 4.4. CHỨC NĂNG 8: NGHIỆP VỤ PHÒNG VÉ: ĐẶT VÉ & HỦY VÉ
    add_h3("4.4. Chức năng 8: Nghiệp vụ phòng vé: Đặt vé & Hủy vé xem phim (hienMenuDatVeHuyVe, datVe, huyVe)")
    doc.add_paragraph(
        "• Mục tiêu nghiệp vụ: Hiện thực hóa quy trình nghiệp vụ cốt lõi của đề tài rạp chiếu phim theo chu trình khép kín: "
        "Chọn phim -> Xem sơ đồ ghế -> Chọn vị trí -> Cấp mã vé tự tăng (#1001) -> Thu thập thông tin khách hàng -> "
        "Cập nhật trạng thái ghế -> Tự động đồng bộ CSDL ngay lập tức. Hỗ trợ hủy vé an toàn và hoàn trả ghế trống tức thì."
    )

    doc.add_paragraph("• Sơ đồ luồng thực thi chi tiết (Execution Flow Diagram):")
    add_flow_box(
        "[Bắt đầu hienMenuDatVeHuyVe(headPhim, veKeTiep)]\n"
        "    │\n"
        "    ├──> Hiển thị Menu: 1. Đặt vé | 2. Hủy vé | 3. Xem sơ đồ ghế | 0. Quay lại\n"
        "    │\n"
        "    ├───► [LỰA CHỌN 1: ĐẶT VÉ XEM PHIM - datVe(headPhim, veKeTiep)]\n"
        "    │       │\n"
        "    │       ├──> B1: Nhập mã phim cần đặt -> timPhimTheoMa(headPhim, maPhim).\n"
        "    │       │      └──> Nếu p == nullptr: Báo lỗi 'Không tìm thấy phim' -> Dừng.\n"
        "    │       │\n"
        "    │       ├──> B2: Gọi xemSoDoGhe(p) hiển thị trực quan 30 ghế của phim đó.\n"
        "    │       │\n"
        "    │       ├──> B3: Vòng lặp chọn ghế an toàn (while true):\n"
        "    │       │      ├──> Nhập số ghế: nhapSoNguyen(1, 30).\n"
        "    │       │      ├──> Tính tọa độ ma trận: r = (soGhe - 1) / 6, c = (soGhe - 1) % 6.\n"
        "    │       │      ├──> [Trường hợp GHẾ ĐÃ ĐẶT (ghe[r][c].daDat == true)]:\n"
        "    │       │      │      └──> Báo: '[!] Ghe so X DA CO NGUOI DAT! Vui long chon ghe khac.' -> Bắt nhập lại.\n"
        "    │       │      └──> [Trường hợp GHẾ CÒN TRỐNG (ghe[r][c].daDat == false)]:\n"
        "    │       │             └──> Hợp lệ -> Thoát vòng lặp chọn ghế.\n"
        "    │       │\n"
        "    │       ├──> B4: Nhập thông tin khách hàng:\n"
        "    │       │      ├──> Họ tên khách: nhapChuoi() (không rỗng).\n"
        "    │       │      └──> Số điện thoại: nhapChuoi() (không rỗng).\n"
        "    │       │\n"
        "    │       ├──> B5: Cấp phát vé và cập nhật ô ghế:\n"
        "    │       │      ├──> Lấy mã số vé tự tăng: maVeMoi = veKeTiep++ (từ #1001 trở đi).\n"
        "    │       │      ├──> Đánh dấu ghế: p->data.ghe[r][c].daDat = true.\n"
        "    │       │      └──> Gán vé: p->data.ghe[r][c].ve = { maVeMoi, tenKhach, sdt }.\n"
        "    │       │\n"
        "    │       ├──> B6: Đồng bộ CSDL tức thì: Gọi ghiToanBoFile(FILE_DB, headPhim).\n"
        "    │       │\n"
        "    │       └──> B7: Xuất hóa đơn vé: In Mã vé, Tên phim, Tọa độ hàng A-E, cột 1-6, tên khách, SĐT và giá tiền.\n"
        "    │\n"
        "    └───► [LỰA CHỌN 2: HỦY VÉ ĐÃ ĐẶT - huyVe(headPhim)]\n"
        "            │\n"
        "            ├──> B1: Nhập mã số vé cần hủy (nhapSoNguyen, nhập 0 để thoát).\n"
        "            │\n"
        "            ├──> B2: Duyệt toàn hệ thống tìm vé (quét qua từng phim và 30 ghế của từng phim):\n"
        "            │      └──> Điều kiện so khớp: if (p->data.ghe[r][c].daDat && p->data.ghe[r][c].ve.soVe == maVeCanHuy).\n"
        "            │\n"
        "            ├──> B3: [Trường hợp KHÔNG TÌM THẤY]: Báo '[!] Khong tim thay ve co ma #... trong he thong!'.\n"
        "            │\n"
        "            └──> B4: [Trường hợp TÌM THẤY VÉ]:\n"
        "                   ├──> In chi tiết vé: Mã vé, Tên phim, Vị trí ghế (Hàng + Cột), Tên khách + SĐT.\n"
        "                   ├──> Xác nhận an toàn: 'Ban co CHAC CHAN muon huy ve nay? (y/n)'.\n"
        "                   ├──> [Nếu chọn n / N]: Hủy thao tác, vé được giữ nguyên vẹn.\n"
        "                   └──> [Nếu chọn y / Y]:\n"
        "                          ├──> Khôi phục ghế trống: daDat = false, ve = {0, \"\", \"\"}.\n"
        "                          ├──> Đồng bộ CSDL: Gọi ghiToanBoFile(FILE_DB, headPhim).\n"
        "                          └──> Thông báo hủy vé thành công và trả ghế về trạng thái sẵn sàng đón khách."
    )

    doc.add_paragraph("• Phân tích các trường hợp rẽ nhánh:")
    doc.add_paragraph(
        "1. Chống đặt trùng ghế: Vòng lặp while true kết hợp điều kiện if (p->data.ghe[r][c].daDat) bảo vệ tuyệt đối tính duy nhất của từng ô ghế. Khách không thể đặt đè lên ghế đã có người ngồi.\n"
        "2. Cơ chế mã vé tự tăng (Auto-increment): Biến veKeTiep được khởi tạo từ tệp CSDL (tìm mã vé lớn nhất hiện có + 1) hoặc mặc định 1001, đảm bảo mỗi vé bán ra có định danh duy nhất trên toàn hệ thống.\n"
        "3. Hủy vé có xác nhận an toàn: Thao tác hủy ghế thay đổi dữ liệu doanh thu nên bắt buộc có bước xác nhận y/n. Ngay khi hủy, hệ thống gọi ghiToanBoFile để lưu ngay trạng thái trống xuống tệp text."
    )

    doc.add_paragraph("• Đoạn mã nguồn then chốt:")
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

    # 4.5. TÌM KIẾM MÃ CHUẨN HÓA & ĐỒNG BỘ DỮ LIỆU
    add_h3("4.5. Hàm nguyên tử dùng chung & Cơ chế đồng bộ CSDL (timPhimTheoMa, ghiToanBoFile)")
    doc.add_paragraph(
        "• Hàm nguyên tử timPhimTheoMa: Chuẩn hóa so sánh mã phim không phân biệt hoa/thường, được tái sử dụng xuyên suốt trong Chức năng 1 (kiểm tra trùng mã), "
        "Chức năng 5 (cập nhật thông tin), Chức năng 7 (xem sơ đồ ghế) và Chức năng 8 (đặt vé xem phim)."
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
        "• Cơ chế đồng bộ hóa CSDL bền vững (Persistence Layer): Quét toàn bộ danh sách liên kết đơn trên RAM và ghi nhận định dạng phân cấp xuống cinema_db.txt:"
    )
    add_code_block(
        "void ghiToanBoFile(const string& file, NodePhim* head) {\n"
        "    ofstream f(file); // Mở chế độ ghi đè toàn bộ (overwrite)\n"
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
    add_note_box("Thành viên 3 chạy chương trình ./main_app (hoặc main_refactored.exe), dùng tổ hợp phím Windows + Shift + S chụp lại màn hình console thực tế và dán trực tiếp vào các khung dưới đây:")

    add_h3("5.1. Màn hình khởi động hệ thống & Menu chính (Nạp 10 phim)")
    add_image_placeholder("Khởi động hệ thống & Menu chính", "Minh họa thông báo nạp thành công 10 phim từ database và menu 8 chức năng")

    add_h3("5.2. Chức năng 2: Xem danh sách phim dạng bảng (Căn lề 104 cột)")
    add_image_placeholder("Bảng danh sách phim căn lề 104 cột", "Minh họa bảng danh sách 10 bộ phim với các cột căn lề thẳng tắp, không bị xô lệch")

    add_h3("5.3. Chức năng 1 & 2: Thêm phim mới & Bắt lỗi trùng mã phim")
    add_image_placeholder("Thêm phim mới & Cảnh báo trùng mã", "Minh họa nhập mã P01 bị chặn lại do đã tồn tại trong CSDL")

    add_h3("5.4. Chức năng 3: Tìm kiếm phim đa tiêu chí (Mã, Tên, Giá vé)")
    add_image_placeholder("Kết quả tìm kiếm phim", "Minh họa kết quả tìm kiếm theo từ khóa tên hoặc theo khoảng giá vé")

    add_h3("5.5. Chức năng 4: Xóa phim khỏi hệ thống (Xác nhận an toàn y/n)")
    add_image_placeholder("Xóa phim thành công", "Minh họa bước hỏi xác nhận (y/n) trước khi xóa và thông báo xóa thành công")

    add_h3("5.6. Chức năng 5: Cập nhật thông tin phim (Sửa từng thuộc tính)")
    add_image_placeholder("Cập nhật thông tin phim", "Minh họa giao diện cho phép chọn sửa Tên, Thể loại, Thời lượng, Giá vé")

    add_h3("5.7. Chức năng 6: Sắp xếp danh sách phim (Giá vé & Thời lượng)")
    add_image_placeholder("Bảng phim sau khi sắp xếp", "Minh họa bảng danh sách phim sau khi sắp xếp giá vé giảm dần hoặc thời lượng tăng dần")

    add_h3("5.8. Chức năng 7: Sơ đồ ghế phòng chiếu trực quan (Ma trận 5x6)")
    add_image_placeholder("Sơ đồ phòng chiếu 30 ghế", "Minh họa ma trận ghế với màn hình chiếu SCREEN, ký hiệu ghế trống [01]..[30] và ghế đã đặt [ X]")

    add_h3("5.9. Chức năng 8: Giao dịch Đặt vé & Hủy vé xem phim")
    add_image_placeholder("Đặt vé & Hủy vé thành công", "Minh họa hóa đơn vé cấp mới #1001 kèm vị trí ghế và quy trình hủy vé")

    # -------------------------------------------------------------
    # MỤC 6: NHẬN XÉT VÀ HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------
    add_h2("6. Nhận xét và hướng phát triển thêm")
    add_h3("6.1. Đánh giá ưu điểm của chương trình")
    doc.add_paragraph(
        "1. Ứng dụng chuẩn mực cấu trúc dữ liệu: Triển khai thành công Danh sách liên kết đơn trong quản lý dữ liệu động, con trỏ hoạt động chính xác, giải phóng RAM sạch sẽ trước khi kết thúc chương trình.\n"
        "2. Kiểm soát nhập liệu toàn diện (Chống Crash 100%): Bộ hàm validation bằng stringstream ngăn chặn triệt để hiện tượng trôi dòng lệnh cin và bắt lỗi người dùng gõ sai kiểu dữ liệu (chữ vào ô số, chuỗi rỗng).\n"
        "3. Giao diện bảng Console đạt tính thẩm mỹ cao: Căn lề 104 cột rộng rãi, giải quyết triệt để lỗi tràn dòng khi tên phim hoặc thể loại quá dài.\n"
        "4. Bố cục mã nguồn chuyên nghiệp (Clean Architecture): Tách biệt 8 tầng rõ ràng, khai báo nguyên mẫu hàm đầy đủ, hàm nguyên tử timPhimTheoMa được tái sử dụng tối ưu.\n"
        "5. Đồng bộ hóa dữ liệu thời gian thực: Tự động ghi nhận mọi thay đổi xuống tệp cinema_db.txt, bảo toàn tuyệt đối dữ liệu."
    )

    add_h3("6.2. Hạn chế còn tồn tại")
    doc.add_paragraph(
        "1. Giao diện người dùng: Hoạt động trên môi trường Console văn bản, chưa có giao diện đồ họa chuột (GUI) hay hiển thị poster phim.\n"
        "2. Cấu hình phòng chiếu: Quy mô phòng chiếu hiện cố định ở mức 30 ghế (5 hàng x 6 cột), chưa hỗ trợ thiết lập số hàng và số cột linh hoạt theo từng phòng thực tế.\n"
        "3. Phân quyền hệ thống: Chưa có module đăng nhập phân quyền giữa Quản trị viên (Admin - thêm/sửa/xóa phim) và Khách hàng (chỉ tra cứu và đặt vé)."
    )

    add_h3("6.3. Hướng phát triển trong tương lai")
    doc.add_paragraph(
        "• Nâng cấp giao diện người dùng: Xây dựng giao diện đồ họa GUI bằng thư viện C++ Qt hoặc chuyển đổi hệ thống sang nền tảng Web Fullstack.\n"
        "• Tích hợp cấu trúc dữ liệu Ngăn xếp (Stack - LIFO): Hiện thực hóa tính năng Undo (Hoàn tác) giúp nhân viên phục hồi lại phim khi lỡ tay xóa hoặc sửa nhầm.\n"
        "• Tích hợp cấu trúc dữ liệu Hàng đợi (Queue - FIFO): Quản lý hàng chờ đặt vé trực tuyến vào các suất chiếu giờ vàng của phim bom tấn.\n"
        "• Tích hợp Cây nhị phân tìm kiếm cân bằng (AVL Tree / Red-Black Tree): Tối ưu hóa thời gian tìm kiếm từ O(n) xuống O(log n) khi dữ liệu phim mở rộng lên hàng nghìn bản ghi.\n"
        "• Báo cáo tài chính: Tự động tính toán tổng doanh thu theo từng ngày, xuất hóa đơn vé và ghi nhật ký giao dịch vào file history.txt."
    )

    # Lưu tài liệu ra cả 2 file để đảm bảo không bị nghẽn
    primary_path = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Tieu_Luan_MovieBooking.docx"
    alt_path = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Tieu_Luan_MovieBooking_ChiTietNghiepVu.docx"
    
    doc.save(alt_path)
    print(f"[OK] Successfully saved: {alt_path}")

    try:
        doc.save(primary_path)
        print(f"[OK] Successfully updated primary file: {primary_path}")
    except Exception as e:
        print(f"[NOTE] Primary file {primary_path} is currently locked by Word: {e}")

if __name__ == "__main__":
    build_full_report()
