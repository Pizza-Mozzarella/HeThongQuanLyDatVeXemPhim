# CRUD DESIGN GUIDE — Hệ thống Quản lý Đặt vé Xem phim

> **Mục đích**: Tài liệu này mô tả **thiết kế nghiệp vụ** và **hướng dẫn triển khai** toàn bộ 8 nhóm chức năng CRUD cho dự án Movie Booking System. Đảm bảo thống nhất cách làm giữa các thành viên, dễ mở rộng, dễ bảo trì.

---

## Mục lục

- [0. Kiến trúc tổng quan](#0-kiến-trúc-tổng-quan)
- [1. Nhập danh sách](#1-nhập-danh-sách)
- [2. Thêm phần tử mới](#2-thêm-phần-tử-mới)
- [3. Hiển thị danh sách](#3-hiển-thị-danh-sách)
- [4. Tìm kiếm phần tử](#4-tìm-kiếm-phần-tử)
- [5. Xóa phần tử](#5-xóa-phần-tử)
- [6. Cập nhật thông tin](#6-cập-nhật-thông-tin)
- [7. Sắp xếp](#7-sắp-xếp)
- [8. Đọc / Ghi file text](#8-đọc--ghi-file-text)
- [Quy ước chung & Nguyên tắc mở rộng](#quy-ước-chung--nguyên-tắc-mở-rộng)

---

## 0. Kiến trúc tổng quan

### Cấu trúc dữ liệu hiện tại

```
headPhim ──→ [NodePhim] ──→ [NodePhim] ──→ ... ──→ nullptr
                │                │
                ▼                ▼
            Phim {             Phim {
              ma, ten,           ma, ten,
              theLoai,           theLoai,
              thoiLuong,         thoiLuong,
              giaVe,             giaVe,
              ghe[5][6]          ghe[5][6]
            }                  }
```

### Bảng kê hàm — mapping chức năng → hàm

| # | Chức năng | Tên hàm | Trạng thái |
|:-:|:--|:--|:-:|
| 1 | Nhập danh sách | `nhapDanhSachPhim()` | 🔲 Chưa làm |
| 2 | Thêm phim mới | `themPhimMoi()` | 🔲 Chưa làm |
| 2b | Thêm phim vào linked list (core) | `themPhim()` | ✅ Đã có |
| 3 | Hiển thị danh sách | `xemDanhSachPhim()` | ✅ Đã có |
| 4a | Tìm kiếm theo mã | `timTheoMa()` | 🔲 Chưa làm |
| 4b | Tìm kiếm theo tên | `timTheoTen()` | 🔲 Chưa làm |
| 4c | Tìm kiếm theo thể loại | `timTheoTheLoai()` | 🔲 Chưa làm |
| 4d | Tìm kiếm theo khoảng giá | `timTheoKhoangGia()` | 🔲 Chưa làm |
| 5 | Xóa phim | `xoaPhim()` | 🔲 Chưa làm |
| 6 | Cập nhật thông tin phim | `capNhatPhim()` | 🔲 Chưa làm |
| 7a | Sắp xếp theo mã | `sapXepTheoMa()` | 🔲 Chưa làm |
| 7b | Sắp xếp theo tên | `sapXepTheoTen()` | 🔲 Chưa làm |
| 7c | Sắp xếp theo giá vé | `sapXepTheoGia()` | 🔲 Chưa làm |
| 8a | Đọc file | `docDanhSachPhim()` | ✅ Đã có |
| 8b | Ghi file | `ghiToanBoFile()` | ✅ Đã có |

---

## 1. Nhập danh sách

### Mô tả nghiệp vụ
Cho phép người dùng nhập nhiều phim liên tiếp từ bàn phím. Sau mỗi phim, hỏi *"Tiếp tục nhập? (y/n)"*. Dữ liệu được kiểm tra hợp lệ **trước** khi thêm vào linked list.

### Thiết kế chi tiết

```
HÀM nhapDanhSachPhim(head, veKeTiep):
    LẶP:
        phim ← nhapMotPhim()          // Hàm con, nhập + validate 1 phim
        NẾU kiemTraTrungMa(head, phim.ma) == TRUE:
            In "Mã phim đã tồn tại!"
            Quay lại đầu vòng lặp
        themPhim(head, phim)
        In "Thêm thành công!"
        Hỏi "Tiếp tục nhập? (y/n)"
        NẾU trả lời != 'y': THOÁT LẶP
```

### Quy tắc validate dữ liệu

| Trường | Kiểu | Validate |
|:--|:--|:--|
| `ma` | `string` | Không rỗng, bắt đầu bằng `"P"`, không trùng trong list |
| `ten` | `string` | Không rỗng, tối đa 50 ký tự |
| `theLoai` | `string` | Không rỗng (tùy chọn: chỉ chấp nhận danh sách predefined) |
| `thoiLuong` | `int` | Số nguyên dương, hợp lý: 1 ≤ x ≤ 600 |
| `giaVe` | `double` | Số dương, hợp lý: 1000 ≤ x ≤ 10.000.000 |

### Hàm validate tái sử dụng (đề xuất)

```cpp
// Nhập số nguyên an toàn, lặp lại nếu nhập sai
int nhapSoNguyen(const string& prompt, int min, int max);

// Nhập số thực an toàn
double nhapSoThuc(const string& prompt, double min, double max);

// Nhập chuỗi không rỗng
string nhapChuoi(const string& prompt);

// Nhập có/không
bool xacNhan(const string& prompt);  // return true nếu 'y'
```

> **Tại sao tách riêng?** Các hàm validate này sẽ được **tái sử dụng** ở chức năng 2 (Thêm), chức năng 6 (Cập nhật), và bất kỳ chỗ nào cần nhập liệu. Viết một lần, dùng mọi nơi.

---

## 2. Thêm phần tử mới

### Mô tả nghiệp vụ
Thêm **1 phim mới** vào cuối linked list. Bắt buộc kiểm tra **trùng mã** trước khi thêm.

### Thiết kế chi tiết

```
HÀM themPhimMoi(head):
    phim ← nhapMotPhim()

    // ── KIỂM TRA TRÙNG MÃ ──
    NẾU kiemTraTrungMa(head, phim.ma) == TRUE:
        In "⚠ Lỗi: Mã phim [phim.ma] đã tồn tại!"
        RETURN

    // ── THÊM VÀO LINKED LIST ──
    themPhim(head, phim)      // Hàm core đã có sẵn
    In "✓ Đã thêm phim [phim.ten] thành công!"
```

### Hàm kiểm tra trùng mã

```cpp
// Duyệt linked list, trả về true nếu tìm thấy mã trùng
bool kiemTraTrungMa(NodePhim* head, const string& ma) {
    NodePhim* p = head;
    while (p) {
        if (p->data.ma == ma) return true;
        p = p->next;
    }
    return false;
}
```

### Lưu ý mở rộng
- Hiện tại `themPhim()` thêm vào **cuối** list → O(n). Nếu cần tối ưu, giữ thêm con trỏ `tailPhim` để thêm cuối O(1).
- Nếu sau này muốn thêm vào **đầu** hoặc **giữa**, tạo thêm hàm `themPhimDau()`, `themPhimSau(NodePhim* viTri, Phim p)`.

---

## 3. Hiển thị danh sách

### Mô tả nghiệp vụ
In toàn bộ danh sách phim ra console dưới dạng **bảng có căn lề**, dễ đọc.

### Thiết kế hiện tại (đã hoàn thiện)

```
╔════════╦══════════════════════════════╦═══════════════╦════════════╦═══════════╗
║ Mã     ║ Tên Phim                     ║ Thể Loại      ║ Thời Lượng ║ Giá Vé    ║
╠════════╬══════════════════════════════╬═══════════════╬════════════╬═══════════╣
║ P01    ║ Avatar: The Way of Water     ║ Hanh Dong      ║ 192 phut   ║ 90000 VND ║
║ P02    ║ Oppenheimer                  ║ Lich Su        ║ 180 phut   ║ 85000 VND ║
╚════════╩══════════════════════════════╩═══════════════╩════════════╩═══════════╝
```

### Mở rộng: Hiển thị sơ đồ ghế

```
HÀM xemSoDoGhe(NodePhim* head):
    maPhim ← nhapChuoi("Nhập mã phim: ")
    p ← timNodeTheoMa(head, maPhim)     // Tái sử dụng hàm tìm kiếm
    NẾU p == nullptr:
        In "Không tìm thấy phim!"
        RETURN

    In tiêu đề: tên phim
    VỚI MỖI hàng r = 0..4:
        In nhãn hàng (A..E)
        VỚI MỖI cột c = 0..5:
            NẾU ghe[r][c].daDat == false:
                In "[O]" (màu xanh nếu hỗ trợ)
            NGƯỢC LẠI:
                In "[X]" (màu đỏ nếu hỗ trợ)
```

---

## 4. Tìm kiếm phần tử

### Mô tả nghiệp vụ
Hỗ trợ **4 kiểu tìm kiếm** khác nhau. Tất cả đều duyệt linked list và in ra các phim thỏa điều kiện.

### Thiết kế pattern chung

Tất cả hàm tìm kiếm đều theo **cùng một pattern**:

```
HÀM timKiem_XXX(head, điều_kiện):
    found ← 0
    p ← head
    WHILE p != nullptr:
        NẾU p->data thỏa điều_kiện:
            In thông tin p->data
            found++
        p ← p->next
    NẾU found == 0:
        In "Không tìm thấy kết quả!"
    NGƯỢC LẠI:
        In "Tìm thấy [found] kết quả."
```

### Chi tiết từng loại tìm kiếm

#### 4a. Tìm theo mã (chính xác)

```cpp
// Trả về con trỏ đến node tìm thấy, hoặc nullptr
NodePhim* timTheoMa(NodePhim* head, const string& ma) {
    NodePhim* p = head;
    while (p) {
        if (p->data.ma == ma) return p;
        p = p->next;
    }
    return nullptr;
}
```

> **Quan trọng**: Hàm này trả về **con trỏ đến node**, không chỉ in ra. Vì nó sẽ được **tái sử dụng** bởi: chức năng 5 (Xóa), chức năng 6 (Cập nhật), chức năng hiển thị sơ đồ ghế, chức năng đặt vé.

#### 4b. Tìm theo tên (chứa chuỗi con, không phân biệt hoa thường)

```cpp
// Kiểm tra chuỗi haystack có chứa chuỗi needle không (case-insensitive)
bool chuaChuoi(const string& haystack, const string& needle) {
    string h = haystack, n = needle;
    transform(h.begin(), h.end(), h.begin(), ::tolower);
    transform(n.begin(), n.end(), n.begin(), ::tolower);
    return h.find(n) != string::npos;
}

void timTheoTen(NodePhim* head, const string& tuKhoa) {
    int found = 0;
    NodePhim* p = head;
    while (p) {
        if (chuaChuoi(p->data.ten, tuKhoa)) {
            // In thông tin phim
            found++;
        }
        p = p->next;
    }
    if (!found) cout << "Không tìm thấy!\n";
}
```

#### 4c. Tìm theo thể loại

```
Giống 4b nhưng so sánh trường theLoai thay vì ten.
Tái sử dụng hàm chuaChuoi().
```

#### 4d. Tìm theo khoảng giá

```cpp
void timTheoKhoangGia(NodePhim* head, double giaMin, double giaMax) {
    // Duyệt list, in phim có giaMin <= giaVe <= giaMax
}
```

### Thiết kế menu tìm kiếm

```
===== TÌM KIẾM PHIM =====
  1. Theo mã phim
  2. Theo tên phim
  3. Theo thể loại
  4. Theo khoảng giá vé
  0. Quay lại
===========================
Chọn: _
```

---

## 5. Xóa phần tử

### Mô tả nghiệp vụ
Xóa **1 node** khỏi linked list theo mã hoặc tên. Cần xác nhận trước khi xóa. Phải xử lý đúng **3 trường hợp**: xóa đầu, xóa giữa, xóa cuối.

### Thiết kế chi tiết

```
HÀM xoaPhim(head):
    ma ← nhapChuoi("Nhập mã phim cần xóa: ")

    // ── TÌM NODE CẦN XÓA + NODE TRƯỚC NÓ ──
    prev ← nullptr
    curr ← head
    WHILE curr != nullptr VÀ curr->data.ma != ma:
        prev ← curr
        curr ← curr->next

    NẾU curr == nullptr:
        In "⚠ Không tìm thấy phim mã [ma]!"
        RETURN

    // ── XÁC NHẬN ──
    In "Bạn có chắc muốn xóa phim [curr->data.ten]? (y/n)"
    NẾU xacNhan() == false: RETURN

    // ── XÓA NODE ──
    NẾU prev == nullptr:
        // Trường hợp 1: Xóa node đầu
        head ← curr->next
    NGƯỢC LẠI:
        // Trường hợp 2 & 3: Xóa giữa hoặc cuối
        prev->next ← curr->next

    DELETE curr
    In "✓ Đã xóa thành công!"
```

### Code C++ đề xuất

```cpp
bool xoaPhim(NodePhim*& head, const string& ma) {
    NodePhim* prev = nullptr;
    NodePhim* curr = head;

    // Tìm node có mã phù hợp
    while (curr && curr->data.ma != ma) {
        prev = curr;
        curr = curr->next;
    }
    if (!curr) return false;  // Không tìm thấy

    // Tháo node ra khỏi list
    if (!prev)
        head = curr->next;       // Xóa đầu
    else
        prev->next = curr->next; // Xóa giữa/cuối

    delete curr;                 // Giải phóng bộ nhớ
    return true;
}
```

### Lưu ý quan trọng

- **Luôn `delete`** node sau khi tháo ra khỏi list → tránh **memory leak**.
- **Luôn xác nhận** trước khi xóa → tránh xóa nhầm.
- Nếu sau này có chức năng **Đặt vé**, cần kiểm tra: phim đang có vé đã đặt → **cảnh báo** user trước khi xóa phim.

---

## 6. Cập nhật thông tin

### Mô tả nghiệp vụ
Tìm phim theo mã → hiển thị thông tin hiện tại → cho phép chọn trường muốn sửa → nhập giá trị mới → validate → lưu.

### Thiết kế chi tiết

```
HÀM capNhatPhim(head):
    ma ← nhapChuoi("Nhập mã phim cần cập nhật: ")
    p ← timTheoMa(head, ma)        // Tái sử dụng hàm tìm kiếm (4a)

    NẾU p == nullptr:
        In "Không tìm thấy!"
        RETURN

    In "Thông tin hiện tại: ..."     // Hiển thị thông tin phim hiện tại

    In "Chọn trường cần sửa:"
    In "  1. Tên phim"
    In "  2. Thể loại"
    In "  3. Thời lượng"
    In "  4. Giá vé"
    In "  0. Quay lại"
    chon ← đọc lựa chọn

    SWITCH chon:
        CASE 1: p->data.ten      ← nhapChuoi("Tên mới: ")
        CASE 2: p->data.theLoai  ← nhapChuoi("Thể loại mới: ")
        CASE 3: p->data.thoiLuong ← nhapSoNguyen("Thời lượng mới: ", 1, 600)
        CASE 4: p->data.giaVe    ← nhapSoThuc("Giá vé mới: ", 1000, 10000000)

    In "✓ Cập nhật thành công!"
```

### Tại sao thiết kế này?

- **Không cho sửa mã phim** (`ma`) vì đó là **khóa chính** (primary key), nếu sửa sẽ gây mất liên kết dữ liệu vé đã đặt.
- **Tái sử dụng** `timTheoMa()` — hàm trả về con trỏ nên có thể sửa trực tiếp `p->data.xxx` mà không cần copy.
- **Tái sử dụng** các hàm validate (`nhapSoNguyen`, `nhapSoThuc`, `nhapChuoi`).

---

## 7. Sắp xếp

### Mô tả nghiệp vụ
Sắp xếp linked list theo các tiêu chí khác nhau, hỗ trợ **tăng dần / giảm dần**.

### Thiết kế menu

```
===== SẮP XẾP DANH SÁCH PHIM =====
  1. Theo mã phim     (tăng dần)
  2. Theo mã phim     (giảm dần)
  3. Theo tên phim    (A → Z)
  4. Theo tên phim    (Z → A)
  5. Theo giá vé      (thấp → cao)
  6. Theo giá vé      (cao → thấp)
  0. Quay lại
====================================
```

### Chọn thuật toán

| Thuật toán | Phức tạp | Phù hợp Linked List? | Đề xuất |
|:--|:-:|:-:|:-:|
| Bubble Sort (hoán vị data) | O(n²) | ✅ Dễ cài đặt | **Ưu tiên cho bài tập** |
| Selection Sort | O(n²) | ✅ | Tùy chọn |
| Merge Sort | O(n log n) | ✅ Rất phù hợp | Nâng cao |

### Chiến lược: Hoán vị DATA, giữ nguyên NODE

> **Quan trọng**: Với linked list, thay vì tháo gỡ và nối lại con trỏ (phức tạp, dễ lỗi), ta **giữ nguyên cấu trúc node** và chỉ **hoán vị `data` (struct Phim)** giữa 2 node. Đơn giản và an toàn hơn rất nhiều.

```cpp
// Sắp xếp linked list bằng Bubble Sort — hoán vị data
// soSanh: hàm so sánh, trả true nếu a "nên đứng trước" b
void sapXep(NodePhim* head, bool (*soSanh)(const Phim&, const Phim&)) {
    if (!head) return;
    bool swapped;
    do {
        swapped = false;
        NodePhim* p = head;
        while (p->next) {
            // Nếu p "không nên đứng trước" p->next → hoán vị
            if (!soSanh(p->data, p->next->data)) {
                swap(p->data, p->next->data);   // std::swap
                swapped = true;
            }
            p = p->next;
        }
    } while (swapped);
}
```

### Các hàm so sánh (function pointer)

```cpp
// Theo mã tăng dần
bool ssMaTang(const Phim& a, const Phim& b) { return a.ma < b.ma; }

// Theo mã giảm dần
bool ssMaGiam(const Phim& a, const Phim& b) { return a.ma > b.ma; }

// Theo tên A→Z
bool ssTenTang(const Phim& a, const Phim& b) { return a.ten < b.ten; }

// Theo tên Z→A
bool ssTenGiam(const Phim& a, const Phim& b) { return a.ten > b.ten; }

// Theo giá tăng
bool ssGiaTang(const Phim& a, const Phim& b) { return a.giaVe < b.giaVe; }

// Theo giá giảm
bool ssGiaGiam(const Phim& a, const Phim& b) { return a.giaVe > b.giaVe; }
```

### Tại sao dùng function pointer?

- **Viết hàm `sapXep()` MỘT LẦN**, muốn sắp theo tiêu chí nào thì truyền hàm so sánh tương ứng.
- Thêm tiêu chí mới (VD: sắp theo thời lượng) → chỉ cần thêm **1 hàm so sánh**, không sửa hàm `sapXep()`.
- Đây là nguyên tắc **Open/Closed Principle** — mở cho mở rộng, đóng cho sửa đổi.

### Ví dụ gọi

```cpp
// Trong menu:
case 1: sapXep(headPhim, ssMaTang);   break;
case 5: sapXep(headPhim, ssGiaTang);  break;
```

---

## 8. Đọc / Ghi file text

### Trạng thái: ✅ Đã hoàn thiện

Cả 2 hàm `docDanhSachPhim()` và `ghiToanBoFile()` đã hoạt động 100%. Định dạng file:

```
#<MaPhim>|<TenPhim>|<TheLoai>|<ThoiLuong>|<GiaVe>     ← Header
01|O                                                    ← Ghế trống
03|X|1001|Nguyen Van A|0912345678                       ← Ghế đã đặt
...
30|O
#<MaPhim>|...                                           ← Phim tiếp theo
```

### Khi nào ghi file?

| Thời điểm | Hành động |
|:--|:--|
| Khi thoát chương trình (chọn `0`) | ✅ Đã có — `ghiToanBoFile()` |
| Sau mỗi thao tác thay đổi dữ liệu | 🔲 **Nên thêm** — gọi `ghiToanBoFile()` sau khi thêm/xóa/sửa/đặt vé |

> **Đề xuất**: Gọi `ghiToanBoFile()` sau mỗi thao tác CRUD để tránh mất dữ liệu khi chương trình crash. Trade-off: tốn I/O hơn, nhưng an toàn hơn nhiều.

### Mở rộng: Backup trước khi ghi

```cpp
void ghiAnToan(const string& file, NodePhim* head) {
    // Bước 1: Ghi vào file tạm
    string tmpFile = file + ".tmp";
    ghiToanBoFile(tmpFile, head);

    // Bước 2: Xóa file cũ, đổi tên file tạm → file chính
    remove(file.c_str());
    rename(tmpFile.c_str(), file.c_str());
}
```

---

## Quy ước chung & Nguyên tắc mở rộng

### 1. Quy ước đặt tên hàm

```
[hành_động] + [đối_tượng] + [bổ_ngữ]
```

| Ví dụ | Giải thích |
|:--|:--|
| `themPhim()` | Thêm + Phim |
| `xoaPhim()` | Xóa + Phim |
| `timTheoMa()` | Tìm + Theo Mã |
| `sapXepTheoGia()` | Sắp xếp + Theo Giá |
| `nhapSoNguyen()` | Nhập + Số Nguyên |

### 2. Quy ước tham số

| Tham số | Quy ước |
|:--|:--|
| `NodePhim*& head` | Dùng khi hàm **có thể thay đổi head** (thêm đầu, xóa đầu) |
| `NodePhim* head` | Dùng khi hàm **chỉ đọc** (hiển thị, tìm kiếm) |
| `const string& x` | Dùng cho chuỗi đầu vào — tránh copy không cần thiết |

### 3. Nguyên tắc thiết kế cho mở rộng

```
┌─────────────────────────────────────────────────────────────────┐
│  MỖI HÀM CHỈ LÀM MỘT VIỆC (Single Responsibility Principle)  │
│                                                                 │
│  ✗ Sai:  void themVaHienThi(...)  ← làm 2 việc                │
│  ✓ Đúng: void themPhim(...)       ← chỉ thêm                  │
│          void hienThiPhim(...)    ← chỉ hiển thị               │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│  TÁI SỬ DỤNG — KHÔNG VIẾT LẠI (Don't Repeat Yourself)         │
│                                                                 │
│  • timTheoMa()    → dùng bởi: Xóa, Cập nhật, Xem ghế, Đặt vé │
│  • nhapSoNguyen() → dùng bởi: Nhập phim, Cập nhật              │
│  • chuaChuoi()    → dùng bởi: Tìm theo tên, Tìm theo thể loại │
│  • sapXep()       → dùng bởi: Mọi tiêu chí (qua function ptr) │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│  MỞ CHO MỞ RỘNG, ĐÓNG CHO SỬA ĐỔI (Open/Closed Principle)    │
│                                                                 │
│  Thêm tiêu chí sắp xếp mới?                                   │
│    → Chỉ thêm 1 hàm so sánh, KHÔNG sửa hàm sapXep()          │
│                                                                 │
│  Thêm trường dữ liệu mới cho Phim (VD: đạo diễn)?             │
│    → Sửa struct Phim + hàm đọc/ghi file                       │
│    → Các hàm CRUD khác KHÔNG cần sửa                          │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Menu chính mở rộng (đề xuất)

```
╔══════════════════════════════════════╗
║    QUẢN LÝ ĐẶT VÉ XEM PHIM         ║
╠══════════════════════════════════════╣
║  1. Xem danh sách phim              ║
║  2. Thêm phim mới                   ║
║  3. Tìm kiếm phim           →       ║
║  4. Xóa phim                        ║
║  5. Cập nhật thông tin phim          ║
║  6. Sắp xếp danh sách       →       ║
║  ──────────────────────────────────  ║
║  7. Xem sơ đồ ghế                   ║
║  8. Đặt vé                          ║
║  9. Hủy vé                          ║
║  ──────────────────────────────────  ║
║  0. Lưu & Thoát                     ║
╚══════════════════════════════════════╝
```

> Các mục có dấu `→` sẽ mở ra **sub-menu** riêng.

### 5. Thứ tự triển khai đề xuất

```
Bước 1 (nền tảng)    → Hàm validate: nhapSoNguyen, nhapSoThuc, nhapChuoi, xacNhan
Bước 2 (tìm kiếm)   → timTheoMa (trả con trỏ) — vì rất nhiều chức năng phụ thuộc
Bước 3 (CRUD cơ bản) → themPhimMoi (dùng validate + kiểm tra trùng mã)
                      → xoaPhim    (dùng timTheoMa)
                      → capNhatPhim (dùng timTheoMa + validate)
Bước 4 (tìm nâng cao) → timTheoTen, timTheoTheLoai, timTheoKhoangGia
Bước 5 (sắp xếp)     → sapXep (generic) + các hàm so sánh
Bước 6 (nghiệp vụ)   → xemSoDoGhe, datVe, huyVe
Bước 7 (hoàn thiện)   → Menu chính + sub-menu + ghi file sau mỗi thao tác
```

---

> **Lưu ý cuối cùng**: Tài liệu này là **bản thiết kế sống** (living document). Khi triển khai xong mỗi chức năng, hãy cập nhật cột **Trạng thái** trong [bảng mapping](#bảng-kê-hàm--mapping-chức-năng--hàm) từ 🔲 → ✅.
