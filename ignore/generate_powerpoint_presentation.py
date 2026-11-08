import os
import sys

try:
    import pptx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    import pptx

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_structured_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    COLOR_BG_DARK   = RGBColor(13, 27, 42)     # #0D1B2A
    COLOR_NAVY      = RGBColor(27, 38, 59)     # #1B263B
    COLOR_BLUE_ACC  = RGBColor(65, 90, 119)    # #415A77
    COLOR_LIGHT_BG  = RGBColor(248, 249, 250)  # #F8F9FA
    COLOR_CARD_BG   = RGBColor(255, 255, 255)  # #FFFFFF
    COLOR_CODE_BG   = RGBColor(241, 245, 249)  # #F1F5F9 (Background code)
    COLOR_GOLD      = RGBColor(230, 126, 34)   # #E67E22
    COLOR_TEXT_MAIN = RGBColor(30, 41, 59)     # #1E293B
    COLOR_WHITE     = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.name = "Segoe UI"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_GOLD

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY

    def add_function_slide(slide, cat, title, flow_steps, code_snippet):
        add_header(slide, cat, title)

        # Cột trái: Khung chèn hình Flowchart & Các bước chạy
        col_w = Inches(5.65)
        h_all = Inches(5.6)
        left1 = Inches(0.8)
        top1 = Inches(1.5)

        card_flow = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left1, top1, col_w, h_all)
        card_flow.fill.solid()
        card_flow.fill.fore_color.rgb = COLOR_CARD_BG
        card_flow.line.color.rgb = COLOR_BLUE_ACC
        card_flow.line.width = Pt(1.2)

        # Placeholder để bạn chèn ảnh Flowchart
        img_placeholder = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left1 + Inches(0.2), top1 + Inches(0.2), col_w - Inches(0.4), Inches(2.2))
        img_placeholder.fill.solid()
        img_placeholder.fill.fore_color.rgb = RGBColor(238, 242, 246)
        img_placeholder.line.color.rgb = COLOR_GOLD
        img_placeholder.line.width = Pt(1.5)
        tf_img = img_placeholder.text_frame
        tf_img.word_wrap = True
        p_img = tf_img.paragraphs[0]
        p_img.alignment = PP_ALIGN.CENTER
        p_img.text = "🖼️ [CHÈN ẢNH VẼ FLOWCHART VÀO ĐÂY]\n(Kéo thả hình vẽ sơ đồ luồng của chức năng này vào khung này)"
        p_img.font.name = "Segoe UI"
        p_img.font.size = Pt(11)
        p_img.font.bold = True
        p_img.font.color.rgb = COLOR_GOLD

        # Khung các bước chạy dưới ảnh
        box_steps = slide.shapes.add_textbox(left1 + Inches(0.2), top1 + Inches(2.45), col_w - Inches(0.4), Inches(3.0))
        tf_steps = box_steps.text_frame
        tf_steps.word_wrap = True
        p_st = tf_steps.paragraphs[0]
        p_st.text = "MÔ TẢ LUỒNG HOẠT ĐỘNG:"
        p_st.font.name = "Segoe UI"
        p_st.font.size = Pt(12)
        p_st.font.bold = True
        p_st.font.color.rgb = COLOR_NAVY
        p_st.space_after = Pt(4)

        for step in flow_steps:
            p = tf_steps.add_paragraph()
            p.text = "• " + step
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(3)

        # Cột phải: Đoạn mã nguồn then chốt
        left2 = Inches(6.85)
        card_code = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left2, top1, col_w, h_all)
        card_code.fill.solid()
        card_code.fill.fore_color.rgb = COLOR_CODE_BG
        card_code.line.color.rgb = COLOR_BLUE_ACC
        card_code.line.width = Pt(1.2)

        tf_code = card_code.text_frame
        tf_code.word_wrap = True
        tf_code.margin_left = Inches(0.25)
        tf_code.margin_top = Inches(0.2)
        p_ct = tf_code.paragraphs[0]
        p_ct.text = "💻 ĐOẠN MÃ NGUỒN THEN CHỐT (C++):"
        p_ct.font.name = "Segoe UI"
        p_ct.font.size = Pt(12)
        p_ct.font.bold = True
        p_ct.font.color.rgb = COLOR_NAVY
        p_ct.space_after = Pt(6)

        p_c = tf_code.add_paragraph()
        p_c.text = code_snippet
        p_c.font.name = "Consolas"
        p_c.font.size = Pt(9.5)
        p_c.font.color.rgb = RGBColor(17, 34, 68)

    # -------------------------------------------------------------
    # SLIDE 1: GIỚI THIỆU ĐỀ TÀI
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_BG_DARK)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(1.5), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_GOLD
    bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.5), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "TIỂU LUẬN MÔN HỌC CẤU TRÚC DỮ LIỆU & GIẢI THUẬT"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_GOLD
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "HỆ THỐNG QUẢN LÝ ĐẶT VÉ RẠP CHIẾU PHIM"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Ứng dụng Danh sách liên kết đơn & Mảng 2 chiều kết hợp Quản lý CSDL bền vững"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(203, 213, 225)

    info_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.3))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = COLOR_NAVY
    info_card.line.color.rgb = COLOR_BLUE_ACC
    tf_info = info_card.text_frame
    tf_info.margin_left = Inches(0.4)
    tf_info.margin_top = Inches(0.3)
    pi1 = tf_info.paragraphs[0]
    pi1.text = "THÔNG TIN THỰC HIỆN ĐỀ TÀI"
    pi1.font.name = "Segoe UI"
    pi1.font.size = Pt(13)
    pi1.font.bold = True
    pi1.font.color.rgb = COLOR_GOLD
    pi1.space_after = Pt(8)

    for item in [
        "• Giảng viên hướng dẫn : [Điền tên Thầy / Cô]",
        "• Nhóm sinh viên thực hiện : Nhóm 3 thành viên",
        "• Ngôn ngữ & Nền tảng : C++ (Standard 17) | Quản lý File CSDL bền vững (cinema_db.txt)"
    ]:
        p = tf_info.add_paragraph()
        p.text = item
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 2: PHÂN TÍCH YÊU CẦU & GIẢI PHÁP
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_LIGHT_BG)
    add_header(s2, "1. Tổng quan", "Phân tích Yêu cầu Bài toán và Giải pháp Kỹ thuật")

    # 2 Card
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.65), Inches(5.5))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_CARD_BG
    c1.line.color.rgb = COLOR_BLUE_ACC
    tf_c1 = c1.text_frame
    tf_c1.margin_left = Inches(0.3)
    tf_c1.margin_top = Inches(0.25)
    p_c1 = tf_c1.paragraphs[0]
    p_c1.text = "📋 Yêu cầu Nghiệp vụ Thực tế"
    p_c1.font.name = "Segoe UI"
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_NAVY
    p_c1.space_after = Pt(10)
    for req in [
        "Quản lý danh mục phim linh hoạt: Thêm phim mới, hiển thị dạng bảng, tìm kiếm gần đúng, xóa an toàn, cập nhật và sắp xếp.",
        "Mô phỏng phòng chiếu thực tế: Sơ đồ 30 ghế ngồi (5 hàng A-E, 6 cột 1-6), nhận diện rõ ghế trống và ghế đã bán.",
        "Nghiệp vụ phòng vé chuẩn xác: Khách đặt vé tự động kiểm tra trùng ghế, cấp mã vé tự tăng, hủy vé hoàn ghế tức thì.",
        "Lưu trữ dữ liệu bền vững: Tự động ghi đè file text cinema_db.txt, đảm bảo dữ liệu không bị mất khi tắt app."
    ]:
        p = tf_c1.add_paragraph()
        p.text = "• " + req
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.5), Inches(5.65), Inches(5.5))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_CARD_BG
    c2.line.color.rgb = COLOR_GOLD
    tf_c2 = c2.text_frame
    tf_c2.margin_left = Inches(0.3)
    tf_c2.margin_top = Inches(0.25)
    p_c2 = tf_c2.paragraphs[0]
    p_c2.text = "🎯 Giải pháp Kỹ thuật & Kiến trúc"
    p_c2.font.name = "Segoe UI"
    p_c2.font.size = Pt(14)
    p_c2.font.bold = True
    p_c2.font.color.rgb = COLOR_GOLD
    p_c2.space_after = Pt(10)
    for sol in [
        "Danh sách liên kết đơn (Singly Linked List): Lưu trữ các bộ phim trên RAM, hỗ trợ thêm xóa động mà không bị giới hạn bộ nhớ tĩnh.",
        "Mảng 2 chiều 5x6 lồng Struct: Mỗi phim sở hữu ma trận ghe[5][6] độc lập, lưu trạng thái daDat và thông tin vé MaVe.",
        "Bộ hàm Atomic & Validation: Chống trôi lệnh cin và chống crash app khi người dùng gõ sai kiểu dữ liệu.",
        "Đồng bộ hóa File an toàn: Cơ chế đọc nạp RAM khi khởi động và ghi đè toàn bộ file text sau mỗi thay đổi."
    ]:
        p = tf_c2.add_paragraph()
        p.text = "• " + sol
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 3: THIẾT KẾ CẤU TRÚC DỮ LIỆU & MÔ HÌNH
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_LIGHT_BG)
    add_header(s3, "2. Thiết kế", "Thiết kế Cấu trúc Dữ liệu và Mô hình Chương trình")

    # 3 Cột: Struct Vé/Ghế, Struct Phim/DSLK, Mô hình Ánh xạ
    w3 = Inches(3.65)
    c3_1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), w3, Inches(5.5))
    c3_1.fill.solid()
    c3_1.fill.fore_color.rgb = COLOR_CARD_BG
    c3_1.line.color.rgb = COLOR_BLUE_ACC
    tf3_1 = c3_1.text_frame
    tf3_1.margin_left = Inches(0.2)
    tf3_1.margin_top = Inches(0.2)
    p = tf3_1.paragraphs[0]
    p.text = "🎟️ Struct MaVe & ThongTinGhe"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(6)
    p = tf3_1.add_paragraph()
    p.text = "struct MaVe {\n  int soVe;      // >= 1001\n  string tenKhach;\n  string sdt;\n};\n\nstruct ThongTinGhe {\n  bool daDat;    // true/false\n  MaVe ve;\n};"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(17, 34, 68)
    p.space_after = Pt(8)
    p = tf3_1.add_paragraph()
    p.text = "• daDat = false: Ghế trống, hiển thị [01]..[30].\n• daDat = true: Ghế đã mua, hiển thị ký hiệu [ X]."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MAIN

    c3_2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), w3, Inches(5.5))
    c3_2.fill.solid()
    c3_2.fill.fore_color.rgb = COLOR_CARD_BG
    c3_2.line.color.rgb = COLOR_BLUE_ACC
    tf3_2 = c3_2.text_frame
    tf3_2.margin_left = Inches(0.2)
    tf3_2.margin_top = Inches(0.2)
    p = tf3_2.paragraphs[0]
    p.text = "🎬 Struct Phim & NodePhim"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(6)
    p = tf3_2.add_paragraph()
    p.text = "struct Phim {\n  string ma, ten, theLoai;\n  int thoiLuong;\n  double giaVe;\n  ThongTinGhe ghe[5][6];\n};\n\nstruct NodePhim {\n  Phim data;\n  NodePhim* next;\n};"
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(17, 34, 68)
    p.space_after = Pt(8)
    p = tf3_2.add_paragraph()
    p.text = "• Con trỏ đầu: NodePhim* headPhim\n• Quản lý động trên bộ nhớ Heap.\n• Node cuối trỏ vào nullptr an toàn."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_MAIN

    c3_3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.5), w3, Inches(5.5))
    c3_3.fill.solid()
    c3_3.fill.fore_color.rgb = COLOR_CARD_BG
    c3_3.line.color.rgb = COLOR_GOLD
    tf3_3 = c3_3.text_frame
    tf3_3.margin_left = Inches(0.2)
    tf3_3.margin_top = Inches(0.2)
    p = tf3_3.paragraphs[0]
    p.text = "🪑 Quy ước Ánh xạ 30 Ghế"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(6)
    p = tf3_3.add_paragraph()
    p.text = "• Hàng r = (soGhe - 1) / 6\n  (r = 0..4 tương ứng Hàng A..E)\n\n• Cột c = (soGhe - 1) % 6\n  (c = 0..5 tương ứng Cột 1..6)\n\n• Tính lại số: soGhe = r * 6 + c + 1\n\n• In đủ 2 chữ số [%02d] giúp các ô ghế luôn đều tắp 4 ký tự, ma trận ghế thẳng hàng tuyệt đối."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_MAIN

    # -------------------------------------------------------------
    # SLIDE 4: QUY CHUẨN ĐỊNH DẠNG CƠ SỞ DỮ LIỆU FILE (cinema_db.txt)
    # -------------------------------------------------------------
    s_db = prs.slides.add_slide(blank_layout)
    set_slide_background(s_db, COLOR_LIGHT_BG)
    add_header(s_db, "3. Cơ sở dữ liệu", "Quy chuẩn Định dạng Cơ sở Dữ liệu File (cinema_db.txt)")

    c_db1 = s_db.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.65), Inches(5.5))
    c_db1.fill.solid()
    c_db1.fill.fore_color.rgb = COLOR_CARD_BG
    c_db1.line.color.rgb = COLOR_BLUE_ACC
    tf_db1 = c_db1.text_frame
    tf_db1.margin_left = Inches(0.3)
    tf_db1.margin_top = Inches(0.25)
    p = tf_db1.paragraphs[0]
    p.text = "📄 Cấu trúc Định dạng Tệp CSDL (Protocol)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    for item in [
        "Dòng Header mỗi bộ phim (bắt đầu bằng dấu #): #MaPhim|TenPhim|TheLoai|ThoiLuong|GiaVe (VD: #P01|Avatar: The Way of Water|Khoa Hoc Vien Tuong|192|95000).",
        "30 dòng trạng thái ghế liên tiếp phía dưới (đánh số 2 chữ số 01 -> 30):",
        "• Ghế còn trống: Định dạng SoGhe|O (Ký hiệu 'O' = Open / Trống. VD: 01|O, 02|O...).",
        "• Ghế đã đặt: Định dạng SoGhe|X|MaVe|TenKhach|SDT (Ký hiệu 'X' = Đã bán. VD: 03|X|1001|Nguyen Van An|0912345671).",
        "Ký tự phân cách dấu gạch đứng '|' giúp việc bóc tách chuỗi bằng stringstream diễn ra cực kỳ nhanh và chính xác."
    ]:
        p = tf_db1.add_paragraph()
        p.text = "• " + item
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    c_db2 = s_db.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.5), Inches(5.65), Inches(5.5))
    c_db2.fill.solid()
    c_db2.fill.fore_color.rgb = COLOR_CARD_BG
    c_db2.line.color.rgb = COLOR_GOLD
    tf_db2 = c_db2.text_frame
    tf_db2.margin_left = Inches(0.3)
    tf_db2.margin_top = Inches(0.25)
    p = tf_db2.paragraphs[0]
    p.text = "🔄 Cơ chế Đồng bộ 2 Chiều (RAM ⮂ File)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(10)
    for item in [
        "Chiều Đọc (docDanhSachPhim): Khi khởi động, đọc tuần tự file text. Dòng '#' tạo node Phim nối vào DSLK; 30 dòng tiếp theo nạp vào mảng ghe[5][6].",
        "Tự động duy trì mã vé: veKeTiep = max(veKeTiep, soVe + 1) để đảm bảo không bao giờ trùng mã vé sau khi bật lại phần mềm.",
        "Chiều Ghi (ghiToanBoFile & taoGheDong): Mở file chế độ ghi đè (ofstream), duyệt DSLK ghi dòng '#' và gọi taoGheDong ghi 30 dòng trạng thái ghế.",
        "Tính toàn vẹn (Persistence): Bất kỳ thao tác thêm/xóa/sửa/đặt vé/hủy vé nào đều tự động đồng bộ ngay lập tức xuống đĩa."
    ]:
        p = tf_db2.add_paragraph()
        p.text = "• " + item
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 5: XÁC ĐỊNH CÁC HÀM TIỆN ÍCH DÙNG CHUNG
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, COLOR_LIGHT_BG)
    add_header(s4, "4. Kiến trúc hàm", "Xác định các Hàm Tiện ích Dùng chung (Atomic Utilities)")

    c4_1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.65), Inches(5.5))
    c4_1.fill.solid()
    c4_1.fill.fore_color.rgb = COLOR_CARD_BG
    c4_1.line.color.rgb = COLOR_BLUE_ACC
    tf4_1 = c4_1.text_frame
    tf4_1.margin_left = Inches(0.3)
    tf4_1.margin_top = Inches(0.25)
    p = tf4_1.paragraphs[0]
    p.text = "🛡️ Bộ hàm Nhập liệu An toàn (Input Validation)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    for u in [
        "chuyenChuThuong(string s): Chuyển toàn bộ chuỗi ký tự về chữ thường (lowercase) phục vụ so khớp không phân biệt hoa thường.",
        "nhapChuoi(string thongBao): Đọc chuỗi bằng getline(), bắt buộc không để trống chuỗi, giải quyết triệt để vấn đề trôi lệnh cin.",
        "nhapSoNguyen(thongBao, min, max): Dùng stringstream ép kiểu an toàn. Khi người dùng lỡ tay gõ chữ cái vào ô số sẽ báo lỗi và cho nhập lại chứ không bị crash app.",
        "nhapSoThuc(thongBao, min, max): Kiểm tra đơn giá vé nằm đúng khoảng quy định từ 10.000 đến 1.000.000 VND."
    ]:
        p = tf4_1.add_paragraph()
        p.text = "• " + u
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    c4_2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.5), Inches(5.65), Inches(5.5))
    c4_2.fill.solid()
    c4_2.fill.fore_color.rgb = COLOR_CARD_BG
    c4_2.line.color.rgb = COLOR_GOLD
    tf4_2 = c4_2.text_frame
    tf4_2.margin_left = Inches(0.3)
    tf4_2.margin_top = Inches(0.25)
    p = tf4_2.paragraphs[0]
    p.text = "💾 Bộ hàm Tìm kiếm Mã & Đồng bộ CSDL"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(10)
    for u in [
        "timPhimTheoMa(head, ma): Hàm tiện ích cực kỳ quan trọng, duyệt DSLK và so sánh mã chữ thường. Được tái sử dụng trong Chức năng 1 (check trùng), CN 5 (cập nhật), CN 7 (xem sơ đồ), CN 8 (đặt vé).",
        "ghiToanBoFile(FILE_DB, head): Mở file cinema_db.txt ở chế độ ghi đè. Duyệt qua từng node ghi dòng header (#Ma|Ten...) và 30 dòng trạng thái ghế của phim đó.",
        "kiemTraTrungMa(head, ma): Gọi timPhimTheoMa, trả về true nếu mã đã tồn tại trên hệ thống để chặn nhập trùng.",
        "giaiPhong(head): Duyệt và delete toàn bộ danh sách liên kết khi kết thúc app, không rò rỉ bộ nhớ Heap."
    ]:
        p = tf4_2.add_paragraph()
        p.text = "• " + u
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 5: CHỨC NĂNG 1 - NHẬP DANH SÁCH PHIM MỚI
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, COLOR_LIGHT_BG)
    add_function_slide(
        s5, "4. Chi tiết chức năng", "Chức năng 1: Nhập Danh sách Phim Mới & Thêm Phim (nhapDanhSachPhim, themPhim)",
        [
            "Bước 1 (Kiểm tra trùng mã): Nhập mã phim qua nhapChuoi(), gọi kiemTraTrungMa(). Nếu mã đã có trong CSDL (so sánh chữ thường) ➔ Bắt nhập lại mã khác.",
            "Bước 2 (Nhập chi tiết): Nhập Tên, Thể loại, Thời lượng (15-360 ph) và Giá vé (10k-1tr) qua các hàm validation an toàn.",
            "Bước 3 (Khởi tạo ghế): Dùng 2 vòng lặp 5x6 đặt toàn bộ 30 ghế về trống: daDat = false và ve = {0, '', ''}.",
            "Bước 4 (Thêm node & Lưu file): Cấp phát new NodePhim, nối vào cuối DSLK đơn và gọi ghiToanBoFile() lưu xuống đĩa."
        ],
        "Phim nhapMotPhim(NodePhim* head) {\n"
        "    Phim p{};\n"
        "    while (true) {\n"
        "        p.ma = nhapChuoi(\"Nhap ma phim: \");\n"
        "        if (kiemTraTrungMa(head, p.ma))\n"
        "            cout << \"[!] Ma phim da ton tai!\\n\";\n"
        "        else break;\n"
        "    }\n"
        "    p.ten       = nhapChuoi(\"Nhap ten phim: \");\n"
        "    p.theLoai   = nhapChuoi(\"Nhap the loai: \");\n"
        "    p.thoiLuong = nhapSoNguyen(\"Thoi luong (15-360): \", 15, 360);\n"
        "    p.giaVe     = nhapSoThuc(\"Gia ve: \", 10000, 1000000);\n"
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

    # -------------------------------------------------------------
    # SLIDE 6: CHỨC NĂNG 2 - XEM DANH SÁCH PHIM BẢNG 104 CỘT
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, COLOR_LIGHT_BG)
    add_function_slide(
        s6, "4. Chi tiết chức năng", "Chức năng 2: Hiển thị Danh sách Phim dạng Bảng (xemDanhSachPhim, inDongPhim)",
        [
            "Bước 1 (Kiểm tra danh sách rỗng): Nếu headPhim == nullptr ➔ Thông báo danh sách trống và quay về menu.",
            "Bước 2 (In tiêu đề bảng): Gọi inTieuDeBang(), định dạng độ rộng 5 cột cố định và kẻ đường viền 104 dấu '-'.",
            "Bước 3 (Chuẩn hóa độ rộng cột): Mã (8), Tên phim (40), Thể loại (24), Thời lượng (14), Giá vé (14). Cột Tên 40 ký tự giúp tên phim dài không bị méo bảng.",
            "Bước 4 (Duyệt DSLK & Đóng bảng): Dùng con trỏ tạm p duyệt từng node gọi inDongPhim(p->data), kết thúc bằng đường kẻ kép 104 dấu '='."
        ],
        "void inTieuDeBang() {\n"
        "    printf(\"\\n%-8s %-40s %-24s %-14s %-14s\\n\",\n"
        "           \"Ma\", \"Ten Phim\", \"The Loai\", \"Thoi Luong\", \"Gia Ve\");\n"
        "    printf(\"%s\\n\", string(104, '-').c_str());\n"
        "}\n\n"
        "void inDongPhim(const Phim& p) {\n"
        "    string thoiLuongStr = to_string(p.thoiLuong) + \" phut\";\n"
        "    string giaVeStr     = to_string((long long)p.giaVe) + \" VND\";\n"
        "    printf(\"%-8s %-40s %-24s %-14s %-14s\\n\",\n"
        "           p.ma.c_str(), p.ten.c_str(), p.theLoai.c_str(),\n"
        "           thoiLuongStr.c_str(), giaVeStr.c_str());\n"
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

    # -------------------------------------------------------------
    # SLIDE 7: CHỨC NĂNG 3 - TÌM KIẾM PHIM ĐA TIÊU CHÍ
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, COLOR_LIGHT_BG)
    add_function_slide(
        s7, "4. Chi tiết chức năng", "Chức năng 3: Tìm kiếm Phim Đa Tiêu chí (hienMenuTimKiem, timTheoMa, timTheoTen, timTheoGia)",
        [
            "Bước 1 (Chọn tiêu chí): Menu cho phép chọn: 1. Tìm theo mã, 2. Tìm theo tên phim, 3. Lọc theo khoảng giá vé [giaMin, giaMax], 0. Quay lại.",
            "Bước 2 (So khớp chuỗi con): Áp dụng chuyenChuThuong() kết hợp hàm string::find() để tìm gần đúng, không phân biệt chữ hoa chữ thường.",
            "Bước 3 (Duyệt DSLK & Xuất bảng): Quét qua từng node, nếu khớp bất kỳ tiêu chí nào thì in ra dạng bảng qua inDongPhim() và tăng biến đếm dem++.",
            "Bước 4 (Tổng kết): Nếu dem == 0 báo không tìm thấy; ngược lại in tổng số phim tìm được."
        ],
        "bool timTheoTen(NodePhim* p, string tenCanTim) {\n"
        "    if (tenCanTim.empty()) return false;\n"
        "    string tenPhim = chuyenChuThuong(p->data.ten);\n"
        "    string tenTim  = chuyenChuThuong(tenCanTim);\n"
        "    return tenPhim.find(tenTim) != string::npos;\n"
        "}\n\n"
        "bool timTheoGia(NodePhim* p, double giaMin, double giaMax) {\n"
        "    return (p->data.giaVe >= giaMin && p->data.giaVe <= giaMax);\n"
        "}\n\n"
        "void inDanhSachKetQua(NodePhim* head, string ma, string ten, double gMin, double gMax) {\n"
        "    int dem = 0;\n"
        "    NodePhim* p = head;\n"
        "    while (p != nullptr) {\n"
        "        bool khop = timTheoMa(p, ma) || timTheoTen(p, ten) || timTheoGia(p, gMin, gMax);\n"
        "        if (khop) {\n"
        "            if (dem == 0) inTieuDeBang();\n"
        "            inDongPhim(p->data);\n"
        "            dem++;\n"
        "        }\n"
        "        p = p->next;\n"
        "    }\n"
        "    if (dem == 0) cout << \"[!] Khong tim thay phim nao!\\n\";\n"
        "    else cout << \"=> Tim thay tong cong: \" << dem << \" phim.\\n\";\n"
        "}"
    )

    # -------------------------------------------------------------
    # SLIDE 8: CHỨC NĂNG 4 - XÓA PHIM KHỎI HỆ THỐNG
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, COLOR_LIGHT_BG)
    add_function_slide(
        s8, "4. Chi tiết chức năng", "Chức năng 4: Xóa Phim khỏi Hệ thống (hienMenuXoaPhim, khopPhim, xoaPhim)",
        [
            "Bước 1 (Chọn phim & Tra cứu): Người dùng chọn xóa theo mã hoặc tên phim. Duyệt danh sách tìm kiếm phim khớp điều kiện.",
            "Bước 2 (Xác nhận an toàn): Nếu tìm thấy, in thông tin phim ra màn hình và hỏi xác nhận: 'Ban co CHAC CHAN muon xoa phim nay? (y/n)'. Nếu chọn 'n' ➔ Hủy thao tác.",
            "Bước 3 (Tách node khỏi DSLK): Xử lý 2 ca biên:\n• Ca 1: Node cần xóa ở đầu danh sách ➔ dời head = head->next.\n• Ca 2: Node ở giữa hoặc cuối ➔ ngắt liên kết p->next = del->next.",
            "Bước 4 (Thu hồi Heap & Lưu file): Gọi delete del giải phóng bộ nhớ RAM, sau đó gọi ghiToanBoFile() lưu lại file database."
        ],
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
        "}\n\n"
        "// Sau khi tách node: \n"
        "// delete del; \n"
        "// ghiToanBoFile(FILE_DB, headPhim);"
    )

    # -------------------------------------------------------------
    # SLIDE 9: CHỨC NĂNG 5 - CẬP NHẬT THÔNG TIN PHIM
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, COLOR_LIGHT_BG)
    add_function_slide(
        s9, "4. Chi tiết chức năng", "Chức năng 5: Cập nhật Thông tin Phim (capNhatThongTinPhim)",
        [
            "Bước 1 (Nhập mã phim): Nhập mã phim cần sửa (nhập '0' để hủy). Gọi timPhimTheoMa() để tìm. Nếu không thấy ➔ Báo lỗi và dừng.",
            "Bước 2 (Hiển thị thông tin cũ): In chi tiết Tên phim, Thể loại, Thời lượng và Giá vé hiện tại để người dùng kiểm tra.",
            "Bước 3 (Hỏi sửa từng trường): Lần lượt hỏi xác nhận (y/n):\n• Đổi tên mới? ➔ nhapChuoi()\n• Đổi thể loại mới? ➔ nhapChuoi()\n• Đổi thời lượng? ➔ nhapSoNguyen(15, 360)\n• Đổi giá vé? ➔ nhapSoThuc(10k, 1tr).",
            "Bước 4 (Đồng bộ file): Bật cờ coThayDoi = true. Nếu có bất kỳ thông tin nào bị sửa thì gọi ghiToanBoFile() lưu lại CSDL."
        ],
        "void capNhatThongTinPhim(NodePhim* headPhim) {\n"
        "    string ma = nhapChuoi(\"Nhap ma phim can cap nhat: \");\n"
        "    NodePhim* p = timPhimTheoMa(headPhim, ma);\n"
        "    if (p == nullptr) { cout << \"[!] Khong tim thay phim!\\n\"; return; }\n\n"
        "    bool coThayDoi = false;\n"
        "    if (nhapChuoi(\"-> Doi ten phim? (y/n): \") == \"y\") {\n"
        "        p->data.ten = nhapChuoi(\"   Nhap ten phim moi: \");\n"
        "        coThayDoi = true;\n"
        "    }\n"
        "    if (nhapChuoi(\"-> Doi thoi luong? (y/n): \") == \"y\") {\n"
        "        p->data.thoiLuong = nhapSoNguyen(\"   Thoi luong (15-360): \", 15, 360);\n"
        "        coThayDoi = true;\n"
        "    }\n"
        "    if (nhapChuoi(\"-> Doi gia ve? (y/n): \") == \"y\") {\n"
        "        p->data.giaVe = nhapSoThuc(\"   Gia ve moi: \", 10000, 1000000);\n"
        "        coThayDoi = true;\n"
        "    }\n"
        "    if (coThayDoi) {\n"
        "        ghiToanBoFile(FILE_DB, headPhim);\n"
        "        cout << \"=> [Thanh cong] Cap nhat va DONG BO CSDL thanh cong!\\n\";\n"
        "    }\n"
        "}"
    )

    # -------------------------------------------------------------
    # SLIDE 10: CHỨC NĂNG 6 - SẮP XẾP DANH SÁCH PHIM
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, COLOR_LIGHT_BG)
    add_function_slide(
        s10, "4. Chi tiết chức năng", "Chức năng 6: Sắp xếp Danh sách Phim (hienThiMenuSapXep, sapXepDanhSachPhim)",
        [
            "Bước 1 (Chọn tiêu chí): Menu 4 tiêu chí: 1. Giá vé tăng dần, 2. Giá vé giảm dần, 3. Thời lượng tăng dần, 4. Thời lượng giảm dần.",
            "Bước 2 (Giải thuật Bubble Sort): Dùng 2 con trỏ kề nhau ptr1 và ptr2 = ptr1->next duyệt danh sách liên kết.",
            "Bước 3 (Tối ưu với con trỏ lptr): Con trỏ lptr làm biên giới hạn cuối, giúp thu hẹp phạm vi quét qua mỗi vòng lặp, không lặp lại các node đã đúng thứ tự.",
            "Bước 4 (Tráo đổi & In kết quả): Hoán đổi trực tiếp dữ liệu Phim temp = ptr1->data. Sắp xếp xong gọi ghiToanBoFile() và gọi xemDanhSachPhim() xuất bảng kết quả ngay."
        ],
        "void sapXepDanhSachPhim(NodePhim*& head, bool giamDan, bool laGiaVe) {\n"
        "    if (head == nullptr || head->next == nullptr) return;\n"
        "    bool swapped;\n"
        "    NodePhim* ptr1;\n"
        "    NodePhim* lptr = nullptr; // Con trỏ biên thu hẹp phạm vi quét\n\n"
        "    do {\n"
        "        swapped = false;\n"
        "        ptr1 = head;\n"
        "        while (ptr1->next != lptr) {\n"
        "            NodePhim* ptr2 = ptr1->next;\n"
        "            double val1 = laGiaVe ? ptr1->data.giaVe : ptr1->data.thoiLuong;\n"
        "            double val2 = laGiaVe ? ptr2->data.giaVe : ptr2->data.thoiLuong;\n"
        "            bool dieuKienDoi = giamDan ? (val1 < val2) : (val1 > val2);\n"
        "            if (dieuKienDoi) {\n"
        "                Phim temp = ptr1->data; // Hoán đổi cấu trúc dữ liệu\n"
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

    # -------------------------------------------------------------
    # SLIDE 11: CHỨC NĂNG 7 - XEM SƠ ĐỒ GHẾ PHÒNG CHIẾU
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, COLOR_LIGHT_BG)
    add_function_slide(
        s11, "4. Chi tiết chức năng", "Chức năng 7: Xem Sơ đồ Ghế Phòng Chiếu (xemSoDoGhe)",
        [
            "Bước 1 (Nhập mã phim): Nhập mã phim muốn xem sơ đồ ghế ➔ Gọi timPhimTheoMa() để lấy con trỏ NodePhim* p.",
            "Bước 2 (Vẽ màn hình chiếu): In khung viền tiêu đề và biểu tượng màn hình chiếu '[ MAN HINH CHIEU (SCREEN) ]' ở phía trên.",
            "Bước 3 (Duyệt ma trận 5x6 ghế):\n• Hàng r in tên Hang A, Hang B... Hang E.\n• Cột c tính số ghế: soGhe = r * 6 + c + 1.\n• Nếu daDat == true ➔ in ký hiệu [ X].\n• Nếu daDat == false ➔ in số ghế [%02d] (đều tắp 4 ký tự).",
            "Bước 4 (Chú thích & Giá vé): In chú thích ký hiệu và thông tin đơn giá vé của bộ phim."
        ],
        "void xemSoDoGhe(NodePhim* p) {\n"
        "    if (p == nullptr) return;\n"
        "    cout << \"\\n  SO DO PHONG CHIEU: \" << p->data.ten << \" (\" << p->data.ma << \")\\n\";\n"
        "    cout << \"                    [ MAN HINH CHIEU (SCREEN) ]                   \\n\";\n"
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
        "    cout << \"Chu thich: [So]: Ghe con trong  |  [ X]: Ghe da dat\\n\";\n"
        "    cout << \"Gia ve   : \" << (long long)p->data.giaVe << \" VND / ghe\\n\";\n"
        "}"
    )

    # -------------------------------------------------------------
    # SLIDE 12: CHỨC NĂNG 8 - ĐẶT VÉ VÀ HỦY VÉ XEM PHIM
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, COLOR_LIGHT_BG)
    add_function_slide(
        s12, "4. Chi tiết chức năng", "Chức năng 8: Nghiệp vụ Phòng Vé (hienMenuDatVeHuyVe, datVe, huyVe)",
        [
            "A. QUY TRÌNH ĐẶT VÉ (datVe):\n"
            "• Bước 1: Nhập mã phim ➔ tự động gọi xemSoDoGhe(p) vẽ 30 ghế.\n"
            "• Bước 2: Chọn số ghế (1-30) ➔ quy đổi r, c ➔ kiểm tra ghe[r][c].daDat. Nếu đã đặt bắt buộc nhập lại ghế khác.\n"
            "• Bước 3: Nhập Họ tên khách & SĐT qua nhapChuoi() chống trôi lệnh.\n"
            "• Bước 4: Cấp mã vé tự tăng veKeTiep++, lưu vào ô ghế, gọi ghiToanBoFile() lưu đĩa và in hóa đơn thanh toán.",
            "B. QUY TRÌNH HỦY VÉ (huyVe):\n"
            "• Bước 1: Nhập mã vé cần hủy (nhập 0 để thoát an toàn).\n"
            "• Bước 2: Duyệt 2 vòng lặp (toàn bộ phim & 30 ghế) tìm vé khớp mã.\n"
            "• Bước 3: Hỏi xác nhận an toàn 'Chac chan muon huy? (y/n)'.\n"
            "• Bước 4: Trả daDat = false, reset vé, gọi ghiToanBoFile() lưu lại CSDL."
        ],
        "void datVe(NodePhim* headPhim, int& veKeTiep) {\n"
        "    string ma = nhapChuoi(\"Nhap ma phim dat ve: \");\n"
        "    NodePhim* p = timPhimTheoMa(headPhim, ma);\n"
        "    if (!p) { cout << \"[!] Khong tim thay phim!\\n\"; return; }\n"
        "    xemSoDoGhe(p);\n"
        "    int soGhe, r, c;\n"
        "    while (true) {\n"
        "        soGhe = nhapSoNguyen(\"Nhap so ghe (1-30): \", 1, TONG_GHE);\n"
        "        r = (soGhe - 1) / SO_COT; c = (soGhe - 1) % SO_COT;\n"
        "        if (p->data.ghe[r][c].daDat) cout << \"[!] Ghe DA CO NGUOI DAT!\\n\";\n"
        "        else break;\n"
        "    }\n"
        "    string ten = nhapChuoi(\"Ho ten khach: \");\n"
        "    string sdt = nhapChuoi(\"So dien thoai: \");\n"
        "    int maVeMoi = veKeTiep++;\n"
        "    p->data.ghe[r][c].daDat = true;\n"
        "    p->data.ghe[r][c].ve = { maVeMoi, ten, sdt };\n"
        "    ghiToanBoFile(FILE_DB, headPhim);\n"
        "    cout << \"=> Da dat ve #\" << maVeMoi << \" thanh cong!\\n\";\n"
        "}"
    )

    # -------------------------------------------------------------
    # SLIDE 13: NHẬN XÉT ĐÁNH GIÁ & HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, COLOR_LIGHT_BG)
    add_header(s13, "5. Tổng kết", "Nhận xét, Đánh giá Kết quả Đạt được và Hướng Phát triển")

    c13_1 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.65), Inches(5.5))
    c13_1.fill.solid()
    c13_1.fill.fore_color.rgb = COLOR_CARD_BG
    c13_1.line.color.rgb = COLOR_BLUE_ACC
    tf13_1 = c13_1.text_frame
    tf13_1.margin_left = Inches(0.3)
    tf13_1.margin_top = Inches(0.25)
    p = tf13_1.paragraphs[0]
    p.text = "🌟 Ưu điểm Nổi bật Đạt được"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    for adv in [
        "Mô hình hóa chuẩn xác: Kết hợp nhuần nhuyễn Danh sách liên kết đơn (lưu phim) và Mảng 2 chiều 5x6 (lưu ghế) giải quyết trọn vẹn bài toán thực tế.",
        "Dữ liệu bền vững 100%: Tự động đồng bộ hóa xuống file text cinema_db.txt, đảm bảo dữ liệu không bị mất mát khi tắt ứng dụng.",
        "Trải nghiệm hiển thị cao: Chuẩn hóa bảng 104 cột chống méo bảng, sơ đồ ghế trực quan, dễ quan sát ghế trống.",
        "Khả năng chống lỗi vượt trội: Bộ hàm Validation chống trôi lệnh cin, chống crash app khi người dùng nhập sai kiểu dữ liệu.",
        "Quản lý bộ nhớ sạch sẽ: Hàm giaiPhong() thu hồi toàn bộ vùng nhớ Heap khi thoát, ngăn ngừa Memory Leak."
    ]:
        p = tf13_1.add_paragraph()
        p.text = "• " + adv
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    c13_2 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.5), Inches(5.65), Inches(5.5))
    c13_2.fill.solid()
    c13_2.fill.fore_color.rgb = COLOR_CARD_BG
    c13_2.line.color.rgb = COLOR_GOLD
    tf13_2 = c13_2.text_frame
    tf13_2.margin_left = Inches(0.3)
    tf13_2.margin_top = Inches(0.25)
    p = tf13_2.paragraphs[0]
    p.text = "🚀 Hạn chế & Hướng Phát triển Tương lai"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(10)
    for dev in [
        "Hạn chế hiện tại: Giao diện Console thuần văn bản; thao tác duyệt tuần tự O(N) khi rạp có quy mô hàng vạn phim.",
        "Giao diện đồ họa (GUI): Nâng cấp phần mềm bằng thư viện Qt C++ để khách hàng click chuột trực quan lên từng ô ghế.",
        "Cấu trúc Ngăn xếp (Stack): Ứng dụng Stack để phát triển tính năng Hoàn tác (Undo), giúp phục hồi lại phim nếu lỡ tay xóa nhầm.",
        "Cấu trúc Hàng đợi (Queue): Ứng dụng Queue để quản lý hàng chờ đặt vé trực tuyến vào các khung giờ phim bom tấn cao điểm.",
        "Cây nhị phân tìm kiếm (BST): Tối ưu hóa tốc độ tra cứu phim từ O(N) xuống O(log N) khi mở rộng quy mô chuỗi rạp."
    ]:
        p = tf13_2.add_paragraph()
        p.text = "• " + dev
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # Lưu file
    out_path = "/mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Thuyet_Trinh_MovieBooking.pptx"
    prs.save(out_path)
    print(f"[OK] Xuất thành công file thuyết trình PowerPoint chuẩn 13 slide: {out_path}")

if __name__ == "__main__":
    create_structured_deck()
