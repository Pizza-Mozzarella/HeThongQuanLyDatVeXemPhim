#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

// ================================================================
// HẰNG SỐ
// ================================================================
const int SO_HANG = 5;          // Hàng A → E
const int SO_COT  = 6;          // Cột  1 → 6
const int TONG_GHE = SO_HANG * SO_COT;  // 30 ghế / phim
const string FILE_DB = "cinema_db.txt";

// ================================================================
// STRUCT
// ================================================================

// Thông tin vé — sẽ được nhúng thẳng vào ô ghế
struct MaVe {
    int    soVe;      // 0 = chưa đặt
    string tenKhach;
    string sdt;
};

// Mỗi ô ghế biết mình trống hay đã đặt, nếu đặt thì lưu luôn thông tin vé
struct ThongTinGhe {
    bool  daDat;      // false = trống, true = đã đặt
    MaVe  ve;         // chỉ có nghĩa khi daDat == true
};

// Một phim chứa luôn toàn bộ sơ đồ ghế
struct Phim {
    string       ma;
    string       ten;
    string       theLoai;
    int          thoiLuong;
    double       giaVe;
    ThongTinGhe  ghe[SO_HANG][SO_COT];
};

// Node của linked list phim
struct NodePhim {
    Phim      data;
    NodePhim* next;
};

// ── KHAI BÁO NGUYÊN MẪU (PROTOTYPES) ─────────────────────────────
bool kiemTraDBTrong(const string& file);
void themPhim(NodePhim*& head, Phim p);
void giaiPhong(NodePhim*& head);
void docDanhSachPhim(const string& file, NodePhim*& head, int& veKeTiep);
string taoGheDong(int so, ThongTinGhe ghe);
void ghiToanBoFile(const string& file, NodePhim* head);
void xemDanhSachPhim(NodePhim* headPhim);
string nhapChuoi(string thongBao);
int nhapSoNguyen(string thongBao, int minVal, int maxVal);
double nhapSoThuc(string thongBao, double minVal, double maxVal); 
bool kiemTraTrungMa(NodePhim* head, string ma);
Phim nhapMotPhim(NodePhim* head);
void nhapDanhSachPhim(NodePhim*& head);
void capNhatThongTinPhim(NodePhim* headPhim);
void sapXepTheoGiaVe(NodePhim* headPhim, bool giamDan);
void sapXepTheoThoiLuong(NodePhim* headPhim, bool giamDan);
void hienThiMenuSapXep(NodePhim* headPhim);
void hienThiMenu();
void khoiTaoHeThong(const string& file, NodePhim*& head, int& veKeTiep);

// ================================================================
// LINKED LIST PHIM
// ================================================================

void themPhim(NodePhim*& head, Phim p) {
    NodePhim* node = new NodePhim{ p, nullptr };
    if (head == nullptr) { head = node; return; }
    NodePhim* t = head;
    while (t->next) t = t->next;
    t->next = node;
}

void giaiPhong(NodePhim*& head) {
    while (head) { NodePhim* t = head; head = head->next; delete t; }
}

void docDanhSachPhim(const string& file, NodePhim*& head, int& veKeTiep) {
    ifstream f(file);
    if (!f.is_open()) return;

    string dong;
    NodePhim* node = nullptr;   // node phim đang đọc

    while (getline(f, dong)) {
        if (!dong.empty() && dong.back() == '\r') dong.pop_back();
        if (dong.empty()) continue;

        if (dong[0] == '#') {
            // --- Header phim ---
            // Định dạng: #P01|Avatar|Hanh Dong|192|90000
            stringstream ss(dong.substr(1));
            Phim p{};
            string thoiStr, giaStr;
            getline(ss, p.ma,       '|');
            getline(ss, p.ten,      '|');
            getline(ss, p.theLoai,  '|');
            getline(ss, thoiStr,    '|');
            getline(ss, giaStr);
            p.thoiLuong = stoi(thoiStr);
            p.giaVe     = stod(giaStr);
            // Khởi tạo tất cả ghế về trạng thái trống
            for (int r = 0; r < SO_HANG; r++)
                for (int c = 0; c < SO_COT;  c++)
                    p.ghe[r][c] = { false, {0, "", ""} };
            themPhim(head, p);
            // Giữ con trỏ tới node vừa thêm để điền ghế tiếp theo
            node = head;
            while (node->next) node = node->next;
        } else {
            // --- Dòng ghế ---
            // Định dạng trống : "03|O"
            // Định dạng đặt   : "03|X|1001|Nguyen Van A|0912345678"
            if (!node) continue;
            stringstream ss(dong);
            string soStr, trangThai;
            getline(ss, soStr,     '|'); //03
            getline(ss, trangThai, '|'); // X or O
            if (trangThai == "X") {
                string soVeStr, tenKhach, sdt;
                getline(ss, soVeStr,  '|'); // 1001
                getline(ss, tenKhach, '|'); // Nguyen Van A
                getline(ss, sdt); // 0912345678
                int so = stoi(soStr);
                int r  = (so - 1) / SO_COT;
                int c  = (so - 1) % SO_COT;
                int soVe = stoi(soVeStr);
                node->data.ghe[r][c] = { true, {soVe, tenKhach, sdt} };
                if (soVe >= veKeTiep) veKeTiep = soVe + 1;
            }
        }
    }
    f.close();
}

