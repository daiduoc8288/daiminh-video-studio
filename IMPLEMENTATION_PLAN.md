# IMPLEMENTATION PLAN - DAIMINH AI VIDEO STUDIO

**Phiên bản:** 1.0  
**Ngày cập nhật:** 2026-10-23  
**Giai đoạn hiện tại:** Chuẩn bị Giai đoạn 1

---

## GIAI ĐOẠN 1 - NỀN TẢNG (Tuần 1-2)

### 1.1 Khởi tạo Dự án

**Tasks:**
- [ ] Tạo repository Git (local)
- [ ] Khởi tạo Next.js 15 project
- [ ] Khởi tạo FastAPI backend
- [ ] Tạo Docker Compose (PostgreSQL, Redis, MinIO)
- [ ] Cấu hình environment (.env.example)
- [ ] Setup CI/CD placeholder

**Deliverables:**
- Project structure hoàn chỉnh
- Docker Compose hoạt động (dev stack running)
- Frontend & Backend can start locally

**Acceptance Criteria:**
- [ ] `npm run dev` chạy được trên `localhost:3000`
- [ ] `python main.py` chạy được trên `localhost:8000`
- [ ] Database khởi động trong Docker
- [ ] Redis khởi động trong Docker
- [ ] MinIO khởi động (S3 mock)

---

### 1.2 Authentication & Authorization

**Frontend Tasks:**
- [ ] Login form (tiếng Việt)
- [ ] Logout
- [ ] Protected routes
- [ ] Store token (localStorage/cookies)
- [ ] Refresh token logic

**Backend Tasks:**
- [ ] User model (PostgreSQL)
- [ ] Password hashing (bcrypt)
- [ ] JWT token generation
- [ ] Login endpoint (`POST /api/v1/auth/login`)
- [ ] Logout endpoint
- [ ] Refresh endpoint
- [ ] Current user endpoint (`GET /api/v1/auth/me`)
- [ ] Middleware xác thực

**Database:**
- [ ] Migration: Create users table

**Tests:**
- [ ] Unit test: password hashing
- [ ] Unit test: JWT token generation
- [ ] Integration test: login flow
- [ ] Integration test: token refresh

**Acceptance Criteria:**
- [ ] User can login với email/password hợp lệ
- [ ] Invalid credentials báo lỗi (tiếng Việt)
- [ ] JWT token trả về
- [ ] Token refresh hoạt động
- [ ] Protected endpoints return 401 nếu no token
- [ ] UI login hoàn toàn tiếng Việt

---

### 1.3 Video Upload & Library

**Frontend Tasks:**
- [ ] Upload UI (drag-drop + file picker)
- [ ] Progress bar
- [ ] Tạo project mới
- [ ] Danh sách projects
- [ ] Danh sách videos trong project
- [ ] Search & filter
- [ ] Xóa video/project (soft delete)

**Backend Tasks:**
- [ ] Project model
- [ ] MediaAsset model
- [ ] Upload endpoint (multipart)
- [ ] Resume upload support
- [ ] List videos endpoint
- [ ] Get video detail
- [ ] Delete video (soft delete)
- [ ] Thumbnail generation (FFmpeg)
- [ ] Proxy video generation (lower quality for editing)
- [ ] File validation (format, size, duration)
- [ ] Storage service (S3 abstraction)

**Database:**
- [ ] Migration: Create projects table
- [ ] Migration: Create media_assets table

**Infrastructure:**
- [ ] MinIO setup & test
- [ ] File upload service
- [ ] FFmpeg integration

**Tests:**
- [ ] Unit test: file validation
- [ ] Integration test: upload flow
- [ ] Integration test: retrieve video metadata
- [ ] Test with various video formats

**Acceptance Criteria:**
- [ ] User can create project (tiếng Việt UI)
- [ ] User can upload video file
- [ ] Upload progress visible
- [ ] Resume upload working
- [ ] Video metadata captured (duration, resolution, codec)
- [ ] Thumbnail generated
- [ ] Proxy video generated (for editor)
- [ ] Video appears in library
- [ ] Pagination working
- [ ] Search & filter working
- [ ] Can delete video (soft)

---

### 1.4 Database & Migrations

**Setup:**
- [ ] PostgreSQL container running
- [ ] Alembic migration tool configured
- [ ] Initial schema created
- [ ] Migration history tracked

**Tables Created:**
- [ ] users
- [ ] projects
- [ ] media_assets
- [ ] refresh_tokens (for JWT refresh)

**Acceptance Criteria:**
- [ ] `alembic upgrade head` runs successfully
- [ ] All tables created with correct columns
- [ ] Indexes created for performance

---

### 1.5 Job Queue & Background Jobs (Setup)

**Infrastructure:**
- [ ] Redis running (Docker)
- [ ] RQ (Redis Queue) setup
- [ ] Worker process can start
- [ ] Job monitoring setup

**Basic Job Example:**
- [ ] Create a simple test job (e.g., send email)
- [ ] Enqueue job from API
- [ ] Worker processes job
- [ ] Job status tracked in Redis

