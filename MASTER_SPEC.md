# MASTER SPECIFICATION - DAIMINH AI VIDEO STUDIO

**Phiên bản:** 1.0  
**Ngày tạo:** 2026-10-23  
**Trạng thái:** Active Development - Giai đoạn 1

---

## I. TỔNG QUAN

### Mục tiêu chính

Xây dựng nền tảng Web sản xuất video chuyên nghiệp cho Nhà thuốc Đại Minh, cho phép:

1. Tải video thô (1-60 phút) và quản lý thư viện
2. AI tự động tạo transcript tiếng Việt (Whisper)
3. AI phân tích nội dung: phát hiện khoảng lặng, highlight, cấu trúc video
4. AI tự động dựng bản nháp (Auto Studio)
5. Nhân viên chỉnh sửa sâu trong Pro Editor (Timeline)
6. Kiểm duyệt nội dung sức khỏe trước xuất bản
7. Render MP4 1080p (tỷ lệ 9:16 và 16:9)

### Quy mô vận hành

- **Người dùng:** 3-10 nhân viên nội bộ
- **Tải trọng:** 20-50 video thô/ngày
- **Thời lượng video:** 1-60 phút
- **Đầu ra:** MP4 1080p, tỷ lệ 9:16 và 16:9
- **Nền tảng:** Trình duyệt trên máy tính
- **Lưu trữ:** Cloud riêng, S3-compatible

---

## II. MODULES CHI TIẾT

### MODULE 01 - QUẢN LÝ VIDEO

**Acceptance Criteria:**

- [x] Tải video lên (MP4, MOV, WebM)
- [x] Hỗ trợ tải lên theo phần (multipart) với resume
- [x] Kiểm tra định dạng, thời lượng, dung lượng
- [x] Tạo thumbnail và proxy video
- [x] Lưu file gốc không thay đổi
- [x] Thư viện video với tìm kiếm, lọc, phân loại
- [x] Xem danh sách dự án
- [x] Xoá dự án (soft delete)

**API Endpoints:**

```
POST   /api/videos/upload         - Tải video lên
GET    /api/videos                - Danh sách video
GET    /api/videos/{id}           - Chi tiết video
DELETE /api/videos/{id}           - Xoá video
```

**Database Entities:**

```
MediaAsset:
  - id: UUID
  - user_id: UUID
  - project_id: UUID
  - original_filename: str
  - file_size: int
  - duration: float (giây)
  - width: int
  - height: int
  - fps: float
  - codec: str
  - status: enum (uploading, ready, processing, error)
  - original_file_path: str
  - proxy_file_path: str
  - thumbnail_path: str
  - metadata: JSON
  - created_at: datetime
  - updated_at: datetime
```

---

### MODULE 02 - AI TRANSCRIPTION

**Acceptance Criteria:**

- [x] Chuyển giọng nói tiếng Việt → văn bản
- [x] Gắn timestamp cho từng câu/đoạn lời nói
- [x] Chỉnh sửa transcript thủ công
- [x] Đồng bộ transcript với video
- [x] Xuất phụ đề SRT
- [x] Lưu cache để tránh xử lý lại

**Integrations:**

- Whisper OpenAI (API)
- Fallback: Silero hoặc local Whisper model

**API Endpoints:**

```
POST   /api/transcripts/{id}/generate    - Tạo transcript từ video
GET    /api/transcripts/{id}             - Lấy transcript
PUT    /api/transcripts/{id}             - Cập nhật transcript
POST   /api/transcripts/{id}/export      - Xuất SRT
```

**Database Entities:**

```
Transcript:
  - id: UUID
  - media_asset_id: UUID
  - video_id: UUID
  - content: str (full text)
  - sentences: JSON[] (segments with timestamps)
  - language: str (vi)
  - status: enum (pending, processing, completed, error)
  - error_message: str (null)
  - created_at: datetime
  - updated_at: datetime

TranscriptSegment:
  - id: UUID
  - transcript_id: UUID
  - start_time: float (seconds)
  - end_time: float (seconds)
  - text: str
  - speaker: str (null cho dùng chung)
  - confidence: float (0-1)
```

---

### MODULE 03 - AI AUTO STUDIO

**Acceptance Criteria:**