string taoGheDong(int so, ThongTinGhe ghe) {
    string soStr = (so < 10 ? "0" : "") + to_string(so);

    if (!ghe.daDat) {
        return soStr + "|O";
    }
    return soStr + "|X|" + to_string(ghe.ve.soVe) + "|" + ghe.ve.tenKhach + "|" + ghe.ve.sdt;
}

void ghiToanBoFile(const string& file, NodePhim* head) {
    ofstream f(file);
    NodePhim* p = head;
    while (p) {
        f << "#" << p->data.ma << "|" << p->data.ten  << "|"
                    << p->data.theLoai  << "|"
                    << p->data.thoiLuong << "|"
                    << p->data.giaVe << "\n";

        for (int r = 0; r < SO_HANG; r++)
            for (int c = 0; c < SO_COT; c++) {
                int so = r * SO_COT + c + 1;
                f << taoGheDong(so, p->data.ghe[r][c]) << "\n";
            }
        p = p->next;
    }
    f.close();
}

// ================================================================
// CORE & CRUD CƠ BẢN (CÓ CHÚ THÍCH NGHIỆP VỤ ĐẦY ĐỦ)
// ================================================================

// Kiểm tra xem db có trống không?
bool kiemTraDBTrong(const string& file) {
    // Mở file ở chế độ đọc (ifstream)
    ifstream f(file);

    // Nghiệp vụ: Nếu file chưa từng được tạo ra (lần đầu chạy ứng dụng)
    // thì coi như hệ thống chưa có dữ liệu nào -> trả về true (trống)
    if (!f.is_open()) {
        return true;
    }

    string dong;
    // Đọc tuần tự từng dòng để kiểm tra nội dung
    while (getline(f, dong)) {
        // Nghiệp vụ: Bỏ qua dòng rỗng hoặc chỉ toàn khoảng trắng tab, enter.
        // Nếu tìm thấy ít nhất 1 dòng có ký tự chữ/số thực sự
        if (!dong.empty() && dong.find_first_not_of(" \t\r\n") != string::npos) {
            f.close();     // Đóng file giải phóng tài nguyên hệ điều hành
            return false;  // Kết luận: Database ĐÃ CÓ dữ liệu từ trước
        }
    }

    f.close();
    // Nghiệp vụ: File có tồn tại nhưng bên trong hoàn toàn rỗng 0 byte
    return true;
}

// Nhập chuỗi ký tự bắt buộc không được để rỗng
string nhapChuoi(string thongBao) {
    string s;
    while (true) {
        cout << thongBao;
        getline(cin, s); // Dùng getline để lấy cả chuỗi có khoảng trắng và nuốt trọn ký tự Enter

        // Nghiệp vụ: Tên phim, thể loại hoặc mã phim không được là chuỗi trắng rỗng
        if (!s.empty()) {
            return s; // Hợp lệ -> trả về chuỗi
        }
        cout << "  [!] Thong tin khong duoc bo trong. Vui long nhap lai!\n";
    }
}

