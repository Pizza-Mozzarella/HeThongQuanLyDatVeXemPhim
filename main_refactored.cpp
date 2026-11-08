// ================================================================
// DỰ ÁN: HỆ THỐNG QUẢN LÝ ĐẶT VÉ XEM PHIM (MOVIE BOOKING SYSTEM)
// CẤU TRÚC DỮ LIỆU: DANH SÁCH LIÊN KẾT ĐƠN (SINGLY LINKED LIST)
// PHIÊN BẢN REFACTOR: TỔ CHỨC LẠI BỐ CỤC MÃ NGUỒN CHUẨN MỰC
// ================================================================

// ================================================================
// 1. KHAI BÁO THƯ VIỆN (LIBRARIES)
// ================================================================
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// ================================================================
// 2. HẰNG SỐ HỆ THỐNG (CONSTANTS)
// ================================================================
const int SO_HANG = 5;                  // Hàng A -> E (chỉ số 0..4)
const int SO_COT  = 6;                  // Cột 1 -> 6 (chỉ số 0..5)
const int TONG_GHE = SO_HANG * SO_COT;  // Tổng số ghế phòng chiếu = 30
const string FILE_DB = "cinema_db.txt"; // Tệp tin cơ sở dữ liệu lưu trữ

// ================================================================
// 3. CẤU TRÚC DỮ LIỆU (STRUCTS)
// ================================================================

// Thông tin vé xem phim
struct MaVe {
    int    soVe;      // 0 = chưa đặt, >= 1001 = mã số vé đã đặt
    string tenKhach;  // Họ và tên khách hàng
    string sdt;       // Số điện thoại liên hệ
};

// Trạng thái của một ô ghế trong phòng chiếu
struct ThongTinGhe {
    bool  daDat;      // false = ghế trống, true = ghế đã có người đặt
    MaVe  ve;         // Dữ liệu vé đi kèm (chỉ có nghĩa khi daDat == true)
};

// Thông tin một bộ phim và toàn bộ sơ đồ 30 ghế của phòng chiếu
struct Phim {
    string       ma;                    // Mã phim định danh duy nhất (VD: "P01")
    string       ten;                   // Tên bộ phim
    string       theLoai;               // Thể loại phim
    int          thoiLuong;             // Thời lượng chiếu (phút)
    double       giaVe;                 // Đơn vị giá vé (VND)
    ThongTinGhe  ghe[SO_HANG][SO_COT]; // Ma trận ghế 5 hàng x 6 cột
};

// Cấu trúc một Node trong Danh sách liên kết đơn
struct NodePhim {
    Phim      data;   // Dữ liệu bộ phim chứa trong node
    NodePhim* next;   // Con trỏ liên kết trỏ tới node kế tiếp
};

// Cấu trúc node BST
struct NodeBST {
    NodePhim* phim;   // Trỏ đến node phim trong linked list
    NodeBST* left;
    NodeBST* right;
};

typedef NodeBST* Tree;

// Thống kê - Lưu các tổng và mức cao/thấp, không sao chép dữ liệu phim.
struct ThongKePhim {
    int tongPhim;
    int tongVe;
    double tongDoanhThu;
    int veNhieuNhat;
    int veItNhat;
    double doanhThuCaoNhat;
    double doanhThuThapNhat;
};

// Dòng hiển thị tạm: chỉ giữ con trỏ phim và số vé đã đếm.
struct DongThongKe {
    NodePhim* phim;
    int soVe;
};

// ================================================================
// 4. KHAI BÁO NGUYÊN MẪU HÀM (FUNCTION PROTOTYPES)
// ================================================================

// --- 4.1. Hàm tiện ích cơ bản & Kiểm tra hợp lệ (Basic Helpers & Validation) ---
string chuyenChuThuong(string s);
string nhapChuoi(string thongBao);
int nhapSoNguyen(string thongBao, int minVal, int maxVal);
double nhapSoThuc(string thongBao, double minVal, double maxVal);
bool kiemTraTrungMa(NodePhim* head, string ma);
NodePhim* timPhimTheoMa(NodePhim* head, string ma);
void inTieuDeBang();
void inDongPhim(const Phim& p);
void giaiPhong(NodePhim*& head);

// --- 4.2. Hàm thao tác Cơ sở dữ liệu (Database Operations) ---
bool kiemTraDBTrong(const string& file);
string taoGheDong(int so, ThongTinGhe ghe);
void docDanhSachPhim(const string& file, NodePhim*& head, int& veKeTiep);
void ghiToanBoFile(const string& file, NodePhim* head);

// --- 4.3. Các hàm nghiệp vụ CRUD ---
// Chức năng 1: Thêm phim
void themPhim(NodePhim*& head, Phim p);
Phim nhapMotPhim(NodePhim* head);
void nhapDanhSachPhim(NodePhim*& head);

// Chức năng 2: Xem danh sách
void xemDanhSachPhim(NodePhim* headPhim);

// Chức năng 3: Tìm kiếm phim
bool timTheoMa(NodePhim* p, string maCanTim);
bool timTheoTen(NodePhim* p, string tenCanTim);
bool timTheoGia(NodePhim* p, double giaMin, double giaMax);
void inDanhSachKetQua(NodePhim* head, string maCanTim, string tenCanTim, double giaMin, double giaMax);
void hienMenuTimKiem(NodePhim* head);

// Chức năng 4: Xóa phim
bool khopPhim(NodePhim* node, string maCanXoa, string tenCanXoa);
NodePhim* xoaPhim(NodePhim*& head, string maCanXoa, string tenCanXoa);
void hienMenuXoaPhim(NodePhim*& headPhim);

// Chức năng 5: Cập nhật thông tin
void capNhatThongTinPhim(NodePhim* headPhim);

// Chức năng 6: Sắp xếp danh sách
void sapXepDanhSachPhim(NodePhim*& head, bool giamDan, bool laGiaVe);
void hienThiMenuSapXep(NodePhim* headPhim);

// Chức năng 7 & 8: Nghiệp vụ phòng vé (Đặt vé & Hủy vé)
void xemSoDoGhe(NodePhim* p);
void datVe(NodePhim* headPhim, int& veKeTiep);
void huyVe(NodePhim* headPhim);
void hienMenuDatVeHuyVe(NodePhim* headPhim, int& veKeTiep);

// BST - Chức năng 12: Tìm kiếm nhanh theo mã phim
void khoiTaoCay(Tree& root);
int soSanhMa(string a, string b);
int chenNodeBST(NodePhim* phim, Tree& root);
void giaiPhongCay(Tree& root);
int taoCayTuDanhSach(NodePhim* head, Tree& root);
NodePhim* timPhimBST(const string& ma, Tree root);
string chuanHoaMaTimKiem(string ma);
void duyetLNR(Tree root);
void hienMenuTimKiemNhanh(Tree root);

// Thống kê - Chức năng 11: Thống kê đặt vé và tỷ lệ lấp đầy
int demVeDaDat(const Phim& phim);
ThongKePhim thuThapThongKe(NodePhim* head);
void inDongThongKe(const Phim& phim, int soVe);
void sapXepThongKeTheoLapDay(DongThongKe* danhSach, int soPhim);
void inHangTongKet(const string& tieuChi, double giaTri, const string& donVi, const string& dsPhim);
void inPhimTheoThongKe(NodePhim* head, const ThongKePhim& thongKe);
void hienThongKePhim(NodePhim* headPhim);

