[PRD.md](https://github.com/user-attachments/files/28431925/PRD.md)[U# 📋 PRD – Product Requirements Document
# Hệ Thống AI Phân Biệt Thể Loại Nhạc (LapTrinhAmThanh)

> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 29/05/2026  
> **Tác giả:** Nhóm LapTrinhAmThanh  
> **Trạng thái:** Released

---

## 1. Tổng Quan Sản Phẩm

### 1.1 Mô Tả

**LapTrinhAmThanh** là hệ thống phân loại thể loại âm nhạc tự động sử dụng Machine Learning. Hệ thống nhận đầu vào là một file âm thanh (`.wav`, `.mp3`,...), phân tích các đặc trưng âm học và đưa ra dự đoán thể loại nhạc tương ứng trong số 10 thể loại được hỗ trợ.

Ứng dụng được xây dựng bằng Python, sử dụng mô hình **SVM (Support Vector Machine)** được huấn luyện trên bộ dữ liệu **GTZAN**, kết hợp thư viện **Librosa** để trích xuất đặc trưng âm thanh và **Gradio** để tạo giao diện web.

### 1.2 Mục Tiêu Sản Phẩm

| STT | Mục tiêu | Chỉ số đo lường |
|-----|----------|-----------------|
| 1 | Phân loại đúng thể loại nhạc từ file âm thanh | Accuracy ≥ 80% trên tập test |
| 2 | Thời gian xử lý chấp nhận được | ≤ 10 giây / bài |
| 3 | Giao diện dễ sử dụng, không cần kỹ thuật | Người dùng phổ thông có thể dùng ngay |
| 4 | Hệ thống chạy offline không cần internet | Chạy local hoàn toàn |

### 1.3 Phạm Vi Phiên Bản 1.0

**Bao gồm:**
- Trích xuất đặc trưng âm thanh từ file 30 giây
- Trích xuất đặc trưng theo đoạn 3 giây (10 đoạn/bài)
- Lưu đặc trưng vào CSV và MySQL
- Giao diện web Gradio để dự đoán
- Mô hình SVM đã huấn luyện sẵn (`.pkl`)

**Không bao gồm:**
- Mobile App
- API REST cho bên thứ ba
- Hỗ trợ streaming audio
- Training lại model từ giao diện

---

## 2. Người Dùng Mục Tiêu

### 2.1 Personas

**Persona 1 – Sinh viên / Nghiên cứu viên**
- Mục đích: Kiểm tra kết quả mô hình, học về audio ML
- Hành vi: Upload file nhạc, xem kết quả dự đoán, so sánh với nhãn thực

**Persona 2 – Giảng viên / Demo**
- Mục đích: Trình bày ứng dụng học máy trong lớp học
- Hành vi: Chạy `app.py`, mở browser, demo trực tiếp trước lớp

**Persona 3 – Developer**
- Mục đích: Tái sử dụng pipeline trích xuất đặc trưng cho dự án khác
- Hành vi: Import `feature_extraction.py`, tích hợp vào pipeline riêng

---

## 3. Yêu Cầu Chức Năng

### 3.1 Module Trích Xuất Đặc Trưng (`feature_extraction.py`)

| ID | Tính năng | Mô tả chi tiết | Ưu tiên |
|----|-----------|----------------|---------|
| F-01 | Load audio 30 giây | Dùng `librosa.load(duration=30.0)` để đọc đúng 30s đầu tiên | P0 |
| F-02 | Trích xuất Tempo | `librosa.beat.beat_track()` – nhịp điệu bài hát (BPM) | P0 |
| F-03 | Trích xuất Chroma STFT | `librosa.feature.chroma_stft()` – phân bố tần số theo 12 nốt nhạc | P0 |
| F-04 | Trích xuất RMS Energy | `librosa.feature.rms()` – năng lượng âm thanh | P0 |
| F-05 | Trích xuất Spectral Centroid | `librosa.feature.spectral_centroid()` – trọng tâm phổ tần số | P0 |
| F-06 | Trích xuất Spectral Bandwidth | `librosa.feature.spectral_bandwidth()` – độ rộng phổ tần số | P0 |
| F-07 | Trích xuất Rolloff | `librosa.feature.spectral_rolloff()` – điểm tần số rolloff 85% | P0 |
| F-08 | Trích xuất ZCR | `librosa.feature.zero_crossing_rate()` – tỷ lệ vượt qua 0 | P0 |
| F-09 | Trích xuất 20 MFCC | `librosa.feature.mfcc(n_mfcc=20)` – 20 hệ số cepstral (mean + var = 40 features) | P0 |
| F-10 | Trích xuất Harmony/Percussive | `librosa.effects.harmonic/percussive()` – tách thành phần hòa âm và tiết tấu | P0 |
| F-11 | Trích xuất Chroma CQT | `librosa.feature.chroma_cqt()` – phân bố tần số theo CQT | P0 |
| F-12 | Lưu CSV | `df.to_csv('example_features_with_path.csv')` với cột `filename`, `file_path`, `genre_label` | P0 |
| F-13 | Lưu MySQL | Ghi vào bảng `songs_features` trong database `music_db` qua SQLAlchemy | P1 |
| F-14 | Multiprocessing | Dùng `multiprocessing.Pool` với tối đa 16 core để xử lý song song | P1 |

**Tổng số đặc trưng được trích xuất: 59 features**
- 1 (`length`) + 2 (`chroma_stft`) + 2 (`rms`) + 2 (`spectral_centroid`) + 2 (`spectral_bandwidth`) + 2 (`rolloff`) + 2 (`zcr`) + 2 (`harmony`) + 2 (`percussive`) + 1 (`tempo`) + 40 (`mfcc1-20 mean+var`) + 2 (`chroma_cqt`) = **60 features**

---

### 3.2 Module Trích Xuất 3 Giây (`extract_features_3sec.py`)

| ID | Tính năng | Mô tả chi tiết | Ưu tiên |
|----|-----------|----------------|---------|
| F-15 | Chia bài thành 10 đoạn 3s | Mỗi bài 30s → 10 segment, offset = `idx * 3.0` | P0 |
| F-16 | Ép `length = 66149` | Chuẩn hóa độ dài mẫu cho đoạn 3s (sample count cố định) | P0 |
| F-17 | Đặt tên segment | Format: `{base_name}.{segment_idx}` (ví dụ: `blues.00000.0`) | P0 |
| F-18 | Xuất CSV 3s | Lưu `example_features_3_sec.csv` với ~10.000 hàng (1000 bài × 10 đoạn) | P0 |
| F-19 | Gán nhãn tự động | Lấy prefix trước dấu `.` đầu tiên của filename làm `genre_label` | P0 |

---

### 3.3 Module Ứng Dụng Web (`app.py`)

| ID | Tính năng | Mô tả chi tiết | Ưu tiên |
|----|-----------|----------------|---------|
| F-20 | Load model `.pkl` | Tự động load `music_scaler.pkl`, `music_svm_model.pkl`, `music_categories.pkl` khi khởi động | P0 |
| F-21 | Upload file nhạc | Gradio `gr.Audio(type="filepath")` – hỗ trợ kéo thả | P0 |
| F-22 | Trích xuất đặc trưng realtime | Chạy `predict_genre_of_file()` với file vừa upload | P0 |
| F-23 | Chuẩn hóa đặc trưng | `scaler.transform()` đảm bảo đúng thứ tự cột theo `feature_names_in_` | P0 |
| F-24 | Dự đoán thể loại | `model.predict()` → map qua `categories_list` → trả về tên thể loại viết hoa | P0 |
| F-25 | Hiển thị kết quả | Textbox với format: `🎵 Dự đoán thể loại: {GENRE}` | P0 |
| F-26 | Xử lý lỗi | Bắt exception, trả về thông báo lỗi thân thiện, log chi tiết ra console | P1 |
| F-27 | Chế độ share | Tham số `share=False` (local), đổi `True` để lấy link Gradio public | P2 |

---

## 4. Yêu Cầu Phi Chức Năng

### 4.1 Hiệu Năng

| Yêu cầu | Giá trị mục tiêu |
|---------|-----------------|
| Thời gian trích xuất đặc trưng 1 bài (30s) | ≤ 5 giây |
| Thời gian trích xuất toàn bộ dataset (1000 bài) | ≤ 10 phút (với 16 core) |
| Thời gian dự đoán trên giao diện web | ≤ 10 giây |
| RAM sử dụng khi chạy app.py | ≤ 2 GB |

### 4.2 Môi Trường

| Thành phần | Yêu cầu |
|-----------|---------|
| Python | ≥ 3.9 |
| OS | Windows / macOS / Linux |
| RAM | ≥ 4 GB |
| Database | MySQL 8.0+ (tùy chọn) |
| Browser | Chrome / Firefox / Edge (cho Gradio UI) |

### 4.3 Bảo Mật

- Không lưu file âm thanh của người dùng sau khi dự đoán
- Thông tin đăng nhập MySQL được hard-code trong `feature_extraction.py` (cần chuyển sang biến môi trường trong production)
- Ứng dụng chạy `share=False` theo mặc định (local only)

---

## 5. Luồng Xử Lý Chính

### 5.1 Luồng Huấn Luyện (Offline)

```
genres_original/
    ├── blues/     (100 file .wav)
    ├── classical/ (100 file .wav)
    ├── ...
    └── rock/      (100 file .wav)
          │
          ▼
feature_extraction.py          extract_features_3sec.py
(trích xuất 30s/bài)           (trích xuất 10×3s/bài)
          │                              │
          ▼                              ▼
example_features_with_path.csv    example_features_3_sec.csv
songs_features (MySQL)
          │
          ▼
ml_classification.ipynb
(Train SVM, GridSearchCV, evaluate)
          │
          ▼
music_svm_model.pkl + music_scaler.pkl + music_categories.pkl
```

### 5.2 Luồng Dự Đoán (Online – app.py)

```
User upload file nhạc
          │
          ▼
librosa.load(duration=30.0)
          │
          ▼
Trích xuất 60 đặc trưng
(tempo, chroma, rms, mfcc×20, ...)
          │
          ▼
pd.DataFrame → reindex theo scaler.feature_names_in_
          │
          ▼
scaler.transform()
          │
          ▼
model_svm.predict()
          │
          ▼
categories_list[pred_code].upper()
          │
          ▼
"🎵 Dự đoán thể loại: BLUES"
```

---

## 6. Thể Loại Nhạc Được Hỗ Trợ

| STT | Thể loại | Số bài (train) |
|-----|----------|---------------|
| 1 | Blues | 100 |
| 2 | Classical | 100 |
| 3 | Country | 100 |
| 4 | Disco | 100 |
| 5 | Hip-hop | 100 |
| 6 | Jazz | 100 |
| 7 | Metal | 100 |
| 8 | Pop | 100 |
| 9 | Reggae | 100 |
| 10 | Rock | 100 |
| **Tổng** | **10 thể loại** | **1.000 bài** |

> **Nguồn dữ liệu:** GTZAN Dataset – chuẩn nghiên cứu phổ biến trong Music Information Retrieval (MIR)

---

## 7. Các Ràng Buộc Kỹ Thuật

| Ràng buộc | Lý do |
|-----------|-------|
| File nhạc phải có thời lượng ≥ 30 giây | `librosa.load(duration=30.0)` lấy đúng 30s đầu |
| Model chỉ nhận đúng 60 features theo thứ tự | `scaler.feature_names_in_` kiểm tra thứ tự cột |
| Cần có 3 file `.pkl` trước khi chạy `app.py` | App exit ngay nếu load model thất bại |
| MySQL cần chạy trước khi chạy `feature_extraction.py` | Kết nối `127.0.0.1:3306/music_db` |
| Không có Chroma CQT trong `extract_features_3sec.py` | File 3s đủ 60 features kể cả chroma_cqt |

---

## 8. Rủi Ro & Giảm Thiểu

| Rủi ro | Mức độ | Giảm thiểu |
|--------|--------|-----------|
| File nhạc < 30 giây → thiếu data | Cao | Thêm validation trước khi predict |
| MySQL không kết nối được | Trung bình | Feature extraction vẫn lưu CSV, MySQL là tùy chọn |
| Model overfit trên GTZAN | Trung bình | Đánh giá trên `music_test/` riêng biệt |
| Hard-code password MySQL trong code | Cao | Chuyển sang `.env` file hoặc `os.environ` |

---

## 9. Định Nghĩa Hoàn Thành (Definition of Done)

- [ ] `feature_extraction.py` chạy thành công trên toàn bộ `genres_original/`
- [ ] `extract_features_3sec.py` tạo ra file CSV với đúng 10.000 hàng
- [ ] `ml_classification.ipynb` train xong và xuất 3 file `.pkl`
- [ ] `app.py` khởi động được và load model thành công
- [ ] Giao diện Gradio mở trên browser, dự đoán đúng ≥ 3/5 file test thủ công
- [ ] Tài liệu README, PRD, Wiki đầy đủ

---

*PRD này được tạo dựa trên phân tích mã nguồn thực tế của project LapTrinhAmThanh.*
ploading PRD.md…]()

