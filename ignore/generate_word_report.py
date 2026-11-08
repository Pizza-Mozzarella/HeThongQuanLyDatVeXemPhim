import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

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

def build_refactored_document(output_path):
    doc = Document()

    # Căn lề chuẩn A4 học thuật Việt Nam: Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)

    # Cấu hình Style mặc định
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

    r_desc = p_title.add_run("(Kiến trúc phân lớp chuẩn mực - Cấu trúc dữ liệu: Danh sách liên kết đơn & Ma trận phòng chiếu)\n")
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
    # HÀM BỔ TRỢ ĐỊNH DẠNG VĂN BẢN (HELPERS)
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

    # 4. Một số đoạn mã quan trọng
    add_h2("4. Một số đoạn mã quan trọng (có chú thích chi tiết)")

    add_h3("4.1. Khởi tạo & Kiểm tra cơ sở dữ liệu rỗng (kiemTraDBTrong)")
    add_code_block(
        "bool kiemTraDBTrong(const string& file) {\n"
        "    ifstream f(file);\n"
        "    if (!f.is_open()) return true; // File chưa tồn tại -> coi như rỗng\n"
        "    string dong;\n"
        "    while (getline(f, dong)) {\n"
        "        if (!dong.empty() && dong.find_first_not_of(\" \\t\\r\\n\") != string::npos) {\n"
        "            f.close();\n"
        "            return false; // File có dữ liệu thực tế\n"
        "        }\n"
        "    }\n"
        "    f.close();\n"
        "    return true; // File rỗng 0 byte\n"
        "}"
    )
    doc.add_paragraph("Chú thích: Giúp hệ thống khởi động an toàn, phân biệt chính xác giữa tệp tin chưa tồn tại, tệp rỗng và tệp đã có dữ liệu hợp lệ.")

    add_h3("4.2. Tìm kiếm mã phim chuẩn hóa & Kiểm tra trùng mã (timPhimTheoMa, kiemTraTrungMa)")
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
        "}\n\n"
        "bool kiemTraTrungMa(NodePhim* head, string ma) {\n"
        "    return timPhimTheoMa(head, ma) != nullptr;\n"
        "}"
    )
    doc.add_paragraph("Chú thích: Hàm nguyên tử timPhimTheoMa so sánh mã không phân biệt hoa/thường ('p01' hay 'P01' đều khớp), tái sử dụng xuyên suốt hệ thống trong kiểm tra trùng mã, cập nhật thông tin, xem sơ đồ ghế và đặt vé.")

    add_h3("4.3. Thuật toán Xóa phim an toàn xử lý triệt để ca biên (xoaPhim, khopPhim)")
    add_code_block(
        "NodePhim* xoaPhim(NodePhim*& head, string maCanXoa, string tenCanXoa) {\n"
        "    if (head == nullptr) return nullptr;\n"
        "    // Ca biên 1: Node cần xóa nằm ngay đầu danh sách\n"
        "    if (khopPhim(head, maCanXoa, tenCanXoa)) {\n"
        "        NodePhim* del = head;\n"
        "        head = head->next;\n"
        "        return del;\n"
        "    }\n"
        "    // Ca biên 2: Node cần xóa nằm ở giữa hoặc cuối danh sách\n"
        "    NodePhim* p = head;\n"
        "    while (p->next != nullptr) {\n"
        "        if (khopPhim(p->next, maCanXoa, tenCanXoa)) {\n"
        "            NodePhim* del = p->next;\n"
        "            p->next = del->next;\n"
        "            return del;\n"
        "        }\n"
        "        p = p->next;\n"
        "    }\n"
        "    return nullptr;\n"
        "}"
    )
    doc.add_paragraph("Chú thích: Ngắt liên kết con trỏ chính xác mà không làm đứt gãy danh sách, trả về con trỏ del để hàm điều khiển hiển thị thông báo và gọi delete del giải phóng bộ nhớ RAM.")

    add_h3("4.4. Thuật toán Sắp xếp Bubble Sort trên Danh sách liên kết đơn (sapXepDanhSachPhim)")
    add_code_block(
        "void sapXepDanhSachPhim(NodePhim*& head, bool giamDan, bool laGiaVe) {\n"
        "    if (head == nullptr || head->next == nullptr) return;\n"
        "    bool swapped;\n"
        "    NodePhim* ptr1;\n"
        "    NodePhim* lptr = nullptr; // Giới hạn phạm vi duyệt của mỗi lượt\n"
        "    do {\n"
        "        swapped = false;\n"
        "        ptr1 = head;\n"
        "        while (ptr1->next != lptr) {\n"
        "            NodePhim* ptr2 = ptr1->next;\n"
        "            double val1 = laGiaVe ? ptr1->data.giaVe : ptr1->data.thoiLuong;\n"
        "            double val2 = laGiaVe ? ptr2->data.giaVe : ptr2->data.thoiLuong;\n"
        "            bool dieuKienDoi = giamDan ? (val1 < val2) : (val1 > val2);\n"
        "            if (dieuKienDoi) {\n"
        "                Phim temp = ptr1->data; // Hoán vị dữ liệu data\n"
        "                ptr1->data = ptr2->data;\n"
        "                ptr2->data = temp;\n"
        "                swapped = true;\n"
        "            }\n"
        "            ptr1 = ptr1->next;\n"
        "        }\n"
        "        lptr = ptr1;\n"
        "    } while (swapped);\n"
        "}"
    )
    doc.add_paragraph("Chú thích: Sắp xếp nổi bọt trên danh sách liên kết đơn thông qua hoán đổi vùng dữ liệu data, tối ưu hóa số vòng lặp bằng con trỏ biên lptr, hỗ trợ linh hoạt cả tiêu chí giá vé và thời lượng.")

    add_h3("4.5. Nghiệp vụ phòng vé: Đặt vé xem phim & Cập nhật ma trận ghế (datVe)")
    add_code_block(
        "void datVe(NodePhim* headPhim, int& veKeTiep) {\n"
        "    string maPhim = nhapChuoi(\"Nhap ma phim ban muon dat ve (VD: P01): \");\n"
        "    NodePhim* p = timPhimTheoMa(headPhim, maPhim);\n"
        "    if (p == nullptr) { cout << \"[!] Khong tim thay phim!\\n\"; return; }\n"
        "    xemSoDoGhe(p); // Hiển thị sơ đồ trực quan 30 ghế\n"
        "    int soGhe, r, c;\n"
        "    while (true) {\n"
        "        soGhe = nhapSoNguyen(\"Nhap so ghe ban muon dat (1 - 30): \", 1, TONG_GHE);\n"
        "        r = (soGhe - 1) / SO_COT;\n"
        "        c = (soGhe - 1) % SO_COT;\n"
        "        if (p->data.ghe[r][c].daDat) cout << \"[!] Ghe da co nguoi dat!\\n\";\n"
        "        else break;\n"
        "    }\n"
        "    string tenKhach = nhapChuoi(\"  + Ho ten khach hang: \");\n"
        "    string sdt      = nhapChuoi(\"  + So dien thoai: \");\n"
        "    int maVeMoi = veKeTiep++;\n"
        "    p->data.ghe[r][c].daDat = true;\n"
        "    p->data.ghe[r][c].ve    = { maVeMoi, tenKhach, sdt };\n"
        "    ghiToanBoFile(FILE_DB, headPhim); // Đồng bộ ngay xuống Database\n"
        "}"
    )
    doc.add_paragraph("Chú thích: Khách chọn ghế trực tiếp theo mã số 1-30, hệ thống tự ánh xạ sang tọa độ ma trận 5x6, kiểm tra chống đặt đè ghế, cấp mã vé tự tăng và lưu trữ thông tin khách hàng.")

    add_h3("4.6. Đồng bộ toàn bộ dữ liệu xuống tệp tin Database (ghiToanBoFile)")
    add_code_block(
        "void ghiToanBoFile(const string& file, NodePhim* head) {\n"
        "    ofstream f(file); // Ghi đè toàn bộ (overwrite)\n"
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
    doc.add_paragraph("Chú thích: Cơ chế đồng bộ hóa dữ liệu toàn vẹn, quét toàn bộ danh sách liên kết đơn trên RAM và ghi nhận xuống file phẳng, đảm bảo tính bền vững (Persistence).")

    # 5. Hình ảnh minh họa
    add_h2("5. Hình ảnh minh họa (Chạy chương trình thực tế)")
    add_note_box("Thành viên 3 chạy chương trình ./main_app (hoặc main.exe), dùng tổ hợp phím Windows + Shift + S chụp lại màn hình console thực tế và dán trực tiếp vào các khung dưới đây:")

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

    # 6. Nhận xét và hướng phát triển thêm
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

    # Save document
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    target = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Tieu_Luan_MovieBooking_Refactored.docx"
    build_refactored_document(target)
