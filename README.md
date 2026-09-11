# Movie Booking System - Core Guide

> **logic:**  
> Hệ thống đọc/ghi Database (`cinema_db.txt`) **đã hoàn thiện 100%**. Dữ liệu khi khởi động đã được đổ sẵn vào RAM.  

---

## 1. Dữ liệu đang tự động từ database được đổ sẵn trên RAM
```cpp
// ================================================================
// FILE DATABASE
//
// Định dạng cinema_db.txt:
//
//   #<ma>|<ten>|<theLoai>|<thoiLuong>|<giaVe>
//   01|O
//   02|O
//   03|X|1001|Nguyen Van A|0912345678
//   ...
//   30|O
//   #<ma>|...   ← phim tiếp theo
//
// - Dòng bắt đầu bằng '#' là header của 1 phim.
// - Ngay bên dưới header là đúng 30 dòng ghế (01 .. 30).
// - Số thứ tự 01..30 ánh xạ: r = (i-1)/6, c = (i-1)%6.
// - Ghế trống:  "05|O"
// - Ghế đã đặt: "05|X|1001|Nguyen Van A|0912345678"
// ================================================================
```

Toàn bộ hệ thống quản lý qua con trỏ:
```cpp
NodePhim* headPhim; // Danh sách liên kết các phim
int veKeTiep;        // Bộ đếm mã vé tự tăng (1001, 1002...)
```

Duyệt danh sách phim bằng con trỏ:
```cpp
NodePhim* p = headPhim;
while (p != nullptr) {
    // Truy xuất thông tin của phim qua p->data
    p = p->next;
}
```

---

## 2. Các biến bên trong mỗi Phim (`p->data`)

Mỗi phim (`p->data`) chứa:
* `p->data.ma`: Mã phim (`string`, vd: `"P01"`)
* `p->data.ten`: Tên phim (`string`, vd: `"Avatar"`)
* `p->data.theLoai`: Thể loại (`string`, vd: `"Hanh Dong"`)
* `p->data.thoiLuong`: Thời lượng (`int`, vd: `192` phút)
* `p->data.giaVe`: Giá vé 1 ghế (`double`, vd: `90000`)
* `p->data.ghe[5][6]`: **Ma trận 30 ghế của phim**
  * Hàng `r` từ `0` đến `4` (tương ứng hàng A đến E)
  * Cột `c` từ `0` đến `5` (tương ứng cột 1 đến 6)

---

## 3. Các biến bên trong mỗi ô Ghế (`ghe[r][c]`)

Mỗi ô `ghe[r][c]` chứa trạng thái và thông tin vé:

| Biến | Kiểu | Ý nghĩa & Cách dùng |
| :--- | :--- | :--- |
| `ghe[r][c].daDat` | `bool` | `false` = Ghế trống<br>`true` = Ghế đã có người đặt |
| `ghe[r][c].ve.soVe` | `int` | Mã số vé (chỉ dùng khi `daDat == true`) |
| `ghe[r][c].ve.tenKhach` | `string` | Tên khách đặt vé |
| `ghe[r][c].ve.sdt` | `string` | Số điện thoại khách |
    
```cpp
r = (i-1)/6,
c = (i-1) % 6.
```

---

