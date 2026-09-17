### 1. Khởi động (Startup)
```
  ./main
    │
    └──► main()
          │
          ├──► khoiTaoHeThong()
          │      ├──► kiemTraDBTrong("cinema_db.txt")
          │      │      ├── [File rỗng] ──► Dừng, báo DB trống
          │      │      └── [Có dữ liệu]
          │      │            └──► docDanhSachPhim()
          │      │                   ├── Đọc dòng '#' ──► themPhim() (tạo node trên RAM)
          │      │                   ├── Đọc 30 dòng ghế ──► gán vào ghe[r][c]
          │      │                   └── Cập nhật biến veKeTiep
          │      └──► Đếm số node và in: "[Init] Da load X phim..."
──────

### 2. Thoát & Thu hồi bộ nhớ (Exit)

  Thoát vòng lặp
    │
    ├──► ghiToanBoFile()  (lưu an toàn lần cuối xuống cinema_db.txt)
    ├──► giaiPhong()      (chạy vòng lặp delete từng NodePhim, tránh rò rỉ RAM)
    └──► return 0         (kết thúc tiến trình)
──────



### Ví dụ về flow nhapDanhSachPhim
nhapDanhSachPhim() // -> sau khi khoiTaoHeThong xong đảm bảo đã có dữ liệu trên ram để thao tác.
            ├── Lặp: nhapMotPhim() // hàm con 
            │          ├── nhapChuoi() ──► kiemTraTrungMa() // valid con
            │          ├── nhapSoNguyen(), nhapSoThuc() // hàm valid chung có thể tái sử dụng
            │          └── Tạo 30 ghế trống (daDat = false) // logic nghiệp vụ
            ├── themPhim() (nối node vào RAM) // hàm con có thể tái sử dụng
            └── [Dừng nhập] ──► ghiToanBoFile() (ghi đè lại cinema_db.txt) // lưu lại vào db sao khi làm xong
──────



NGUYÊN TẮC CHUNG CHO 1 HÀM:

xác định vị trí code -> KHAI BÁO NGUYÊN MẪU (PROTOTYPES): vd: void nhapDanhSachPhim(NodePhim*& head);
                        │
                        ▼
[Thao tác] ──► Mọi Thêm / Sửa / Xóa / Đặt vé CHỈ LÀM TRÊN RAM (Linked List) -> làm nghiệp vụ logic 
                        │
                        ▼
[Lưu lại]  ──► ghiToanBoFile() (Quét sạch RAM ghi đè lại toàn bộ xuống DB) -> nhớ lưu lại vào db, có hàm vét linklist để lưu ghiToanBoFile;

```