**Acceptance Criteria:**
- [ ] Job Queue running without errors
- [ ] Jobs can be enqueued
- [ ] Workers process jobs in order
- [ ] Job status can be checked

---

## GIAI ĐOẠN 2 - AI VIDEO MVP (Tuần 3-4)

### 2.1 Transcription (Whisper)

**Backend Tasks:**
- [ ] Transcription model (database)
- [ ] Transcription job worker
- [ ] Call Whisper API (OpenAI)
- [ ] Save transcript to DB
- [ ] Endpoint: `POST /api/v1/transcripts/generate`
- [ ] Endpoint: `GET /api/v1/transcripts/{id}`
- [ ] Transcript segments with timestamps

**Frontend Tasks:**
- [ ] Trigger transcription button
- [ ] Progress indicator
- [ ] Display transcript
- [ ] Edit transcript UI (simple)
- [ ] Export SRT button

**Tests:**
- [ ] Test with sample video
- [ ] Verify timestamps accuracy
- [ ] Test error handling

**Acceptance Criteria:**
- [ ] Whisper processes video → Vietnamese text
- [ ] Segments with accurate timestamps
- [ ] Transcript editable
- [ ] Can export as SRT

---

### 2.2 Auto Subtitle Generation

**Backend Tasks:**
- [ ] Subtitle model (database)
- [ ] Generate subtitles from transcript
- [ ] SRT format output
- [ ] Sync with video

**Frontend Tasks:**
- [ ] Preview subtitles on video
- [ ] Adjust timing UI
- [ ] Edit text UI

**Acceptance Criteria:**
- [ ] Subtitles auto-generated from transcript
- [ ] Timing accurate
- [ ] SRT exportable

---

### 2.3 Smart Cut / Silence Detection

**Backend Tasks:**
- [ ] Analyze audio for silence
- [ ] Detect speech segments
- [ ] Suggest cuts (segments to remove)
- [ ] Save suggestions to DB

**Frontend Tasks:**
- [ ] Display silence segments
- [ ] Allow user to approve/reject cuts
- [ ] Visual timeline showing silence

**Acceptance Criteria:**
- [ ] Silence detected accurately
- [ ] Suggestions provided
- [ ] User can apply suggestions

---

### 2.4 Brand Templates

**Backend Tasks:**
- [ ] BrandTemplate model
- [ ] Admin endpoint to upload/update templates
- [ ] Apply template to video

**Frontend Tasks:**
- [ ] Admin: Upload logo, colors, fonts
- [ ] Editor: Preview template applied

**Acceptance Criteria:**
- [ ] Admin can manage brand template
- [ ] Template applied to video

---

### 2.5 Render to MP4

**Backend Tasks:**
- [ ] RenderJob model
- [ ] FFmpeg render worker
- [ ] Support aspect ratios (9:16, 16:9)
- [ ] Queue management
- [ ] Endpoint: `POST /api/v1/render`
- [ ] Endpoint: `GET /api/v1/render/{id}/status`
- [ ] Download endpoint

**Frontend Tasks:**
- [ ] Export dialog
- [ ] Select aspect ratio
- [ ] Progress tracking
- [ ] Download link when ready

**Tests:**
- [ ] Render test video
- [ ] Check output quality
- [ ] Test different aspect ratios

**Acceptance Criteria:**
- [ ] Render job queued
- [ ] Progress tracked
- [ ] MP4 1080p generated
- [ ] Both 9:16 and 16:9 aspect ratios work
- [ ] Can download result

---

### 2.6 Review & Approval Workflow

**Database:**
- [ ] ReviewRequest model
- [ ] ApprovalRecord model

**Endpoints:**
- [ ] `POST /api/v1/projects/{id}/request-review`
- [ ] `GET /api/v1/review-requests`
- [ ] `POST /api/v1/review-requests/{id}/approve`
- [ ] `POST /api/v1/review-requests/{id}/reject`

**Frontend:**
- [ ] Request review button
- [ ] Review queue
- [ ] Approve/Reject UI
- [ ] Comments field

**Acceptance Criteria:**
- [ ] Editor can request review
- [ ] Reviewer sees requests
- [ ] Can approve/reject with comments
- [ ] Status updates in project

---

## GIAI ĐOẠN 3 - PRO EDITOR (Tuần 5-6)

### 3.1 Timeline Component (Frontend)

**Features:**
- [ ] Multiple tracks (video, audio, text, effects)
- [ ] Clip rendering
- [ ] Drag-drop clips
- [ ] Trim/resize clips
- [ ] Clip deletion
- [ ] Timeline zoom in/out
- [ ] Playhead navigation
- [ ] Track management (add/remove)

**Tech:**
- [ ] Canvas or SVG rendering
- [ ] Framer Motion for interactions
- [ ] State management (Zustand)

**Acceptance Criteria:**
- [ ] Timeline renders correctly
- [ ] Clips editable (move, resize, delete)
- [ ] Multiple tracks work
- [ ] Smooth interactions

---