// --- 4.4. Hàm điều khiển hệ thống & Menu ---
void hienThiMenu();
void khoiTaoHeThong(const string& file, NodePhim*& head, int& veKeTiep);

// ================================================================
// 5. CÁC HÀM TIỆN ÍCH CƠ BẢN NHẤT (ATOMIC / REUSABLE / VALIDATION)
// (Các hàm nhỏ nhất, không thể chia nhỏ hơn, dùng làm nền tảng tái sử dụng)
// ================================================================

// Chuyển toàn bộ chuỗi ký tự về chữ thường (lowercase) phục vụ so sánh chuỗi
string chuyenChuThuong(string s) {
    for (char& c : s) {
        c = tolower(c);
    }
    return s;
}

// Nhập chuỗi ký tự an toàn, bắt buộc không được để trống (chống trôi lệnh cin)
string nhapChuoi(string thongBao) {
    string s;
    while (true) {
        cout << thongBao;
        getline(cin, s);
        if (!s.empty()) {
            return s;
        }
        cout << "  [!] Thong tin khong duoc bo trong. Vui long nhap lai!\n";
    }
}

// Nhập số nguyên an toàn trong đoạn [minVal, maxVal] (chống crash khi nhập chữ cái)
int nhapSoNguyen(string thongBao, int minVal, int maxVal) {
    string s;
    while (true) {
        cout << thongBao;
        getline(cin, s);

        stringstream ss(s);
        int val;
        if (ss >> val && ss.eof()) {
            if (val >= minVal && val <= maxVal) {
                return val;
            }
            cout << "  [!] Gia tri phai nam trong khoang [" << minVal << " - " << maxVal << "]!\n";
        } else {
            cout << "  [!] Dinh dang khong hop le! Vui long nhap so nguyen.\n";
        }
    }
}

// Nhập số thực an toàn trong đoạn [minVal, maxVal] (áp dụng cho đơn giá vé)
double nhapSoThuc(string thongBao, double minVal, double maxVal) {
    string s;
    while (true) {
        cout << thongBao;
        getline(cin, s);

        stringstream ss(s);
        double val;
        if (ss >> val && ss.eof()) {
            if (val >= minVal && val <= maxVal) {
                return val;
            }
            cout << "  [!] Gia ve phai tu " << (long long)minVal << " den " << (long long)maxVal << " VND!\n";
        } else {
            cout << "  [!] Dinh dang khong hop le! Vui long nhap dung so thuc.\n";
        }
    }
}

// Tìm con trỏ NodePhim theo mã phim (so sánh không phân biệt hoa/thường, khớp chính xác mã)
NodePhim* timPhimTheoMa(NodePhim* head, string ma) {
    if (ma.empty()) return nullptr;
    string maTim = chuyenChuThuong(ma);
    NodePhim* p = head;
    while (p != nullptr) {
        if (chuyenChuThuong(p->data.ma) == maTim) {
            return p;
        }
        p = p->next;
    }
    return nullptr;
}

// Kiểm tra tính duy nhất của mã phim trong danh sách liên kết (chống trùng khóa chính)
bool kiemTraTrungMa(NodePhim* head, string ma) {
    return timPhimTheoMa(head, ma) != nullptr;
}

// In dòng tiêu đề chuẩn cho bảng hiển thị danh sách phim
void inTieuDeBang() {
    printf("\n%-8s %-40s %-24s %-14s %-14s\n", "Ma", "Ten Phim", "The Loai", "Thoi Luong", "Gia Ve");
    printf("%s\n", string(104, '-').c_str());
}

// In một dòng dữ liệu của bộ phim ra bảng theo đúng định dạng cột (căn lề rộng rãi, không bị xô lệch)
void inDongPhim(const Phim& p) {
    string thoiLuongStr = to_string(p.thoiLuong) + " phut";
    string giaVeStr     = to_string((long long)p.giaVe) + " VND";
    printf("%-8s %-40s %-24s %-14s %-14s\n",
           p.ma.c_str(),
           p.ten.c_str(),
           p.theLoai.c_str(),
           thoiLuongStr.c_str(),
           giaVeStr.c_str());
}

// Giải phóng toàn bộ bộ nhớ RAM của Danh sách liên kết khi kết thúc chương trình
void giaiPhong(NodePhim*& head) {
    while (head != nullptr) {
        NodePhim* t = head;
        head = head->next;
        delete t;
    }
}

// ================================================================
// 6. THAO TÁC CƠ SỞ DỮ LIỆU (DATABASE OPERATIONS - FILE I/O)
// ================================================================

// Kiểm tra tệp cơ sở dữ liệu có dữ liệu hay đang rỗng
bool kiemTraDBTrong(const string& file) {
    ifstream f(file);
    if (!f.is_open()) {
        return true; // File chưa tồn tại -> coi như rỗng
    }

    string dong;
    while (getline(f, dong)) {
        if (!dong.empty() && dong.find_first_not_of(" \t\r\n") != string::npos) {
            f.close();
            return false; // File có dữ liệu
        }
    }

    f.close();
    return true; // File rỗng 0 byte
}

// Chuyển đổi trạng thái một ô ghế thành định dạng văn bản để ghi file
string taoGheDong(int so, ThongTinGhe ghe) {
    string soStr = (so < 10 ? "0" : "") + to_string(so);
    if (!ghe.daDat) {
        return soStr + "|O"; // Ghế trống
    }
    return soStr + "|X|" + to_string(ghe.ve.soVe) + "|" + ghe.ve.tenKhach + "|" + ghe.ve.sdt;
}

// Đọc toàn bộ danh sách phim và tình trạng ghế từ tệp text nạp lên RAM
void docDanhSachPhim(const string& file, NodePhim*& head, int& veKeTiep) {
    ifstream f(file);
    if (!f.is_open()) return;

    string dong;
    NodePhim* node = nullptr;

    while (getline(f, dong)) {
        if (!dong.empty() && dong.back() == '\r') dong.pop_back();
        if (dong.empty()) continue;

        if (dong[0] == '#') {
            // Header phim: #P01|Avatar|Hanh Dong|192|90000
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

            // Khởi tạo 30 ô ghế trống ban đầu
            for (int r = 0; r < SO_HANG; r++) {
                for (int c = 0; c < SO_COT; c++) {
                    p.ghe[r][c] = { false, {0, "", ""} };
                }
            }

            themPhim(head, p);

            // Con trỏ giữ node vừa thêm để tiếp tục nạp 30 ghế bên dưới
            node = head;
            while (node->next) node = node->next;
        } else {
            // Dòng dữ liệu ghế ngồi
            if (!node) continue;
            stringstream ss(dong);
            string soStr, trangThai;
            getline(ss, soStr,     '|');
            getline(ss, trangThai, '|');

            if (trangThai == "X") {
                string soVeStr, tenKhach, sdt;
                getline(ss, soVeStr,  '|');
                getline(ss, tenKhach, '|');
                getline(ss, sdt);

                int so = stoi(soStr);
                int r  = (so - 1) / SO_COT;
                int c  = (so - 1) % SO_COT;
                int soVe = stoi(soVeStr);

                node->data.ghe[r][c] = { true, {soVe, tenKhach, sdt} };
                if (soVe >= veKeTiep) veKeTiep = soVe + 1; // Duy trì mã vé tự tăng
            }
        }
    }
    f.close();
}