// Nhập số nguyên có ràng buộc ngưỡng giá trị (áp dụng cho thời lượng phim)
int nhapSoNguyen(string thongBao, int minVal, int maxVal) {
    string s;
    while (true) {
        cout << thongBao;
        getline(cin, s); // Nhận chuỗi trước để tránh lỗi trôi lệnh cin >> truyền thống

        stringstream ss(s); // Dùng luồng chuỗi để ép kiểu sang số nguyên
        int val;
        // Kiểm tra 2 điều kiện: ép sang int thành công VÀ không còn ký tự rác phía sau (ss.eof())
        if (ss >> val && ss.eof()) {
            // Nghiệp vụ: Thời lượng phim phải nằm trong khung giờ chiếu thực tế (VD: 15 đến 360 phút)
            if (val >= minVal && val <= maxVal) {
                return val; // Hợp lệ -> trả về số nguyên
            }
            cout << "  [!] Gia tri phai nam trong khoang [" << minVal << " - " << maxVal << "]!\n";
        } else {
            // Bắt lỗi khi người dùng lỡ tay gõ chữ cái vào ô số
            cout << "  [!] Dinh dang khong hop le! Vui long nhap so nguyen.\n";
        }
    }
}

// Nhập số thực có ràng buộc ngưỡng giá trị (áp dụng cho giá vé xem phim)
double nhapSoThuc(string thongBao, double minVal, double maxVal) {
    string s;
    while (true) {
        cout << thongBao;
        getline(cin, s);

        stringstream ss(s);
        double val;
        // Ép kiểu chuỗi sang số thực double
        if (ss >> val && ss.eof()) {
            // Nghiệp vụ: Giá vé xem phim của rạp phải nằm trong biên độ quy định (VD: 10,000 -> 1,000,000 VND)
            if (val >= minVal && val <= maxVal) {
                return val; // Hợp lệ -> trả về giá vé
            }
            cout << "  [!] Gia ve phai tu " << (long long)minVal << " den " << (long long)maxVal << " VND!\n";
        } else {
            cout << "  [!] Dinh dang khong hop le! Vui long nhap dung so tien.\n";
        }
    }
}

// Nghiệp vụ: Kiểm tra tính duy nhất của Mã phim (Khóa chính - Primary Key)
bool kiemTraTrungMa(NodePhim* head, string ma) {
    NodePhim* p = head; // Bắt đầu duyệt từ đầu danh sách liên kết
    while (p != nullptr) {
        // So sánh mã phim hiện tại với mã người dùng vừa gõ
        if (p->data.ma == ma) {
            return true; // Phát hiện trùng mã -> trả về true
        }
        p = p->next; // Nhảy sang node phim tiếp theo
    }
    return false; // Duyệt hết danh sách không thấy trùng -> an toàn
}

Phim nhapMotPhim(NodePhim* head) {
    Phim p{}; // Khởi tạo struct Phim mới với dữ liệu rỗng ban đầu

    // --- BƯỚC 1: NHẬP VÀ KIỂM TRA MÃ PHIM ---
    while (true) {
        p.ma = nhapChuoi("  + Nhap ma phim (VD: P05): ");
        // Nghiệp vụ: Kiểm tra mã phim vừa nhập có trùng với các phim ĐÃ CÓ trong DB không
        if (kiemTraTrungMa(head, p.ma)) {
            // Nếu trùng thì cảnh báo và bắt nhập lại mã khác ngay tại đây (không bắt nhập lại từ đầu)
            cout << "  [!] Ma phim '" << p.ma << "' DA TON TAI trong he thong! Vui long dung ma khac.\n";
        } else {
            break; // Mã hợp lệ và duy nhất -> thoát vòng lặp kiểm tra
        }
    }

    // --- BƯỚC 2: NHẬP CÁC THUỘC TÍNH NGHIỆP VỤ CÒN LẠI ---
    p.ten       = nhapChuoi("  + Nhap ten phim: ");
    p.theLoai   = nhapChuoi("  + Nhap the loai: ");
    p.thoiLuong = nhapSoNguyen("  + Nhap thoi luong (15 - 360 phut): ", 15, 360);
    p.giaVe     = nhapSoThuc("  + Nhap gia ve (10,000 - 1,000,000 VND): ", 10000, 1000000);

    // --- BƯỚC 3: NGHIỆP VỤ KHỞI TẠO SƠ ĐỒ PHÒNG CHIẾU CHO PHIM MỚI ---
    // Mỗi bộ phim mới khi đưa vào hệ thống mặc định phải có phòng chiếu gồm 30 ghế (5 hàng x 6 cột)
    for (int r = 0; r < SO_HANG; r++) {       // Duyệt qua 5 hàng (A -> E)
        for (int c = 0; c < SO_COT; c++) {    // Duyệt qua 6 cột (1 -> 6)
            p.ghe[r][c].daDat = false;        // Nghiệp vụ: Tất cả ghế ban đầu đều phải TRỐNG
            p.ghe[r][c].ve = {0, "", ""};     // Thông tin vé mặc định chưa có (mã vé = 0, khách rỗng)
        }
    }

    return p; // Trả về struct Phim hoàn chỉnh sẵn sàng nạp vào danh sách
}

