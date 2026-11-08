# KỊCH BẢN & DÀN Ý THUYẾT TRÌNH BẢO VỆ TIỂU LUẬN
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ ĐẶT VÉ RẠP CHIẾU PHIM (C++)

File PowerPoint tương ứng: [Bao_Cao_Thuyet_Trinh_MovieBooking.pptx](file:///mnt/c/Users/VuongQuocKhang/movie_booking/Bao_Cao_Thuyet_Trinh_MovieBooking.pptx)

---

### PHÂN CHIA THỜI LƯỢNG & VAI TRÒ 3 THÀNH VIÊN (Khoảng 10 - 15 phút)
* **Thành viên 1 (Slide 1 ➔ 4)**: Giới thiệu, Mục tiêu bài toán thực tế, Thiết kế cấu trúc dữ liệu (DSLK đơn, Mảng 2 chiều) & CSDL file.
* **Thành viên 2 (Slide 5 ➔ 7)**: Bố cục Menu điều phối, Nghiệp vụ Quản lý phim (CRUD, Tìm kiếm gần đúng) & Thuật toán Sắp xếp Bubble Sort.
* **Thành viên 3 (Slide 8 ➔ 12)**: Nghiệp vụ trọng tâm Đặt vé & Hủy vé phòng chiếu, Demo màn hình thực tế, Đánh giá & Trả lời Q&A.

---

### CHI TIẾT NỘI DUNG TỪNG SLIDE & LỜI THOẠI GỢI Ý

#### SLIDE 1: TRANG BÌA
* **Tiêu đề**: BÁO CÁO TIỂU LUẬN MÔN HỌC CẤU TRÚC DỮ LIỆU & GIẢI THUẬT
* **Đề tài**: HỆ THỐNG QUẢN LÝ ĐẶT VÉ RẠP CHIẾU PHIM
* **Lời thoại gợi ý (Thành viên 1)**:
  > *"Kính chào Quý Thầy/Cô và các bạn. Hôm nay nhóm em xin phép được trình bày bài báo cáo tiểu luận môn học Cấu trúc Dữ liệu và Giải thuật với đề tài 'Xây dựng Hệ thống Quản lý Đặt vé Rạp chiếu phim bằng C++'. Nhóm em gồm có 3 thành viên: [Đọc tên 3 bạn]..."*

#### SLIDE 2: BÀI TOÁN THỰC TẾ & MỤC TIÊU GIẢI PHÁP
* **Nội dung**:
  * Thực trạng: Quản lý vé thủ công dễ nhầm ghế, mất thời gian tra cứu, thất thoát dữ liệu khi tắt máy.
  * Mục tiêu: Tin học hóa quy trình, tự động hóa việc hiển thị sơ đồ 30 ghế ngồi, đồng bộ dữ liệu bền vững xuống file `cinema_db.txt`.
* **Lời thoại gợi ý (Thành viên 1)**:
  > *"Xuất phát từ thực tế quản lý tại các phòng chiếu vừa và nhỏ, việc ghi chép thủ công rất dễ trùng ghế của khách. Mục tiêu của nhóm em là xây dựng một ứng dụng console hoàn chỉnh, mô phỏng đúng sơ đồ ghế thực tế và đảm bảo dữ liệu không bao giờ bị mất sau khi tắt máy..."*

#### SLIDE 3: THIẾT KẾ CẤU TRÚC DỮ LIỆU (CORE DATA STRUCTURES)
* **Nội dung**:
  * `struct MaVe`: Lưu mã vé tự tăng từ #1001, Họ tên khách, SĐT.
  * `struct ThongTinGhe`: Cờ `bool daDat` và thông tin `MaVe`.
  * `struct Phim`: Chứa mã, tên, thể loại, thời lượng, giá vé và ma trận 2 chiều `ghe[5][6]` (30 ghế độc lập).
  * `struct NodePhim`: Dùng **Danh sách liên kết đơn (Singly Linked List)** để lưu trữ các bộ phim trên bộ nhớ Heap.
* **Lời thoại gợi ý (Thành viên 1)**:
  > *"Về mặt cấu trúc dữ liệu, thay vì dùng mảng tĩnh bị giới hạn số lượng, nhóm em chọn Danh sách liên kết đơn để có thể thêm, bớt phim linh hoạt trên RAM. Đặc biệt, mỗi bộ phim đều sở hữu riêng một ma trận ghế 5x6 tương ứng với 30 ghế thực tế..."*

#### SLIDE 4: QUY ƯỚC ÁNH XẠ SỐ GHẾ & CƠ SỞ DỮ LIỆU FILE
* **Nội dung**:
  * Công thức ánh xạ: Hàng `r = (soGhe - 1) / 6`, Cột `c = (soGhe - 1) % 6`. Quy đổi ngược: `soGhe = r * 6 + c + 1`.
  * Cấu trúc lưu trữ trong `cinema_db.txt`: Mỗi phim có 1 dòng header `#P01|...` và theo sau là đúng 30 dòng trạng thái ghế `1|TRONG|...` hoặc `3|DAT|1001|...`.
* **Lời thoại gợi ý (Thành viên 1)**:
  > *"Để in sơ đồ ghế thẳng tắp, nhóm dùng định dạng số 2 chữ số `[%02d]`. Mọi thay đổi đều được ghi đè an toàn xuống file cinema_db.txt. Tiếp theo xin mời bạn [Tên TV2] trình bày về các chức năng quản lý phim."*

---

#### SLIDE 5: TỔ CHỨC MENU 8 CHỨC NĂNG & PHÂN CÔNG NHÓM
* **Nội dung**:
  * Hệ thống menu 8 chức năng chuẩn từ 1 đến 8 (Thêm, Xem bảng, Tìm kiếm, Xóa, Cập nhật, Sắp xếp, Sơ đồ ghế, Đặt/Hủy vé).
  * Phân công module rõ ràng giữa các thành viên.
* **Lời thoại gợi ý (Thành viên 2)**:
  > *"Chào Thầy Cô, em xin tiếp tục phần trình bày về các chức năng nghiệp vụ của hệ thống..."*

#### SLIDE 6: NGHIỆP VỤ QUẢN LÝ PHIM (CRUD & TÌM KIẾM GẦN ĐÚNG)
* **Nội dung**:
  * Chức năng 1: Nhập danh sách phim, kiểm tra trùng mã không phân biệt hoa thường (`timPhimTheoMa`), khởi tạo 30 ghế trống.
  * Chức năng 2: Bảng hiển thị 104 cột cố định, không vỡ layout khi tên phim dài 40 ký tự.
  * Chức năng 3: Tìm kiếm chuỗi con không phân biệt hoa thường (`chuyenChuThuong` + `string::find`) hoặc lọc theo khoảng giá `[min, max]`.
  * Chức năng 4: Xóa phim an toàn, xử lý ca xóa ở đầu vs ở giữa/cuối DSLK đơn, giải phóng Heap bằng `delete del`.
* **Lời thoại gợi ý (Thành viên 2)**:
  > *"Ở chức năng tìm kiếm, hệ thống hỗ trợ tìm kiếm gần đúng chuỗi con, người dùng gõ 'mai' hay 'MAI' đều tìm thấy chính xác. Còn chức năng xóa được lập trình cẩn thận để thu hồi bộ nhớ Heap bằng lệnh delete, tránh rò rỉ RAM..."*

#### SLIDE 7: THUẬT TOÁN SẮP XẾP BUBBLE SORT TRÊN DSLK ĐƠN
* **Nội dung**:
  * Áp dụng Bubble Sort trên danh sách liên kết: Dùng 2 con trỏ `ptr1` và `ptr2 = ptr1->next`, thu hẹp phạm vi quét bằng con trỏ biên `lptr`.
  * Kỹ thuật tráo `data` (`Phim temp = ptr1->data; ptr1->data = ptr2->data;`).
  * 4 tiêu chí: Giá vé tăng/giảm, Thời lượng tăng/giảm.
* **Lời thoại gợi ý (Thành viên 2)**:
  > *"Để sắp xếp danh sách liên kết đơn, nhóm em áp dụng thuật toán Bubble Sort với kỹ thuật hoán đổi phần dữ liệu data. Con trỏ biên lptr giúp thuật toán không phải duyệt lại các node đã nằm đúng vị trí ở cuối danh sách. Sau đây xin mời bạn [Tên TV3] trình bày về nghiệp vụ phòng vé."*

---

#### SLIDE 8: TRỌNG TÂM: QUY TRÌNH ĐẶT VÉ XEM PHIM
* **Nội dung**:
  * Bước 1: Chọn mã phim -> Gọi `xemSoDoGhe(p)` vẽ sơ đồ 30 ghế.
  * Bước 2: Chọn ghế (1-30) -> Kiểm tra `ghe[r][c].daDat`. Nếu đã đặt báo lỗi bắt chọn ghế khác.
  * Bước 3: Nhập Tên khách & SĐT bằng bộ hàm an toàn `nhapChuoi()` chống trôi lệnh.
  * Bước 4: Cấp mã số vé tự tăng `veKeTiep++` (từ #1001), cập nhật trạng thái ô ghế.
  * Bước 5: Gọi `ghiToanBoFile()` lưu đĩa tức thì và in hóa đơn biên lai vé thành công.
* **Lời thoại gợi ý (Thành viên 3)**:
  > *"Chào Thầy Cô, đây là chức năng cốt lõi của phần mềm. Khi khách chọn phim, hệ thống lập tức vẽ sơ đồ 30 ghế. Nếu khách chọn phải ghế đã có người đặt, hệ thống sẽ cảnh báo ngay lập tức. Sau khi đặt thành công, mã vé tự tăng được cấp phát và đồng bộ trực tiếp xuống file database..."*

#### SLIDE 9: TRỌNG TÂM: QUY TRÌNH HỦY VÉ & HOÀN TRẢ GHẾ
* **Nội dung**:
  * Nhập mã số vé cần hủy -> Duyệt 2 vòng lặp (toàn bộ phim và 30 ghế mỗi phim).
  * Nếu tìm thấy vé: In thông tin và hỏi xác nhận chắc chắn `(y/n)`.
  * Nếu đồng ý: Trả ghế về trống (`daDat = false`, xóa vé), gọi `ghiToanBoFile()` cập nhật lại CSDL.
* **Lời thoại gợi ý (Thành viên 3)**:
  > *"Trong nghiệp vụ hủy vé, tính an toàn được đặt lên hàng đầu: hệ thống luôn hỏi xác nhận trước khi hủy. Ngay khi xác nhận, ghế đó được giải phóng ngay lập tức thành ghế trống để khách khác có thể đặt mua..."*

#### SLIDE 10: KẾT QUẢ THỰC NGHIỆM & PHÒNG CHỐNG NGOẠI LỆ
* **Nội dung**:
  * Minh họa bảng danh sách 104 cột & sơ đồ phòng chiếu 30 ghế có ký hiệu màn hình `[SCREEN]`.
  * Cơ chế phòng chống lỗi nhập liệu: `cin.fail()`, `stringstream`, `getline` ngăn chặn crash chương trình khi nhập sai kiểu dữ liệu.
* **Lời thoại gợi ý (Thành viên 3)**:
  > *"Một ưu điểm lớn của ứng dụng là tính bền vững: dù người dùng lỡ tay nhập chữ vào ô số nguyên hay khoảng giá, chương trình đều nhắc nhở và bắt nhập lại chứ không bao giờ bị văng app đột ngột..."*

#### SLIDE 11: ĐÁNH GIÁ & HƯỚNG PHÁT TRIỂN TƯƠNG LAI
* **Nội dung**:
  * Đạt được: Quản lý bộ nhớ động tốt, CSDL bền vững, mã nguồn modular dễ bảo trì.
  * Hướng phát triển: Làm GUI bằng Qt C++, dùng Ngăn xếp (Stack) làm tính năng Hoàn tác (Undo), dùng Hàng đợi (Queue) xếp hàng đặt vé giờ cao điểm, dùng Cây nhị phân tìm kiếm (BST) khi dữ liệu lớn.
* **Lời thoại gợi ý (Thành viên 3)**:
  > *"Trong tương lai, nhóm dự kiến sẽ nâng cấp giao diện đồ họa GUI bằng thư viện Qt và tích hợp thêm cấu trúc dữ liệu Stack để làm chức năng Undo hoàn tác khi xóa nhầm..."*

#### SLIDE 12: KẾT THÚC & SẴN SÀNG VẤN ĐÁP (Q&A)
* **Nội dung**: Lời cảm ơn Quý Thầy/Cô & Sẵn sàng trả lời câu hỏi và demo chạy chương trình trực tiếp.
* **Lời thoại gợi ý (Thành viên 3)**:
  > *"Bài thuyết trình của nhóm em đến đây là kết thúc. Chúng em xin chân thành cảm ơn Thầy/Cô và các bạn đã chú ý lắng nghe. Nhóm em rất mong nhận được những góp ý quý báu và sẵn sàng trả lời các câu hỏi vấn đáp!"*
