# BÁO CÁO TIỂU LUẬN: HỆ THỐNG QUẢN LÝ ĐẶT VÉ RẠP CHIẾU PHIM
Ứng dụng Cấu trúc Dữ liệu Danh sách Liên kết Đơn & Mảng 2 Chiều trong C++
* **Môn học:** Cấu trúc Dữ liệu & Giải thuật
* **Nhóm thực hiện:** Nhóm 3 Thành viên (Thành viên 1, Thành viên 2, Thành viên 3)
* **Giảng viên hướng dẫn:** [Điền tên Thầy / Cô]
* **Nền tảng:** C++17 | Quản lý File CSDL bền vững (cinema_db.txt)

---

# 1. Bối cảnh thực tế & Mục tiêu Đề tài
Giải pháp tin học hóa toàn diện quy trình vận hành phòng chiếu phim

### 📌 Thách thức trong quản lý thủ công
* **Dễ nhầm lẫn:** Ghi chép sổ sách thủ công dễ gây bán trùng ghế giữa các nhân viên bán vé.
* **Tra cứu chậm:** Khó khăn khi tìm kiếm phim theo tên, thể loại hoặc lọc mức giá vé.
* **Mất dữ liệu:** Không có cơ chế lưu trữ bền vững khi phần mềm bị tắt hoặc mất điện đột ngột.

### 🎯 Mục tiêu giải pháp phần mềm
* **Quản lý linh hoạt:** Áp dụng Danh sách liên kết đơn để thêm, bớt phim động trên RAM mà không bị giới hạn bộ nhớ tĩnh.
* **Mô phỏng thực tế:** Dùng mảng 2 chiều 5x6 mô phỏng chuẩn xác 30 ghế ngồi (Hàng A-E, Cột 1-6).
* **Đồng bộ 100%:** Mọi thay đổi về vé và phim đều được ghi đè an toàn xuống file `cinema_db.txt`.

---

# 2. Thiết kế Cấu trúc Dữ liệu Cốt lõi
Mô hình hóa dữ liệu tinh gọn và cấp phát bộ nhớ động

### 🎟️ Struct MaVe & ThongTinGhe
* **struct MaVe:** Lưu mã vé tự tăng (`soVe >= 1001`), họ tên khách hàng và số điện thoại.
* **struct ThongTinGhe:** Gồm cờ `bool daDat` và đối tượng `MaVe` đi kèm.
* **Trạng thái:** `daDat = false` là ghế trống (hiển thị số ghế `[01]`..`[30]`), `daDat = true` là ghế đã mua (hiển thị `[ X]`).

### 🎬 Struct Phim & Ma trận ghế
* **Thông tin phim:** Mã phim duy nhất (`ma`), tên phim (`ten`), thể loại (`theLoai`), thời lượng (`thoiLuong`), giá vé (`giaVe`).
* **Ma trận phòng chiếu:** `ThongTinGhe ghe[5][6]` độc lập cho từng bộ phim, tránh xung đột dữ liệu.

### 🔗 Struct NodePhim (DSLK Đơn)
* **Thành phần:** Gồm `Phim data` và con trỏ `NodePhim* next`.
* **Quản lý:** Con trỏ đầu `headPhim` quản lý toàn bộ danh sách trên vùng nhớ Heap, node cuối trỏ về `nullptr`.

---

# 3. Quy ước Ánh xạ Ghế & Quản lý CSDL File
Công thức tính toán tọa độ phòng chiếu và định dạng lưu trữ bền vững

### 🪑 Công thức ánh xạ số ghế (1 -> 30)
* **Xác định hàng (Row):** `r = (soGhe - 1) / 6` (Tương ứng hàng A = 0 đến hàng E = 4).
* **Xác định cột (Col):** `c = (soGhe - 1) % 6` (Tương ứng cột 1 = 0 đến cột 6 = 5).
* **Tính lại số ghế:** `soGhe = r * 6 + c + 1`.
* **Căn lề hiển thị:** Dùng format 2 chữ số `[%02d]` giúp các ô ghế luôn đều tắp 4 ký tự, ma trận ghế thẳng hàng tuyệt đối.

