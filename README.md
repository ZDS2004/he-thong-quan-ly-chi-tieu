# Hệ thống quản lý chi tiêu — Quản lý chi tiêu cá nhân

Đồ án Django nhỏ: theo dõi thu/chi, danh mục, ghi chú cá nhân và dashboard biểu đồ.

## Công nghệ

- Python 3.12, Django 5.2
- SQLite (không cần cài database riêng)
- Chart.js cho biểu đồ

## Chạy máy local

```powershell
cd C:\Users\Asus\Desktop\Code\Python\BTL
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Mở http://127.0.0.1:8000/

Tài khoản demo: `demo` / `demo12345`  
Hoặc đăng ký tài khoản mới (sẽ có sẵn danh mục mặc định).

Admin: `python manage.py createsuperuser` rồi vào `/admin/`.

## Chức năng

| Phần | Mô tả |
|---|---|
| Tài khoản | Đăng ký, đăng nhập, đăng xuất |
| Danh mục | CRUD thu/chi, màu hiển thị |
| Giao dịch | CRUD, lọc theo tháng / loại / danh mục |
| Ghi chú | Tạo, xem, sửa và xóa ghi chú cá nhân theo dạng bảng |
| Tổng quan | Tổng thu, chi, còn lại và biểu đồ theo ngày/danh mục |

Mỗi user chỉ thấy dữ liệu của mình.

## Cấu trúc

```
config/          settings, urls
accounts/        đăng ký / đăng nhập, seed danh mục khi tạo user
expenses/        models, forms, services, views
dashboard/       trang tổng quan + dữ liệu chart
templates/       giao diện HTML
static/css/      giao diện
```

### Đọc code theo luồng

1. `config/urls.py` nối các URL với từng ứng dụng.
2. `accounts/` xử lý đăng ký, đăng nhập và tạo danh mục mặc định.
3. `expenses/models.py` định nghĩa dữ liệu; `forms.py` kiểm tra dữ liệu nhập.
4. `expenses/views.py` nhận yêu cầu trang; `services.py` chứa phép tính dùng chung.
5. `dashboard/views.py` lấy số liệu tháng; `templates/` dựng HTML; `static/css/app.css` định dạng giao diện.

Các trang dùng một mẫu CRUD chung trong `templates/expenses/form.html`. Vì vậy, view chỉ truyền tiêu đề, nút lưu và URL quay lại; vòng lặp trong template tự hiển thị từng trường của form.

Giao diện dùng CSS thuần, màu sắc và khoảng cách tập trung trong `static/css/app.css`. Dashboard dùng Chart.js để vẽ biểu đồ; dữ liệu JSON được đưa vào trang bằng bộ lọc `json_script` của Django.

Logic tính tháng nằm ở `expenses/services.py` (`month_summary`), không nhét vào view.

## Kiểm thử

```powershell
python manage.py test
```

## Gợi ý báo cáo / video

1. Đăng ký tài khoản, chỉ danh mục mặc định.
2. Thêm vài khoản thu/chi tháng hiện tại.
3. Thêm vài ghi chú, sửa một ghi chú và xem danh sách dạng bảng.
4. Dashboard: 3 thẻ số + 2 biểu đồ.
5. Django Admin.
6. Nêu hạn chế: SQLite, chưa xuất Excel, chưa nhiều thiết bị đồng bộ.

Hướng dẫn GitHub: `docs/HUONG_DAN_DAY_CODE_LEN_GITHUB.md`  
Kịch bản video demo: `docs/KICH_BAN_VIDEO_DEMO.md`

## Báo cáo đồ án

- Word báo cáo 19 trang: `output/word/Bao_cao_He_thong_quan_ly_chi_tieu.docx`
- PDF báo cáo 19 trang: `output/pdf/Bao_cao_He_thong_quan_ly_chi_tieu.pdf`
- Mã nguồn tạo PDF: `reports/generate_report.py`; mã nguồn tạo Word: `reports/generate_docx_report.py`.
- Trước khi nộp, điền tên giảng viên, URL GitHub và URL video YouTube nếu cần trong `reports/generate_report.py`, sau đó chạy:

```powershell
python reports/generate_report.py
python reports/generate_docx_report.py
```

Điểm tự đánh giá trong báo cáo chỉ là ước lượng ban đầu. Chạy kiểm thử và bổ sung ảnh chụp/video thực tế trước khi gửi bài.