### 3.2 Timeline Data Model & API

**Backend:**
- [ ] Timeline model (database)
- [ ] Timeline schema (Pydantic)
- [ ] `POST /api/v1/projects/{id}/timeline/save`
- [ ] `GET /api/v1/projects/{id}/timeline`
- [ ] `POST /api/v1/projects/{id}/timeline/preview`

**Frontend:**
- [ ] Save timeline on edit
- [ ] Autosave every 30 seconds
- [ ] Conflict resolution (if multi-user later)

**Acceptance Criteria:**
- [ ] Timeline data persisted correctly
- [ ] Autosave working
- [ ] Can retrieve timeline

---

### 3.3 Text & Image Overlays

**Frontend:**
- [ ] Add text overlay dialog
- [ ] Position text on timeline
- [ ] Style text (font, color, size)
- [ ] Add image overlay
- [ ] Position image on timeline

**Backend:**
- [ ] Store text/image data in timeline

**Acceptance Criteria:**
- [ ] Text overlay added and positioned
- [ ] Image overlay added and positioned
- [ ] Styling applied
- [ ] Rendered in output

---

### 3.4 Audio Editing

**Frontend:**
- [ ] Audio track display
- [ ] Volume adjustment slider
- [ ] Fade in/out UI
- [ ] Multiple audio tracks

**Backend:**
- [ ] Store audio adjustments in timeline

**Acceptance Criteria:**
- [ ] Audio volume adjustable
- [ ] Fade effects work
- [ ] Applied in render

---

### 3.5 Undo/Redo

**Frontend:**
- [ ] History stack (≥20 items)
- [ ] Undo button
- [ ] Redo button
- [ ] Keyboard shortcuts (Ctrl+Z, Ctrl+Y)

**Tech:**
- [ ] Zustand with history middleware
- [ ] Or immer.js for immutable state

**Acceptance Criteria:**
- [ ] Undo works (≥20 steps)
- [ ] Redo works
- [ ] Keyboard shortcuts work

---

### 3.6 Versioning

**Backend:**
- [ ] Version model
- [ ] Save version on major changes
- [ ] Retrieve version history
- [ ] Revert to previous version

**Frontend:**
- [ ] Version history UI
- [ ] Show version diffs
- [ ] Restore button

**Acceptance Criteria:**
- [ ] Versions saved automatically
- [ ] Can view history
- [ ] Can revert to previous

---

## GIAI ĐOẠN 4 - AI AUTO STUDIO (Tuần 7-8)

### 4.1 Video Analysis

**Backend:**
- [ ] Analyze video content
- [ ] Extract key phrases
- [ ] Identify transitions
- [ ] Detect scenes

**Worker:**
- [ ] Integration with OpenAI API
- [ ] Process transcript for insights

**Acceptance Criteria:**
- [ ] Content analyzed
- [ ] Highlights identified
- [ ] Suggestions stored

---

### 4.2 Auto Draft Generation

**Backend:**
- [ ] Algorithm to create initial timeline
- [ ] Apply cuts based on silence
- [ ] Position highlights
- [ ] Add transitions

**Frontend:**
- [ ] Preview auto-generated draft
- [ ] Option to accept/edit

**Acceptance Criteria:**
- [ ] Auto draft generated
- [ ] Matches transcript timing
- [ ] Sensible cuts applied
- [ ] Can be imported to Pro Editor

---

### 4.3 Style Recommendation

**Backend:**
- [ ] Analyze content type
- [ ] Recommend style (professional, casual, educational)
- [ ] Apply style presets

**Acceptance Criteria:**
- [ ] Style recommended
- [ ] Can change style
- [ ] Style applied to timeline

---

## GIAI ĐOẠN 5 - AI ADVANCED (Tuần 9-10)

### 5.1 Visual & B-Roll Engine

### 5.2 AI Image Generation

### 5.3 Audio Enhancement

### 5.4 Text-to-Speech & Narration

*Details in separate phase document*

---

## GIAI ĐOẠN 6 - HOÀN THIỆN (Tuần 11-12)

### 6.1 Dashboard & Admin Panel

### 6.2 Monitoring & Logging

### 6.3 Performance Testing

### 6.4 Security Testing

### 6.5 User Documentation

---

## DEPENDENCIES & BLOCKERS

| Task | Depends On | Priority |
|------|-----------|----------|
| Transcription | Video Upload | High |
| Auto Studio | Transcription + Analysis | High |
| Pro Editor | Timeline API | High |
| Render | Timeline Finalized | High |
| Approval | Project Status | Medium |

---

## RISKS & MITIGATION

| Risk | Impact | Mitigation |
|------|--------|-----------|
| FFmpeg compatibility | High | Use Docker for consistent env |
| Whisper API limits | High | Implement queue & retry logic |
| Real-time preview lag | Medium | Use proxy video, optimize render |
| Database scaling | Medium | Monitor query performance, add indexes |
| Storage cost | Medium | Cleanup old files, compression |

---

**Next:** Bắt đầu GIAI ĐOẠN 1 - Task 1.1
