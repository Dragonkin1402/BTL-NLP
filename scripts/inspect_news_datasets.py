from collections import Counter
from datetime import datetime
from pathlib import Path
import re

from datasets import load_dataset


ROOT = Path(__file__).resolve().parents[1]
DATASET_REVISIONS = {
    "VLUS06/VietOnlineNews": "bd8d2a865c8981d34cb9d85f69f62bda7c40b520",
    "undertheseanlp/UVN-1": "42a81b44e1e8228146e56a3fa066cc035384b7d9",
}
ECONOMIC_MARKERS = {
    "%": re.compile(r"%", re.IGNORECASE),
    "tỷ đồng": re.compile(r"tỷ\s+đồng", re.IGNORECASE),
    "USD": re.compile(r"USD", re.IGNORECASE),
    "quý": re.compile(r"\bquý\b", re.IGNORECASE),
}


def main() -> None:
    retrieved_at = datetime.now().astimezone().isoformat(timespec="seconds")
    news = load_dataset(
        "VLUS06/VietOnlineNews",
        revision=DATASET_REVISIONS["VLUS06/VietOnlineNews"],
    )
    split_rows = {name: len(split) for name, split in news.items()}
    total_rows = sum(split_rows.values())
    columns = news["train"].column_names
    category_counts = Counter()
    for split in news.values():
        category_counts.update(split["category"])

    marker_counts = Counter()
    economic_ids: set[str] = set()
    for split in news.values():
        selected = split.select_columns(
            ["id", "category", "title", "description", "content"]
        )
        for row in selected:
            if row["category"] != "Kinh doanh":
                continue
            text = " ".join(
                row[field] or "" for field in ("title", "description", "content")
            )
            matching_markers = [
                marker
                for marker, pattern in ECONOMIC_MARKERS.items()
                if pattern.search(text)
            ]
            if matching_markers:
                economic_ids.add(str(row["id"]))
                marker_counts.update(matching_markers)

    uvn = load_dataset(
        "undertheseanlp/UVN-1",
        revision=DATASET_REVISIONS["undertheseanlp/UVN-1"],
    )
    uvn_train = uvn["train"]
    uvn_dates = [
        str(value)[:10]
        for value in uvn_train["publish_date"]
        if value is not None
    ]
    uvn_date_range = (
        f"{min(uvn_dates)} đến {max(uvn_dates)}" if uvn_dates else "không có dữ liệu"
    )

    ids_path = ROOT / "data" / "vietonline_news_economic_numeric_ids.txt"
    ids_path.parent.mkdir(parents=True, exist_ok=True)
    ids_path.write_text(
        "\n".join(sorted(economic_ids)) + "\n",
        encoding="utf-8",
    )
    categories = sorted(category_counts)
    schema_path = ROOT / "data" / "vietonline_news_schema.txt"
    schema_lines = [
        "Dataset: VLUS06/VietOnlineNews",
        f"Retrieved at: {retrieved_at}",
        f"Revision: {DATASET_REVISIONS['VLUS06/VietOnlineNews']}",
        f"column_names: {', '.join(columns)}",
        f"category ({len(categories)}):",
        *(f"- {category}" for category in categories),
    ]
    schema_path.write_text("\n".join(schema_lines) + "\n", encoding="utf-8")

    report = render_data_card(
        retrieved_at=retrieved_at,
        columns=columns,
        split_rows=split_rows,
        total_rows=total_rows,
        category_counts=category_counts,
        marker_counts=marker_counts,
        economic_match_count=len(economic_ids),
        ids_path=ids_path.relative_to(ROOT).as_posix(),
        uvn_rows=len(uvn_train),
        uvn_columns=uvn_train.column_names,
        uvn_date_range=uvn_date_range,
    )
    card_path = ROOT / "data_card.md"
    previous_card = card_path.read_text(encoding="utf-8") if card_path.exists() else ""
    manual_section = previous_card.find("\n## 7. ")
    if manual_section >= 0:
        report = f"{report.rstrip()}\n\n{previous_card[manual_section + 1:]}"
    card_path.write_text(report, encoding="utf-8")

    print(f"VietOnlineNews columns: {columns}")
    print(f"VietOnlineNews rows by split: {split_rows} (total={total_rows})")
    print("VietOnlineNews category distribution:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} ({count / total_rows:.2%})")
    print("Kinh doanh articles matching numeric markers:")
    for marker in ECONOMIC_MARKERS:
        print(f"  {marker}: {marker_counts[marker]}")
    print(f"  unique matching articles: {len(economic_ids)}")
    print(f"UVN-1 columns: {uvn_train.column_names}")
    print(f"UVN-1 rows: {len(uvn_train)}")
    print(f"UVN-1 publish_date range: {uvn_date_range}")
    print(f"Wrote {card_path}")
    print(f"Wrote ID-only list {ids_path}")
    print(f"Wrote schema and categories {schema_path}")


