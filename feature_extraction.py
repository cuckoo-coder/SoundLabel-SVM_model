import pandas as pd
import os
import numpy as np
import librosa
from multiprocessing import Pool, cpu_count

path = "genres_original/"

# --- ĐOẠN CODE NÀY THAY THẾ HOÀN TOÀN CHO FILE FTROSA.PY CỦA TÁC GIẢ ---
def get_all_musical_features(audio_path, song_name, start=0, chroma_method_list=['cqt']):
    # 1. Tải file âm thanh bằng librosa (mặc định lấy 30 giây đầu)
    y, sr = librosa.load(audio_path, offset=start, duration=30.0)
    
    # 2. Trích xuất các đặc trưng thời gian và thực thể phổ
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    
    # 3. Tính toán giá trị Trung bình (Mean) và Độ lệch chuẩn (Var) cho từng thông số
    features = {
        'length': len(y),
        'chroma_stft_mean': np.mean(chroma_stft), 'chroma_stft_var': np.var(chroma_stft),
        'rms_mean': np.mean(rmse), 'rms_var': np.var(rmse),
        'spectral_centroid_mean': np.mean(spec_cent), 'spectral_centroid_var': np.var(spec_cent),
        'spectral_bandwidth_mean': np.mean(spec_bw), 'spectral_bandwidth_var': np.var(spec_bw),
        'rolloff_mean': np.mean(rolloff), 'rolloff_var': np.var(rolloff),
        'zero_crossing_rate_mean': np.mean(zcr), 'zero_crossing_rate_var': np.var(zcr),
        'harmony_mean': np.mean(librosa.effects.harmonic(y)), 'harmony_var': np.var(librosa.effects.harmonic(y)),
        'perceptr_mean': np.mean(librosa.effects.percussive(y)), 'perceptr_var': np.var(librosa.effects.percussive(y)),
        'tempo': tempo[0] if isinstance(tempo, (list, np.ndarray)) else tempo
    }
    
    # Bổ sung 20 đặc trưng MFCC (Mean và Var)
    for i in range(20):
        features[f'mfcc{i+1}_mean'] = np.mean(mfcc[i])
        features[f'mfcc{i+1}_var'] = np.var(mfcc[i])
        
    # Tính toán thêm Chroma CQT nếu có yêu cầu trong list
    if 'cqt' in chroma_method_list:
        chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
        features['chroma_cqt_mean'] = np.mean(chroma_cqt)
        features['chroma_cqt_var'] = np.var(chroma_cqt)

    # Trả về dưới dạng DataFrame 1 cột, lấy tên bài hát làm tên cột
    return pd.DataFrame(features, index=[song_name])

# --- LUỒNG CHẠY ĐA NHÂN TỰ ĐỘNG ---
def extract_single_song(wav_path):
    try:
        # Lấy tên file nhạc để làm ID (Ví dụ: blues.00000)
        song_name = wav_path.split('/')[-1].split('.wav')[0]
        df_ = get_all_musical_features(wav_path, song_name, start=0, chroma_method_list=['cqt'])
        return df_
    except Exception as e:
        print(f"Lỗi khi xử lý file {wav_path}: {e}")
        return None

if __name__ == '__main__':
    # 1. Định nghĩa thủ công 10 thư mục con chuẩn của bộ dữ liệu GTZAN để tránh lỗi nhận diện
    genre_list = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

    # 2. Gom toàn bộ file nhạc .wav
    wav_list = []
    for g in genre_list:
        genre_path = os.path.join(path, g)
        # Sửa lỗi dấu gạch chéo trên Windows/Mac
        if os.path.exists(genre_path):
            for wav in os.listdir(genre_path):
                if wav.endswith('.wav'):
                    wav_list.append(os.path.join(genre_path, wav))

    total_songs = len(wav_list)
    
    if total_songs == 0:
        print("❌ Vẫn không tìm thấy file nhạc nào! Hãy kiểm tra lại tên thư mục 'genres_original'.")
    else:
        num_processors = cpu_count()
        print(f"🚀 Tìm thấy {total_songs} bài hát. Đang dùng {num_processors} nhân CPU để trích xuất...")

        # Bật chế độ chạy song song đa nhân
        with Pool(processes=num_processors) as pool:
            df_list = pool.map(extract_single_song, wav_list)

        # Lọc bỏ file lỗi và gộp dữ liệu thành bảng ngang
        df_list = [df for df in df_list if df is not None]
        print("✅ Đã trích xuất xong! Đang gộp dữ liệu...")
        
        df_features = pd.concat(df_list, axis=0)

        # Tạo nhãn thể loại nhạc từ tên hàng
        labels = []
        for i in df_features.index:
            labels.append(i.split('.')[0])
        df_features['genre_label'] = labels

        # Lưu kết quả bằng đường dẫn tuyệt đối để file Notebook tìm thấy dễ dàng
        current_dir = os.getcwd()
        output_path = os.path.join(current_dir, 'example_features.csv')
        df_features.to_csv(output_path, index_label='filename')
        print(f"🎉 Thành công mỹ mãn! File dữ liệu đã được lưu tại: {output_path}")