// Ghi đè toàn bộ danh sách liên kết từ RAM xuống tệp tin cơ sở dữ liệu
void ghiToanBoFile(const string& file, NodePhim* head) {
    ofstream f(file);
    NodePhim* p = head;

    while (p != nullptr) {
        // Ghi tiêu đề phim
        f << "#" << p->data.ma << "|" << p->data.ten << "|"
                 << p->data.theLoai << "|" << p->data.thoiLuong << "|"
                 << p->data.giaVe << "\n";

        // Ghi tuần tự 30 ghế
        for (int r = 0; r < SO_HANG; r++) {
            for (int c = 0; c < SO_COT; c++) {
                int so = r * SO_COT + c + 1;
                f << taoGheDong(so, p->data.ghe[r][c]) << "\n";
            }
        }
        p = p->next;
    }
    f.close();
}

// ================================================================
// 7. CÁC CHỨC NĂNG NGHIỆP VỤ CRUD
// ================================================================

// ----------------------------------------------------------------
// 7.1. NHẬP & THÊM PHIM MỚI (CREATE)
// ----------------------------------------------------------------

// Thêm một node phim mới vào cuối danh sách liên kết
void themPhim(NodePhim*& head, Phim p) {
    NodePhim* node = new NodePhim{ p, nullptr };
    if (head == nullptr) {
        head = node;
        return;
    }
    NodePhim* t = head;
    while (t->next != nullptr) {
        t = t->next;
    }
    t->next = node;
}

// Nhập chi tiết một bộ phim, kiểm tra trùng mã và khởi tạo 30 ghế trống
Phim nhapMotPhim(NodePhim* head) {
    Phim p{};

    // Bước 1: Nhập và kiểm tra mã phim duy nhất
    while (true) {
        p.ma = nhapChuoi("  + Nhap ma phim (VD: P05): ");
        if (kiemTraTrungMa(head, p.ma)) {
            cout << "  [!] Ma phim '" << p.ma << "' DA TON TAI! Vui long dung ma khac.\n";
        } else {
            break;
        }
    }

    // Bước 2: Nhập thông tin chi tiết qua các hàm validation
    p.ten       = nhapChuoi("  + Nhap ten phim: ");
    p.theLoai   = nhapChuoi("  + Nhap the loai: ");
    p.thoiLuong = nhapSoNguyen("  + Nhap thoi luong (15 - 360 phut): ", 15, 360);
    p.giaVe     = nhapSoThuc("  + Nhap gia ve (10,000 - 1,000,000 VND): ", 10000, 1000000);

    // Bước 3: Khởi tạo 30 ô ghế trống cho phim mới
    for (int r = 0; r < SO_HANG; r++) {
        for (int c = 0; c < SO_COT; c++) {
            p.ghe[r][c].daDat = false;
            p.ghe[r][c].ve = {0, "", ""};
        }
    }

    return p;
}

// Nhập danh sách nhiều phim liên tiếp và đồng bộ xuống tệp CSDL
void nhapDanhSachPhim(NodePhim*& head) {
    cout << "\n========================================\n";
    cout << "        NHAP DANH SACH PHIM MOI          \n";
    cout << "========================================\n";

    int dem = 0;
    while (true) {
        dem++;
        cout << "\n>> Nhap thong tin phim thu " << dem << ":\n";

        Phim p = nhapMotPhim(head);
        themPhim(head, p);

        cout << "=> Da them tam thoi vao RAM: [" << p.ma << " - " << p.ten << "]\n";

        string tiep = nhapChuoi("\nBan co muon nhap them phim nua khong? (y/n): ");
        if (tiep != "y" && tiep != "Y") {
            break;
        }
    }

    // Đồng bộ toàn bộ dữ liệu xuống đĩa
    cout << "\n[Dang luu...] Dang ghi de du lieu moi vao " << FILE_DB << "...\n";
    ghiToanBoFile(FILE_DB, head);

    cout << "[Thanh cong] Da them " << dem << " phim va DONG BO 100% vao Database!\n";
    cout << "========================================\n";
}

// ----------------------------------------------------------------
// 7.2. HIỂN THỊ DANH SÁCH PHIM DẠNG BẢNG (READ)
// ----------------------------------------------------------------
void xemDanhSachPhim(NodePhim* headPhim) {
    inTieuDeBang();
    NodePhim* p = headPhim;
    while (p != nullptr) {
        inDongPhim(p->data);
        p = p->next;
    }
    printf("%s\n", string(104, '=').c_str());
}

// ----------------------------------------------------------------
// 7.3. TÌM KIẾM PHIM ĐA TIÊU CHÍ (SEARCH)
// ----------------------------------------------------------------

// Kiểm tra trùng khớp mã phim (tìm kiếm gần đúng, không phân biệt hoa thường)
bool timTheoMa(NodePhim* p, string maCanTim) {
    if (maCanTim.empty()) return false;
    string maPhim = chuyenChuThuong(p->data.ma);
    string maTim  = chuyenChuThuong(maCanTim);
    return maPhim.find(maTim) != string::npos;
}

// Kiểm tra trùng khớp tên phim (tìm kiếm chuỗi con không phân biệt hoa thường)
bool timTheoTen(NodePhim* p, string tenCanTim) {
    if (tenCanTim.empty()) return false;
    string tenPhim = chuyenChuThuong(p->data.ten);
    string tenTim  = chuyenChuThuong(tenCanTim);
    return tenPhim.find(tenTim) != string::npos;
}

// Kiểm tra phim có nằm trong khoảng giá vé [giaMin, giaMax]
bool timTheoGia(NodePhim* p, double giaMin, double giaMax) {
    if (giaMin < 0 || giaMax <= giaMin) return false;
    return (p->data.giaVe >= giaMin && p->data.giaVe <= giaMax);
}

// In danh sách các phim thỏa mãn tiêu chí tìm kiếm
void inDanhSachKetQua(NodePhim* head, string maCanTim, string tenCanTim, double giaMin, double giaMax) {
    int dem = 0;
    NodePhim* p = head;

    while (p != nullptr) {
        bool khop = timTheoMa(p, maCanTim) || timTheoTen(p, tenCanTim) || timTheoGia(p, giaMin, giaMax);
        if (khop) {
            if (dem == 0) {
                inTieuDeBang();
            }
            inDongPhim(p->data);
            dem++;
        }
        p = p->next;
    }

    if (dem == 0) {
        cout << "[!] Khong tim thay phim nao thoa man tieu chi!\n";
    } else {
        printf("%s\n", string(104, '=').c_str());
        cout << "=> Tim thay tong cong " << dem << " phim.\n";
    }
}

