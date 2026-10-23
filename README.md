# DAIMINH AI VIDEO STUDIO

Hệ thống sản xuất và chỉnh sửa video bằng trí tuệ nhân tạo cho Nhà thuốc Đại Minh.

## Mô tả dự án

**DAIMINH AI VIDEO STUDIO** là một nền tảng Web hiện đại giúp đội ngũ nội bộ Nhà thuốc Đại Minh:

1. Tải và quản lý video thô (1-60 phút)
2. Tự động phân tích nội dung, tạo transcript tiếng Việt
3. AI tự động dựng video hoàn chỉnh (Auto Studio)
4. Nhân viên chỉnh sửa sâu trong Pro Editor
5. Kiểm duyệt nội dung sức khỏe trước công bố
6. Xuất video MP4 1080p (tỷ lệ 9:16 và 16:9)

Ứng dụng hỗ trợ 2 chế độ:
- **AI Auto Studio**: AI tự động dựng nháp video
- **Pro Video Editor**: Chỉnh sửa chuyên sâu trên Web

## Công nghệ

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Cache & Queue**: Redis
- **Video Processing**: FFmpeg
- **AI/ML**: Whisper (STT), OpenAI/Claude (analysis), Stable Diffusion (image gen)
- **Storage**: S3-compatible Object Storage
- **Deployment**: Docker, Docker Compose

## Cấu trúc dự án

```
daiminh-video-studio/
├── frontend/              # Next.js app
├── backend/               # FastAPI app
├── docs/                  # Tài liệu toàn hệ thống
├── docker-compose.yml     # Local development stack
├── README.md
└── PROGRESS.md
```

## Bắt đầu nhanh

### Yêu cầu
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose

### Cài đặt môi trường phát triển

```bash
# 1. Clone hoặc vào thư mục dự án
cd "D:\Nhà máy sản xuất app\Chỉnh sửa Video"

# 2. Cài đặt Frontend
cd frontend
npm install

# 3. Cài đặt Backend
cd ../backend
pip install -r requirements.txt

# 4. Khởi chạy môi trường phát triển
cd ..
docker-compose up -d

# 5. Frontend dev server
cd frontend
npm run dev

# 6. Backend dev server (trong terminal khác)
cd backend
python main.py
```

## Tài liệu

Xem các file tài liệu trong thư mục `docs/`:

- **MASTER_SPEC.md** - Yêu cầu chi tiết từng module
- **ARCHITECTURE.md** - Kiến trúc hệ thống
- **DATABASE.md** - Schema database
- **API.md** - API contracts
- **IMPLEMENTATION_PLAN.md** - Kế hoạch triển khai
- **TASKS.md** - Danh sách công việc
- **PROGRESS.md** - Tiến độ thực hiện

## Liên hệ

- Email: daiduoc8288@gmail.com
- Dự án: DaiMinh AI Video Studio v1.0
