 ### BẢN QUY CHUẨN CODE NHÓM (DỰ ÁN MOVIE BOOKING)
 
 Mục tiêu: Code đồng bộ 100% phong cách, không lỗi trôi dòng cin, không crash ứng dụng. 
  
  ──────
  ### 1. QUY ƯỚC ĐẶT TÊN (NAMING CONVENTION)

  • Tên hàm & Biến: Dùng chuẩn camelCase (chữ đầu viết thường, các chữ sau viết hoa).
  • Tên Struct: Viết hoa chữ cái đầu PascalCase (vd: Phim, NodePhim, ThongTinGhe).
  • Hằng số: Viết hoa toàn bộ và có gạch dưới UPPER_CASE (vd: SO_HANG, FILE_DB).
  
  ──────
  ### 2. LUÔN VALID DỮ LIỆU:

  │ Lý do: Dùng cin >> xen kẽ getline sẽ gây trôi lệnh, và người dùng lỡ gõ chữ cái vào ô số sẽ làm chương trình bị văng (crash) ngay lập tức.

  Mọi thành viên khi cần nhập liệu từ bàn phím BẮT BUỘC gọi các hàm an toàn đã viết sẵn:

  • Nhập chuỗi (tên, mã, thể loại):
    string ten = nhapChuoi("Nhap ten phim: ");

  • Nhập số nguyên (thời lượng, số ghế):
    int thoiLuong = nhapSoNguyen("Nhap thoi luong (15 - 360): ", 15, 360);

  • Nhập số thực (giá vé):
    double giaVe = nhapSoThuc("Nhap gia ve: ", 10000, 1000000);

  ──────
  ### 3. QUY TẮC ĐỒNG BỘ DATABASE (AUTO-SYNC)

  • Bất kỳ hàm nào làm thay đổi dữ liệu (Thêm phim, Sửa thông tin, Xóa phim, Đặt vé, Hủy vé, Sắp xếp):
  •  Dòng cuối cùng trước khi return nếu có thay đổi dữ liệu thì BẮT BUỘC phải gọi:
    ghiToanBoFile(FILE_DB, headPhim);

  • Tuyệt đối không được để dữ liệu chỉ thay đổi trên RAM mà quên lưu xuống đĩa.
  ──────
  ### 4. QUY TẮC AN TOÀN KHI XÓA & TÌM KIẾM

  • Hỏi xác nhận trước khi xóa: Những thao tác nguy hiểm (Xóa phim, Hủy vé) bắt buộc phải có bước hỏi xác nhận:
    string xn = nhapChuoi("Ban co CHAC CHAN muon xoa? (y/n): ");
    if (xn != "y" && xn != "Y") return;

  ──────
  ### 5. QUY CHUẨN THÔNG BÁO RA MÀN HÌNH (CONSOLE UI)

  Để giao diện phần mềm nhìn chuyên nghiệp, thống nhất các ký hiệu đầu dòng:

  • [!] : Dùng cho cảnh báo, lỗi (vd: [!] Ma phim da ton tai!).
  • =>  : Dùng cho kết quả thành công (vd: => Da them thanh cong phim Avatar!).
  • *   : Dùng cho thông tin chi tiết trên hóa đơn/vé (vd: * Gia ve: 90,000 VND).
  • === : Đường kẻ phân chia tiêu đề chức năng.

