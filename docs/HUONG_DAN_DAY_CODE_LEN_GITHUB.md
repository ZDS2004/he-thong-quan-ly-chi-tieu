# Hướng dẫn đưa dự án lên GitHub

## 1. Tạo kho mã nguồn

1. Đăng nhập GitHub và chọn **New repository**.
2. Đặt tên, ví dụ `tui-tien-quan-ly-chi-tieu`.
3. Chọn Public nếu thầy cần mở liên kết trực tiếp và học phần cho phép công khai mã nguồn. Nếu chọn Private, thêm thầy làm collaborator.
4. Để kho trống: không chọn tạo README, `.gitignore` hoặc license vì dự án đã có các tệp này.

## 2. Mở PowerShell tại thư mục dự án

```powershell
cd "C:\Users\Asus\Desktop\Code\Python\BTL"
```

Thư mục dự án đang nằm bên trong một repository khác ở thư mục cha. Tạo repository riêng tại đây trước khi thêm file, để tránh đẩy nhầm repository cha:

```powershell
git init
git rev-parse --show-toplevel
```

Lệnh thứ hai phải in đúng đường dẫn kết thúc bằng `Code/Python/BTL`. Nếu vẫn hiện một thư mục cha, dừng lại và không chạy `git add` hoặc `git push`.

## 3. Kiểm tra và commit mã nguồn

```powershell
git status --short
git add .
git status
```

Kiểm tra danh sách staged files. `.env`, cơ sở dữ liệu SQLite, thư mục `.venv` và cache Python phải bị bỏ qua theo `.gitignore`. Không đưa mật khẩu, khóa bí mật hoặc dữ liệu cá nhân lên GitHub.

Sau khi xác nhận danh sách chỉ gồm file dự án:

```powershell
git commit -m "Hoan thien ung dung quan ly chi tieu"
git branch -M main
```

## 4. Kết nối kho GitHub và đẩy code

Thay `TEN_TAI_KHOAN` và `TEN_REPOSITORY` bằng thông tin kho bạn vừa tạo:

```powershell
git remote add origin https://github.com/TEN_TAI_KHOAN/TEN_REPOSITORY.git
git push -u origin main
```

GitHub có thể mở trang đăng nhập trong trình duyệt hoặc yêu cầu xác thực Git. Đăng nhập bằng tài khoản của bạn; không gửi mật khẩu hay token cho người khác.

## 5. Các lần cập nhật sau

```powershell
git add .
git commit -m "Mo ta thay doi"
git push
```

Sau khi đẩy thành công, mở trang repository, sao chép URL và dán vào biểu mẫu nộp bài cùng PDF báo cáo và liên kết video demo.