void nhapDanhSachPhim(NodePhim*& head) {
    cout << "\n========================================\n";
    cout << "        NHAP DANH SACH PHIM MOI          \n";
    cout << "========================================\n";

    int dem = 0; // Biến đếm số lượng phim được nhập trong phiên làm việc này

    // Vòng lặp cho phép quản lý rạp nhập liên tiếp nhiều phim
    while (true) {
        dem++;
        cout << "\n>> Nhap thong tin phim thu " << dem << ":\n";

        // Nhập đầy đủ 1 phim (hàm này tự bảo đảm không trùng mã với các phim đã có trên RAM)
        Phim p = nhapMotPhim(head);

        // Đưa phim mới vào cuối Danh sách liên kết trên bộ nhớ RAM
        themPhim(head, p);

        cout << "=> Da them tam thoi vao bo nho RAM: [" << p.ma << " - " << p.ten << "]\n";

        // Nghiệp vụ: Tương tác hỏi người dùng có muốn nhập tiếp không
        string tiep = nhapChuoi("\nBan co muon nhap them phim nua khong? (y/n): ");
        if (tiep != "y" && tiep != "Y") {
            break; // Thoát vòng lặp nhập
        }
    }

    // --- BƯỚC ĐỒNG BỘ: GHI TOÀN BỘ DỮ LIỆU TỪ RAM XUỐNG FILE DATABASE ---
    // Nghiệp vụ cốt lõi: Lấy toàn bộ danh sách liên kết ghi đè lại toàn bộ vào file cinema_db.txt
    cout << "\n[Dang luu...] Dang ghi de toan bo du lieu moi vao file " << FILE_DB << "...\n";
    ghiToanBoFile(FILE_DB, head);

    cout << "[Thanh cong] Da them " << dem << " phim va DONG BO 100% vao Database!\n";
    cout << "========================================\n";
}

void xemDanhSachPhim(NodePhim* headPhim) {
    printf("\n%-8s %-30s %-15s %-12s %s\n",
            "Ma", "Ten Phim", "The Loai", "Thoi Luong", "Gia Ve");
    printf("%s\n", string(72, '-').c_str());
    NodePhim* p = headPhim;
    while (p) {
        printf("%-8s %-30s %-15s %-9d %s  %.0f VND\n",
                p->data.ma.c_str(),
                p->data.ten.c_str(),
                p->data.theLoai.c_str(),
                p->data.thoiLuong,
                "phut",
                p->data.giaVe);
        p = p->next;
    }
    printf("%s\n", string(72, '=').c_str());
}

// ================================================================
// CHỨC NĂNG 4: TIM PHIM
// ================================================================
bool check_TimKiem(NodePhim* p, string maCanTim, string tenCanTim, double giaMin, double giaMax) {
    string maPhim = p->data.ma;
    string tenPhim = p->data.ten;
    
    // Chuyen du lieu trong node ve chu thuong de so sanh
    for (char &c : maPhim) c = tolower(c);
    for (char &c : tenPhim) c = tolower(c);

    // Kiem tra dieu kien: neu nguoi dung nhap rong thi bo qua dieu kien do
    bool khopMa = (maCanTim != "" && maPhim.find(maCanTim) != string::npos);
    bool khopTen = (tenCanTim != "" && tenPhim.find(tenCanTim) != string::npos);
    bool khopGia = (giaMin >= 0 && giaMax > giaMin)   &&   (p->data.giaVe >= giaMin && p->data.giaVe <= giaMax);

    // Neu thoa man tat ca dieu kien
    if (khopMa || khopTen || khopGia) {
        return true;
    }
    return false;
}