- [x] Phân tích video thô (duration, scenes, speech)
- [x] Phát hiện khoảng lặng (silence detection)
- [x] Đề xuất cắt bỏ đoạn lặp/sai
- [x] Xác định highlight (phrases quan trọng)
- [x] Đề xuất cấu trúc video (intro, body, outro)
- [x] AI tự tạo bản nháp (timeline)
- [x] Tự thêm phụ đề
- [x] Áp dụng brand template
- [x] Cho phép mở bản nháp trong Pro Editor

**Constraints:**

- Không tự ý cắt bỏ nội dung làm thay đổi ý nghĩa
- AI chỉ đề xuất, yêu cầu nhân viên xem trước

**API Endpoints:**

```
POST   /api/auto-studio/analyze         - Phân tích video
POST   /api/auto-studio/generate        - Tạo bản nháp
GET    /api/auto-studio/{id}/preview    - Xem trước
POST   /api/auto-studio/{id}/finalize   - Chuyển sang editor
```

**Database Entities:**

```
AIAnalysisJob:
  - id: UUID
  - video_id: UUID
  - status: enum (pending, analyzing, completed, error)
  - silence_segments: JSON[]
  - highlights: JSON[]
  - suggested_structure: JSON
  - confidence_score: float

AutoStudioDraft:
  - id: UUID
  - video_id: UUID
  - timeline_data: JSON (timeline structure)
  - applied_template_id: UUID (null)
  - created_at: datetime
  - approved_by: UUID (null)
  - approved_at: datetime (null)
```

---

### MODULE 04 - AI SHORT VIDEO GENERATOR

**Acceptance Criteria:**

- [x] Phân tích video dài
- [x] Đề xuất clip 30-60s phù hợp cho TikTok/Reels
- [x] Người dùng chọn clip cần cắt
- [x] Tự động căn khung hình 9:16
- [x] Tự thêm hook, tiêu đề, phụ đề
- [x] Tạo nhiều phiên bản từ cùng nguồn
- [x] Lưu metadata để track source

**API Endpoints:**

```
POST   /api/short-video/suggest         - Đề xuất clip ngắn
POST   /api/short-video/generate        - Tạo video ngắn
GET    /api/short-video/{id}/versions   - Danh sách phiên bản
```

---

### MODULE 05 - PRO VIDEO EDITOR

**Acceptance Criteria:**

- [x] Timeline nhiều track (video, audio, text, effects)
- [x] Cắt, chia, ghép clip
- [x] Di chuyển, resize clip (thay đổi thời lượng)
- [x] Chỉnh sửa dựa trên transcript (linked editing)
- [x] Chèn văn bản (text overlay)
- [x] Chèn hình ảnh (image overlay)
- [x] Chèn logo, intro, outro
- [x] Chèn B-roll
- [x] Chỉnh sửa phụ đề
- [x] Điều chỉnh âm thanh (volume, fade)
- [x] Xem trước real-time
- [x] Undo/Redo (≥20 steps)
- [x] Autosave mỗi 30 giây
- [x] Quản lý phiên bản (versioning)

**Timeline Data Model:**

```json
{
  "id": "uuid",
  "duration": 300,
  "fps": 30,
  "width": 1920,
  "height": 1080,
  "tracks": [
    {
      "id": "track-v1",
      "type": "video",
      "clips": [
        {
          "id": "clip-1",
          "asset_id": "uuid",
          "start": 0,
          "duration": 30,
          "offset": 0,
          "effects": []
        }
      ]
    }
  ]
}
```

**API Endpoints:**

```
POST   /api/projects/{id}/timeline/save      - Lưu timeline
GET    /api/projects/{id}/timeline           - Lấy timeline
POST   /api/projects/{id}/timeline/preview   - Xem trước
POST   /api/projects/{id}/timeline/undo      - Hoàn tác
POST   /api/projects/{id}/timeline/redo      - Làm lại
```

---

### MODULE 06 - AI SUBTITLE STUDIO

**Acceptance Criteria:**

- [x] Tạo phụ đề từ transcript
- [x] Chỉnh sửa từng câu
- [x] Đồng bộ thời gian
- [x] Thay đổi font, màu, kích thước, vị trí
- [x] Làm nổi bật từ khóa
- [x] Áp dụng mẫu phụ đề
- [x] Kiểm tra safe zone (không vượt khung hình)

---

### MODULE 07 - BRAND TEMPLATE ENGINE

**Acceptance Criteria:**