[Wiki_README.md](https://github.com/user-attachments/files/28431909/Wiki_README.md)
# 📖 WIKI – Tài Liệu Hướng Dẫn Đầy Đủ
# LapTrinhAmThanh – AI Phân Biệt Thể Loại Nhạc

> **Phiên bản:** 1.0 | **Cập nhật:** 29/05/2026

---

## Mục Lục

1. [Giới thiệu dự án](#1-giới-thiệu-dự-án)
2. [Yêu cầu cài đặt](#2-yêu-cầu-cài-đặt)
3. [Cài đặt môi trường](#3-cài-đặt-môi-trường)
4. [Cấu trúc thư mục](#4-cấu-trúc-thư-mục)
5. [Hướng dẫn chạy từng module](#5-hướng-dẫn-chạy-từng-module)
6. [Giải thích chi tiết từng file](#6-giải-thích-chi-tiết-từng-file)
7. [Các đặc trưng âm thanh được trích xuất](#7-các-đặc-trưng-âm-thanh-được-trích-xuất)
8. [Cơ sở dữ liệu MySQL](#8-cơ-sở-dữ-liệu-mysql)
9. [Mô hình Machine Learning](#9-mô-hình-machine-learning)
10. [Giao diện Web Gradio](#10-giao-diện-web-gradio)
11. [Xử lý lỗi thường gặp](#11-xử-lý-lỗi-thường-gặp)
12. [Thư viện và dependencies](#12-thư-viện-và-dependencies)

---

## 1. Giới Thiệu Dự Án

**LapTrinhAmThanh** là hệ thống phân loại thể loại âm nhạc tự động sử dụng Machine Learning, được xây dựng bằng Python.

### Tính năng chính

- Phân tích file âm thanh và dự đoán 1 trong 10 thể loại nhạc
- Trích xuất 60 đặc trưng âm học từ thư viện **Librosa**
- Sử dụng mô hình **SVM (Support Vector Machine)** để phân loại
- Giao diện web trực quan bằng **Gradio** (kéo thả file, click dự đoán)
- Hỗ trợ lưu dữ liệu vào **MySQL** và **CSV**
- Xử lý song song (multiprocessing) để tăng tốc trích xuất

### 10 thể loại được hỗ trợ

`blues` | `classical` | `country` | `disco` | `hiphop` | `jazz` | `metal` | `pop` | `reggae` | `rock`

---

## 2. Yêu Cầu Cài Đặt

### Phần mềm bắt buộc

| Phần mềm | Phiên bản tối thiểu | Tải về |
|---------|-------------------|--------|
| Python | 3.9+ | https://python.org |
| pip | 21+ | (đi kèm Python) |

### Phần mềm tùy chọn

| Phần mềm | Mục đích | Ghi chú |
|---------|---------|---------|
| MySQL Server | Lưu features vào database | Chỉ cần cho `feature_extraction.py` |
| JupyterLab | Chạy `ml_classification.ipynb` | Đã có trong `requirements.txt` |

### Phần cứng khuyến nghị

| Thành phần | Tối thiểu | Khuyến nghị |
|-----------|-----------|------------|
| RAM | 4 GB | 8 GB+ |
| CPU | 4 cores | 8+ cores (cho multiprocessing) |
| Ổ cứng | 5 GB trống | 10 GB+ |

---

## 3. Cài Đặt Môi Trường

### Bước 1: Clone hoặc mở project

```bash
cd ~/Desktop/LTAT/LapTrinhAmThanh
```

### Bước 2: Tạo virtual environment

```bash
# Tạo .venv
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Kích hoạt (macOS / Linux)
source .venv/bin/activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Chi tiết `requirements.txt`:
```
numpy==2.4.6          # Xử lý mảng đa chiều, ma trận
pandas==3.0.3         # Đọc/ghi CSV, thao tác DataFrame
scipy                 # Toán học nâng cao (hỗ trợ librosa, sklearn)
matplotlib==3.10.0    # Vẽ biểu đồ cơ bản
seaborn==0.13.2       # Vẽ Confusion Matrix, Heatmap
scikit-learn==1.6.0   # SVM, StandardScaler, train/test split
xgboost==2.1.3        # XGBoost (có trong notebook)
librosa==0.11.0       # Phân tích và trích xuất đặc trưng âm thanh
gradio==6.15.2        # Giao diện web UI
joblib==1.5.3         # Lưu/tải model .pkl
jupyterlab==4.3.0     # Môi trường chạy notebook .ipynb
```

### Bước 4: (Tùy chọn) Thiết lập MySQL

```sql
-- Tạo database
CREATE DATABASE music_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user (nếu không dùng root)
CREATE USER 'music_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON music_db.* TO 'music_user'@'localhost';
FLUSH PRIVILEGES;
```

> ⚠️ **Quan trọng:** Nếu đổi thông tin đăng nhập, cập nhật trong `feature_extraction.py` tại:
> ```python
> username = "root"
> password = quote_plus("22092005@Dung")
> host = "127.0.0.1"
> port = "3306"
> database_name = "music_db"
> ```

---

## 4. Cấu Trúc Thư Mục

```
LapTrinhAmThanh/
│
├── .venv/                              # Virtual environment (không commit)
│
├── genres_original/                    # Dataset GTZAN – 1000 bài WAV (30s)
│   ├── blues/         → blues.00000.wav ... blues.00099.wav
│   ├── classical/     → classical.00000.wav ... classical.00099.wav
│   ├── country/       → ...
│   ├── disco/         → ...
│   ├── hiphop/        → ...
│   ├── jazz/          → ...
│   ├── metal/         → ...
│   ├── pop/           → ...
│   ├── reggae/        → ...
│   └── rock/          → rock.00000.wav ... rock.00099.wav
│
├── music_test/                         # Dataset test độc lập
│   ├── blues/
│   ├── classical/
│   ├── disco/
│   ├── hiphop/
│   ├── jazz/
│   ├── metal/
│   ├── pop/
│   ├── reggae/
│   └── rock/
│
├── ── SCRIPTS ──
├── feature_extraction.py               # Trích xuất 60 features / bài 30s → CSV + MySQL
├── extract_features_3sec.py            # Trích xuất 60 features / đoạn 3s → CSV
├── ml_classification.ipynb             # Huấn luyện và đánh giá mô hình SVM
├── app.py                              # Web app Gradio – dự đoán thể loại
│
├── ── DATA ──
├── example_features.csv                # Features mẫu (format cơ bản)
├── example_features_3_sec.csv          # ~10.000 hàng × 61 cột (3s segments)
├── example_features_with_path.csv      # ~1.000 hàng × 63 cột (30s + path)
│
├── ── MODELS ──
├── music_svm_model.pkl                 # Mô hình SVM đã huấn luyện
├── music_scaler.pkl                    # StandardScaler đã fit trên train data
├── music_categories.pkl                # ['blues', 'classical', ..., 'rock']
│
├── ── DOCUMENTATION ──
├── Bao_cao_Testcase_Phan_Cap.csv       # Test case phân cấp
├── Dump20260528.sql                    # MySQL dump
└── requirements.txt                    # Dependencies
```

---

## 5. Hướng Dẫn Chạy Từng Module

### 5.1 Trích Xuất Đặc Trưng 30 Giây

**Mục đích:** Xử lý toàn bộ `genres_original/`, tạo CSV và ghi vào MySQL.

```bash
# Đảm bảo đang ở thư mục gốc và đã kích hoạt .venv
python feature_extraction.py
```

**Đầu ra:**
- File: `example_features_with_path.csv` (~1.000 hàng × 63 cột)
- Database: bảng `songs_features` trong MySQL `music_db`

**Console output mẫu:**
```
🚀 Tìm thấy 1000 bài hát.
⚡ Đang dùng 16 nhân CPU...
✅ Đã trích xuất xong!
💾 Đã lưu CSV: example_features_with_path.csv
✅ Kết nối MySQL thành công!
🎉 Đã lưu dữ liệu vào MySQL!
🚀 HOÀN THÀNH!
```

---

### 5.2 Trích Xuất Đặc Trưng 3 Giây

**Mục đích:** Băm mỗi bài 30s thành 10 đoạn 3s, tạo dataset lớn hơn (10.000 samples).

```bash
python extract_features_3sec.py
```

**Đầu ra:**
- File: `example_features_3_sec.csv` (~10.000 hàng × 61 cột)

**Console output mẫu:**
```
🚀 Tìm thấy 1000 bài hát gốc.
🔥 Sẵn sàng băm nhỏ thành 10000 đoạn 3 giây sử dụng 8 nhân CPU...
✅ Đã trích xuất xong toàn bộ 10.000 đoạn! Đang gộp dữ liệu...
🎉 THÀNH CÔNG RỰC RỠ! Bản 3s đã được tạo lập.
💾 File lưu tại: /path/to/example_features_3_sec.csv
📊 Tổng quy mô dữ liệu thu được: 10000 hàng, 61 cột.
```

---

### 5.3 Huấn Luyện Mô Hình

**Mục đích:** Đọc CSV đặc trưng, train SVM, lưu 3 file `.pkl`.

```bash
# Khởi động JupyterLab
jupyter lab

# Mở file ml_classification.ipynb
# Chạy tuần tự các ô code từ trên xuống dưới
```

**Kết quả sau khi chạy notebook:**
- `music_svm_model.pkl` – mô hình SVM
- `music_scaler.pkl` – StandardScaler
- `music_categories.pkl` – danh sách thể loại

> ⚠️ **Bắt buộc phải chạy notebook này trước khi chạy `app.py`!**

---

### 5.4 Chạy Web App

**Mục đích:** Khởi động giao diện web để dự đoán thể loại nhạc.

```bash
python app.py
```

**Sau khi khởi động:**
```
Đang nạp cấu hình AI từ file .pkl... Vui lòng đợi...
Nạp AI thành công! Hệ thống sẵn sàng hoạt động.
Running on local URL:  http://127.0.0.1:7860
```

Mở trình duyệt, truy cập: **http://127.0.0.1:7860**

**Cách sử dụng:**
1. Kéo thả file nhạc vào ô "Tải file nhạc của bạn lên tại đây"
2. Nhấn nút **"🔮 Bắt đầu phân tích & Dự đoán"**
3. Chờ khoảng 5–10 giây
4. Kết quả hiện ở ô bên phải: `🎵 Dự đoán thể loại: BLUES`

**Muốn chia sẻ link cho người khác:**
```python
# Trong app.py, đổi dòng cuối thành:
demo.launch(share=True)
# Gradio sẽ tạo link dạng: https://xxxx.gradio.live
```

---

### 5.5 Thứ Tự Chạy Đúng (Lần Đầu Cài)

```
Bước 1: pip install -r requirements.txt
Bước 2: python feature_extraction.py     ← Tạo CSV + MySQL
Bước 3: python extract_features_3sec.py  ← Tạo CSV 3s (tùy chọn)
Bước 4: jupyter lab → ml_classification.ipynb → Run All  ← Tạo .pkl
Bước 5: python app.py                    ← Chạy web app
```

---

## 6. Giải Thích Chi Tiết Từng File

### 6.1 `feature_extraction.py`

**Hàm chính: `get_all_musical_features()`**

```python
def get_all_musical_features(
    audio_path,      # Đường dẫn file .wav
    song_name,       # Tên bài (dùng làm index)
    start=0,         # Offset giây bắt đầu (mặc định 0)
    chroma_method_list=['cqt']  # Phương pháp chroma thêm
)
```

Hàm này load file âm thanh và trích xuất 60 đặc trưng. Kết quả là một DataFrame 1 hàng.

**Xử lý song song:**

```python
# Sử dụng multiprocessing để xử lý nhiều file cùng lúc
num_processors = min(16, cpu_count())  # Tối đa 16 core
with Pool(processes=num_processors) as pool:
    df_list = pool.map(extract_single_song, wav_list)
```

> **Lưu ý:** Trên Windows, code multiprocessing phải nằm trong `if __name__ == '__main__':` – đã được đảm bảo trong file.

---

### 6.2 `extract_features_3sec.py`

**Khác biệt so với `feature_extraction.py`:**

| Tiêu chí | feature_extraction.py | extract_features_3sec.py |
|---------|----------------------|--------------------------|
| Thời lượng | 30 giây / bài | 3 giây / đoạn |
| Số mẫu đầu ra | ~1.000 hàng | ~10.000 hàng |
| `length` | Tự nhiên (~661.794) | Ép cứng = `66149` |
| Lưu MySQL | Có | Không |
| Offset | 0 | `idx * 3.0` (idx từ 0 đến 9) |

**Tại sao ép `length = 66149`?**

Vì dataset GTZAN 3-second gốc có cột `length = 66149` (3s × 22050 Hz ≈ 66.150 samples). Ép cứng giá trị này giúp đặc trưng nhất quán với mô hình đã train trên dataset 3s gốc.

---

### 6.3 `app.py`

**Hàm dự đoán: `predict_genre_of_file()`**

Hàm này thực hiện chính xác cùng pipeline trích xuất như `feature_extraction.py`, nhưng chỉ cho 1 file tại thời điểm runtime:

```python
# Bước quan trọng: reindex theo đúng thứ tự cột của scaler
if hasattr(scaler, 'feature_names_in_'):
    df_song = df_song.reindex(columns=scaler.feature_names_in_)
```

> ⚠️ Nếu bỏ dòng này, predict có thể sai hoặc crash do sai thứ tự cột!

**Graceful Error Handling:**

```python
try:
    prediction = predict_genre_of_file(...)
    return f"🎵 Dự đoán thể loại: {prediction}"
except Exception as e:
    error_msg = traceback.format_exc()
    print(f"Chi tiết lỗi hệ thống:\n{error_msg}")  # Log chi tiết ra console
    return f"Lỗi trích xuất đặc trưng âm thanh: {str(e)}"  # Thông báo ngắn gọn cho user
```

---

## 7. Các Đặc Trưng Âm Thanh Được Trích Xuất

### 7.1 Danh Sách Đầy Đủ 60 Đặc Trưng

| STT | Tên cột | Thư viện | Ý nghĩa |
|-----|---------|---------|---------|
| 1 | `length` | numpy | Số lượng sample của file âm thanh |
| 2 | `chroma_stft_mean` | librosa | Phân bố năng lượng trung bình theo 12 nốt nhạc (STFT) |
| 3 | `chroma_stft_var` | librosa | Độ biến thiên phân bố nốt nhạc |
| 4 | `rms_mean` | librosa | Biên độ âm thanh trung bình (cường độ) |
| 5 | `rms_var` | librosa | Độ biến thiên cường độ |
| 6 | `spectral_centroid_mean` | librosa | Tần số "trọng tâm" – nhạc bass vs treble |
| 7 | `spectral_centroid_var` | librosa | Độ biến thiên trọng tâm phổ |
| 8 | `spectral_bandwidth_mean` | librosa | Độ rộng dải tần số |
| 9 | `spectral_bandwidth_var` | librosa | Độ biến thiên độ rộng phổ |
| 10 | `rolloff_mean` | librosa | Điểm tần số chứa 85% năng lượng |
| 11 | `rolloff_var` | librosa | Độ biến thiên rolloff |
| 12 | `zero_crossing_rate_mean` | librosa | Tỷ lệ tín hiệu đổi dấu (noise level) |
| 13 | `zero_crossing_rate_var` | librosa | Độ biến thiên ZCR |
| 14 | `harmony_mean` | librosa | Trung bình thành phần hòa âm (sau HPSS) |
| 15 | `harmony_var` | librosa | Độ biến thiên hòa âm |
| 16 | `perceptr_mean` | librosa | Trung bình thành phần nhịp/tiết tấu (sau HPSS) |
| 17 | `perceptr_var` | librosa | Độ biến thiên tiết tấu |
| 18 | `tempo` | librosa | Ước tính nhịp điệu BPM |
| 19–38 | `mfcc1_mean` → `mfcc10_var` | librosa | 10 MFCC đầu (mean + var) – màu âm sắc |
| 39–58 | `mfcc11_mean` → `mfcc20_var` | librosa | 10 MFCC sau (mean + var) – chi tiết âm sắc |
| 59 | `chroma_cqt_mean` | librosa | Phân bố nốt nhạc theo CQT (chính xác hơn) |
| 60 | `chroma_cqt_var` | librosa | Độ biến thiên Chroma CQT |

### 7.2 Tại Sao MFCC Quan Trọng?

MFCC (Mel-Frequency Cepstral Coefficients) mô phỏng cách tai người cảm nhận âm thanh. 20 MFCC × 2 (mean + var) = 40 features, chiếm 67% tổng số đặc trưng. Đây là nhóm đặc trưng quan trọng nhất cho phân loại thể loại nhạc.

---

## 8. Cơ Sở Dữ Liệu MySQL

### 8.1 Kết Nối

```python
# Trong feature_extraction.py
from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "root"
password = quote_plus("22092005@Dung")  # URL-encode ký tự đặc biệt
host = "127.0.0.1"
port = "3306"
database_name = "music_db"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
)
```

### 8.2 Ghi Dữ Liệu

```python
df_features_sql.to_sql(
    name='songs_features',
    con=engine,
    if_exists='replace',   # Xóa bảng cũ và tạo lại
    index=False
)
```

> ⚠️ `if_exists='replace'` sẽ **xóa toàn bộ dữ liệu cũ** mỗi lần chạy. Đổi thành `'append'` nếu muốn cộng dồn.

### 8.3 Restore từ Dump

```bash
# Restore database từ file Dump20260528.sql
mysql -u root -p music_db < Dump20260528.sql
```

---

## 9. Mô Hình Machine Learning

### 9.1 Thuật Toán SVM

**Support Vector Machine (SVM)** tìm hyperplane tối ưu để phân chia các thể loại nhạc trong không gian 60 chiều đặc trưng. Đặc biệt hiệu quả với dữ liệu tầm trung (1000–10000 mẫu) và đặc trưng số.

### 9.2 Pipeline Huấn Luyện (trong `ml_classification.ipynb`)

```python
# 1. Load data
df = pd.read_csv('example_features_with_path.csv')  # hoặc _3_sec.csv

# 2. Tách features và labels
X = df.drop(['filename', 'genre_label', 'file_path'], axis=1)
y = df['genre_label']

# 3. Encode labels
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# 5. Chuẩn hóa
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Train SVM
from sklearn.svm import SVC
model = SVC(kernel='rbf', C=10, gamma='scale')
model.fit(X_train_scaled, y_train)

# 7. Lưu model
import joblib
joblib.dump(model, 'music_svm_model.pkl')
joblib.dump(scaler, 'music_scaler.pkl')
joblib.dump(list(le.classes_), 'music_categories.pkl')
```

### 9.3 File `.pkl`

| File | Nội dung | Dùng trong |
|------|---------|-----------|
| `music_svm_model.pkl` | Object `SVC` đã fit | `app.py` – `model.predict()` |
| `music_scaler.pkl` | Object `StandardScaler` đã fit | `app.py` – `scaler.transform()` |
| `music_categories.pkl` | `['blues', 'classical', ..., 'rock']` | `app.py` – map index → tên |

---

## 10. Giao Diện Web Gradio

### 10.1 Khởi Động

```bash
python app.py
# → http://127.0.0.1:7860
```

### 10.2 Luồng Sử Dụng

```
1. Upload file nhạc (WAV, MP3, FLAC, ...)
          ↓
2. Gradio lưu file vào thư mục temp → trả filepath cho app
          ↓
3. app.py gọi predict_genre_of_file(filepath)
          ↓
4. Trích xuất 60 đặc trưng (mất 3–8 giây)
          ↓
5. Chuẩn hóa → SVM predict → map category
          ↓
6. Hiển thị: "🎵 Dự đoán thể loại: JAZZ"
```

### 10.3 Tùy Chỉnh

**Đổi theme giao diện:**
```python
# Các theme có sẵn trong Gradio
gr.Blocks(theme=gr.themes.Soft())    # Hiện tại
gr.Blocks(theme=gr.themes.Default()) # Mặc định
gr.Blocks(theme=gr.themes.Monochrome()) # Đen trắng
gr.Blocks(theme=gr.themes.Glass())   # Trong suốt
```

**Cho phép share link công khai:**
```python
demo.launch(share=True)
# Sẽ in ra: Running on public URL: https://xxxx.gradio.live
```

---

## 11. Xử Lý Lỗi Thường Gặp

### Lỗi 1: Không load được model

```
LỖI KHÔNG NẠP ĐƯỢC AI: [Errno 2] No such file or directory: 'music_svm_model.pkl'
```

**Nguyên nhân:** Chưa chạy `ml_classification.ipynb`  
**Giải pháp:** Chạy toàn bộ notebook để tạo file `.pkl`

---

### Lỗi 2: MySQL connection failed

```
❌ Lỗi MySQL: (OperationalError) Can't connect to MySQL server on '127.0.0.1'
```

**Nguyên nhân:** MySQL chưa khởi động hoặc sai thông tin đăng nhập  
**Giải pháp:** Kiểm tra MySQL service, hoặc bỏ qua (feature extraction vẫn lưu CSV thành công)

---

### Lỗi 3: Không tìm thấy dataset

```
❌ Không tìm thấy dataset!
```

**Nguyên nhân:** Chưa đặt dataset vào thư mục `genres_original/`  
**Giải pháp:** Tải GTZAN dataset và giải nén đúng cấu trúc thư mục

---

### Lỗi 4: Lỗi âm thanh khi predict

```
Lỗi trích xuất đặc trưng âm thanh: Audio is too short
```

**Nguyên nhân:** File nhạc ngắn hơn 30 giây  
**Giải pháp:** Sử dụng file nhạc có thời lượng ≥ 30 giây

---

### Lỗi 5: Sai thứ tự cột features

```
ValueError: X has 58 features, but StandardScaler is expecting 60 features
```

**Nguyên nhân:** Model được train với tập đặc trưng khác số cột hiện tại  
**Giải pháp:** Train lại model và lưu `.pkl` mới từ đúng pipeline trích xuất

---

### Lỗi 6: Lỗi encoding trên Windows

```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Nguyên nhân:** Terminal Windows không hỗ trợ UTF-8 mặc định  
**Giải pháp:** Đã được xử lý trong code với dòng:
```python
sys.stdout.reconfigure(encoding='utf-8')
```

---

## 12. Thư Viện và Dependencies

| Thư viện | Phiên bản | Vai trò |
|---------|---------|---------|
| `numpy` | 2.4.6 | Tính mean, var, xử lý mảng |
| `pandas` | 3.0.3 | DataFrame, đọc/ghi CSV |
| `scipy` | latest | Hỗ trợ librosa, sklearn |
| `matplotlib` | 3.10.0 | Vẽ biểu đồ trong notebook |
| `seaborn` | 0.13.2 | Confusion Matrix, Heatmap |
| `scikit-learn` | 1.6.0 | SVM, StandardScaler, metrics |
| `xgboost` | 2.1.3 | Thử nghiệm XGBoost trong notebook |
| `librosa` | 0.11.0 | Phân tích âm thanh, extract features |
| `gradio` | 6.15.2 | Giao diện web |
| `joblib` | 1.5.3 | Lưu/load file .pkl |
| `jupyterlab` | 4.3.0 | Chạy file .ipynb |
| `sqlalchemy` | (auto) | Kết nối MySQL từ pandas |
| `pymysql` | (auto) | MySQL driver cho SQLAlchemy |

---

## Ghi Chú Bảo Mật

> ⚠️ **Quan trọng cho môi trường Production:**
> 
> File `feature_extraction.py` hiện đang hard-code thông tin đăng nhập MySQL:
> ```python
> username = "root"
> password = quote_plus("22092005@Dung")
> ```
> 
> Khuyến nghị chuyển sang dùng biến môi trường:
> ```python
> import os
> username = os.environ.get("DB_USER", "root")
> password = quote_plus(os.environ.get("DB_PASS", ""))
> ```

---

[Design_Architecture.md](https://github.com/user-attachments/files/28431912/Design_Architecture.md)
# 🎨 Design & Architecture Document
# Hệ Thống AI Phân Biệt Thể Loại Nhạc – LapTrinhAmThanh

> **Phiên bản:** 1.0  
> **Ngày cập nhật:** 29/05/2026  
> **Trạng thái:** Released

---

## 1. Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────────────────────┐
│                     HỆ THỐNG LAPTRINHÂMTHANH                        │
│                                                                     │
│  ┌─────────────────────┐      ┌──────────────────────────────────┐  │
│  │   PIPELINE OFFLINE  │      │       PIPELINE ONLINE (app.py)   │  │
│  │  (Huấn luyện mô hình│      │       (Dự đoán thời gian thực)  │  │
│  └─────────────────────┘      └──────────────────────────────────┘  │
│           │                                    │                    │
│           ▼                                    ▼                    │
│  ┌─────────────────┐                ┌─────────────────────┐        │
│  │ genres_original │                │   Gradio Web UI     │        │
│  │  (1000 .wav)    │                │   localhost:7860    │        │
│  └────────┬────────┘                └──────────┬──────────┘        │
│           │                                    │                    │
│           ▼                                    ▼                    │
│  ┌─────────────────┐                ┌─────────────────────┐        │
│  │feature_extraction│               │  predict_genre_of_  │        │
│  │      .py        │                │     file()          │        │
│  │extract_features_│                │  (60 features)      │        │
│  │  3sec.py        │                └──────────┬──────────┘        │
│  └────────┬────────┘                           │                    │
│           │                                    │                    │
│           ▼                                    ▼                    │
│  ┌────────────────────┐            ┌─────────────────────┐        │
│  │  example_features  │            │   music_scaler.pkl  │        │
│  │     _with_path.csv │            │   music_svm_model   │        │
│  │  example_features  │            │       .pkl          │        │
│  │   _3_sec.csv       │            │  music_categories   │        │
│  └────────┬───────────┘            │       .pkl          │        │
│           │                        └──────────┬──────────┘        │
│           ▼                                    │                    │
│  ┌─────────────────────┐                       │                    │
│  │ ml_classification   │                       │                    │
│  │     .ipynb          │──────────────────────►│                    │
│  │  (Train SVM Model)  │    xuất .pkl files    │                    │
│  └─────────────────────┘                       │                    │
│           │                                    ▼                    │
│           ▼                        ┌─────────────────────┐        │
│  ┌─────────────────────┐           │  🎵 Kết quả dự đoán │        │
│  │  MySQL: music_db    │           │  "BLUES / JAZZ / ..." │       │
│  │  songs_features     │           └─────────────────────┘        │
│  └─────────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Thiết Kế Cơ Sở Dữ Liệu

### 2.1 Database: `music_db`

**Kết nối:**
```
Host    : 127.0.0.1
Port    : 3306
Database: music_db
User    : root
Engine  : MySQL 8.0+
```

### 2.2 Bảng `songs_features`

Bảng này được tạo tự động bởi `feature_extraction.py` thông qua `pandas.to_sql()` với `if_exists='replace'`.

| STT | Tên cột | Kiểu dữ liệu | Mô tả |
|-----|---------|-------------|-------|
| 1 | `filename` | VARCHAR(100) | Tên file gốc. VD: `blues.00000` |
| 2 | `length` | INT | Số lượng sample (≈ 661.794 với 30s@22050Hz) |
| 3 | `chroma_stft_mean` | FLOAT | Mean của Chroma STFT |
| 4 | `chroma_stft_var` | FLOAT | Variance của Chroma STFT |
| 5 | `rms_mean` | FLOAT | Mean của RMS Energy |
| 6 | `rms_var` | FLOAT | Variance của RMS Energy |
| 7 | `spectral_centroid_mean` | FLOAT | Mean của Spectral Centroid |
| 8 | `spectral_centroid_var` | FLOAT | Variance của Spectral Centroid |
| 9 | `spectral_bandwidth_mean` | FLOAT | Mean của Spectral Bandwidth |
| 10 | `spectral_bandwidth_var` | FLOAT | Variance của Spectral Bandwidth |
| 11 | `rolloff_mean` | FLOAT | Mean của Spectral Rolloff |
| 12 | `rolloff_var` | FLOAT | Variance của Spectral Rolloff |
| 13 | `zero_crossing_rate_mean` | FLOAT | Mean của Zero Crossing Rate |
| 14 | `zero_crossing_rate_var` | FLOAT | Variance của Zero Crossing Rate |
| 15 | `harmony_mean` | FLOAT | Mean của Harmonic component |
| 16 | `harmony_var` | FLOAT | Variance của Harmonic component |
| 17 | `perceptr_mean` | FLOAT | Mean của Percussive component |
| 18 | `perceptr_var` | FLOAT | Variance của Percussive component |
| 19 | `tempo` | FLOAT | Tempo ước tính (BPM) |
| 20–59 | `mfcc1_mean` → `mfcc20_var` | FLOAT | 20 MFCC × (mean + var) = 40 cột |
| 60 | `chroma_cqt_mean` | FLOAT | Mean của Chroma CQT |
| 61 | `chroma_cqt_var` | FLOAT | Variance của Chroma CQT |
| 62 | `genre_label` | VARCHAR(20) | Nhãn thể loại: `blues`, `rock`,... |
| 63 | `file_path` | VARCHAR(200) | Đường dẫn tương đối. VD: `genres_original/blues/blues.00000.wav` |

**Tổng: 63 cột** (60 features + filename + genre_label + file_path)

### 2.3 ERD (Entity Relationship)

```
┌──────────────────────────────────────────────────┐
│                  songs_features                  │
├──────────────────────────────────────────────────┤
│ PK  filename            VARCHAR(100)             │
│     length              INT                      │
│     chroma_stft_mean    FLOAT                    │
│     chroma_stft_var     FLOAT                    │
│     rms_mean            FLOAT                    │
│     rms_var             FLOAT                    │
│     spectral_centroid_mean  FLOAT                │
│     spectral_centroid_var   FLOAT                │
│     spectral_bandwidth_mean FLOAT                │
│     spectral_bandwidth_var  FLOAT                │
│     rolloff_mean        FLOAT                    │
│     rolloff_var         FLOAT                    │
│     zero_crossing_rate_mean FLOAT                │
│     zero_crossing_rate_var  FLOAT                │
│     harmony_mean        FLOAT                    │
│     harmony_var         FLOAT                    │
│     perceptr_mean       FLOAT                    │
│     perceptr_var        FLOAT                    │
│     tempo               FLOAT                    │
│     mfcc1_mean ... mfcc20_var  FLOAT (40 cols)   │
│     chroma_cqt_mean     FLOAT                    │
│     chroma_cqt_var      FLOAT                    │
│     genre_label         VARCHAR(20)              │
│     file_path           VARCHAR(200)             │
└──────────────────────────────────────────────────┘
```

> **Lưu ý:** Bảng không có khóa ngoại vì là bảng phẳng (flat table) dùng cho ML training. Không có quan hệ với bảng khác.

---

## 3. Thiết Kế Module

### 3.1 `feature_extraction.py`

```
feature_extraction.py
│
├── get_all_musical_features(audio_path, song_name, start, chroma_method_list)
│   ├── INPUT : đường dẫn file .wav, tên bài, offset, list method chroma
│   ├── PROCESS: load audio → extract 60 features → build dict → DataFrame
│   └── OUTPUT: pd.DataFrame 1 hàng × 60 cột, index = song_name
│
├── extract_single_song(wav_path)
│   ├── INPUT : đường dẫn file .wav
│   ├── PROCESS: gọi get_all_musical_features() → bắt exception
│   └── OUTPUT: DataFrame hoặc None nếu lỗi
│
└── __main__
    ├── Duyệt genres_original/ → gom danh sách .wav
    ├── Pool(processes=16).map(extract_single_song, wav_list)
    ├── Gộp DataFrame, gán genre_label, file_path
    ├── Lưu CSV: example_features_with_path.csv
    └── Lưu MySQL: songs_features (if_exists='replace')
```

### 3.2 `extract_features_3sec.py`

```
extract_features_3sec.py
│
├── get_single_3s_feature(audio_path, base_song_name, segment_idx)
│   ├── INPUT : đường dẫn, tên gốc, index đoạn (0-9)
│   ├── PROCESS: load 3s tại offset=idx*3 → extract → force length=66149
│   └── OUTPUT: DataFrame 1 hàng với index "{name}.{idx}"
│
├── extract_single_song_to_10_segments(wav_path)
│   ├── INPUT : đường dẫn file .wav
│   ├── PROCESS: vòng for 0→9, gọi get_single_3s_feature, concat
│   └── OUTPUT: DataFrame 10 hàng × 60 cột
│
└── __main__
    ├── Gom toàn bộ .wav từ genres_original/
    ├── Pool(processes=cpu_count()).map(extract_single_song_to_10_segments)
    ├── Gộp → ~10.000 hàng
    ├── Gán genre_label từ prefix filename
    └── Lưu: example_features_3_sec.csv
```

### 3.3 `app.py`

```
app.py
│
├── [Khởi động] Load 3 file .pkl
│   ├── music_scaler.pkl     → StandardScaler đã fit
│   ├── music_svm_model.pkl  → SVM model đã train
│   └── music_categories.pkl → list ['blues', 'classical', ..., 'rock']
│
├── predict_genre_of_file(song_path, model, scaler, categories)
│   ├── INPUT : đường dẫn file nhạc tạm thời từ Gradio
│   ├── PROCESS:
│   │   ├── librosa.load(duration=30.0)
│   │   ├── Extract 60 features (giống feature_extraction.py)
│   │   ├── pd.DataFrame → reindex theo scaler.feature_names_in_
│   │   ├── scaler.transform()
│   │   └── model.predict()[0] → map categories
│   └── OUTPUT: string tên thể loại viết hoa (VD: "BLUES")
│
├── gradio_predict(audio_file)
│   ├── INPUT : filepath từ Gradio component
│   ├── PROCESS: validate → gọi predict_genre_of_file → format output
│   └── OUTPUT: "🎵 Dự đoán thể loại: BLUES" hoặc thông báo lỗi
│
└── Gradio Blocks UI
    ├── Theme: gr.themes.Soft()
    ├── Title: "AI Phân Biệt Thể Loại Nhạc"
    ├── Layout: gr.Row() → 2 Column
    │   ├── Left:  gr.Audio(type="filepath") + Button
    │   └── Right: gr.Textbox (output)
    └── demo.launch(share=False)
```

---

## 4. Thiết Kế Giao Diện (UI Design)

### 4.1 Wireframe Giao Diện Web

```
┌─────────────────────────────────────────────────────────┐
│           🎵 HỆ THỐNG AI PHÂN BIỆT THỂ LOẠI NHẠC        │
│   (ỨNG DỤNG ĐỘC LẬP)                                   │
│                                                         │
│   Ứng dụng sử dụng SVM + Librosa để phân tích           │
│   dải tần số, nhịp điệu và MFCC để nhận diện...        │
├─────────────────────────┬───────────────────────────────┤
│                         │                               │
│  📁 Tải file nhạc lên  │  📊 Kết quả từ AI             │
│  ┌───────────────────┐  │  ┌─────────────────────────┐  │
│  │                   │  │  │                         │  │
│  │  Kéo thả file     │  │  │  🎵 Dự đoán thể loại:  │  │
│  │  nhạc vào đây     │  │  │       BLUES             │  │
│  │  hoặc click chọn  │  │  │                         │  │
│  │                   │  │  └─────────────────────────┘  │
│  └───────────────────┘  │                               │
│                         │                               │
│  [ 🔮 Bắt đầu phân     │                               │
│    tích & Dự đoán ]    │                               │
│                         │                               │
└─────────────────────────┴───────────────────────────────┘
```

### 4.2 Component Map

| Component | Gradio Class | Tham số quan trọng |
|-----------|-------------|-------------------|
| Header | `gr.Markdown` | Markdown text với HTML |
| Container | `gr.Blocks(theme=gr.themes.Soft())` | Theme Soft |
| Layout | `gr.Row()` | 2 cột ngang |
| File Input | `gr.Audio` | `type="filepath"`, label |
| Predict Button | `gr.Button` | `variant="primary"` |
| Output | `gr.Textbox` | `text_align="center"` |

### 4.3 Trạng Thái UI

| Trạng thái | Output Hiển Thị |
|-----------|----------------|
| Chưa upload file | `"Vui lòng kéo thả hoặc chọn một file nhạc trước khi bấm dự đoán!"` |
| Đang xử lý | Loading spinner (Gradio tự động) |
| Thành công | `"🎵 Dự đoán thể loại: {GENRE}"` |
| Lỗi xử lý | `"Lỗi trích xuất đặc trưng âm thanh: {error_message}"` |

---

## 5. Thiết Kế Đặc Trưng Âm Thanh (Feature Engineering Design)

### 5.1 Bảng Đặc Trưng

| Nhóm | Đặc trưng | Số cột | Ý nghĩa âm nhạc |
|------|-----------|--------|----------------|
| **Temporal** | `length` | 1 | Độ dài file (samples) |
| **Rhythm** | `tempo` | 1 | Nhịp điệu (BPM) – phân biệt nhạc nhanh/chậm |
| **Harmonic** | `chroma_stft_mean/var` | 2 | Phân bố năng lượng theo 12 nốt nhạc (C,D,E,...) |
| **Harmonic** | `chroma_cqt_mean/var` | 2 | Chroma theo CQT – chính xác hơn với nhạc cụ thực |
| **Energy** | `rms_mean/var` | 2 | Biên độ âm thanh tổng thể |
| **Spectral** | `spectral_centroid_mean/var` | 2 | "Độ sáng" của âm thanh – treble vs bass |
| **Spectral** | `spectral_bandwidth_mean/var` | 2 | Độ rộng dải tần – nhạc phức tạp vs đơn giản |
| **Spectral** | `rolloff_mean/var` | 2 | Điểm 85% năng lượng phổ |
| **Percussive** | `zero_crossing_rate_mean/var` | 2 | Tỷ lệ noise – nhạc rock/metal vs classical |
| **Separation** | `harmony_mean/var` | 2 | Thành phần giai điệu thuần |
| **Separation** | `perceptr_mean/var` | 2 | Thành phần nhịp trống/bass |
| **Timbre** | `mfcc1_mean` → `mfcc20_var` | 40 | Màu sắc âm sắc – quan trọng nhất trong phân loại |
| **Tổng** | | **60** | |

### 5.2 Pipeline Chuẩn Hóa

```
Raw Features (60 cols)
        │
        ▼
StandardScaler.fit_transform()  ← fit trên training data
        │                          saved vào music_scaler.pkl
        ▼
Normalized Features (mean=0, std=1)
        │
        ▼
SVM.fit()  ← train
        │     saved vào music_svm_model.pkl
        ▼
Predict time:
        │
Raw Features → reindex → StandardScaler.transform() → SVM.predict()
```

---

## 6. Cấu Trúc File Dự Án

```
LapTrinhAmThanh/
│
├── genres_original/          # Dataset train (GTZAN)
│   ├── blues/                # 100 file blues.00000.wav → blues.00099.wav
│   ├── classical/
│   ├── country/
│   ├── disco/
│   ├── hiphop/
│   ├── jazz/
│   ├── metal/
│   ├── pop/
│   ├── reggae/
│   └── rock/
│
├── music_test/               # Dataset test độc lập
│   ├── blues/
│   ├── classical/
│   ├── disco/
│   ├── hiphop/
│   ├── jazz/
│   ├── metal/
│   ├── pop/
│   ├── reggae/
│   └── rock/
│
├── feature_extraction.py     # Script trích xuất 60 features từ file 30s
├── extract_features_3sec.py  # Script trích xuất 60 features từ đoạn 3s
├── ml_classification.ipynb   # Notebook huấn luyện SVM, đánh giá mô hình
├── app.py                    # Web app Gradio – giao diện dự đoán
│
├── example_features.csv           # Features mẫu (format đơn giản)
├── example_features_3_sec.csv     # Features 10.000 đoạn 3s
├── example_features_with_path.csv # Features 1.000 bài 30s + file_path
│
├── music_svm_model.pkl       # Mô hình SVM đã train
├── music_scaler.pkl          # StandardScaler đã fit
├── music_categories.pkl      # List thể loại: ['blues', ..., 'rock']
│
├── Bao_cao_Testcase_Phan_Cap.csv  # Báo cáo test case phân cấp
├── Dump20260528.sql               # MySQL dump của music_db
├── requirements.txt               # Danh sách thư viện Python
└── .venv/                         # Virtual environment Python
```

---

## 7. Sơ Đồ Luồng Dữ Liệu (Data Flow)

```
[File .wav]
    │
    │  librosa.load(duration=30.0 hoặc 3.0)
    ▼
[Audio Signal: y, sr]
    │
    ├──► beat_track()        → tempo
    ├──► chroma_stft()       → chroma_stft [12 × T]
    ├──► rms()               → rmse [1 × T]
    ├──► spectral_centroid() → spec_cent [1 × T]
    ├──► spectral_bandwidth()→ spec_bw [1 × T]
    ├──► spectral_rolloff()  → rolloff [1 × T]
    ├──► zero_crossing_rate()→ zcr [1 × T]
    ├──► mfcc(n_mfcc=20)     → mfcc [20 × T]
    ├──► harmonic()          → harmony [N]
    ├──► percussive()        → percussive [N]
    └──► chroma_cqt()        → chroma_cqt [12 × T]
             │
             │  np.mean() + np.var() cho từng feature
             ▼
    [Feature Vector: 60 giá trị số]
             │
             │  pd.DataFrame → StandardScaler.transform()
             ▼
    [Normalized Vector: 60 giá trị chuẩn hóa]
             │
             │  SVM.predict()
             ▼
    [Predicted Class Index: 0-9]
             │
             │  categories_list[index].upper()
             ▼
    ["BLUES" / "CLASSICAL" / ... / "ROCK"]
```

---

[requirements.txt](https://github.com/user-attachments/files/28431913/requirements.txt)
# --- XỬ LÝ SỐ HỌC & DỮ LIỆU ---
numpy==2.2.6          # Xử lý mảng số học đa chiều; nền tảng cho librosa và scikit-learn
pandas==2.2.3         # Đọc/ghi file CSV, tạo DataFrame chứa đặc trưng âm thanh đã trích xuất
scipy==1.15.3         # Hỗ trợ tính toán tín hiệu số nâng cao; được librosa dùng nội bộ
 
# --- TRỰC QUAN HÓA ---
matplotlib==3.10.0    # Vẽ biểu đồ cơ bản (đường, cột) khi phân tích và kiểm tra dữ liệu
seaborn==0.13.2       # Vẽ Confusion Matrix (Heatmap) để đánh giá hiệu suất mô hình SVM
 
# --- MACHINE LEARNING ---
scikit-learn==1.6.1   # Huấn luyện mô hình SVM, chuẩn hóa dữ liệu (StandardScaler), chia train/test
xgboost==2.1.3        # Thuật toán Gradient Boosting; dùng thử nghiệm so sánh với SVM trong notebook
joblib==1.4.2         # Lưu (dump) và tải (load) các file .pkl: model, scaler, danh sách nhãn
 
# --- XỬ LÝ ÂM THANH ---
librosa==0.11.0       # Trích xuất toàn bộ đặc trưng âm thanh: MFCC, Chroma, ZCR, Tempo, RMS...
 
# --- GIAO DIỆN WEB ---
gradio==5.31.0        # Xây dựng giao diện web app (app.py) để người dùng upload nhạc và nhận kết quả
 
# --- MÔI TRƯỜNG PHÁT TRIỂN ---
jupyterlab==4.4.3     # Môi trường chạy file ml_classification.ipynb để huấn luyện và đánh giá mô hình
 
# --- KẾT NỐI CƠ SỞ DỮ LIỆU (dùng trong feature_extraction.py) ---
sqlalchemy==2.0.41    # ORM/engine kết nối Python với MySQL; dùng để ghi DataFrame vào database
pymysql==1.1.1        # Driver MySQL thuần Python; sqlalchemy cần cài thêm gói này để kết nối