void DanhSach_TimKiem(NodePhim* head, string maCanTim, string tenCanTim, double giaMin, double giaMax) {
    for (char &c : maCanTim)  c = tolower(c);
    for (char &c : tenCanTim) c = tolower(c);

    int dem = 0;
    NodePhim* p = head;
    while (p != nullptr) {
        if (check_TimKiem(p, maCanTim, tenCanTim, giaMin, giaMax)) {
            if (dem == 0) {
                printf("\n%-8s %-30s %-15s %-12s %s\n",
                    "Ma", "Ten Phim", "The Loai", "Thoi Luong", "Gia Ve");
                printf("%s\n", string(72, '-').c_str());
            }
            printf("%-8s %-30s %-15s %-9d %s  %.0f VND\n",
                p->data.ma.c_str(),
                p->data.ten.c_str(),
                p->data.theLoai.c_str(),
                p->data.thoiLuong,
                "phut",
                p->data.giaVe);
            dem++;
        }
        p = p->next;
    }

    if (dem == 0){
        cout << "[!] Khong tim thay phim nao thoa man tieu chi!\n";
    }
    else {
        cout << "\n=> Tim thay " << dem << " phim.\n";
    }
}

// ================================================================
// CHỨC NĂNG 5: XOA PHIM
// ================================================================
bool KhopPhim(NodePhim* node, string MaCanXoa, string TenCanXoa) {
    string ma  = node->data.ma;
    string ten = node->data.ten;
    for (char &c : ma)  c = tolower(c);
    for (char &c : ten) c = tolower(c);

    bool maProvided  = !MaCanXoa.empty(); // kiem tra chui rong
    bool tenProvided = !TenCanXoa.empty();

    if (!maProvided && !tenProvided) return false;

    bool khopMa  = maProvided  && (ma.find(MaCanXoa)  != string::npos);
    bool khopTen = tenProvided && (ten.find(TenCanXoa) != string::npos);

    return khopMa || khopTen;
}

NodePhim* XoaPhim(NodePhim* &head, string MaCanXoa, string TenCanXoa) {
    if (head == nullptr) return nullptr;

    for (char &c : MaCanXoa) c = tolower(c);
    for (char &c : TenCanXoa) c = tolower(c);

    // Node dau tien khop
    if (KhopPhim(head, MaCanXoa, TenCanXoa)) {
        NodePhim* del = head;
        head = head->next;  
        return del;
    }

    NodePhim* p = head;
    while (p->next != nullptr) {
        if (KhopPhim(p->next, MaCanXoa, TenCanXoa)) {
            NodePhim* del = p->next;
            p->next = del->next; 
            return del;
        }
        p = p->next;
    }

    return nullptr; // Khong tim thay
}

// ================================================================
// CHỨC NĂNG 6: CẬP NHẬT THÔNG TIN PHIM
// ================================================================
void capNhatThongTinPhim(NodePhim* headPhim) {
    string ma;
    cout << "\n--- CAP NHAT THONG TIN PHIM ---\n";
    cout << "Nhap ma phim can cap nhat (vd: P01): ";
    cin >> ma;

    NodePhim* p = headPhim;
    while (p != nullptr) {
        if (p->data.ma == ma) {
            cout << "Da tim thay phim: " << p->data.ten << "\n";
            cout << "Nhap ten phim moi: ";
            cin.ignore();
            getline(cin, p->data.ten);
            cout << "Nhap the loai moi: ";
            getline(cin, p->data.theLoai);
            cout << "Nhap thoi luong moi (phut): ";
            cin >> p->data.thoiLuong;
            cout << "Nhap gia ve moi: ";
            cin >> p->data.giaVe;
            
            // Đồng bộ xuống file ngay sau khi cập nhật thành công
            ghiToanBoFile(FILE_DB, headPhim);
            cout << "=> Cap nhat thong tin phim va dong bo file thanh cong!\n";
            return;
        }
        p = p->next;
    }
    cout << "=> Khong tim thay phim co ma: " << ma << "\n";
}