### 💾 Cấu trúc File CSDL (cinema_db.txt)
* **Dòng Header phim:** Bắt đầu bằng dấu `#` (VD: `#P01|Mai|Tam Ly|131|85000`).
* **30 dòng ghế liên tiếp:**
  * Ghế trống: `1|TRONG|0||`
  * Ghế đã mua: `3|DAT|1001|Nguyen Van A|0912345678`
* **Cơ chế nạp & lưu:** Tự động đọc lên RAM khi khởi động (`docDanhSachPhim`) và ghi đè an toàn khi có thay đổi (`ghiToanBoFile`).

---

# 4. Tổ chức Hệ thống & Phân công Trách nhiệm
Kiến trúc Modular 8 chức năng chuẩn hóa phân chia cho 3 thành viên

### 👤 Thành viên 1: Quản trị & Hiển thị
* **Chức năng 1:** Nhập danh sách phim mới & kiểm tra trùng lặp mã không phân biệt hoa thường (`timPhimTheoMa`).
* **Chức năng 2:** Hiển thị danh sách phim dạng bảng 104 cột chuẩn lề, chống méo bảng (`xemDanhSachPhim`).
* **Hạ tầng CSDL:** Quản lý cơ chế đọc và ghi toàn bộ dữ liệu xuống file text.

### 👤 Thành viên 2: Tra cứu & Xóa phim
* **Chức năng 3:** Tìm kiếm phim đa tiêu chí (mã phim, tên phim gần đúng, lọc theo khoảng giá vé).
* **Chức năng 4:** Xóa phim an toàn khỏi hệ thống (`xoaPhim`), xử lý cả 2 ca biên ở đầu và giữa/cuối DSLK đơn.
* **Bảo vệ dữ liệu:** Xác nhận an toàn `(y/n)` trước khi xóa và dùng `delete del` giải phóng bộ nhớ Heap.

### 👤 Thành viên 3: Cập nhật & Nghiệp vụ Vé
* **Chức năng 5:** Cập nhật thông tin phim theo từng trường độc lập (`capNhatThongTinPhim`).
* **Chức năng 6:** Sắp xếp danh sách phim bằng thuật toán Bubble Sort (`sapXepDanhSachPhim`).
* **Chức năng 7 & 8:** Vẽ sơ đồ phòng chiếu 30 ghế & Nghiệp vụ phòng vé Đặt vé / Hủy vé.

---

# 5. Nghiệp vụ Quản lý Phim (CRUD & Search)
Thực thi trọn bộ nghiệp vụ cơ bản với khả năng kiểm soát dữ liệu chặt chẽ

### ➕ 1. Thêm phim & Kiểm tra mã (Chức năng 1)
* Nhập mã phim qua `nhapChuoi()`, gọi `timPhimTheoMa()` so sánh chữ thường để chống trùng lặp (P01 vs p01).
* Nhập an toàn: thời lượng (15 - 360 phút), giá vé (10k - 1tr VND).
* Tự động khởi tạo 30 ô ghế trống và nối node mới vào cuối danh sách liên kết.

### 📋 2. Bảng hiển thị 104 cột (Chức năng 2)
* Phân chia độ rộng chuẩn: Mã (8), Tên phim (40), Thể loại (24), Thời lượng (14), Giá vé (14).
* Dung sai lớn giúp tên phim dài đến 40 ký tự vẫn thẳng tắp, không bị xô lệch bảng.

### 🔍 3. Tìm kiếm gần đúng (Chức năng 3)
* So khớp chuỗi con qua `chuyenChuThuong()` và `string::find()` (người dùng gõ `mai` hay `MAI` đều tìm thấy).
* Hỗ trợ tìm theo khoảng giá vé `[giaMin, giaMax]` và in kết quả ra dạng bảng.