- [x] Quản lý logo Nhà thuốc Đại Minh
- [x] Quản lý font và màu brand
- [x] Mẫu intro, outro
- [x] Mẫu call-to-action
- [x] Mẫu phụ đề
- [x] Mẫu video ngắn/dài
- [x] Admin có thể thay đổi bộ nhận diện

---

### MODULE 08 - AI EDITING STYLE ENGINE

**Three Editing Styles:**

1. **Chuyên gia sức khỏe** - Chuyên nghiệp, không quá hiệu ứng
2. **Video ngắn thu hút** - Nhanh, hiệu ứng, music/text overlay nhiều
3. **Giáo dục chuyên sâu** - Chi tiết, minh họa, slide text kỹ lưỡng

**Acceptance Criteria:**

- [x] AI đề xuất phong cách dựa trên nội dung + platform
- [x] Nhân viên chọn/thay đổi phong cách
- [x] Chỉnh cường độ hiệu ứng, nhịp cắt, màu sắc
- [x] Một video có thể tạo nhiều phiên bản với phong cách khác

---

### MODULE 09 - AI VISUAL & B-ROLL ENGINE

**Workflow:**

1. Phân tích transcript
2. Xác định vị trí cần minh họa
3. Tìm tài nguyên trong thư viện
4. Nếu thiếu, đề xuất tạo mới (AI image gen)
5. Nhân viên xem trước & phê duyệt
6. Chèn vào timeline

**Acceptance Criteria:**

- [x] Thư viện tài nguyên quản lý (ảnh, video B-roll)
- [x] Metadata: source, license, cost, status
- [x] AI đề xuất (bằng mô tả từ transcript)
- [x] Tạo hình minh họa AI (Stable Diffusion)
- [x] Kiểm duyệt hình y khoa

---

### MODULE 10 - AI AUDIO & VOICE ENGINE

**Acceptance Criteria:**

- [x] Khử tiếng ồn (noise reduction)
- [x] Giảm tiếng vang (reverb removal)
- [x] Làm rõ giọng nói (voice clarity)
- [x] Cân bằng âm lượng (normalization)
- [x] Nhạc nền thông minh (smart music)
- [x] Tự giảm âm lượng nhạc khi có lời nói (ducking)
- [x] Text-to-speech AI từ kịch bản duyệt
- [x] Thuyết minh AI
- [x] Lồng tiếng đa ngôn ngữ (Phase 2)
- [x] Thư viện giọng nói AI

**Constraints:**

- Chỉ cho phép mô phỏng giọng nói thực người với sự đồng ý hợp lệ

---

### MODULE 11 - KIỂM DUYỆT NỘI DUNG SỨC KHỎE

**Quy trình:**

```
Bản nháp → Chờ kiểm duyệt → Bình luận từ duyệt phẩm → Phê duyệt/Từ chối → Xuất bản
```

**Roles:**

- Admin (quản lý toàn hệ)
- Editor (tạo nội dung)
- Reviewer (kiểm duyệt chuyên môn)

**AI hỗ trợ phát hiện:**

- [x] Tuyên bố sức khỏe cần xác minh
- [x] Nội dung có nguy cơ hiểu sai
- [x] Hình ảnh y khoa chưa duyệt
- [x] Đoạn cắt làm thay đổi ngữ cảnh
- [x] Lời thuyết minh/bản dịch cần kiểm tra

**Constraints:**

- AI chỉ phát hiện, không thay thế người duyệt
- Không tự động công bố nội dung chưa duyệt

---

### MODULE 12 - RENDER & EXPORT

**Acceptance Criteria:**

- [x] Xuất MP4 1080p
- [x] Tỷ lệ 9:16 (vertical) và 16:9 (landscape)
- [x] Render bằng background workers
- [x] Theo dõi tiến trình
- [x] Hàng đợi xử lý (job queue)
- [x] Retry khi lỗi (≤3 lần)
- [x] Hủy tác vụ
- [x] Ngăn tác vụ trùng (user bấm nhiều lần)
- [x] Tải video thành phẩm
- [x] Lưu lịch sử render

---

### MODULE 13 - DASHBOARD & QUẢN TRỊ

**Dashboard Metrics:**

- Tổng video tải lên
- Video đang xử lý
- Video hoàn thành
- Video lỗi
- Video chờ duyệt
- Số lần render
- Thời gian xử lý trung bình
- Dung lượng lưu trữ
- Chi phí AI ước tính
- Chi phí render & hạ tầng

