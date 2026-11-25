# Data Card — VietOnlineNews (dataset chính)

## 1. Tóm tắt

Chọn `VLUS06/VietOnlineNews` làm nguồn bài báo chính cho đề tài tóm tắt tin kinh tế tiếng Việt có kiểm chứng dữ kiện. Dataset gốc có nhãn phân loại chủ đề 13 lớp (`category`), nhưng nhãn này không phải nhãn tóm tắt. Gold của BTL được nhóm tự xây dựng trên 60 bài chọn lọc (10 dev, 50 test), gồm tóm tắt tham chiếu và phiếu dữ kiện số. Không dùng các dataset tóm tắt tin như `Linhz/Vietnews` hoặc `harouzie/vietnews`.

## 2. Dataset snapshot

| Thuộc tính | VietOnlineNews |
|---|---|
| Hugging Face ID | [`VLUS06/VietOnlineNews`](https://huggingface.co/datasets/VLUS06/VietOnlineNews) |
| Ngôn ngữ / tác vụ | Tiếng Việt / dataset gốc phân loại chủ đề đơn nhãn; BTL tạo gold tóm tắt tin kinh tế và dữ kiện số |
| Tổng số dòng | 265,729 |
| Cột | `id, title, description, content, category` |
| Retrieved at | `2026-11-25T09:51:48+07:00` |
| Revision đã pin | `bd8d2a865c8981d34cb9d85f69f62bda7c40b520` |

| Split | Số dòng |
|---|---:|
| train | 186,010 |
| validation | 39,859 |
| test | 39,860 |

Hub README mô tả dữ liệu từ VietnamNet, Thanh Niên và Tuổi Trẻ, thời gian 2023–2025. Schema được tải không có cột nguồn hoặc ngày đăng, nên không thể kiểm chứng các trường đó ở cấp từng bài từ bản này.

**Nguồn đối chiếu UVN-1 (không phải dataset chính):** [`undertheseanlp/UVN-1`](https://huggingface.co/datasets/undertheseanlp/UVN-1), revision `42a81b44e1e8228146e56a3fa066cc035384b7d9`, 3,268 dòng, cột `id, source, url, category, title, content, publish_date`. Metadata có trường `publish_date` với khoảng giá trị **2011-06-28 đến 2026-01-29**; không có trường `published_at`. Khoảng ngày này lấy từ metadata của dataset, không suy ra từ ngày crawl. Hub khai báo license `CC-BY-NC-4.0`.

## 3. Mục đích sử dụng

- Phù hợp: làm nguồn bài báo cho bộ gold 60 bài của BTL, phục vụ đánh giá tóm tắt tin kinh tế và bảo toàn dữ kiện số.
- Giới hạn: dataset gốc không cung cấp nhãn tóm tắt; `category` chỉ là nhãn chủ đề. Tóm tắt và phiếu dữ kiện do nhóm tạo, cần được đánh giá theo quy trình annotation dưới đây.
- Chỉ dùng kết quả theo split và revision đã ghi; không suy rộng sang toàn bộ báo chí Việt Nam.

## 4. License và quy tắc lưu trữ

Hub gắn `license: other` cho VietOnlineNews, không phải một SPDX license cụ thể. Repo có mục `LICENSE` nhưng nội dung truy cập được trong lần kiểm tra này rỗng; vì vậy **chưa xác minh được quyền sử dụng hoặc tái phân phối**. Cần hỏi người phát hành/giảng viên và kiểm tra điều khoản của các nguồn báo trước khi công bố hay chia sẻ dữ liệu.

Không commit/push `title`, `description`, `content` hoặc các bản dump CSV/Parquet/JSONL. Corpus đầy đủ không được lưu trong workspace. Pipeline tạo một mẫu 60 bài trong `data/processed/selected_articles.jsonl`, có chứa toàn văn để làm việc cục bộ; các file chứa nội dung được thêm vào `.gitignore` và không được đẩy công khai.

## 5. Bằng chứng chất lượng và lọc bài kinh doanh

### Phân bố category

Split sizes quan sát được khi tải revision đã pin ở trên khác với con số split trong Hub README (README ghi 187,682 / 40,218 / 40,218, tổng 268,118). Dùng số đếm trực tiếp từ loader cho báo cáo này; cần xác minh sai khác với người phát hành trước khi so sánh theo split.

| Category | Số bài | Tỷ lệ |
|---|---:|---:|
| Giải trí | 40,864 | 15.38% |
| Kinh doanh | 33,242 | 12.51% |
| Thể thao | 32,278 | 12.15% |
| Thời sự | 27,399 | 10.31% |
| Giáo dục | 22,433 | 8.44% |
| Khoa học công nghệ | 21,008 | 7.91% |
| Đời sống | 19,116 | 7.19% |
| Xe | 18,805 | 7.08% |
| Sức khỏe | 16,666 | 6.27% |
| Thế giới | 14,847 | 5.59% |
| Du lịch | 9,179 | 3.45% |
| Bất động sản | 6,636 | 2.50% |
| Pháp luật | 3,256 | 1.23% |

### Bài `Kinh doanh` có dấu hiệu số liệu

Đếm bài thuộc `Kinh doanh` có ít nhất một chuỗi dưới đây trong `title`, `description` hoặc `content` (không phân biệt hoa/thường):

| Chuỗi dò | Số bài khớp |
|---|---:|
| `%` | 20,954 |
| `tỷ đồng` | 5,267 |
| `USD` | 11,095 |
| `quý` | 8,625 |
| **Khớp ít nhất một chuỗi (duy nhất)** | **25,182** |

Đây là bộ lọc từ khóa thô, không khẳng định bài có số liệu tài chính hợp lệ (đặc biệt `quý` có thể mang nghĩa khác). Danh sách ID, không có nội dung bài: [`data/vietonline_news_economic_numeric_ids.txt`](data/vietonline_news_economic_numeric_ids.txt).

## 6. Tái lập

Chạy `python scripts/inspect_news_datasets.py` từ thư mục `BTL` sau khi cài `datasets`. Script tải theo revision đã pin, in schema/số dòng/phân bố, cập nhật Data Card, ghi danh sách ID khớp và metadata schema. Không lưu nội dung toàn văn từ lần kiểm tra này ra workspace.

## 7. Annotation Process và Quality Checks

- Bộ gold gồm 60 bài: 10 dev và 50 test. Cả 60 dòng tóm tắt ghi `guideline_version = v1.0`; nguồn bản nháp ghi `llm_edited`.
- Nhật ký ghi nhận 31/50 bài test được người thứ hai rà soát (62%); cả 31 quyết định là `keep`, không ghi nhận bất đồng hoặc mục `unresolved`. 19 bài còn lại có trạng thái `annotated`, không có reviewer độc lập trong metadata; 7 bài trong nhóm này có cờ REVIEW của checker và đã được A1 tự kiểm, ghi rõ là self-check (không tính vào rà soát chéo).
- Trên dev, 7/10 bài có trạng thái `reviewed`; 3/10 ở trạng thái `annotated`. Tính cả dev và test, 38/60 bài (63,3%) có trạng thái `reviewed`.
- Trong pilot dev, 5 bài có bất đồng được ghi nhận: loại A xuất hiện ở 4/5 bài (80%), loại B ở 5/5 (100%), loại C ở 0/5. Các loại có thể chồng lấp trên cùng một bài; nhật ký có resolution cho cả 5 và không có mục ghi `unresolved`.
- Chạy `python src/check_gold.py --locked-version v1.0` từ thư mục `BTL`: **0 ERROR, 23 REVIEW, 14 WARN**. Cả 50 test dùng v1.0; không có lỗi `guideline_changed_after_lock`. Các cờ REVIEW đã có kiểm tra thủ công trong nhật ký; REVIEW/WARN là cờ tự động, không phải bất đồng nhãn. Xem [báo cáo checker](reports/gold_check_report.md); chi tiết review nằm trong `data/annotations/review_log.csv` (bản cục bộ, không đưa lên repo công khai).

## 10. Lịch sử chia tập và khóa test

- Chia dev được điều chỉnh **một lần** vào `2026-11-25T10:14:05+07:00`, trước khi gắn nhãn; kiểm tra template xác nhận cả 60 `reference_summary` vẫn còn trống.
- Lý do: split cũ không có chủ đề `doanh_nghiep` và `khac` trong dev. Split mới giữ nguyên 60 bài được chọn, đảm bảo dev có đại diện cả 8 chủ đề và có cả hai mức số liệu; seed `42`, dev `10`, tối thiểu 2 bài ít số liệu.
- Dev mới: 8 bài có ít nhất 4 dữ kiện số và 2 bài có ít hơn 4.

| Chủ đề | Ít số liệu | Nhiều số liệu | Tổng dev |
|---|---:|---:|---:|
| bat_dong_san | 1 | 0 | 1 |
| chung_khoan | 0 | 1 | 1 |
| doanh_nghiep | 0 | 2 | 2 |
| hang_hoa | 0 | 1 | 1 |
| khac | 1 | 0 | 1 |
| tien_te_ngan_hang | 0 | 1 | 1 |
| vi_mo | 0 | 1 | 1 |
| xuat_nhap_khau | 0 | 2 | 2 |
| **Tổng** | **2** | **8** | **10** |

- Danh sách đã ghi: [`dev_ids.txt`](data/splits/dev_ids.txt), [`test_ids.txt`](data/splits/test_ids.txt); lịch sử: [`split_history.json`](data/splits/split_history.json). Chỉ đổi split cho 20/60 bài; test gồm 50 bài.
- Split files được tạo trước khi viết gold. Gold test hiện có đủ 50 tóm tắt v1.0; checker cho 0 ERROR. Mã nguồn, Data Card, báo cáo checker và danh sách ID có thể lưu trong repository công khai; toàn văn bài báo cùng các CSV annotation chứa tóm tắt/câu nguồn tiếp tục ở local vì chưa xác minh quyền tái phân phối.