### 🗑️ 4. Xóa phim & Thu hồi Heap (Chức năng 4)
* Ca biên 1: Node cần xóa ở đầu danh sách ➔ Dời `head = head->next`.
* Ca biên 2: Node ở giữa hoặc cuối ➔ Ngắt liên kết `p->next = del->next`.
* Thu hồi vùng nhớ bằng `delete del`, ngay lập tức cập nhật lại file database.

---

# 6. Thuật toán Sắp xếp (Bubble Sort trên DSLK Đơn)
Tối ưu giải thuật sắp xếp nổi bọt trực tiếp trên cấu trúc Danh sách liên kết

### ⚙️ Nguyên lý vận hành giải thuật
* **Duyệt cặp node kề nhau:** Sử dụng 2 con trỏ `ptr1` và `ptr2 = ptr1->next`.
* **Tối ưu bằng con trỏ biên `lptr`:** Giới hạn vùng đã sắp xếp ở cuối danh sách, giảm thiểu số lần quét thừa qua mỗi vòng lặp.
* **Kỹ thuật tráo đổi dữ liệu (Swap data):** Hoán đổi cấu trúc `Phim temp = ptr1->data; ptr1->data = ptr2->data;` thay vì đảo liên kết con trỏ phức tạp.
* **Dừng sớm:** Biến cờ `swapped` nhận diện khi danh sách đã hoàn toàn đúng thứ tự.

### 📊 4 Tiêu chí sắp xếp trên Menu
* **1. Giá vé tăng dần:** Thấp đến cao (Hỗ trợ khách hàng tìm vé rẻ).
* **2. Giá vé giảm dần:** Cao đến thấp.
* **3. Thời lượng tăng dần:** Phim ngắn đến phim dài.
* **4. Thời lượng giảm dần:** Phim dài đến phim ngắn.
* **Đồng bộ tức thì:** Gọi `ghiToanBoFile()` lưu lại thứ tự mới và gọi `xemDanhSachPhim()` xuất kết quả ngay.

---

# 7. Trọng tâm: Quy trình Đặt vé Xem phim
Nghiệp vụ phòng vé cốt lõi - Tự động hóa kiểm tra ghế và phát hành vé

### 1️⃣ Chọn phim & Xem sơ đồ
* Khách hàng nhập mã phim muốn xem (VD: `P01`).
* Hệ thống tự động gọi `xemSoDoGhe()` vẽ trực quan sơ đồ 30 ghế ra màn hình console.

### 2️⃣ Chọn ghế & Kiểm tra trùng
* Khách chọn số ghế từ 1 đến 30 (quy đổi ra vị trí hàng `r` và cột `c`).
* Nếu `ghe[r][c].daDat == true`: Cảnh báo ghế đã có người mua và bắt buộc chọn ghế khác. Vòng lặp chỉ dừng khi chọn được ghế trống.

### 3️⃣ Nhập thông tin khách hàng
* Nhập Họ tên khách và Số điện thoại liên hệ.
* Dùng hàm `nhapChuoi()` kiểm tra chặt chẽ, chống trôi lệnh ký tự `cin`.

### 4️⃣ Cấp mã vé & Xuất biên lai
* Cấp mã vé tự tăng từ bộ đếm `veKeTiep++` (bắt đầu từ `#1001`).
* Đánh dấu ô ghế đã đặt (`daDat = true`), lưu vé, ghi ngay xuống file và in hóa đơn thanh toán ra màn hình.

---

# 8. Trọng tâm: Quy trình Hủy vé & Hoàn trả Ghế
Xử lý nghiệp vụ hủy vé an toàn và giải phóng ghế tức thì cho phòng chiếu

### 🔍 1. Tra cứu vé trên toàn hệ thống
* Người dùng nhập mã số vé cần hủy (nhập `0` để thoát nhanh).
* Hệ thống chạy 2 vòng lặp quét qua toàn bộ các bộ phim và toàn bộ 30 ghế ngồi để tìm kiếm mã vé trùng khớp.

