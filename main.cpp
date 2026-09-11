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

// ----------------------------------------------------------------



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

// ----------------------------------------------------------------




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



// Logic code
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

// ----------------------------------------------------------------





// ================================================================
// MAIN
// ================================================================

void hienThiMenu() {
    cout << "\n===== QUAN LY DAT VE XEM PHIM =====\n";
    cout << "  1. Xem danh sach phim\n";
    cout << "  0. Thoat\n";
    cout << "====================================\n";
    cout << "Chon: ";
}

int main() {
    NodePhim* headPhim = nullptr;
    int veKeTiep = 1001;

    // ── INIT ─────────────────────────────────────────────────────
    docDanhSachPhim(FILE_DB, headPhim, veKeTiep);

    // Đếm số phim đã load
    int soPhim = 0;
    NodePhim* t = headPhim;
    while (t) { soPhim++; t = t->next; }
    cout << "[Init] Da load " << soPhim << " phim tu database.\n";
    // ─────────────────────────────────────────────────────────────

    // ── VÒNG LẶP CHÍNH ───────────────────────────────────────────
    string chon;
    while (true) {
        hienThiMenu();
        getline(cin, chon);

        if (chon == "1") {
            xemDanhSachPhim(headPhim);
        } else if (chon == "0") {
            ghiToanBoFile(FILE_DB, headPhim);
            cout << "Da luu du lieu. Tam biet!\n";
            break;
        }
    }
    // ─────────────────────────────────────────────────────────────
    
    giaiPhong(headPhim);
    return 0;
}

// ----------------------------------------------------------------