**Admin Features:**

- Quản lý tài khoản người dùng
- Quản lý vai trò & quyền
- Quản lý mẫu brand
- Thống kê hoạt động
- Cấu hình hệ thống

---

### MODULE 14 - TÍCH HỢP MỞ RỘNG

**Future Integration Points:**

- DaiMinh365 CRM
- n8n automation
- Content Management System
- Auto-posting platforms (TikTok, Facebook, YouTube)

**In Phase 1:** Thiết kế API & Webhook, không tích hợp vội.

---

## III. KIẾN TRÚC DỮ LIỆU

### Core Entities

```
User
├─ id: UUID
├─ email: str (unique)
├─ password_hash: str
├─ full_name: str
├─ avatar_url: str
├─ role: enum (admin, editor, reviewer)
└─ created_at: datetime

Project
├─ id: UUID
├─ user_id: UUID
├─ title: str
├─ description: str
├─ status: enum (draft, reviewing, approved, published, archived)
├─ media_asset_ids: UUID[]
├─ created_at: datetime
└─ updated_at: datetime

MediaAsset
├─ id: UUID
├─ project_id: UUID
├─ original_filename: str
├─ file_size: int
├─ duration: float
├─ width: int
├─ height: int
├─ status: enum (uploading, ready, processing, error)
├─ original_path: str
├─ proxy_path: str
├─ thumbnail_path: str
└─ metadata: JSON

Transcript
├─ id: UUID
├─ media_asset_id: UUID
├─ content: str
├─ segments: JSON[]
├─ language: str (vi)
└─ status: enum (pending, completed, error)

Timeline
├─ id: UUID
├─ project_id: UUID
├─ duration: float
├─ fps: int
├─ width: int
├─ height: int
├─ tracks: JSON[] (video, audio, text, effects)
├─ version: int
└─ updated_at: datetime

BrandTemplate
├─ id: UUID
├─ name: str
├─ logo_url: str
├─ fonts: JSON (primary, secondary)
├─ colors: JSON (brand colors)
├─ intro_path: str
├─ outro_path: str
└─ is_active: bool

RenderJob
├─ id: UUID
├─ project_id: UUID
├─ aspect_ratio: enum (9:16, 16:9)
├─ output_path: str
├─ status: enum (pending, processing, completed, error)
├─ progress: float (0-100)
├─ retry_count: int
├─ error_message: str
└─ created_at: datetime

ReviewRequest
├─ id: UUID
├─ project_id: UUID
├─ requested_by: UUID
├─ assigned_to: UUID
├─ status: enum (pending, approved, rejected)
├─ comments: str
└─ created_at: datetime

AuditLog
├─ id: UUID
├─ user_id: UUID
├─ action: str
├─ resource_type: str
├─ resource_id: UUID
├─ changes: JSON
└─ timestamp: datetime
```

---

## IV. API CONTRACTS (Chi tiết Giai đoạn 1)

### Authentication

```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
GET  /api/auth/me
```

### Video Management

```
POST   /api/videos/upload
GET    /api/videos
GET    /api/videos/{id}
DELETE /api/videos/{id}
```

### Project Management

```
POST   /api/projects
GET    /api/projects
GET    /api/projects/{id}
PUT    /api/projects/{id}
DELETE /api/projects/{id}
```

### Transcription

```
POST   /api/transcripts/generate
GET    /api/transcripts/{id}
PUT    /api/transcripts/{id}
```

---

## V. YÊუcầu CHẤT LƯỢNG

- ✅ TypeScript type checking
- ✅ Unit tests cho business logic
- ✅ Integration tests cho API
- ✅ E2E tests cho luồng chính
- ✅ Database migrations
- ✅ Error handling & validation
- ✅ Logging & monitoring
- ✅ Security checks

---

## VI. NGÔN NGỮ & LOCALIZATION

- ✅ 100% UI tiếng Việt
- ✅ Menu, button, dialog, message tiếng Việt
- ✅ Mã nguồn & API tiếng Anh
- ✅ Không có Lorem Ipsum hay placeholder text

---

**Tiến độ:** Cập nhật trong PROGRESS.md
**Next:** Bắt đầu Giai đoạn 1 - Nền tảng