def render_data_card(
    *,
    retrieved_at: str,
    columns: list[str],
    split_rows: dict[str, int],
    total_rows: int,
    category_counts: Counter,
    marker_counts: Counter,
    economic_match_count: int,
    ids_path: str,
    uvn_rows: int,
    uvn_columns: list[str],
    uvn_date_range: str,
) -> str:
    split_table = "\n".join(
        f"| {name} | {count:,} |" for name, count in split_rows.items()
    )
    category_table = "\n".join(
        f"| {category} | {count:,} | {count / total_rows:.2%} |"
        for category, count in sorted(
            category_counts.items(), key=lambda item: (-item[1], item[0])
        )
    )
    marker_table = "\n".join(
        f"| `{marker}` | {marker_counts[marker]:,} |"
        for marker in ECONOMIC_MARKERS
    )
    return f"""# Data Card — VietOnlineNews (dataset chính)

## 1. Tóm tắt

Chọn `VLUS06/VietOnlineNews` làm nguồn bài báo chính cho đề tài tóm tắt tin kinh tế tiếng Việt có kiểm chứng dữ kiện. Dataset gốc có nhãn phân loại chủ đề 13 lớp (`category`), nhưng nhãn này không phải nhãn tóm tắt. Gold của BTL được nhóm tự xây dựng trên 60 bài chọn lọc (10 dev, 50 test), gồm tóm tắt tham chiếu và phiếu dữ kiện số. Không dùng các dataset tóm tắt tin như `Linhz/Vietnews` hoặc `harouzie/vietnews`.

## 2. Dataset snapshot

| Thuộc tính | VietOnlineNews |
|---|---|
| Hugging Face ID | [`VLUS06/VietOnlineNews`](https://huggingface.co/datasets/VLUS06/VietOnlineNews) |
| Ngôn ngữ / tác vụ | Tiếng Việt / dataset gốc phân loại chủ đề đơn nhãn; BTL tạo gold tóm tắt tin kinh tế và dữ kiện số |
| Tổng số dòng | {total_rows:,} |
| Cột | `{", ".join(columns)}` |
| Retrieved at | `{retrieved_at}` |
| Revision đã pin | `{DATASET_REVISIONS["VLUS06/VietOnlineNews"]}` |

| Split | Số dòng |
|---|---:|
{split_table}

Hub README mô tả dữ liệu từ VietnamNet, Thanh Niên và Tuổi Trẻ, thời gian 2023–2025. Schema được tải không có cột nguồn hoặc ngày đăng, nên không thể kiểm chứng các trường đó ở cấp từng bài từ bản này.

**Nguồn đối chiếu UVN-1 (không phải dataset chính):** [`undertheseanlp/UVN-1`](https://huggingface.co/datasets/undertheseanlp/UVN-1), revision `{DATASET_REVISIONS["undertheseanlp/UVN-1"]}`, {uvn_rows:,} dòng, cột `{", ".join(uvn_columns)}`. Metadata có trường `publish_date` với khoảng giá trị **{uvn_date_range}**; không có trường `published_at`. Khoảng ngày này lấy từ metadata của dataset, không suy ra từ ngày crawl. Hub khai báo license `CC-BY-NC-4.0`.

## 3. Mục đích sử dụng

- Phù hợp: làm nguồn bài báo cho bộ gold 60 bài của BTL, phục vụ đánh giá tóm tắt tin kinh tế và bảo toàn dữ kiện số.
- Giới hạn: dataset gốc không cung cấp nhãn tóm tắt; `category` chỉ là nhãn chủ đề. Tóm tắt và phiếu dữ kiện do nhóm tạo, cần được đánh giá theo quy trình annotation dưới đây.
- Chỉ dùng kết quả theo split và revision đã ghi; không suy rộng sang toàn bộ báo chí Việt Nam.

## 4. License và quy tắc lưu trữ

Hub gắn `license: other` cho VietOnlineNews, không phải một SPDX license cụ thể. Repo có mục `LICENSE` nhưng nội dung truy cập được trong lần kiểm tra này rỗng; vì vậy **chưa xác minh được quyền sử dụng hoặc tái phân phối**. Cần hỏi người phát hành/giảng viên và kiểm tra điều khoản của các nguồn báo trước khi công bố hay chia sẻ dữ liệu.

Không commit/push `title`, `description`, `content` hoặc các bản dump CSV/Parquet/JSONL. Bộ 60 bài dùng cho annotation được lưu cục bộ trong `data/processed/selected_articles.jsonl`, có chứa toàn văn; file này cùng các annotation có trích câu nguồn được đưa vào `.gitignore` và không được đẩy công khai.

## 5. Bằng chứng chất lượng và lọc bài kinh doanh

### Phân bố category

Split sizes quan sát được khi tải revision đã pin ở trên khác với con số split trong Hub README (README ghi 187,682 / 40,218 / 40,218, tổng 268,118). Dùng số đếm trực tiếp từ loader cho báo cáo này; cần xác minh sai khác với người phát hành trước khi so sánh theo split.

| Category | Số bài | Tỷ lệ |
|---|---:|---:|
{category_table}

### Bài `Kinh doanh` có dấu hiệu số liệu

Đếm bài thuộc `Kinh doanh` có ít nhất một chuỗi dưới đây trong `title`, `description` hoặc `content` (không phân biệt hoa/thường):

| Chuỗi dò | Số bài khớp |
|---|---:|
{marker_table}
| **Khớp ít nhất một chuỗi (duy nhất)** | **{economic_match_count:,}** |

Đây là bộ lọc từ khóa thô, không khẳng định bài có số liệu tài chính hợp lệ (đặc biệt `quý` có thể mang nghĩa khác). Danh sách ID, không có nội dung bài: [`{ids_path}`]({ids_path}).

## 6. Tái lập

Chạy `python scripts/inspect_news_datasets.py` từ thư mục `BTL` sau khi cài `datasets`. Script tải theo revision đã pin, in schema/số dòng/phân bố, cập nhật Data Card và ghi danh sách ID khớp cùng metadata schema; không lưu nội dung bài. Các phần annotation-process và lịch sử test bắt đầu từ mục 7 được giữ lại khi Data Card được tái tạo.
"""


if __name__ == "__main__":
    main()