// ================================================================
// CHỨC NĂNG 7: SẮP XẾP DANH SÁCH PHIM (Giá vé & Thời lượng)
// ================================================================
void sapXepTheoGiaVe(NodePhim* headPhim, bool giamDan) {
    if (headPhim == nullptr || headPhim->next == nullptr) return;

    bool swapped;
    NodePhim* ptr1;
    NodePhim* lptr = nullptr;

    do {
        swapped = false;
        ptr1 = headPhim;

        while (ptr1->next != lptr) {
            bool dieuKienDoi = giamDan ? (ptr1->data.giaVe < ptr1->next->data.giaVe)
                                       : (ptr1->data.giaVe > ptr1->next->data.giaVe);

            if (dieuKienDoi) {
                Phim temp = ptr1->data;
                ptr1->data = ptr1->next->data;
                ptr1->next->data = temp;
                swapped = true;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
}

void sapXepTheoThoiLuong(NodePhim* headPhim, bool giamDan) {
    if (headPhim == nullptr || headPhim->next == nullptr) return;

    bool swapped;
    NodePhim* ptr1;
    NodePhim* lptr = nullptr;

    do {
        swapped = false;
        ptr1 = headPhim;

        while (ptr1->next != lptr) {
            bool dieuKienDoi = giamDan ? (ptr1->data.thoiLuong < ptr1->next->data.thoiLuong)
                                       : (ptr1->data.thoiLuong > ptr1->next->data.thoiLuong);

            if (dieuKienDoi) {
                Phim temp = ptr1->data;
                ptr1->data = ptr1->next->data;
                ptr1->next->data = temp;
                swapped = true;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
}

void hienThiMenuSapXep(NodePhim* headPhim) {
    if (headPhim == nullptr) {
        cout << "Danh sach phim trống!\n";
        return;
    }
    cout << "\n--- SAP XEP DANH SACH PHIM ---\n";
    cout << "1. Gia ve tang dan (Thap -> Cao)\n";
    cout << "2. Gia ve giam dan (Cao -> Thap)\n";
    cout << "3. Thoi luong tang dan (Ngan -> Dai)\n";
    cout << "4. Thoi luong giam dan (Dai -> Ngan)\n";
    cout << "Chon tuy chon (1-4): ";
    string luaChon;
    cin >> luaChon;

    if (luaChon == "1") {
        sapXepTheoGiaVe(headPhim, false);
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> Đã sắp xếp theo giá vé TĂNG DẦN thành công!\n";
        xemDanhSachPhim(headPhim);
    } else if (luaChon == "2") {
        sapXepTheoGiaVe(headPhim, true);
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> Đã sắp xếp theo giá vé GIẢM DẦN thành công!\n";
        xemDanhSachPhim(headPhim);
    } else if (luaChon == "3") {
        sapXepTheoThoiLuong(headPhim, false);
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> Đã sắp xếp theo thời lượng TĂNG DẦN thành công!\n";
        xemDanhSachPhim(headPhim);
    } else if (luaChon == "4") {
        sapXepTheoThoiLuong(headPhim, true);
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> Đã sắp xếp theo thời lượng GIẢM DẦN thành công!\n";
        xemDanhSachPhim(headPhim);
    } else {
        cout << "=> Tuy chon khong hop le!\n";
    }
}

// ================================================================
// MAIN & MENU
// ================================================================

void hienThiMenu() {
    cout << "\n===== QUAN LY DAT VE XEM PHIM =====\n";
    cout << "  1. Them danh sach phim moi\n";
    cout << "  2. Xem danh sach phim\n";
    cout << "  4. Tim kiem phim\n";
    cout << "  5. Xoa phim\n";
    cout << "  6. Cap nhat thong tin phim\n";
    cout << "  7. Sap xep danh sach phim\n";
    cout << "  0. Thoat\n";
    cout << "====================================\n";
    cout << "Chon: ";
}

void khoiTaoHeThong(const string& file, NodePhim*& head, int& veKeTiep) {
    cout << "[System] Dang khoi dong va kiem tra co so du lieu...\n";

    // Bước 1: Kiểm tra xem file database có rỗng hoặc chưa tồn tại hay không
    if (kiemTraDBTrong(file)) {
        // Nghiệp vụ: Nếu DB trống thì báo cho nhân viên biết hệ thống chưa có phim nào
        cout << "[Thong bao] Co so du lieu hien dang TRONG (chua co phim nao)!\n";
        cout << "-> He thong san sang de ban nhap danh sach phim ban dau.\n";
        return; // Dừng khởi tạo sớm vì không có dữ liệu cũ để đọc
    }

    // Bước 2: Nếu Database ĐÃ CÓ DỮ LIỆU -> Kéo toàn bộ từ file text lên RAM
    docDanhSachPhim(file, head, veKeTiep);

    // Bước 3: Đếm số lượng phim thực tế đã nạp thành công vào bộ nhớ RAM
    int soPhim = 0;
    NodePhim* p = head;
    while (p != nullptr) {
        soPhim++;    // Tăng biến đếm qua từng node
        p = p->next; // Nhảy sang node tiếp theo
    }

    // Xuất thông báo sẵn sàng phục vụ
    cout << "[Init] Da keo thanh cong " << soPhim << " phim co san tu Database len RAM!\n";
}

int main() {
    NodePhim* headPhim = nullptr; // Con trỏ đầu danh sách liên kết quản lý toàn bộ phim trên RAM
    int veKeTiep = 1001;          // Bộ đếm mã số vé tự tăng (bắt đầu từ 1001)

    // --- BƯỚC 1: KHỞI TẠO HỆ THỐNG ---
    khoiTaoHeThong(FILE_DB, headPhim, veKeTiep);

    // --- BƯỚC 2: VÒNG LẶP MENU NGHIỆP VỤ ---
    string chon;
    while (true) {
        hienThiMenu();       // Xuất menu các chức năng ra màn hình
        getline(cin, chon);  // Đọc lựa chọn của người dùng

        if (chon == "1") {
            // Nghiệp vụ: Nhập danh sách phim mới
            nhapDanhSachPhim(headPhim);
        }
        else if (chon == "2") {
            // Nghiệp vụ: Xem danh sách phim dạng bảng
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong, vui long nhap phim truoc!\n";
            } else {
                xemDanhSachPhim(headPhim);
            }
        }
        else if (chon == "4"){
            string MaPhim, TenPhim;
            double giaMin, giaMax;
            cout << "======== Tim Kiem ========" << endl;
            cout << "[*] Muon tim theo thuoc tinh gi thi bo trong cac thuoc tinh khac" << endl;
            cout << "Ma phim : ";
            getline(cin, MaPhim);
            cout << "Ten Phim : ";
            getline(cin, TenPhim);
            cout << "gia Min - gia Max : ";
            cin >> giaMin >> giaMax;
            cin.ignore(1, '\n');
            cout << "============== KET QUA ==============" << endl;
            DanhSach_TimKiem(headPhim, MaPhim, TenPhim, giaMin, giaMax);
        }
        else if(chon == "5") {
            string TenCanXoa, MaCanXoa;
            cout << "---Xoa Phim--- \n[*] Tim theo ma thi bo trong ten va nguoc lai." << endl;
            cout << "Ma : ";
            getline(cin, MaCanXoa);
            cout << "Ten : ";
            getline(cin, TenCanXoa);

            // Lay du lieu xuong RAM
            NodePhim* kq = XoaPhim(headPhim, MaCanXoa, TenCanXoa);

            // in KQ
            cout << "\n======== KET QUA ========\n";
            if (kq != nullptr) {
                printf("\n%-8s %-30s %-15s %-12s %s\n", 
                    "Ma", "Ten Phim", "The Loai", "Thoi Luong", "Gia Ve");
                printf("%-8s %-30s %-15s %-9d %s  %.0f VND\n",
                        kq->data.ma.c_str(),
                        kq->data.ten.c_str(),
                        kq->data.theLoai.c_str(),
                        kq->data.thoiLuong,
                        "phut",
                        kq->data.giaVe);
                
                    // Tra du lieu ve file
                    ghiToanBoFile(FILE_DB, headPhim);
                    cout << "[Thanh cong] Da xoa va dong bo lai vao file Database!\n";
                    delete kq;
            } 
            else {
                cout << "[That bai] Khong tim thay phim de xoa!\n";
            }
        }
        else if (chon == "6") {
            // Nghiệp vụ: Cập nhật thông tin phim
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong!\n";
            } else {
                capNhatThongTinPhim(headPhim);
            }
        }
        else if (chon == "7") {
            // Nghiệp vụ: Sắp xếp danh sách phim
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong!\n";
            } else {
                hienThiMenuSapXep(headPhim);
            }
        }
        else if (chon == "0") {
            // Nghiệp vụ: Thoát ứng dụng an toàn, ghi đè lại toàn bộ dữ liệu xuống đĩa
            ghiToanBoFile(FILE_DB, headPhim);
            cout << "Da dong bo du lieu an toan xuong dia. Tam biet!\n";
            break; 
        }
    }

    // --- BƯỚC 3: DỌN DẸP BỘ NHỚ TRƯỚC KHI KẾT THÚC ---
    giaiPhong(headPhim);

    return 0;
}