// Menu điều phối tìm kiếm phim
void hienMenuTimKiem(NodePhim* head) {
    if (head == nullptr) {
        cout << "[!] Danh sach phim hien dang trong, vui long nhap phim truoc!\n";
        return;
    }

    cout << "\n======== TIM KIEM PHIM ========\n";
    cout << "   1. Tim theo ma phim\n";
    cout << "   2. Tim theo ten phim\n";
    cout << "   3. Tim theo khoang gia ve\n";
    cout << "   0. Quay lai menu chinh\n";
    cout << "================================\n";

    string maCanTim = "", tenCanTim = "";
    double giaMin = -1, giaMax = -1;

    string chonTimKiem = nhapChuoi("   Chon: ");

    if (chonTimKiem == "0") {
        cout << "=> Tro ve menu chinh.\n";
        return;
    } else if (chonTimKiem == "1") {
        maCanTim = nhapChuoi("   Nhap ma phim can tim: ");
    } else if (chonTimKiem == "2") {
        tenCanTim = nhapChuoi("   Nhap ten phim can tim: ");
    } else if (chonTimKiem == "3") {
        giaMin = nhapSoThuc("   Nhap gia Min (VND): ", 0, 1000000);
        giaMax = nhapSoThuc("   Nhap gia Max (VND): ", giaMin, 1000000);
    } else {
        cout << "[!] Tuy chon khong hop le!\n";
        return;
    }

    cout << "\n======== KET QUA TIM KIEM ========\n";
    inDanhSachKetQua(head, maCanTim, tenCanTim, giaMin, giaMax);
}

// ----------------------------------------------------------------
// 7.4. XÓA PHIM (DELETE)
// ----------------------------------------------------------------

// Kiểm tra bộ phim có khớp với mã hoặc tên cần xóa không
bool khopPhim(NodePhim* node, string maCanXoa, string tenCanXoa) {
    if (maCanXoa.empty() && tenCanXoa.empty()) return false;

    string ma  = chuyenChuThuong(node->data.ma);
    string ten = chuyenChuThuong(node->data.ten);
    string maTim  = chuyenChuThuong(maCanXoa);
    string tenTim = chuyenChuThuong(tenCanXoa);

    bool khopMa  = !maCanXoa.empty()  && (ma == maTim);
    bool khopTen = !tenCanXoa.empty() && (ten.find(tenTim)  != string::npos);

    return khopMa || khopTen;
}

// Tách node cần xóa ra khỏi danh sách liên kết đơn (xử lý cả ca đầu, giữa, cuối)
NodePhim* xoaPhim(NodePhim*& head, string maCanXoa, string tenCanXoa) {
    if (head == nullptr) return nullptr;

    // Ca biên 1: Node cần xóa nằm ngay đầu danh sách
    if (khopPhim(head, maCanXoa, tenCanXoa)) {
        NodePhim* del = head;
        head = head->next;
        return del;
    }

    // Ca biên 2: Node cần xóa nằm ở giữa hoặc cuối danh sách
    NodePhim* p = head;
    while (p->next != nullptr) {
        if (khopPhim(p->next, maCanXoa, tenCanXoa)) {
            NodePhim* del = p->next;
            p->next = del->next;
            return del;
        }
        p = p->next;
    }

    return nullptr;
}

// Menu điều phối chức năng xóa phim (có xác nhận y/n an toàn)
void hienMenuXoaPhim(NodePhim*& headPhim) {
    if (headPhim == nullptr) {
        cout << "[!] Danh sach phim hien dang trong, khong co gi de xoa!\n";
        return;
    }

    cout << "\n======== XOA PHIM ========\n";
    cout << "   1. Xoa theo ma phim\n";
    cout << "   2. Xoa theo ten phim\n";
    cout << "   0. Quay lai menu chinh\n";
    cout << "==========================\n";

    string chonXoa = nhapChuoi("   Chon: ");
    string maCanXoa = "", tenCanXoa = "";

    if (chonXoa == "0") {
        cout << "=> Tro ve menu chinh.\n";
        return;
    } else if (chonXoa == "1") {
        maCanXoa = nhapChuoi("   Nhap ma phim can xoa: ");
    } else if (chonXoa == "2") {
        tenCanXoa = nhapChuoi("   Nhap ten phim can xoa: ");
    } else {
        cout << "[!] Tuy chon khong hop le!\n";
        return;
    }

    // Tìm kiếm xem phim có tồn tại không trước khi hỏi xác nhận
    NodePhim* kq = nullptr;
    NodePhim* p  = headPhim;
    while (p != nullptr) {
        if (khopPhim(p, maCanXoa, tenCanXoa)) {
            kq = p;
            break;
        }
        p = p->next;
    }

    if (kq == nullptr) {
        cout << "[!] Khong tim thay phim nao khop tieu chi de xoa!\n";
        return;
    }

    cout << "\n[Phim tim thay can xoa]\n";
    inTieuDeBang();
    inDongPhim(kq->data);
    printf("%s\n", string(104, '=').c_str());

    // Xác nhận an toàn trước khi xóa dữ liệu vĩnh viễn
    string xacNhan = nhapChuoi("Ban co CHAC CHAN muon xoa phim nay? (y/n): ");
    if (xacNhan != "y" && xacNhan != "Y") {
        cout << "=> Da huy thao tac xoa. Phim duoc giu nguyen!\n";
        return;
    }

    // Thực hiện ngắt liên kết node và giải phóng vùng nhớ
    NodePhim* del = xoaPhim(headPhim, maCanXoa, tenCanXoa);
    if (del != nullptr) {
        cout << "=> [Thanh cong] Da xoa phim [" << del->data.ma << " - " << del->data.ten << "]!\n";
        delete del;

        // Cập nhật lại toàn bộ file database
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> Da dong bo lai vao file Database an toan!\n";
    }
}