### ⚠️ 2. Cảnh báo & Xác nhận an toàn
* Nếu không tìm thấy: Thông báo mã vé không tồn tại trong CSDL.
* Nếu tìm thấy: In đầy đủ thông tin vé (Tên phim, Tên khách, Vị trí ghế) và hỏi xác nhận: `Ban co CHAC CHAN muon huy ve nay? (y/n)`.

### ♻️ 3. Giải phóng ghế & Cập nhật CSDL
* Nếu chọn `n`: Hủy thao tác, giữ nguyên trạng thái vé.
* Nếu chọn `y`: Đưa ô ghế về trạng thái trống (`daDat = false`, xóa thông tin vé), gọi `ghiToanBoFile()` đồng bộ lại file `cinema_db.txt`.
* Ghế lập tức có thể được mở bán lại cho khách hàng khác.

---

# 9. Khả năng Chống lỗi & Trải nghiệm Console
Thiết kế hướng đến sự bền vững, thân thiện và phòng chống ngoại lệ (Robustness)

### 🛡️ Cơ chế Input Validation an toàn
* **Chống trôi lệnh cin:** Kết hợp `getline()` và kiểm tra chuỗi rỗng triệt để.
* **Chống văng app (Crash-proof):** Nhập nhầm chữ cái vào các trường số nguyên (thời lượng, số ghế) hoặc số thực (giá vé) được xử lý mượt mà bằng `stringstream`, nhắc nhở nhập lại thay vì tắt ứng dụng.
* **Kiểm tra biên:** Giới hạn thời lượng (15-360), giá vé (10k-1tr), ghế (1-30).

### 🖥️ Giao diện Console trực quan
* Bảng danh sách 104 cột căn lề chuẩn mực, kẻ khung viền phân cách rõ ràng.
* Sơ đồ phòng chiếu có tiêu đề màn hình `[SCREEN]`, hàng A-E, cột 1-6 và chú thích đơn giá vé.

### 🧹 Quản lý bộ nhớ sạch sẽ
* Hàm `giaiPhong()` duyệt và `delete` toàn bộ các Node trong DSLK đơn trước khi thoát, đảm bảo không xảy ra hiện tượng rò rỉ bộ nhớ (Memory Leak).

---

# 10. Đánh giá Đề tài & Hướng phát triển
Những thành tựu kỹ thuật đã đạt được và tiềm năng mở rộng ứng dụng

### 🌟 Kết quả đạt được
* Vận dụng hiệu quả cấu trúc dữ liệu Danh sách liên kết đơn kết hợp Mảng 2 chiều giải quyết hoàn hảo bài toán thực tế.
* Kiến trúc mã nguồn rõ ràng, phân lớp chặt chẽ: Hằng số ➔ Struct ➔ Nguyên mẫu ➔ Hàm atomic ➔ Nghiệp vụ CRUD ➔ File I/O ➔ Menu điều phối.
* Dữ liệu có tính bền vững (Persistence) 100%.

### 🚀 Hướng phát triển trong tương lai
* **Giao diện đồ họa (GUI):** Nâng cấp bằng thư viện Qt C++ để khách hàng click chuột trực quan lên ghế phòng chiếu.
* **Cấu trúc Ngăn xếp (Stack):** Phát triển tính năng Hoàn tác (Undo) khi lỡ tay xóa nhầm phim.
* **Cấu trúc Hàng đợi (Queue):** Xây dựng hàng đợi đặt vé trực tuyến vào các khung giờ phim bom tấn.
* **Cây nhị phân tìm kiếm (BST):** Tối ưu hóa tốc độ tìm kiếm khi hệ thống mở rộng lên quy mô chuỗi cụm rạp.

---

# CẢM ƠN QUÝ THẦY CÔ VÀ CÁC BẠN!
Nhóm thực hiện sẵn sàng trả lời các câu hỏi Vấn đáp (Q&A) và Demo trực tiếp chương trình
* **Đề tài:** Hệ thống Quản lý Đặt vé Rạp chiếu phim (C++)
* **Môn học:** Cấu trúc Dữ liệu & Giải thuật
* **Liên hệ:** [Email / Thông tin nhóm]
