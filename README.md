# BÁO CÁO BÀI TẬP LỚN
**Học viện Công nghệ Bưu Chính Viễn Thông**

**Môn học:** Lập Trình Âm Thanh 

**Nhóm:** 6 

**Giảng viên hướng dẫn:** GV. Phạm Văn Sự

---

## Mục lục
 
- [Lời cảm ơn](#lời-cảm-ơn)
- [Phần 1: Thông Tin Thành Viên Nhóm](#phần-1-thông-tin-thành-viên-nhóm)
- [Phần 2: Thông Tin Chi Tiết Các Project](#phần-2-thông-tin-chi-tiết-các-project)
  - [Phần 2.1 — Project 1: AudioProcessor](#phần-21--project-1-audioprocessor--dsp-studio-v2)
    - [2.1.1. Thiết kế hệ thống](#211-thiết-kế-hệ-thống)
    - [2.1.2. Thư viện sử dụng](#212-thư-viện-sử-dụng)
    - [2.1.3. Tập dữ liệu (Dataset)](#213-tập-dữ-liệu-dataset)
    - [2.1.4. Cách tái deploy và chạy lại project](#214-cách-tái-deploy-và-chạy-lại-project)
    - [2.1.5. Kết quả đạt được](#215-kết-quả-đạt-được)
  - [Phần 2.2 — Project 2: SoundLabel — Hệ thống nhận diện thể loại nhạc](#phần-22--project-2-soundlabel--hệ-thống-nhận-diện-thể-loại-nhạc)
    - [2.2.1. Thiết kế hệ thống](#221-thiết-kế-hệ-thống)
    - [2.2.2. Thư viện sử dụng](#222-thư-viện-sử-dụng)
    - [2.2.3. Tập dữ liệu (Dataset)](#223-tập-dữ-liệu-dataset)
    - [2.2.4. Cách tái deploy và chạy lại project](#224-cách-tái-deploy-và-chạy-lại-project)
    - [2.2.5. Kết quả đạt được](#225-kết-quả-đạt-được)
- [Phần 3: Kết Luận Của Nhóm](#phần-3-kết-luận-của-nhóm)
---

## Lời cảm ơn

Chúng em xin gửi lời cảm ơn chân thành đến thầy Phạm Văn Sự, giảng viên phụ trách môn Lập trình âm thanh. Những kiến thức chuyên môn và sự hướng dẫn trực tiếp từ thầy trong suốt quá trình học tập là cơ sở quan trọng giúp chúng em hoàn thành cả hai đồ án và báo cáo này. Dù đã nỗ lực hoàn thiện, báo cáo chắc chắn không tránh khỏi những hạn chế và thiếu sót. Chúng em rất mong nhận được sự nhận xét và góp ý từ thầy để có thể cải thiện và rút kinh nghiệm cho các dự án sau.

---

## Phần 1: Thông Tin Thành Viên Nhóm

| Họ và Tên | Mã Sinh Viên |
|-----------|-------------|
| Đặng Nam Đức Bắc | B23DCPT032 |
| Mai Hoàng Minh Hải | B23DCPT108 |
| Nguyễn Đình Chiến | B23DCPT048 |
| Lê Quốc Dũng | B23DCPT076 |

---

## Phần 2: Thông Tin Chi Tiết Các Project

---

### Phần 2.1 — Project 1: AudioProcessor 

> Ứng dụng xử lý tín hiệu âm thanh viết bằng **C++17**, hỗ trợ đa định dạng (WAV/MP3/FLAC/OGG), 6 hiệu ứng DSP, giao diện đồ họa Raylib với Spectrum Analyzer real-time.

---

#### 2.1.1. Thiết kế hệ thống

##### Kiến trúc phân lớp (Layered Architecture)

Project tổ chức thành 4 tầng độc lập, mỗi tầng chỉ giao tiếp với tầng liền kề qua interface rõ ràng:

```
┌──────────────────────────────────────────────┐
│  Tầng UI — Raylib                            │
│  AudioPlayerUI.cpp  ·  FFTAnalyzer.cpp       │
├──────────────────────────────────────────────┤
│  Tầng Điều phối — Facade Pattern             │
│  AudioPlayer.cpp  (quản lý m_raw/m_processed)│
├──────────────────────────────────────────────┤
│  Tầng DSP — Chain of Responsibility          │
│  EffectChain → Volume·EQ·Compressor          │
│              → Reverb·NoiseGate·Echo         │
├──────────────────────────────────────────────┤
│  Tầng I/O — Strategy Pattern                 │
│  WavIO · Mp3IO · SndfileIO                   │
│  (đều implement IAudioIO)                    │
├──────────────────────────────────────────────┤
│  Tầng Dữ liệu Cốt lõi                       │
│  AudioSignal — PCM Float [-1.0, 1.0]         │
│  data[channel][sample]                       │
└──────────────────────────────────────────────┘
```

##### Cấu trúc thư mục

```
AudioProcessor/
├── CMakeLists.txt              ← Build system (CMake 3.16+)
├── setup_deps.bat / .sh        ← Script cài Raylib tự động
├── external/minimp3/           ← Git submodule, header-only MP3
├── libs/
│   ├── raylib/                 ← Raylib được setup_deps tải về
│   └── sndfile/                ← libsndfile bundled (Windows)
├── include/
│   ├── AudioSignal.h           ← Core data: vector<vector<float>>
│   ├── AudioPlayer.h           ← Facade: quản lý m_raw + m_processed
│   ├── io/
│   │   ├── IAudioIO.h          ← Interface: load() + save()
│   │   ├── WavIO.h             ← Tự parse RIFF header, không thư viện
│   │   ├── Mp3IO.h             ← Wrapper minimp3, chỉ load()
│   │   └── SndfileIO.h         ← FLAC, OGG, AIFF qua libsndfile
│   ├── dsp/
│   │   ├── IAudioEffect.h      ← Interface: process() + setEnabled()
│   │   ├── EffectChain.h       ← vector<unique_ptr<IAudioEffect>>
│   │   └── Effects.h           ← 6 effects cụ thể
│   └── ui/
│       ├── FFTAnalyzer.h       ← Cooley-Tukey FFT + Hann window
│       └── AudioPlayerUI.h     ← Giao diện Raylib 1280×720
├── src/                        ← File .cpp tương ứng
└── data/
    └── output_processed.wav    ← File WAV tạm sau khi áp dụng DSP
```

##### Design Patterns áp dụng

| Pattern | Vị trí trong code | Tác dụng |
|---|---|---|
| **Strategy** | `IAudioIO` ← `WavIO` / `Mp3IO` / `SndfileIO` | `AudioPlayer::createHandler()` chọn đúng handler theo đuôi file, không cần sửa logic player |
| **Chain of Responsibility** | `EffectChain::processAll()` duyệt `m_effects[]` | Thêm/xóa/tắt effect linh hoạt, không ảnh hưởng nhau |
| **Facade** | `AudioPlayer` che giấu I/O + DSP + export | UI chỉ gọi `loadFile()`, `toggleEffect()`, `exportFile()` |
| **Observer** | `AudioPlayer::toggleEffect()` → `applyChain()` → UI reload | UI phản ánh ngay khi effect thay đổi |
| **RAII** | `EffectChain` dùng `unique_ptr<IAudioEffect>` | Không có `new`/`delete` thủ công, không rò rỉ bộ nhớ |

##### Luồng xử lý DSP (Offline Processing)

Hệ thống xử lý **toàn bộ file trước khi phát** (offline), đảm bảo chất lượng âm thanh:

```
User: Load File / Click Toggle Effect
        ↓
AudioPlayer::applyChain()
  → m_processed = m_raw          (copy từ bản gốc, không bao giờ sửa m_raw)
  → EffectChain::processAll()    (duyệt effects, chỉ apply effect isEnabled=true)
  → clamp() mỗi sample về [-1.0, 1.0]
        ↓
AudioPlayer::exportFile("../data/output_processed.wav")
  → WavIO::save() ghi file WAV 16-bit
        ↓
Raylib: LoadMusicStream → PlayMusicStream
        ↓
AudioPlayerUI: vẽ Waveform + FFT Spectrum ~60 FPS
```

##### Các hiệu ứng DSP (từ Effects.cpp)

| Effect | Thuật toán thực tế trong code | Tham số |
|---|---|---|
| **VolumeEffect** | `s = clamp(s * m_mult)` | multiplier (mặc định 1.5×) |
| **EchoEffect** | Circular delay buffer: `ch[i] += original[i-D] * m_decay` + feedback pass | delay=0.25s, decay=0.6, feedback=0.3 |
| **ReverbEffect** | Schroeder: 4 Comb filters song song (29.7/37.1/41.1/43.7 ms) + 2 Allpass filters nối tiếp | roomSize=0.6, damping=0.5, wetMix=0.25 |
| **EqualizerEffect** | Biquad IIR Peak EQ, 10 dải: 31·62·125·250·500·1k·2k·4k·8k·16k Hz | gainDB mỗi band ∈ [-12, +12] |
| **CompressorEffect** | Envelope follower + Gain Reduction: `gainReductionDB = (thresh - ampDB) * (1 - 1/ratio)` | thresh=-12dB, ratio=4, attack=10ms, release=100ms |
| **NoiseGateEffect** | Zero-out khi `abs(s) < threshLin`, có hold timer | thresh=-50dB, hold=30ms |

---

#### 2.1.2. Thư viện sử dụng

| Thư viện | Phiên bản | Vai trò trong project | Bắt buộc? |
|---|---|---|---|
| **C++17** | ISO C++17 | Ngôn ngữ chính: `unique_ptr`, structured bindings, `std::vector` | Có |
| **CMake** | 3.16+ | Build system, phát hiện tự động Raylib/libsndfile/minimp3 | Có |
| **Raylib** | 5.0 | Render GUI + Audio engine (load/play/seek WAV stream) | Có |
| **minimp3** | latest | Decode MP3 — header-only, nhúng qua `external/minimp3/` | Tùy chọn |
| **libsndfile** | 1.2.x | Đọc/ghi FLAC, OGG, AIFF | Tùy chọn |

##### Raylib 5.0 *(bắt buộc)*

**Vai trò:** Cung cấp cả render đồ họa (`DrawRectangle`, `DrawText`, `DrawLineV`...) và audio engine (`LoadMusicStream`, `PlayMusicStream`, `SeekMusicStream`, `UpdateMusicStream`). Toàn bộ `AudioPlayerUI.cpp` phụ thuộc Raylib.

**Cài đặt — cách đơn giản nhất:**
```bash
# Windows
setup_deps.bat          # tự tải raylib-5.0_win64_mingw-w64.zip → libs/raylib/

# Linux/macOS
bash setup_deps.sh
```

**Cài thủ công:**
```bash
# Ubuntu 22.04+
sudo apt install libraylib-dev

# macOS
brew install raylib

# Windows (thủ công)
# 1. Tải https://github.com/raysan5/raylib/releases/tag/5.0
# 2. Giải nén raylib-5.0_win64_mingw-w64.zip
# 3. Copy include/*.h  → libs/raylib/include/
#    Copy lib/libraylib.a → libs/raylib/lib/
```

##### minimp3 *(tùy chọn — đã bundle sẵn)*

**Vai trò:** `Mp3IO::load()` dùng `mp3dec_load()` từ `minimp3_ex.h` để decode toàn bộ MP3 thành PCM float. Không hỗ trợ encode (save MP3).

**Cài đặt:** Đã có sẵn trong `external/minimp3/`.
```bash
# Nếu chưa có (clone lần đầu):
git submodule update --init --recursive
```
CMake tự phát hiện qua kiểm tra `external/minimp3/minimp3_ex.h` → bật cờ `HAS_MINIMP3`.

##### libsndfile 1.2.x *(tùy chọn)*

**Vai trò:** `SndfileIO::load()` dùng `sf_open()` + `sf_readf_float()` để đọc FLAC/OGG/AIFF. `SndfileIO::save()` hỗ trợ xuất FLAC và OGG.

**Cài đặt:**
```bash
# Ubuntu/Debian
sudo apt install libsndfile1-dev

# macOS
brew install libsndfile

# Windows (thủ công)
# 1. Tải https://github.com/libsndfile/libsndfile/releases
# 2. Giải nén, copy:
#    include/sndfile.h     → libs/sndfile/include/
#    lib/libsndfile.a      → libs/sndfile/lib/
#    bin/sndfile.dll       → cùng thư mục AudioApp.exe
```
CMake tìm `libs/sndfile/` trước, sau đó pkg-config. Nếu không thấy → chỉ hỗ trợ WAV + MP3.

---

#### 2.1.3. Tập dữ liệu (Dataset)

Project **không dùng dataset ML**. Dữ liệu đầu vào là **file âm thanh local** do người dùng cung cấp. Sau khi xử lý DSP, output tự động được ghi ra `data/output_processed.wav`.

##### Định dạng hỗ trợ

| Format | Module | Ghi chú |
|---|---|---|
| `.wav` | `WavIO` — tự parse RIFF | 16-bit, 24-bit, 32-bit float; không cần thư viện ngoài |
| `.mp3` | `Mp3IO` + minimp3 | Chỉ load, không save |
| `.flac` | `SndfileIO` + libsndfile | Load + save |
| `.ogg` | `SndfileIO` + libsndfile | Load + save |

**Yêu cầu kỹ thuật:** Sample rate 44100 Hz hoặc 48000 Hz, Mono hoặc Stereo.

##### File kiểm thử — nguồn public miễn phí bản quyền

| Nguồn | Format | Link |
|---|---|---|
| Free Music Archive | MP3, FLAC | https://freemusicarchive.org |
| ccMixter | MP3, WAV | https://ccmixter.org |
| Pixabay Music | MP3 | https://pixabay.com/music |
| Wikimedia Commons | OGG, FLAC | https://commons.wikimedia.org/wiki/Category:Audio_files |

**Lưu ý khi chọn file kiểm thử:**
- Lần đầu nên dùng **WAV 16-bit 44100 Hz Stereo** — format đơn giản nhất, dễ debug nhất
- File MP3 để kiểm tra minimp3 decode chain
- File FLAC/OGG để kiểm tra libsndfile wrapper
- Tránh file dài hơn 10 phút ở lần test đầu vì `AudioSignal` load **toàn bộ vào RAM**
- Đặt file vào thư mục `data/` hoặc chọn qua hộp thoại **OPEN FILE** trong GUI

##### File kiểm thử của nhóm: https://drive.google.com/open?id=1TqeuvVlh8GL7NVr8u5iNg-DSJXOHnnL7&usp=drive_copy
---

#### 2.1.4. Cách tái deploy và chạy lại project

##### Yêu cầu hệ thống

| Thành phần | Tối thiểu | Khuyến nghị |
|---|---|---|
| OS | Ubuntu 20.04 / macOS 12 / Windows 10 | Ubuntu 22.04 / macOS 14 / Windows 11 |
| Compiler | GCC 9+ / Clang 11+ / MSVC 2019+ | GCC 12+ |
| CMake | 3.16+ | 3.27+ |
| RAM | 512 MB | 2 GB |
| Sound card | Bất kỳ | 24-bit/48kHz |

##### Ubuntu / Debian

```bash
# Bước 1 — Cài dependencies
sudo apt update
sudo apt install -y build-essential cmake git
sudo apt install -y libsndfile1-dev libasound2-dev
sudo apt install -y libraylib-dev      # Ubuntu 22.04+
# Nếu không có libraylib-dev thì chạy:
# bash setup_deps.sh

# Bước 2 — Sau khi tải/giải nén file SNDPRGSP26B23DCPT048PRJ01.zip thì tải submodule
cd AudioProcessor
git submodule update --init --recursive   # tải minimp3

# Bước 3 — Build
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Bước 4 — Chạy
./AudioApp
# Hoặc truyền file thẳng:
./AudioApp ../data/test.wav
```

##### Windows (MinGW-w64 — khuyến nghị): Sau khi đã tải/giải nén file SNDPRGSP26B23DCPT048PRJ01.zip

```bat
REM Bước 1 — Cài Raylib tự động (bắt buộc chạy lần đầu)
setup_deps.bat

REM Bước 2 — Mở thư mục
cd AudioProcessor

REM Bước 3 — Build
mkdir build && cd build
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
mingw32-make -j4

REM Bước 4 — Chạy (hộp thoại File Dialog tự mở)
.\AudioApp.exe
```

##### macOS (Homebrew): Sau Tải/giải nén file SNDPRGSP26B23DCPT048PRJ01.zip

```bash
brew install cmake libsndfile raylib

cd AudioProcessor
git submodule update --init --recursive

mkdir build && cd build
cmake ..
make -j4

./AudioApp
```



> **Lưu ý Windows:** `main.cpp` dùng `#define Rectangle WinRectangle` để tránh xung đột giữa `windows.h` và Raylib. `comdlg32` được link trong CMakeLists để dùng `GetOpenFileNameA` (hộp thoại chọn file).

##### Windows (MSVC + vcpkg)

```powershell
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg && bootstrap-vcpkg.bat
vcpkg install libsndfile raylib

cd AudioProcessor
mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=<vcpkg>/scripts/buildsystems/vcpkg.cmake
cmake --build . --config Release
.\Release\AudioApp.exe
```

##### Điều khiển giao diện

| Thao tác | Phím / Hành động |
|---|---|
| Mở file mới | Nút **OPEN FILE** (góc trên phải) — mở hộp thoại hệ điều hành |
| Play / Pause | `SPACE` |
| Tua ±5 giây | `LEFT` / `RIGHT` |
| Tăng / giảm âm lượng | `UP` / `DOWN` hoặc kéo thanh VOL |
| Bật/tắt effect DSP | Click vào tên effect trong panel bên phải |
| Thoát | `ESC` |

---

#### 2.1.5. Kết quả đạt được

##### Bảng kiểm tra mục tiêu

| Mục tiêu | File thực hiện | Kết quả |
|---|---|---|
| Đọc WAV 16/24/32-bit không dùng thư viện ngoài | `WavIO.cpp` — tự parse RIFF header | Hỗ trợ đủ 3 bit depth |
| Decode MP3 | `Mp3IO.cpp` + `minimp3_ex.h` | Vòng lặp `mp3dec_load()` hoàn chỉnh |
| Đọc/ghi FLAC và OGG | `SndfileIO.cpp` — `sf_readf_float()` / `sf_writef_float()` | Load + Save |
| Chuẩn hóa mọi format về `AudioSignal` duy nhất | `AudioSignal.h` — `data[ch][sample]` float [-1,1] | Hoàn thành |
| Thay thế format tại runtime không sửa player | `IAudioIO` interface + `AudioPlayer::createHandler()` | Hoàn thành |
| DSP pipeline 6 effects bật/tắt độc lập | `EffectChain` + `Effects.cpp` | Toggle real-time |
| FFT Spectrum Analyzer real-time | `FFTAnalyzer.cpp` — Cooley-Tukey radix-2 + Hann window | FFT size 2048, ~60 FPS |
| Giao diện đồ họa đầy đủ | `AudioPlayerUI.cpp` — Raylib 1280×720, resizable | Waveform L/R + Spectrum + Controls |
| Export file đã xử lý | `WavIO::save()` → `data/output_processed.wav` | WAV 16-bit |
| Build đa nền tảng | `CMakeLists.txt` — tự phát hiện thư viện | Linux / macOS / Windows |

##### Điểm mạnh

- **Phụ thuộc một chiều:** `WavIO.h` không bao giờ include `AudioPlayerUI.h`. Sửa một module chỉ ảnh hưởng các module phía trên trong chuỗi phụ thuộc.
- **Dễ mở rộng:** Thêm format mới (`.aac`) chỉ cần tạo class implement `IAudioIO` — không sửa `AudioPlayer.h`. Thêm effect mới tương tự với `IAudioEffect`.
- **Không rò rỉ bộ nhớ:** `EffectChain` dùng `vector<unique_ptr<IAudioEffect>>` — destructor tự gọi, không có `new`/`delete` thủ công.

##### Hạn chế đã biết

| Hạn chế | Mô tả | Hướng xử lý |
|---|---|---|
| Load toàn bộ file vào RAM | File >60 phút (~600 MB RAM) sẽ gây vấn đề | Thêm streaming buffer `readChunk(N)` |
| Mp3IO không hỗ trợ save() | MP3 encoding cần license; export chỉ ra WAV/FLAC/OGG | Tích hợp LAME encoder |
| Echo/Reverb chưa reset() khi seek | Circular buffer còn samples cũ sau khi tua | Thêm `reset()` vào `IAudioEffect` |

---

### Phần 2.2 — Project 2: SoundLabel — Hệ thống nhận diện thể loại nhạc

> Hệ thống phân loại thể loại nhạc tự động sử dụng Machine Learning (SVM), trích xuất 60 đặc trưng âm thanh từ librosa, giao diện web Gradio, triển khai trên dataset chuẩn GTZAN.

---

#### 2.2.1. Thiết kế hệ thống

Hệ thống **SoundLabel** được thiết kế theo kiến trúc **hai pipeline tách biệt**:

##### Pipeline Offline (Huấn luyện — chạy một lần)

```
genres_original/ (1000 file .wav GTZAN)
        │
        ├─► feature_extraction.py      → example_features_with_path.csv + MySQL (songs_features)
        ├─► extract_features_3sec.py   → example_features_3_sec.csv (~10.000 hàng)
        │
        └─► ml_classification.ipynb
                │
                ├── Load dữ liệu từ MySQL (songs_features) hoặc CSV
                ├── Train/Test split: 70% train / 30% test, StratifiedKFold 3 folds
                ├── GridSearchCV tối ưu siêu tham số cho 3 mô hình:
                │       ├── SVM  (SVC, kernel=RBF)         → clf1
                │       ├── Random Forest (RF)             → clf2
                │       └── XGBoost (XGB)                  → clf3
                ├── So sánh Accuracy + F1-score + Confusion Matrix
                └── Chọn SVM (clf1) – kết quả tốt nhất → lưu 3 file .pkl
                        ├── music_svm_model.pkl
                        ├── music_scaler.pkl
                        └── music_categories.pkl
```

##### Pipeline Online (Dự đoán — giao diện người dùng)

```
User upload file nhạc (.wav / .mp3)
        │
        ▼
app.py  ─ load 3 file .pkl khi khởi động (fail-fast: thoát ngay nếu thiếu)
        │
        ├─ librosa.load(duration=30.0)    → waveform y, sample rate sr
        ├─ Trích xuất 60 đặc trưng âm thanh (11 nhóm feature)
        ├─ pd.DataFrame → reindex theo scaler.feature_names_in_
        ├─ StandardScaler.transform()
        └─ SVM.predict() → categories_list[code].upper()
                        → "🎵 Dự đoán thể loại: BLUES"
```

##### Các Module Chính

| File | Vai trò |
|------|---------|
| `feature_extraction.py` | Trích xuất 60 features từ 1000 bài 30s, lưu CSV + MySQL, multiprocessing tối đa 16 core |
| `extract_features_3sec.py` | Băm mỗi bài 30s → 10 đoạn 3s, tạo dataset 10.000 mẫu để tăng cường dữ liệu |
| `ml_classification.ipynb` | Train 3 mô hình (SVM/RF/XGB) với GridSearchCV, so sánh, chọn SVM, lưu `.pkl` |
| `app.py` | Web app Gradio: load `.pkl`, trích xuất + dự đoán realtime |

##### Tổng số đặc trưng: 60 features

| Nhóm | Đặc trưng | Số cột |
|------|-----------|--------|
| Temporal | `length` | 1 |
| Rhythm | `tempo` | 1 |
| Harmonic | `chroma_stft_mean/var`, `chroma_cqt_mean/var` | 4 |
| Energy | `rms_mean/var` | 2 |
| Spectral | `spectral_centroid`, `spectral_bandwidth`, `rolloff` (mean+var mỗi loại) | 6 |
| Percussive | `zero_crossing_rate_mean/var` | 2 |
| Separation | `harmony_mean/var`, `perceptr_mean/var` | 4 |
| Timbre | `mfcc1_mean/var` → `mfcc20_mean/var` | **40** |
| **Tổng** | | **60** |

> MFCC chiếm 40/60 = **67% tổng features**, là nhóm quan trọng nhất cho phân loại âm sắc.

##### Quy trình huấn luyện 3 mô hình trong notebook(ml_classification.ipynb)

**Bước 1 – Chuẩn bị dữ liệu**
- Load từ MySQL (`songs_features`) hoặc CSV
- Tách X (60 features số, bỏ `length`) và y (`genre_label` → encode số 0–9)
- Split 70/30: `train_test_split(test_size=0.3, random_state=123)`
- Chuẩn hóa: `StandardScaler.fit_transform(X_train)` → chỉ `transform(X_test)`

**Bước 2 – GridSearchCV tối ưu siêu tham số (StratifiedKFold n=3)**

| Mô hình | Siêu tham số tìm kiếm | Ý nghĩa |
|---------|----------------------|---------|
| **SVM** (`SVC`) | `C`: [10, 100] — `gamma`: [0.1, 0.01, 0.001] | C điều chỉnh margin; gamma kiểm soát RBF kernel |
| **Random Forest** | `n_estimators`: [50, 100] — `max_depth`: [None, 6, 12] | Số cây và độ sâu cây |
| **XGBoost** | `learning_rate`: [0.01, 0.1, 0.3, 0.5] | Tốc độ học của gradient boosting |

**Bước 3 – Train mô hình tốt nhất từ GridSearch**
```python
clf1 = grid1.best_estimator_  # SVM tốt nhất
clf2 = grid2.best_estimator_  # RF tốt nhất
clf3 = grid3.best_estimator_  # XGB tốt nhất
```

**Bước 4 – Đánh giá và so sánh**
- In Accuracy, F1-score (macro) cho cả 3 mô hình
- Vẽ Confusion Matrix (heatmap seaborn) cho từng mô hình
- Vẽ Feature Importance từ XGBoost

**Bước 5 – Chọn SVM, lưu artifact**
```python
joblib.dump(clf1,              'music_svm_model.pkl')
joblib.dump(scaler,            'music_scaler.pkl')
joblib.dump(cat_y.categories,  'music_categories.pkl')
```

---

#### 2.2.2. Thư viện sử dụng

**Cài đặt bằng file requirements.txt đã có trong file SNDPRGSP26B23DCPT048PRJ02.zip:**
```bash
pip install -r requirements.txt
```

| Thư viện | Phiên bản | Vai trò cụ thể trong project |
|---------|---------|------------------------------|
| `librosa` | 0.11.0 | **Cốt lõi xử lý âm thanh** – `librosa.load()`, `beat_track()`, `chroma_stft/cqt()`, `mfcc()`, `rms()`, `spectral_centroid/bandwidth/rolloff()`, `zero_crossing_rate()`, `harmonic/percussive()` |
| `scikit-learn` | 1.6.0 | `SVC` (train SVM), `RandomForestClassifier`, `StandardScaler`, `GridSearchCV`, `StratifiedKFold`, `train_test_split`, `accuracy_score`, `f1_score`, `confusion_matrix`, `classification_report` |
| `xgboost` | 2.1.3 | `XGBClassifier` – train mô hình gradient boosting, `plot_importance()` – vẽ feature importance |
| `numpy` | 2.4.6 | `np.mean()` và `np.var()` nén ma trận feature time-series xuống scalar, xử lý mảng số |
| `pandas` | 3.0.3 | Tạo/thao tác DataFrame features, `read_csv/to_csv`, `read_sql/to_sql`, `reindex()` đảm bảo thứ tự cột |
| `gradio` | 6.15.2 | Xây dựng giao diện web: `gr.Blocks`, `gr.Audio(type="filepath")`, `gr.Button`, `gr.Textbox` |
| `joblib` | 1.5.3 | `joblib.dump()` lưu 3 file `.pkl`, `joblib.load()` tải lại model/scaler/categories khi chạy `app.py` |
| `jupyterlab` | 4.3.0 | Môi trường chạy `ml_classification.ipynb` – huấn luyện, đánh giá, visualize |
| `sqlalchemy` + `pymysql` | latest | `create_engine()` + `pandas.to_sql/read_sql` – kết nối Python ↔ MySQL |
| `seaborn` | 0.13.2 | `sns.heatmap(confusion_matrix(...))` – vẽ Confusion Matrix cho cả 3 mô hình |
| `matplotlib` | 3.10.0 | Vẽ biểu đồ, subplot, figure sizing trong notebook |
| `scipy` | latest | Hỗ trợ tính toán nền cho librosa và scikit-learn |

---

#### 2.2.3. Tập dữ liệu (Dataset)

##### Dataset Huấn Luyện: GTZAN Music Genre Dataset

| Thuộc tính | Chi tiết |
|-----------|---------|
| **Nguồn gốc** | George Tzanetakis & Perry Cook (2002) – chuẩn benchmark phổ biến nhất trong Music Information Retrieval (MIR) |
| **Public/Private** | **Public**  |
| **Link download** | https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification |
| **Cấu trúc** | 1.000 file `.wav`, mỗi file 30 giây, mono, 22.050 Hz, 16-bit |
| **Phân bố** | 10 thể loại × 100 bài: Blues, Classical, Country, Disco, HipHop, Jazz, Metal, Pop, Reggae, Rock |
| **Dung lượng** | ~1.2 GB sau giải nén |

**Cách đặt vào project (bắt buộc đúng cấu trúc):**
```
SoundLabel/
└── genres_original/
    ├── blues/        → blues.00000.wav ... blues.00099.wav
    ├── classical/    → classical.00000.wav ... classical.00099.wav
    ├── country/
    ├── disco/
    ├── hiphop/
    ├── jazz/
    ├── metal/
    ├── pop/
    ├── reggae/
    └── rock/         → rock.00000.wav ... rock.00099.wav
```

**Lưu ý khi lấy dataset:**
- File nhạc phải có thời lượng **≥ 30 giây** (code đọc cố định 30s đầu với `duration=30.0`)
- Tên file phải đúng format: `{genre}.{số 5 chữ số}.wav` (ví dụ: `blues.00000.wav`)
- Không đổi tên thư mục — code dùng tên thư mục để gán `genre_label`

##### Dataset Kiểm Thử: `music_test/`

| Thuộc tính | Chi tiết |
|-----------|---------|
| **Nguồn** | Tập file test riêng biệt, độc lập với GTZAN train, bao gồm file `.wav` và `.mp3` |
| **Cấu trúc** | 9 thể loại (thiếu `country`), ~3–5 file/thể loại |
| **Public/Private** | **Không public** – tập test nội bộ của nhóm |
| **Link download** | https://drive.google.com/drive/folders/1ICd57kOAHmPjnXoDiJOHptj7u_LBBgeF?usp=sharing |

**Cách đặt vào project sau khi tải xuống từ link drive và giải nén:**
```
SoundLabel/
└── genres_original/
└── music_test/
```

---

#### 2.2.4. Cách tái deploy và chạy lại project

##### Yêu cầu môi trường

| Thành phần | Tối thiểu | Khuyến nghị |
|-----------|-----------|------------|
| Python | 3.9+ | 3.11+ |
| RAM | 4 GB | 8 GB+ |
| CPU | 4 cores | 8+ cores (multiprocessing tận dụng tối đa 16 core) |
| Ổ cứng | 5 GB trống | 10 GB+ (GTZAN ~1.2 GB) |
| MySQL | 8.0+ (tùy chọn) | Chỉ cần cho `feature_extraction.py` và notebook |
| Browser | Chrome / Firefox / Edge | Cho giao diện Gradio tại `localhost:7860` |

##### Các bước chi tiết: Sau khi tải/giải nén file SNDPRGSP26B23DCPT048PRJ02.zip

**Bước 1 – Tạo môi trường và cài thư viện**
```bash
cd SoundLabel

python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```
Nếu bị mất file requirements.txt, cài đặt thủ công:
```bash
pip install numpy==2.2.6 pandas==2.2.3 scipy==1.15.3 matplotlib==3.10.0 seaborn==0.13.2 scikit-learn==1.6.1 xgboost==2.1.3 joblib==1.4.2 librosa==0.11.0 gradio==5.31.0 jupyterlab==4.4.3 sqlalchemy==2.0.41 pymysql==1.1.1
```

**Bước 2 – Chuẩn bị dataset GTZAN**
```
Tải từ Kaggle → giải nén → đặt vào genres_original/ đúng cấu trúc thư mục
Tải từ Google Drive → giải nén → đặt vào thư mục
```
Link dataset GTZAN: https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification/data?select=Data

Link drive tải music_test: https://drive.google.com/drive/folders/1ICd57kOAHmPjnXoDiJOHptj7u_LBBgeF?usp=sharing

**Bước 3 – Trích xuất đặc trưng**
```bash
# Trích xuất 60 features từ 1000 bài 30s → CSV + MySQL
python feature_extraction.py

# (Tùy chọn) Tạo dataset 10.000 đoạn 3s
python extract_features_3sec.py
```

Output mong đợi:
```
🚀 Tìm thấy 1000 bài hát.
⚡ Đang dùng 16 nhân CPU...
✅ Đã trích xuất xong!
💾 Đã lưu CSV: example_features_with_path.csv
🎉 Đã lưu dữ liệu vào MySQL!
```

**Bước 4 – Huấn luyện 3 mô hình và chọn SVM**
```bash
jupyter lab
# Mở ml_classification.ipynb → Kernel → Restart & Run All
```

Notebook sẽ:
1. Load dữ liệu từ MySQL / CSV
2. Chạy GridSearchCV cho SVM, Random Forest, XGBoost
3. In Accuracy + F1 + Confusion Matrix cho cả 3 mô hình
4. Lưu SVM (clf1) tốt nhất vào 3 file `.pkl`

Output cuối notebook:
```
💾 ĐÃ LƯU THÀNH CÔNG 3 FILE:
   'music_scaler.pkl', 'music_svm_model.pkl', 'music_categories.pkl'
```

**Bước 5 – Chạy ứng dụng web**
```bash
python app.py
# Mở trình duyệt: http://127.0.0.1:7860
```

Output khi khởi động thành công:
```
Đang nạp cấu hình AI từ file .pkl... Vui lòng đợi...
Nạp AI thành công! Hệ thống sẵn sàng hoạt động.
Running on local URL: http://127.0.0.1:7860
```

**Bước 6 (Tùy chọn) – Restore database MySQL**
```bash
mysql -u root -p music_db < Dump20260528.sql
```

> ⚡ **Shortcut:** Nếu đã có sẵn 3 file `.pkl` trong thư mục, **bỏ qua Bước 2–4**, chạy thẳng `python app.py`.

##### Sử dụng giao diện web
1. Kéo thả (hoặc click chọn) file nhạc `.wav` / `.mp3` vào ô upload
2. Nhấn **"🔮 Bắt đầu phân tích & Dự đoán"**
3. Chờ ~5–10 giây → kết quả: `🎵 Dự đoán thể loại: JAZZ`

---

#### 2.2.5. Kết quả đạt được

##### So sánh 3 mô hình (train/test split 70/30)

| Mô hình | Siêu tham số tốt nhất | Accuracy (test set) | F1-score (macro) | Được chọn? |
|---------|----------------------|--------------------|--------------------|-----------|
| **SVM** (SVC, kernel=RBF) | `C=10, gamma=0.01` | **~69%** | **~0.69** |  **Chọn** |
| Random Forest | `n_estimators=100, max_depth=None` | ~65–68% | ~0.65–0.68 | ❌ |
| XGBoost | `learning_rate=0.1` | ~65–68% | ~0.65–0.68 | ❌ |

> **Lý do chọn SVM:** Trên **data 30s** (data được dùng để deploy), SVM (clf1) cho kết quả tổng thể ổn định nhất và được lưu vào `.pkl` để triển khai trong `app.py`.

##### Phân tích lỗi (dựa trên Confusion Matrix)

Nhóm thể loại dễ nhầm lẫn nhất:
- **Blues ↔ Country**: chung nốt pentatonic và giai điệu folk
- **Classical ↔ Jazz**: cùng cấu trúc hòa âm phức tạp
- **Disco ↔ Hip-Hop**: cùng BPM nhanh, pattern nhịp tương tự
- **Rock ↔ Metal**: cùng nhạc cụ điện, ZCR cao (Rock bị nhầm Metal: 69 ca)
- **Pop ↔ Hip-Hop**: giai điệu đơn giản, beat điện tử

##### Kết quả kiểm thử thực tế trên giao diện Gradio (28 file test)

| Thể loại | Test Cases | PASS | Tỷ lệ |
|---------|-----------|------|-------|
| Classical | 5 | 5 | **100%** |
| HipHop | 2 | 2 | **100%** |
| Jazz | 4 | 3 | 75% |
| Blues | 4 | 2 | 50% |
| Disco | 4 | 2 | 50% |
| Pop | 4 | 2 | 50% |
| Rock | 3 | 1 | 33% |
| Metal | 1 | 0 | 0% |
| Reggae | 1 | 0 | 0% |
| **Tổng** | **28** | **17** | **60.7%** |

Kết quả bộ testcase mở rộng (31 file, chạy tự động qua script trong notebook): **20/31 PASS – Độ chính xác 64.52%**

##### Các tính năng đã hoàn thành

- Pipeline trích xuất 60 đặc trưng âm thanh hoàn chỉnh, có cấu trúc rõ ràng
- Multiprocessing xử lý 1.000 bài trong ~8 phút (16 core)
- Huấn luyện và so sánh 3 mô hình ML với GridSearchCV tự động tối ưu
- SVM đạt ~64–69% accuracy trên tập test
- Giao diện web Gradio trực quan, hỗ trợ `.wav` và `.mp3`
- Lưu trữ đặc trưng vào cả CSV và MySQL
- Tái sử dụng model qua `.pkl` không cần train lại mỗi lần chạy app
- Script testcase tự động sinh báo cáo CSV (`Bao_cao_Testcase_Phan_Cap.csv`)


## Phần 3: Kết Luận Của Nhóm

### Kiến thức thu được

**Từ Project 1 — AudioProcessor (C++/DSP):**

Nhóm nắm vững C++17 hiện đại: `unique_ptr` / RAII để quản lý bộ nhớ an toàn, template và interface thuần ảo để tách biệt "cần gì" (interface) khỏi "làm thế nào" (implementation), `std::vector<std::vector<float>>` để lưu trữ PCM đa kênh hiệu quả.

Về xử lý tín hiệu số (DSP), nhóm tự implement từ đầu: Biquad IIR Peak EQ, Schroeder Reverb (comb + allpass), Envelope Follower/Compressor, Cooley-Tukey FFT, Hann Windowing. Qua đó hiểu và xử lý được các vấn đề thực tế như clipping, spectral leakage, delay buffer tuần hoàn.

**Từ Project 2 — SoundLabel (Python/ML):**

Nhóm hiểu sâu về **Music Information Retrieval (MIR)**: cách biểu diễn âm thanh dưới dạng số (waveform → spectrogram → feature vector), và ý nghĩa âm nhạc thực sự của từng đặc trưng — MFCC phản ánh âm sắc, Chroma phản ánh hòa âm, ZCR đo độ "thô" của tín hiệu, Tempo là nhịp điệu BPM.

Nhóm cũng hiểu rõ tại sao phân loại nhạc khó hơn nhiều bài toán classification khác: các thể loại âm nhạc không có ranh giới cứng. Về Machine Learning, nhóm nắm vững toàn bộ quy trình từ thu thập, trích xuất đặc trưng, chuẩn hóa, GridSearchCV, đánh giá đến triển khai. Đặc biệt hiểu được tại sao không fit scaler trên test set (data leakage) và tầm quan trọng của `reindex(columns=scaler.feature_names_in_)` khi predict bài mới.

Về Machine Learning, nhóm nắm vững toàn bộ quy trình: thu thập → trích xuất đặc trưng → chuẩn hóa → GridSearchCV → đánh giá → triển khai. Đặc biệt hiểu được **tại sao không fit scaler trên test set** (data leakage) và tầm quan trọng của `reindex(columns=scaler.feature_names_in_)` khi dự đoán bài mới.

### Kỹ năng thu được

Qua hai project, nhóm rèn luyện được các kỹ năng thực tế: thiết kế phần mềm theo Layered Architecture với phụ thuộc một chiều; áp dụng các Design Pattern (Strategy, Chain of Responsibility, Facade) vào code thực tế; xử lý tín hiệu âm thanh với cả **Raylib** (C++) lẫn **Librosa** (Python); so sánh và chọn mô hình ML với **scikit-learn + XGBoost**; tối ưu hiệu suất xử lý với **multiprocessing**; triển khai ứng dụng AI thực tế với **Gradio**; build đa nền tảng với CMake; và tổ chức project có tài liệu đầy đủ.

### Hạn chế và hướng phát triển

**Project 1:** AudioProcessor còn hạn chế ở việc load toàn bộ file vào RAM (không phù hợp với file rất dài), Mp3IO chưa hỗ trợ save, và Echo/Reverb chưa reset khi seek. Kiến trúc phân lớp hiện tại đã đủ linh hoạt để mở rộng mà không cần đập bỏ nền tảng đã xây dựng.

**Project 2:** Độ chính xác ~64% còn thấp hơn kỳ vọng 80%, chủ yếu do dataset chỉ 100 bài/thể loại và sự chồng lấp đặc trưng giữa các thể loại liên quan. Hướng cải thiện: tăng dataset (500+ bài/thể loại), thử **CNN với mel-spectrogram** hoặc **Transfer Learning** từ model âm thanh pretrained, và triển khai lên cloud (Hugging Face Spaces / Docker).

---
