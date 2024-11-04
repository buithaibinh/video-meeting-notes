# Project: Meeting Notes Extractor

## Mô tả
Dự án này cho phép trích xuất văn bản từ video họp và chuyển đổi thành meeting notes đơn giản.

## Cấu trúc
- `src/extract_meeting_notes.py`: Mã Python để trích xuất âm thanh từ video, chuyển đổi thành văn bản và tạo meeting notes.
- `data/`: Chứa video đầu vào và file âm thanh được trích xuất.
- `output/`: Chứa file meeting notes đầu ra.
- `requirements.txt`: Danh sách các thư viện cần cài đặt.
- `README.md`: Hướng dẫn sử dụng.

## Cài đặt
1. Cài đặt các thư viện bằng pip:
   ```bash
   pip install -r requirements.txt
   ```
2. Đảm bảo ffmpeg được cài đặt trên hệ thống.

## Sử dụng

1. Đặt video của bạn vào thư mục `data/` với tên `meeting_video.mov`.
2. Chạy mã Python để trích xuất âm thanh và tạo meeting notes:
   ```bash
   python src/extract_meeting_notes.py
3. Kết quả sẽ được lưu trong thư mục `output/` với tên `meeting_notes.txt`.

## Lưu ý

* Có thể thay đổi tên video hoặc đường dẫn trong script để phù hợp với nhu cầu của bạn.

