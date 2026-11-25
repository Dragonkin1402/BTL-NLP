# ĐT05 – Tóm tắt tin tức kinh tế tiếng Việt có kiểm chứng dữ kiện

Bài tập lớn học phần **CSC4007 – Xử lý ngôn ngữ tự nhiên** (năm học 2026–2027).

- **Nhóm thực hiện:** Cường (`A1`), Hoàng (`A2`)
- **Đề tài:** ĐT05 – Tóm tắt tin tức kinh tế có kiểm chứng
- **Đầu vào → Đầu ra:** Bài báo kinh tế tiếng Việt (`title`, `content`) → bản tóm tắt 3–5 câu (50–120 từ) bảo toàn chủ thể, số liệu, đơn vị, mốc thời gian, kèm trích xuất/đối chiếu câu nguồn cho các phát biểu định lượng.
- **Metric chính:** ROUGE-L (âm tiết tiếng Việt, phụ: ROUGE-1/2), đối chiếu claim số/đơn vị bề mặt và rubric factuality (0–2), `numeric_precision`, `numeric_hallucination_rate`, `gold_numeric_recall` (chi tiết tại [`evaluation_protocol.md`](evaluation_protocol.md)).

> [!IMPORTANT]
> **Quyền dữ liệu & phạm vi phát hành:** Nguồn dữ liệu [`VLUS06/VietOnlineNews`](https://huggingface.co/datasets/VLUS06/VietOnlineNews) (revision `bd8d2a865c8981d34cb9d85f69f62bda7c40b520`) khai báo `license: other` với tệp `LICENSE` rỗng (`OTHER_UNVERIFIED`). Các tệp chứa toàn văn bài báo, `reference_summary` hoặc `source_sentence` trích nguyên văn được `.gitignore` giữ cục bộ và **không đẩy lên GitHub công khai**.

## Báo cáo tiến độ và kết quả hiện tại

Cập nhật ngày **25/11/2026**. Bộ dữ liệu đánh giá gồm 60 bài đã gán nhãn theo guideline v1.0: 10 bài `dev` và 50 bài `test`. Kết quả dưới đây chỉ phản ánh những lượt chạy đã hoàn tất; không gộp dữ liệu mock vào kết quả thực nghiệm.

| Thí nghiệm | Trạng thái | Kết quả / ghi chú |
|---|---|---|
| E0 — Lead-3, `dev` | Hoàn tất, 10/10 bài | ROUGE-1 F1: **0.3921**; ROUGE-2 F1: **0.2086**; ROUGE-L F1: **0.2516**. Trong 40 claim số được trích xuất, 16 khớp bề mặt cả giá trị và đơn vị (**40%**); gold fact surface recall: **0.2533**. |
| E1 — prompt cơ bản, `dev` | Chưa hoàn tất | Run `20261125T122128Z-600f3317` dừng ở trạng thái `partial`, hoàn tất **0/10** bài; manifest ghi `HTTPError` tại `DT05-004`. Chưa có dự đoán để chấm. |
| E2 — prompt ràng buộc số liệu, `dev` | Chưa chạy thực nghiệm thật | Chỉ có smoke test bằng dữ liệu tổng hợp để kiểm tra pipeline; không dùng làm kết quả hay so sánh với E0/E1. |
| Unit tests | Đạt | **9/9** kiểm thử tự động thành công trong lần chạy ngày 25/11/2026. |
| E0–E2 — `test` | Chưa chạy | Chưa xác nhận được cấu hình E0–E2 đã khóa bằng tag `configs-frozen`; E1 và E2 cũng chưa có kết quả thật hoàn chỉnh trên `dev`. |

**Diễn giải:** 40% của E0 là tỷ lệ khớp bề mặt `giá trị + đơn vị`, không phải numeric precision hay tỷ lệ factuality. Gold fact surface recall đo mức tái hiện fact trong gold, không thay thế việc người đọc đối chiếu claim với bài nguồn. Chưa có điểm factuality do người chấm đánh giá, vì vậy chưa thể kết luận E1/E2 tốt hơn E0 về độ chính xác dữ kiện.

**Việc cần làm tiếp:** khắc phục lỗi gọi API và hoàn tất E1 trên `dev`; chạy E2 thật trên `dev`; chấm factuality và rà soát đầu ra; sau đó khóa cấu hình E0–E2 trước khi chạy `test` đúng một lần theo [`evaluation_protocol.md`](evaluation_protocol.md). Không dùng kết quả mock hoặc mở tập `test` để thay cho các bước này.

---

## 1. Cấu trúc thư mục và bảng ánh xạ vị trí minh chứng

Theo Mục 10.1 của hướng dẫn BTL CSC4007, bảng dưới đây ánh xạ vị trí từng minh chứng trong dự án:

| Minh chứng theo hướng dẫn | Đường dẫn trong dự án | Ghi chú phát hành |
|---|---|---|
| README hướng dẫn chạy | [`README.md`](README.md) | Công khai |
| Danh sách thư viện | [`requirements.txt`](requirements.txt) | Công khai |
| Data Card 14 mục | [`data_card.md`](data_card.md) | Công khai |
| Tài liệu tầng dữ liệu & Schema | [`data/README.md`](data/README.md), [`data/data_schema.md`](data/data_schema.md) | Công khai |
| Manifest & toàn văn/annotation | `data/data_manifest.csv`, `data/processed/*`, `data/annotations/gold_*.csv`, `review_log.csv` | **Cục bộ** (`.gitignore` vì `license: other`) |
| Chia split & khóa guideline | [`data/splits/dev_ids.txt`](data/splits/dev_ids.txt), [`data/splits/test_ids.txt`](data/splits/test_ids.txt), [`data/splits/split_history.json`](data/splits/split_history.json), [`annotation_guideline.md`](annotation_guideline.md), [`data/annotations/guideline_lock.json`](data/annotations/guideline_lock.json) | Công khai |
| Cấu hình & prompt E0–E2 | [`configs/`](configs/README.md) (`e0_lead3.json`, `e1_basic_v1.json`, `e2_numeric_v1.json`) | Công khai |
| Mã nguồn chuẩn hóa, kiểm gold, suy luận, đánh giá | [`data/prepare_data.py`](data/prepare_data.py), [`src/check_gold.py`](src/check_gold.py), [`src/run_ollama.py`](src/run_ollama.py), [`src/evaluate.py`](src/evaluate.py), [`src/build_human_eval_sheet.py`](src/build_human_eval_sheet.py), [`src/summarize_experiments.py`](src/summarize_experiments.py), [`src/export_error_candidates.py`](src/export_error_candidates.py) | Công khai |
| Giao thức đánh giá | [`evaluation_protocol.md`](evaluation_protocol.md) | Công khai (`protocol-frozen`) |
| Báo cáo chất lượng & kiểm gold | `reports/data_quality_report.md` (cục bộ), [`reports/gold_check_report.md`](reports/gold_check_report.md), [`reports/gold_check_issues.csv`](reports/gold_check_issues.csv) | `gold_check_*` công khai |
| Nhật ký thí nghiệm, dự đoán & chấm người | `reports/experiments.csv`, `reports/*_predictions_*.csv`, `reports/*_numeric_claims_*.csv`, `reports/human_eval_sheet.csv`, `reports/numeric_error_table.csv` | **Cục bộ** (chứa văn bản tóm tắt/tham chiếu) |
| Bảng tổng hợp chỉ số | [`reports/metrics_summary.csv`](reports/metrics_summary.csv) | Công khai (chỉ số tổng hợp) |
| Phân tích lỗi (≥10 mẫu) | [`reports/error_analysis.md`](reports/error_analysis.md) | Công khai (không trích nguyên văn bài báo) |
| Nhật ký & tuyên bố sử dụng AI | [`Nhat_ky_su_dung_AI.md`](Nhat_ky_su_dung_AI.md), [`reports/Tuyen_bo_su_dung_AI.md`](reports/Tuyen_bo_su_dung_AI.md) | Công khai |
| Báo cáo kỹ thuật | [`reports/Bao_cao_BTL.md`](reports/Bao_cao_BTL.md), `reports/Bao_cao_BTL.pdf` | `.pdf` nộp cục bộ/ZIP |
| Demo & ca kiểm thử mẫu | [`app/`](app/README.md) (`demo.py`, `sample_input.txt`, `sample_output.json`) | Công khai |
| Kiểm thử tự động | [`tests/test_pipeline.py`](tests/test_pipeline.py) | Công khai |

---

## 2. Cài đặt môi trường

Yêu cầu Python 3.10+ (đã kiểm thử với Python 3.13 trong `.venv`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Nếu chạy E1/E2 hoặc chế độ LLM của demo qua Ollama Cloud, cấu hình biến môi trường ở shell cục bộ (**không lưu hoặc commit vào mã nguồn**):

```bash
export OLLAMA_API_KEY="<your-ollama-cloud-api-key>"
```

Trong PowerShell, có thể nhập key theo kiểu không hiển thị trên màn hình:

```powershell
$secure = Read-Host "OLLAMA_API_KEY" -AsSecureString
$env:OLLAMA_API_KEY = [System.Net.NetworkCredential]::new("", $secure).Password
```

Khi bản sao làm việc chưa có Git commit hợp lệ, chạy lệnh từ thư mục `BTL` và bỏ `--repo-root`. Runner để trống `run_commit`, ghi SHA-256 của mã nguồn/dữ liệu/config vào `source_fingerprint` và đặt `worktree_status` là `uncommitted`; fingerprint loại trừ `.git`, môi trường ảo, cache và `reports/`. Không dùng fingerprint như một Git commit hoặc để mở tập test.

---

## 3. Quy trình tái lập từng bước

### Bước 1: Kiểm tra dữ liệu và bộ gold (D1)

```bash
# Dựng lại tập dữ liệu từ Hugging Face revision đã pin (nếu chạy trong thư mục mới)
python data/prepare_data.py --out /tmp/btl_rebuild

# Kiểm tra tự động 60 bài gold theo guideline v1.0 đã khóa
python src/check_gold.py --root . --locked-version v1.0
```

### Bước 2: Chạy và chấm các cấu hình trên tập `dev` (10 bài)

```bash
# E0: Baseline Lead-3 (chạy cục bộ, không cần API key)
python src/evaluate.py --root . --repo-root ../repo-BTL-NLP --split dev --experiment E0

# E1: Prompt cơ bản với Ollama Cloud
python src/run_ollama.py --repo-root ../repo-BTL-NLP --experiment E1 --split dev
python src/evaluate.py --root . --repo-root ../repo-BTL-NLP --split dev --experiment E1 \
  --predictions reports/dev_ollama_predictions_E1_<RUN_ID>.csv \
  --model-id deepseek-v4.1-flash --run-label <RUN_ID> \
  --prompt-version e1-basic-v1 --temperature 0.1 \
  --api-endpoint https://ollama.com/api/chat

# E2: Prompt ràng buộc số liệu + hậu kiểm regenerate_once_then_drop
python src/run_ollama.py --repo-root ../repo-BTL-NLP --experiment E2 --split dev
python src/evaluate.py --root . --repo-root ../repo-BTL-NLP --split dev --experiment E2 \
  --predictions reports/dev_ollama_predictions_E2_<RUN_ID>.csv \
  --model-id deepseek-v4.1-flash --run-label <RUN_ID> \
  --prompt-version e2-numeric-v1 --temperature 0.1 \
  --api-endpoint https://ollama.com/api/chat \
  --postcheck-policy regenerate_once_then_drop
```

### Bước 3: Khóa cấu hình và chạy `test` đúng một lần (50 bài)

Chỉ thực hiện sau khi hoàn tất đánh giá trên `dev` và không còn chỉnh sửa prompt/tham số:

```bash
# 1. Commit và gắn tag configs-frozen trên repo-BTL-NLP
git -C ../repo-BTL-NLP tag -a configs-frozen -m "Freeze E0-E2 configs before single test run"
CONFIG_COMMIT=$(git -C ../repo-BTL-NLP rev-parse configs-frozen^{})

# 2. Chấm E0 trên test (1 lần duy nhất)
python src/evaluate.py --root . --repo-root ../repo-BTL-NLP --split test --experiment E0 \
  --config-tag configs-frozen --config-tag-commit "$CONFIG_COMMIT" --confirm-test-once

# 3. Chạy và chấm E1, E2 trên test (1 lần duy nhất mỗi cấu hình)
python src/run_ollama.py --repo-root ../repo-BTL-NLP --experiment E1 --split test \
  --config-tag configs-frozen --config-tag-commit "$CONFIG_COMMIT" --confirm-test-once
python src/evaluate.py --root . --repo-root ../repo-BTL-NLP --split test --experiment E1 \
  --predictions reports/test_ollama_predictions_E1_<RUN_ID>.csv \
  --model-id deepseek-v4.1-flash --run-label <RUN_ID> \
  --prompt-version e1-basic-v1 --temperature 0.1 \
  --api-endpoint https://ollama.com/api/chat \
  --config-tag configs-frozen --config-tag-commit "$CONFIG_COMMIT" --confirm-test-once

python src/run_ollama.py --repo-root ../repo-BTL-NLP --experiment E2 --split test \
  --config-tag configs-frozen --config-tag-commit "$CONFIG_COMMIT" --confirm-test-once
python src/evaluate.py --root . --repo-root ../repo-BTL-NLP --split test --experiment E2 \
  --predictions reports/test_ollama_predictions_E2_<RUN_ID>.csv \
  --model-id deepseek-v4.1-flash --run-label <RUN_ID> \
  --prompt-version e2-numeric-v1 --temperature 0.1 \
  --api-endpoint https://ollama.com/api/chat \
  --postcheck-policy regenerate_once_then_drop \
  --config-tag configs-frozen --config-tag-commit "$CONFIG_COMMIT" --confirm-test-once
```

### Bước 4: Xuất phiếu chấm con người, bảng lỗi số liệu & tổng hợp chỉ số

```bash
python src/build_human_eval_sheet.py --root .
python src/summarize_experiments.py --root .
python src/export_error_candidates.py --root .
```

### Bước 5: Chạy Demo & kiểm thử đơn vị

```bash
# Chạy CLI demo với bài mẫu (E0 offline)
python app/demo.py --mode E0 --input-file app/sample_input.txt

# Hoặc khởi chạy giao diện web cục bộ
python app/demo.py --serve --port 8000

# Chạy toàn bộ unit tests
python -m unittest discover -s tests -v
```