// ----------------------------------------------------------------
// 7.5. CẬP NHẬT THÔNG TIN PHIM (UPDATE)
// ----------------------------------------------------------------
void capNhatThongTinPhim(NodePhim* headPhim) {
    cout << "\n--- CAP NHAT THONG TIN PHIM ---\n";
    cout << "Huong dan: Nhap '0' neu muon huy thao tac.\n";

    string ma = nhapChuoi("Nhap ma phim can cap nhat (VD: P01): ");
    if (ma == "0") {
        cout << "=> Da huy thao tac cap nhat.\n";
        return;
    }

    NodePhim* p = timPhimTheoMa(headPhim, ma);
    if (p == nullptr) {
        cout << "=> [!] Khong tim thay phim co ma: " << ma << "\n";
        return;
    }

    cout << "\n[Thong tin phim hien tai]\n";
    cout << "- Ten phim     : " << p->data.ten << "\n";
    cout << "- The loai     : " << p->data.theLoai << "\n";
    cout << "- Thoi luong   : " << p->data.thoiLuong << " phut\n";
    cout << "- Gia ve       : " << (long long)p->data.giaVe << " VND\n";
    cout << "----------------------------------------\n";
    cout << "Ban co muon thay doi cac thong tin sau khong? (Nhap y/n)\n";

    bool coThayDoi = false;
    string traLoi;

    // 1. Cập nhật tên phim
    traLoi = nhapChuoi("-> Doi ten phim moi? (y/n): ");
    if (traLoi == "y" || traLoi == "Y") {
        p->data.ten = nhapChuoi("   Nhap ten phim moi: ");
        coThayDoi = true;
    }

    // 2. Cập nhật thể loại
    traLoi = nhapChuoi("-> Doi the loai moi? (y/n): ");
    if (traLoi == "y" || traLoi == "Y") {
        p->data.theLoai = nhapChuoi("   Nhap the loai moi: ");
        coThayDoi = true;
    }

    // 3. Cập nhật thời lượng
    traLoi = nhapChuoi("-> Doi thoi luong moi? (y/n): ");
    if (traLoi == "y" || traLoi == "Y") {
        p->data.thoiLuong = nhapSoNguyen("   Nhap thoi luong moi (15 - 360 phut): ", 15, 360);
        coThayDoi = true;
    }

    // 4. Cập nhật giá vé
    traLoi = nhapChuoi("-> Doi gia ve moi? (y/n): ");
    if (traLoi == "y" || traLoi == "Y") {
        p->data.giaVe = nhapSoThuc("   Nhap gia ve moi (10,000 - 1,000,000 VND): ", 10000, 1000000);
        coThayDoi = true;
    }

    if (coThayDoi) {
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> [Thanh cong] Cap nhat thong tin va DONG BO file thanh cong!\n";
    } else {
        cout << "=> Khong co thong tin nao bi thay doi.\n";
    }
}

// ----------------------------------------------------------------
// 7.6. SẮP XẾP DANH SÁCH PHIM (SORT)
// ----------------------------------------------------------------

