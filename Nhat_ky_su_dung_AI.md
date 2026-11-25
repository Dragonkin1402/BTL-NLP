# Nhật ký sử dụng AI

## 2026-11-25 — Hoàn thiện hồ sơ D1 và pre-audit dữ liệu

- **Công cụ AI:** AI assistant using Copilot SDK in VS Code. Model/version cụ thể không được hiển thị trong phiên làm việc.
- **Công cụ hỗ trợ:** Python và shell chạy cục bộ; Hugging Face Dataset Viewer/`datasets-server` để truy vấn mẫu dữ liệu công khai. Không tải lên gold, annotation hoặc văn bản cục bộ.
- **AI đã hỗ trợ:** soạn/sửa Data Card 14 mục và evaluation protocol; tổng hợp mã REVIEW/WARN từ báo cáo checker; đối chiếu sơ bộ 9 cặp cùng tiêu đề bằng mức tương đồng chuỗi nội dung; kiểm tra ngữ cảnh 12 ứng viên trong numeric audit; đọc mẫu nội dung để ghi nhận xét cho 8 bài `khac`.
- **Lịch sử bản nháp gold:** các dòng gold ghi `draft_source=llm_edited`; log hiện có không lưu model ID hoặc thời điểm tạo riêng cho từng bản nháp, nên không suy đoán các thông tin này. Việc người kiểm chứng được ghi riêng trong review log.
- **Giới hạn xác nhận:** các nhận xét trên được ghi là AI-assisted pre-audit, chưa có xác nhận độc lập của A1/A2. Không sửa tóm tắt hoặc fact sheet gold đã khóa; chưa chạy mô hình tóm tắt.
- **Phát hành:** chỉ code/tài liệu không chứa toàn văn hoặc gold được đẩy lên GitHub. Báo cáo kiểm tra có danh sách tiêu đề và các tệp dữ liệu/annotation tiếp tục ở local trong khi quyền tái phân phối chưa rõ.
