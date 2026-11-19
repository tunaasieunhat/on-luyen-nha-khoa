# Slide Anh văn chuyên ngành 2 (từ bản 2.6.3)

Nguồn để dựng lại slide 15 Unit của môn Anh văn chuyên ngành 2.

- `w1.txt`–`w3.txt`: từ vựng cho người mất gốc (bản 2.6.1): phiên âm, đọc gần giống, nghĩa, mẹo nhớ, ví dụ, định nghĩa dịch từng cụm.
- `ex1.txt`–`ex3.txt`: 2 câu ví dụ thêm cho mỗi từ (354 câu), có dịch.
- `deck.py`: dựng dữ liệu bộ slide (`out/decks.json` có slide đáp án; `out/decks-app.json` cho app). Câu điền từ lấy đáp án nhiễu ở Unit khác, cùng loại từ, để chỉ có một đáp án hợp nghĩa.
- `avs.css`, `avs.js`: vẽ slide bằng HTML trong khung "Slide bài giảng" của app (nút loa, trắc nghiệm bấm chọn).
- `pptx.js`: xuất PowerPoint chỉnh sửa được, có ghi chú người trình bày (pptxgenjs).
- `mkrender.py`, `slidepdf.js`, `impose.py`: bản in 4 slide/trang A4 ngang, chữ dạng vector (font Carlito, tương đương Calibri).
- `patch263.py`: vá file app đã dựng.

File đã dựng nằm ở `slides/avcn2/`.