// Thuật toán Bubble Sort sắp xếp danh sách liên kết đơn bằng cách hoán đổi data
void sapXepDanhSachPhim(NodePhim*& head, bool giamDan, bool laGiaVe) {
    if (head == nullptr || head->next == nullptr) return;

    bool swapped;
    NodePhim* ptr1;
    NodePhim* lptr = nullptr;

    do {
        swapped = false;
        ptr1 = head;

        while (ptr1->next != lptr) {
            NodePhim* ptr2 = ptr1->next;

            double val1 = laGiaVe ? ptr1->data.giaVe : ptr1->data.thoiLuong;
            double val2 = laGiaVe ? ptr2->data.giaVe : ptr2->data.thoiLuong;

            bool dieuKienDoi = giamDan ? (val1 < val2) : (val1 > val2);

            if (dieuKienDoi) {
                Phim temp = ptr1->data;
                ptr1->data = ptr2->data;
                ptr2->data = temp;
                swapped = true;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
}

// Menu điều phối các tiêu chí sắp xếp danh sách phim
void hienThiMenuSapXep(NodePhim* headPhim) {
    if (headPhim == nullptr) {
        cout << "[!] Danh sach phim hien dang trong, chua co du lieu de sap xep!\n";
        return;
    }

    cout << "\n--- SAP XEP DANH SACH PHIM ---\n";
    cout << "1. Gia ve tang dan (Thap -> Cao)\n";
    cout << "2. Gia ve giam dan (Cao -> Thap)\n";
    cout << "3. Thoi luong tang dan (Ngan -> Dai)\n";
    cout << "4. Thoi luong giam dan (Dai -> Ngan)\n";
    cout << "0. Quay lai menu chinh\n";

    string luaChon = nhapChuoi("Chon tuy chon (0-4): ");

    if (luaChon == "0") {
        cout << "=> Tro ve menu chinh.\n";
        return;
    }

    bool daXuLy = true;
    if (luaChon == "1") {
        sapXepDanhSachPhim(headPhim, false, true);  // Giá vé tăng dần
    } else if (luaChon == "2") {
        sapXepDanhSachPhim(headPhim, true, true);   // Giá vé giảm dần
    } else if (luaChon == "3") {
        sapXepDanhSachPhim(headPhim, false, false); // Thời lượng tăng dần
    } else if (luaChon == "4") {
        sapXepDanhSachPhim(headPhim, true, false);  // Thời lượng giảm dần
    } else {
        cout << "=> [!] Tuy chon khong hop le!\n";
        daXuLy = false;
    }

    if (daXuLy) {
        ghiToanBoFile(FILE_DB, headPhim);
        cout << "=> Da sap xep va DONG BO file thanh cong!\n";
        xemDanhSachPhim(headPhim);
    }
}

// ----------------------------------------------------------------
// 7.7. NGHIỆP VỤ PHÒNG VÉ: ĐẶT VÉ & HỦY VÉ (TICKETING)
// ----------------------------------------------------------------

// Hiển thị trực quan sơ đồ 30 ghế (5 hàng x 6 cột) của 1 bộ phim
void xemSoDoGhe(NodePhim* p) {
    if (p == nullptr) return;

    cout << "\n==================================================================\n";
    cout << "  SO DO PHONG CHIEU: " << p->data.ten << " (" << p->data.ma << ")\n";
    cout << "==================================================================\n";
    cout << "                    [ MAN HINH CHIEU (SCREEN) ]                   \n";
    cout << "------------------------------------------------------------------\n";
    cout << "        Cot 1   Cot 2   Cot 3   Cot 4   Cot 5   Cot 6\n";

    char tenHang = 'A';
    for (int r = 0; r < SO_HANG; r++) {
        cout << "Hang " << (char)(tenHang + r) << "  ";
        for (int c = 0; c < SO_COT; c++) {
            int soGhe = r * SO_COT + c + 1;
            if (p->data.ghe[r][c].daDat) {
                cout << " [ X]  ";
            } else {
                printf(" [%02d]  ", soGhe);
            }
        }
        cout << "\n\n";
    }
    cout << "Chu thich: [So]: Ghe con trong (co the dat)  |  [ X]: Ghe da dat\n";
    cout << "Gia ve   : " << (long long)p->data.giaVe << " VND / ghe\n";
    cout << "------------------------------------------------------------------\n";
}

// Đặt vé xem phim: chọn phim -> xem ghế -> chọn ghế -> nhập khách -> cấp vé -> lưu CSDL
void datVe(NodePhim* headPhim, int& veKeTiep) {
    if (headPhim == nullptr) {
        cout << "[!] He thong chua co phim nao de dat ve!\n";
        return;
    }

    cout << "\n========================================\n";
    cout << "           DAT VE XEM PHIM              \n";
    cout << "========================================\n";

    string maPhim = nhapChuoi("Nhap ma phim ban muon dat ve (VD: P01): ");
    NodePhim* p = timPhimTheoMa(headPhim, maPhim);

    if (p == nullptr) {
        cout << "  [!] Khong tim thay phim co ma: " << maPhim << "\n";
        return;
    }

    // Hiển thị sơ đồ ghế để khách dễ dàng lựa chọn
    xemSoDoGhe(p);

    int soGhe, r, c;
    while (true) {
        soGhe = nhapSoNguyen("Nhap so ghe ban muon dat (1 - 30): ", 1, TONG_GHE);
        r = (soGhe - 1) / SO_COT;
        c = (soGhe - 1) % SO_COT;

        if (p->data.ghe[r][c].daDat) {
            cout << "  [!] Ghe so " << soGhe << " DA CO NGUOI DAT! Vui long chon ghe khac.\n";
        } else {
            break;
        }
    }

    cout << "\n--- Nhap thong tin khach hang ---\n";
    string tenKhach = nhapChuoi("  + Ho ten khach hang: ");
    string sdt      = nhapChuoi("  + So dien thoai: ");

    int maVeMoi = veKeTiep++;
    p->data.ghe[r][c].daDat = true;
    p->data.ghe[r][c].ve    = { maVeMoi, tenKhach, sdt };

    // Tự động đồng bộ xuống tệp tin cơ sở dữ liệu
    ghiToanBoFile(FILE_DB, headPhim);

    char hangGhe = 'A' + r;
    int cotGhe   = c + 1;
    cout << "\n========================================\n";
    cout << "           DAT VE THANH CONG!           \n";
    cout << "========================================\n";
    cout << "  * Ma so ve  : #" << maVeMoi << "\n";
    cout << "  * Ten phim  : " << p->data.ten << "\n";
    cout << "  * Vi tri ghe: Hang " << hangGhe << ", Cot " << cotGhe << " (Ghe so " << soGhe << ")\n";
    cout << "  * Khach hang: " << tenKhach << " - " << sdt << "\n";
    cout << "  * Gia ve    : " << (long long)p->data.giaVe << " VND\n";
    cout << "=> Da cap nhat ghe va dong bo vao file database!\n";
    cout << "========================================\n";
}

// Hủy vé xem phim theo mã số vé
void huyVe(NodePhim* headPhim) {
    if (headPhim == nullptr) {
        cout << "[!] Danh sach phim dang trong!\n";
        return;
    }

    cout << "\n========================================\n";
    cout << "             HUY VE XEM PHIM            \n";
    cout << "========================================\n";

    int maVeCanHuy = nhapSoNguyen("Nhap ma so ve can huy (VD: 1001, hoac 0 de thoat): ", 0, 9999999);
    if (maVeCanHuy == 0) {
        cout << "=> Da huy thao tac.\n";
        return;
    }

    NodePhim* p = headPhim;
    bool timThay = false;

    while (p != nullptr && !timThay) {
        for (int r = 0; r < SO_HANG; r++) {
            for (int c = 0; c < SO_COT; c++) {
                if (p->data.ghe[r][c].daDat && p->data.ghe[r][c].ve.soVe == maVeCanHuy) {
                    timThay = true;
                    int soGhe = r * SO_COT + c + 1;
                    char hangGhe = 'A' + r;

                    cout << "\n--- THONG TIN VE TIM THAY ---\n";
                    cout << "  * Ma ve   : #" << maVeCanHuy << "\n";
                    cout << "  * Phim    : " << p->data.ten << " (" << p->data.ma << ")\n";
                    cout << "  * Vi tri  : Hang " << hangGhe << (c + 1) << " (Ghe " << soGhe << ")\n";
                    cout << "  * Khach   : " << p->data.ghe[r][c].ve.tenKhach 
                         << " (" << p->data.ghe[r][c].ve.sdt << ")\n";

                    string xacNhan = nhapChuoi("\nBan co CHAC CHAN muon huy ve nay? (y/n): ");
                    if (xacNhan == "y" || xacNhan == "Y") {
                        p->data.ghe[r][c].daDat = false;
                        p->data.ghe[r][c].ve    = { 0, "", "" };

                        ghiToanBoFile(FILE_DB, headPhim);
                        cout << "=> [Thanh cong] Da huy ve #" << maVeCanHuy 
                             << " va tra ghe " << hangGhe << (c + 1) << " ve trang thai trong!\n";
                    } else {
                        cout << "=> Da huy thao tac. Ve van duoc giu nguyen!\n";
                    }
                    return;
                }
            }
        }
        p = p->next;
    }

    if (!timThay) {
        cout << "  [!] Khong tim thay ve co ma #" << maVeCanHuy << " trong he thong!\n";
    }
}

// Menu điều phối nghiệp vụ phòng vé (Chức năng 8)
void hienMenuDatVeHuyVe(NodePhim* headPhim, int& veKeTiep) {
    if (headPhim == nullptr) {
        cout << "[!] Danh sach phim hien dang trong, vui long nhap phim truoc!\n";
        return;
    }

    cout << "\n======== DAT VE & HUY VE XEM PHIM ========\n";
    cout << "   1. Dat ve xem phim\n";
    cout << "   2. Huy ve da dat\n";
    cout << "   3. Xem so do ghe phong chieu\n";
    cout << "   0. Quay lai menu chinh\n";
    cout << "==========================================\n";

    string chon = nhapChuoi("   Chon: ");
    if (chon == "0") {
        cout << "=> Tro ve menu chinh.\n";
        return;
    } else if (chon == "1") {
        datVe(headPhim, veKeTiep);
    } else if (chon == "2") {
        huyVe(headPhim);
    } else if (chon == "3") {
        string maPhim = nhapChuoi("   Nhap ma phim can xem so do ghe (VD: P01): ");
        NodePhim* p = timPhimTheoMa(headPhim, maPhim);
        if (p == nullptr) {
            cout << "  [!] Khong tim thay phim co ma: " << maPhim << "\n";
        } else {
            xemSoDoGhe(p);
        }
    } else {
        cout << "[!] Tuy chon khong hop le!\n";
    }
}

// ----------------------------------------------------------------
// 7.12. TÌM KIẾM NHANH THEO MÃ PHIM (BST)
// ----------------------------------------------------------------

void khoiTaoCay(Tree& root) {
    root = nullptr;
}

int soSanhMa(string a, string b) {
    a = chuyenChuThuong(a);
    b = chuyenChuThuong(b);
    int i = 0;

    while (a[i] != '\0' && b[i] != '\0') {
        if (a[i] < b[i]) return -1;
        if (a[i] > b[i]) return 1;
        i++;
    }

    if (a[i] == '\0' && b[i] == '\0') return 0;
    if (a[i] == '\0') return -1;
    return 1;
}

int chenNodeBST(NodePhim* phim, Tree& root) {
    if (phim == nullptr) return -1;

    if (root != nullptr) {
        int k = soSanhMa(phim->data.ma, root->phim->data.ma);
        if (k == 0) return 0;
        if (k < 0) return chenNodeBST(phim, root->left);
        return chenNodeBST(phim, root->right);
    }

    root = new NodeBST{phim, nullptr, nullptr};
    return 1;
}

void giaiPhongCay(Tree& root) {
    if (root == nullptr) return;

    giaiPhongCay(root->left);
    giaiPhongCay(root->right);
    delete root;
    root = nullptr;
}

int taoCayTuDanhSach(NodePhim* head, Tree& root) {
    giaiPhongCay(root);
    NodePhim* p = head;

    while (p != nullptr) {
        int k = chenNodeBST(p, root);
        if (k != 1) {
            giaiPhongCay(root);
            return k;
        }
        p = p->next;
    }

    return 1;
}

NodePhim* timPhimBST(const string& ma, Tree root) {
    if (root == nullptr) return nullptr;

    int k = soSanhMa(ma, root->phim->data.ma);
    if (k == 0) return root->phim;
    if (k < 0) return timPhimBST(ma, root->left);
    return timPhimBST(ma, root->right);
}

void duyetLNR(Tree root) {
    if (root == nullptr) return;

    duyetLNR(root->left);
    inDongPhim(root->phim->data);
    duyetLNR(root->right);
}

string chuanHoaMaTimKiem(string ma) {
    if (ma.empty()) return ma;
    for (char c : ma) {
        if (c < '0' || c > '9') return ma;
    }

    if (ma.size() == 1) return "P0" + ma;
    return "P" + ma;
}

void hienMenuTimKiemNhanh(Tree root) {
    if (root == nullptr) {
        cout << "[!] Chua co cay tim kiem. Vui long kiem tra danh sach phim!\n";
        return;
    }

    cout << "\n======== TIM KIEM NHANH THEO MA PHIM ========\n";
    string ma = nhapChuoi("   Nhap ma phim hoac phan so (VD: P01, 01, 1): ");
    NodePhim* phim = timPhimBST(ma, root);
    if (phim == nullptr) {
        string maChuan = chuanHoaMaTimKiem(ma);
        if (maChuan != ma) {
            phim = timPhimBST(maChuan, root);
        }
    }

    if (phim == nullptr) {
        cout << "[!] Khong tim thay phim co ma: " << ma << "\n";
        return;
    }

    inTieuDeBang();
    inDongPhim(phim->data);
    cout << "=> Tim thay phim co ma: " << phim->data.ma << "\n";
}

// ----------------------------------------------------------------
// 7.11. THỐNG KÊ ĐẶT VÉ & TỶ LỆ LẤP ĐẦY
// ----------------------------------------------------------------

int demVeDaDat(const Phim& phim) {
    int soVe = 0;
    for (int r = 0; r < SO_HANG; r++) {
        for (int c = 0; c < SO_COT; c++) {
            if (phim.ghe[r][c].daDat) soVe++;
        }
    }
    return soVe;
}

// Lượt 1: tính tổng và khởi tạo các mức cao/thấp từ phim đầu tiên.
ThongKePhim thuThapThongKe(NodePhim* head) {
    ThongKePhim thongKe{};
    NodePhim* p = head;

    while (p != nullptr) {
        int soVe = demVeDaDat(p->data);
        double doanhThu = soVe * p->data.giaVe;

        if (thongKe.tongPhim == 0) {
            thongKe.veNhieuNhat = thongKe.veItNhat = soVe;
            thongKe.doanhThuCaoNhat = thongKe.doanhThuThapNhat = doanhThu;
        } else {
            if (soVe > thongKe.veNhieuNhat) thongKe.veNhieuNhat = soVe;
            if (soVe < thongKe.veItNhat) thongKe.veItNhat = soVe;
            if (doanhThu > thongKe.doanhThuCaoNhat) thongKe.doanhThuCaoNhat = doanhThu;
            if (doanhThu < thongKe.doanhThuThapNhat) thongKe.doanhThuThapNhat = doanhThu;
        }

        thongKe.tongPhim++;
        thongKe.tongVe += soVe;
        thongKe.tongDoanhThu += doanhThu;
        p = p->next;
    }
    return thongKe;
}

void inDongThongKe(const Phim& phim, int soVe) {
    double doanhThu = soVe * phim.giaVe;
    double tyLeLapDay = soVe * 100.0 / TONG_GHE;
    string veDaDat = to_string(soVe) + "/" + to_string(TONG_GHE);
    printf("%-8s %-40s %-12s %9.2f%% %20.2f\n",
           phim.ma.c_str(), phim.ten.c_str(), veDaDat.c_str(),
           tyLeLapDay, doanhThu);
}

void inHangTongKet(const string& tieuChi, double giaTri, const string& donVi, const string& dsPhim) {
    stringstream danhSach(dsPhim);
    string tenPhim;
    if (!getline(danhSach, tenPhim)) tenPhim = "-";

    int soLe = (donVi == "VND") ? 2 : 0;
    printf("| %-26s | %14.*f %-4s | %-50s |\n",
           tieuChi.c_str(), soLe, giaTri, donVi.c_str(), tenPhim.c_str());
    while (getline(danhSach, tenPhim)) {
        printf("| %-26s | %-19s | %-50s |\n", "", "", tenPhim.c_str());
    }
    cout << '+' << string(28, '-') << '+' << string(21, '-')
         << '+' << string(52, '-') << "+\n";
}

void sapXepThongKeTheoLapDay(DongThongKe* danhSach, int soPhim) {
    for (int i = 1; i < soPhim; i++) {
        DongThongKe dong = danhSach[i];
        int j = i - 1;
        while (j >= 0 && danhSach[j].soVe < dong.soVe) {
            danhSach[j + 1] = danhSach[j];
            j--;
        }
        danhSach[j + 1] = dong;
    }
}

// Lượt 2: gom dòng hiển thị và tên phim đồng hạng, sau đó sắp mảng và in.
void inPhimTheoThongKe(NodePhim* head, const ThongKePhim& thongKe) {
    printf("\n%-8s %-40s %-12s %10s %20s\n",
           "Ma", "Ten phim", "Ve da dat", "Lap day", "Doanh thu (VND)");
    cout << string(104, '-') << '\n';
    string phimNhieuVe, phimItVe, phimDoanhThuCao, phimDoanhThuThap;
    DongThongKe* danhSach = new DongThongKe[thongKe.tongPhim];
    int soPhim = 0;

    NodePhim* p = head;
    while (p != nullptr) {
        int soVe = demVeDaDat(p->data);
        double doanhThu = soVe * p->data.giaVe;
        danhSach[soPhim++] = {p, soVe};

        string tenPhim = p->data.ma + " - " + p->data.ten + "\n";
        if (soVe == thongKe.veNhieuNhat) phimNhieuVe += tenPhim;
        if (soVe == thongKe.veItNhat) phimItVe += tenPhim;
        if (doanhThu == thongKe.doanhThuCaoNhat) phimDoanhThuCao += tenPhim;
        if (doanhThu == thongKe.doanhThuThapNhat) phimDoanhThuThap += tenPhim;
        p = p->next;
    }

    sapXepThongKeTheoLapDay(danhSach, soPhim);
    for (int i = 0; i < soPhim; i++) {
        inDongThongKe(danhSach[i].phim->data, danhSach[i].soVe);
    }
    delete[] danhSach;

    cout << string(104, '-') << '\n';
    cout << "\n======== TONG KET THONG KE ========\n";
    cout << '+' << string(28, '-') << '+' << string(21, '-')
         << '+' << string(52, '-') << "+\n";
    printf("| %-26s | %-19s | %-50s |\n", "Tieu chi", "Gia tri", "Phim");
    cout << '+' << string(28, '-') << '+' << string(21, '-')
         << '+' << string(52, '-') << "+\n";
    inHangTongKet("Tong so phim", thongKe.tongPhim, "phim", "");
    inHangTongKet("Tong so ve dang dat", thongKe.tongVe, "ve", "");
    inHangTongKet("Tong doanh thu tam tinh", thongKe.tongDoanhThu, "VND", "");
    inHangTongKet("Phim dat ve nhieu nhat", thongKe.veNhieuNhat, "ve", phimNhieuVe);
    inHangTongKet("Phim dat ve it nhat", thongKe.veItNhat, "ve", phimItVe);
    inHangTongKet("Doanh thu cao nhat", thongKe.doanhThuCaoNhat, "VND", phimDoanhThuCao);
    inHangTongKet("Doanh thu thap nhat", thongKe.doanhThuThapNhat, "VND", phimDoanhThuThap);
}

void hienThongKePhim(NodePhim* headPhim) {
    if (headPhim == nullptr) {
        cout << "[!] Danh sach phim hien dang trong, chua co du lieu thong ke!\n";
        return;
    }

    cout << "\n======== THONG KE TINH HINH DAT VE ========\n";
    ThongKePhim thongKe = thuThapThongKe(headPhim);
    cout << "* Doanh thu tam tinh theo gia ve hien tai, chi tinh ve dang dat.\n";
    cout << "* Ty le lap day = so ve dang dat / " << TONG_GHE << " x 100%.\n";
    cout << "* Bang phim sap theo ty le lap day tu cao xuong thap.\n";

    inPhimTheoThongKe(headPhim, thongKe);
    cout << "==========================================\n";
}

// ================================================================
// 8. MENU & ĐIỀU PHỐI HỆ THỐNG (MAIN & CONTROL FLOW)
// ================================================================

// Xuất giao diện Menu chính
void hienThiMenu() {
    cout << "\n===== QUAN LY DAT VE XEM PHIM =====\n";
    cout << "  1. Them danh sach phim moi\n";
    cout << "  2. Xem danh sach phim\n";
    cout << "  3. Tim kiem phim\n";
    cout << "  4. Xoa phim\n";
    cout << "  5. Cap nhat thong tin phim\n";
    cout << "  6. Sap xep danh sach phim\n";
    cout << "  7. Xem so do ghe phong chieu\n";
    cout << "  8. Dat ve & Huy ve xem phim\n";
    // Thống kê - Chức năng 11 có cột tỷ lệ lấp đầy của từng phim.
    cout << " 11. Thong ke dat ve & Ty le lap day\n";
    // BST - Thêm chức năng 12 vào menu chính.
    cout << " 12. Tim kiem nhanh theo ma phim (BST)\n";
    cout << "  0. Thoat\n";
    cout << "====================================\n";
    cout << "Chon: ";
}

// Khởi tạo hệ thống, nạp dữ liệu từ CSDL vào RAM khi bật ứng dụng
void khoiTaoHeThong(const string& file, NodePhim*& head, int& veKeTiep) {
    cout << "[System] Dang khoi dong va kiem tra co so du lieu...\n";

    if (kiemTraDBTrong(file)) {
        cout << "[Thong bao] Co so du lieu hien dang TRONG (chua co phim nao)!\n";
        cout << "-> He thong san sang de ban nhap danh sach phim ban dau.\n";
        return;
    }

    docDanhSachPhim(file, head, veKeTiep);

    int soPhim = 0;
    NodePhim* p = head;
    while (p != nullptr) {
        soPhim++;
        p = p->next;
    }

    cout << "[Init] Da keo thanh cong " << soPhim << " phim co san tu Database len RAM!\n";
}

// Hàm thực thi chính của chương trình
int main() {
    NodePhim* headPhim = nullptr; // Con trỏ đầu danh sách liên kết
    int veKeTiep = 1001;          // Bộ đếm mã số vé tự tăng
    // BST - Khởi tạo cây riêng, linked list vẫn quản lý dữ liệu phim.
    Tree root;
    khoiTaoCay(root);

    // Bước 1: Khởi tạo hệ thống
    khoiTaoHeThong(FILE_DB, headPhim, veKeTiep);
    // BST - Dựng cây sau khi dữ liệu đã được nạp vào linked list.
    if (taoCayTuDanhSach(headPhim, root) != 1) {
        cout << "[!] Khong tao duoc BST do ma phim trung hoac khong hop le. Chuc nang 12 chua san sang!\n";
    }

    // Bước 2: Vòng lặp Menu chính
    string chon;
    while (true) {
        hienThiMenu();
        getline(cin, chon);

        // BST - Liên quan chức năng 1 (thêm), 4 (xóa), 6 (sắp xếp).
        // Xóa phim hủy node gốc; sắp xếp đổi data giữa các node.
        // Dọn cây trước các thao tác này rồi dựng lại từ danh sách mới.
        bool canTaoLaiCay = (chon == "1" || chon == "4" || chon == "6");
        if (canTaoLaiCay) {
            giaiPhongCay(root);
        }

        if (chon == "1") {
            nhapDanhSachPhim(headPhim);
        }
        else if (chon == "2") {
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong, vui long nhap phim truoc!\n";
            } else {
                xemDanhSachPhim(headPhim);
            }
        }
        else if (chon == "3") {
            hienMenuTimKiem(headPhim);
        }
        else if (chon == "4") {
            hienMenuXoaPhim(headPhim);
        }
        else if (chon == "5") {
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong!\n";
            } else {
                capNhatThongTinPhim(headPhim);
            }
        }
        else if (chon == "6") {
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong!\n";
            } else {
                hienThiMenuSapXep(headPhim);
            }
        }
        else if (chon == "7") {
            if (headPhim == nullptr) {
                cout << "[!] Danh sach hien dang trong!\n";
            } else {
                string maPhim = nhapChuoi("Nhap ma phim can xem so do ghe (VD: P01): ");
                NodePhim* p = timPhimTheoMa(headPhim, maPhim);
                if (p == nullptr) {
                    cout << "  [!] Khong tim thay phim co ma: " << maPhim << "\n";
                } else {
                    xemSoDoGhe(p);
                }
            }
        }
        else if (chon == "8") {
            hienMenuDatVeHuyVe(headPhim, veKeTiep);
        }
        else if (chon == "12") {
            // BST - Điều phối chức năng 12: tìm kiếm nhanh theo mã phim.
            hienMenuTimKiemNhanh(root);
        }
        else if (chon == "11") {
            // Thống kê - Đọc trạng thái ghế hiện tại từ linked list.
            hienThongKePhim(headPhim);
        }
        else if (chon == "0") {
            ghiToanBoFile(FILE_DB, headPhim);
            cout << "Da dong bo du lieu an toan xuong dia. Tam biet!\n";
            break;
        }
        else {
            cout << "[!] Lua chon khong hop le, vui long chon lai!\n";
        }

        // BST - Dựng lại cây sau chức năng 1, 4, 6 để khớp linked list hiện tại.
        if (canTaoLaiCay && taoCayTuDanhSach(headPhim, root) != 1) {
            cout << "[!] Khong tao duoc BST do ma phim trung hoac khong hop le. Chuc nang 12 chua san sang!\n";
        }
    }

    // Bước 3: Giải phóng bộ nhớ RAM trước khi thoát
    // BST - Giải phóng cây trước khi xóa các node phim của linked list.
    giaiPhongCay(root);
    giaiPhong(headPhim);

    return 0;
}
