# TASKS - DAIMINH AI VIDEO STUDIO

**Phiên bản:** 1.0  
**Ngày cập nhật:** 2026-10-23  
**Trạng thái:** Active

---

## GIAI ĐOẠN 1: NỀN TẢNG

### Task 1.1 - Khởi tạo Project Structure

**Status:** ⏳ READY TO START  
**Priority:** P0 (Critical)  
**Assigned to:** AI Assistant  
**Effort:** 4 hours

**Description:**
- Tạo thư mục frontend/ và backend/
- Khởi tạo Next.js 15 project
- Khởi tạo FastAPI app
- Tạo Docker Compose (PostgreSQL, Redis, MinIO)
- Tạo .env.example
- Setup git

**Acceptance Criteria:**
- [ ] `npm run dev` chạy trên localhost:3000
- [ ] `python main.py` chạy trên localhost:8000
- [ ] Database, Redis, MinIO trong Docker
- [ ] .env.example có tất cả biến cần thiết

**Files to Create:**
- frontend/package.json
- backend/requirements.txt
- docker-compose.yml
- .env.example

---

### Task 1.2 - Frontend: Login Page

**Status:** ⏳ BLOCKED (wait 1.1)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Tạo login form (React component)
- Email + password input
- Submit button
- Error messages (tiếng Việt)
- Styling with Tailwind
- Store token in localStorage

**Acceptance Criteria:**
- [ ] Form renders correctly
- [ ] All text in Vietnamese
- [ ] Can submit login
- [ ] Token stored after successful login
- [ ] Error messages display in Vietnamese

---

### Task 1.3 - Backend: User Model & Auth Endpoints

**Status:** ⏳ BLOCKED (wait 1.1)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 4 hours

**Description:**
- Create User ORM model (SQLAlchemy)
- Create User Pydantic schema
- Implement password hashing (bcrypt)
- JWT token generation
- `POST /api/v1/auth/login` endpoint
- `POST /api/v1/auth/refresh` endpoint
- `GET /api/v1/auth/me` endpoint
- `POST /api/v1/auth/logout` endpoint
- Auth middleware

**Acceptance Criteria:**
- [ ] User can login with valid email/password
- [ ] Invalid credentials return 401
- [ ] JWT token returned
- [ ] Token refresh works
- [ ] Protected endpoints verify token
- [ ] Logout clears session

---

### Task 1.4 - Database: Initial Migrations

**Status:** ⏳ BLOCKED (wait 1.3)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 2 hours

**Description:**
- Setup Alembic migration tool
- Create initial migration (users table)
- Create projects table
- Create media_assets table
- Run migrations

**Acceptance Criteria:**
- [ ] Alembic configured
- [ ] Migration files created
- [ ] `alembic upgrade head` runs successfully
- [ ] Tables created in PostgreSQL

---

### Task 1.5 - Frontend: Protected Routes & Layout

**Status:** ⏳ BLOCKED (wait 1.2)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Create app layout (header, sidebar, main)
- Implement route protection (redirect to login if not authenticated)
- Logout functionality
- Navigation menu (tiếng Việt)
- Dashboard stub

**Acceptance Criteria:**
- [ ] Non-authenticated users redirected to login
- [ ] Authenticated users see app layout
- [ ] Logout button works
- [ ] Navigation menu in Vietnamese

---

### Task 1.6 - Frontend: Project & Video Upload

**Status:** ⏳ BLOCKED (wait 1.5)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 4 hours

**Description:**
- Create new project form
- List existing projects
- Upload video UI (drag-drop + file picker)
- Progress bar for upload
- List uploaded videos in project
- Delete project/video

**Acceptance Criteria:**
- [ ] Can create project
- [ ] Can upload video (drag-drop and picker)
- [ ] Progress bar shows upload progress
- [ ] Videos list after upload
- [ ] Can delete project/video
- [ ] All UI in Vietnamese

---

### Task 1.7 - Backend: Video Upload Endpoints

**Status:** ⏳ BLOCKED (wait 1.4)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 4 hours

**Description:**
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `DELETE /api/v1/projects/{id}` - Delete project (soft)
- `POST /api/v1/videos/upload` - Upload video
- `GET /api/v1/videos` - List videos
- `DELETE /api/v1/videos/{id}` - Delete video
- File validation (format, size)
- Storage service (MinIO integration)

**Acceptance Criteria:**
- [ ] Can create/read/delete projects
- [ ] Can upload video file
- [ ] File validation works
- [ ] Files stored in MinIO
- [ ] Video metadata saved to DB

---

### Task 1.8 - Backend: FFmpeg Integration (Thumbnail & Proxy)

**Status:** ⏳ BLOCKED (wait 1.7)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Extract video metadata (duration, resolution, codec) using FFmpeg
- Generate thumbnail from first frame
- Generate proxy video (lower bitrate for editing)
- Run as background job
- Update DB with paths

**Acceptance Criteria:**
- [ ] Metadata extracted correctly
- [ ] Thumbnail generated
- [ ] Proxy video generated
- [ ] Paths saved to DB
- [ ] Jobs queued in background

---

### Task 1.9 - Setup Redis & Job Queue

**Status:** ⏳ BLOCKED (wait 1.1)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 2 hours

**Description:**
- Configure RQ (Redis Queue) in FastAPI
- Create worker process
- Implement basic job enqueue/process
- Monitor job status

**Acceptance Criteria:**
- [ ] Redis running in Docker
- [ ] RQ configured
- [ ] Worker process starts
- [ ] Jobs can be enqueued
- [ ] Worker processes jobs

---

### Task 1.10 - Tests: Authentication & Upload

**Status:** ⏳ BLOCKED (wait 1.8)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Unit tests for password hashing
- Unit tests for JWT token generation
- Integration tests for login flow
- Integration tests for upload flow
- Test error cases

**Acceptance Criteria:**
- [ ] All tests passing
- [ ] >80% code coverage for auth & upload
- [ ] Tests can be run with `pytest`

---

## GIAI ĐOẠN 2: AI VIDEO MVP

### Task 2.1 - Backend: Transcription Service (Whisper)

**Status:** ⏳ BLOCKED (wait 1.9)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 5 hours

**Description:**
- Create Transcript ORM model
- Integrate Whisper API (OpenAI)
- Create transcription worker
- Endpoint: `POST /api/v1/transcripts/generate`
- Endpoint: `GET /api/v1/transcripts/{id}`
- Endpoint: `PUT /api/v1/transcripts/{id}` (edit)
- Handle API errors & retries
- Save transcript segments with timestamps

**Acceptance Criteria:**
- [ ] Can call Whisper API
- [ ] Transcript saved to DB
- [ ] Segments with accurate timestamps
- [ ] Endpoint returns transcript data
- [ ] Edit endpoint works

---

### Task 2.2 - Frontend: Transcript Display & Editing

**Status:** ⏳ BLOCKED (wait 2.1)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Display transcript text with timestamps
- Edit transcript (simple text editing)
- Sync with video (click segment → jump to time)
- Save edits
- Export SRT button

**Acceptance Criteria:**
- [ ] Transcript displays correctly
- [ ] Can edit text
- [ ] Click segment → video jumps
- [ ] Edits saved
- [ ] Can export as SRT

---

### Task 2.3 - Backend: Audio Analysis (Silence Detection)

**Status:** ⏳ BLOCKED (wait 1.9)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Analyze audio for silence
- Detect speech segments
- Create suggestions for cuts
- Store suggestions in DB
- Endpoint: `POST /api/v1/videos/{id}/analyze`

**Acceptance Criteria:**
- [ ] Silence detected accurately
- [ ] Suggestions generated
- [ ] Endpoint returns suggestions
- [ ] Can apply suggestions

---

### Task 2.4 - Backend: Render Pipeline (FFmpeg)

**Status:** ⏳ BLOCKED (wait 1.10)  
**Priority:** P0  
**Assigned to:** AI Assistant  
**Effort:** 5 hours

**Description:**
- Create RenderJob model
- Create render worker (FFmpeg)
- Support aspect ratios (9:16, 16:9)
- Queue management
- Endpoint: `POST /api/v1/projects/{id}/render`
- Endpoint: `GET /api/v1/render/{id}/status`
- Download endpoint
- Retry logic on failure
- Error handling

**Acceptance Criteria:**
- [ ] Can queue render job
- [ ] Render worker processes job
- [ ] MP4 1080p output
- [ ] Both aspect ratios work
- [ ] Progress trackable
- [ ] Can download result

---

### Task 2.5 - Frontend: Export & Download UI

**Status:** ⏳ BLOCKED (wait 2.4)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 2 hours

**Description:**
- Export dialog (select aspect ratio)
- Progress indicator during render
- Download button when ready
- Show download link

**Acceptance Criteria:**
- [ ] Dialog shows aspect ratio options
- [ ] Progress updates
- [ ] Download button appears
- [ ] Can download MP4

---

### Task 2.6 - Backend: Review Workflow

**Status:** ⏳ BLOCKED (wait 1.10)  
**Priority:** P1  
**Assigned to:** AI Assistant  
**Effort:** 3 hours

**Description:**
- Create ReviewRequest model
- Endpoint: `POST /api/v1/projects/{id}/request-review`
- Endpoint: `GET /api/v1/review-requests`
- Endpoint: `POST /api/v1/review-requests/{id}/approve`
- Endpoint: `POST /api/v1/review-requests/{id}/reject`
- Update project status

**Acceptance Criteria:**
- [ ] Can request review
- [ ] Review requests show up
- [ ] Can approve/reject
- [ ] Project status updates
- [ ] Notifications sent

---

## STATUS SUMMARY

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1 | ⏳ Planning | 0% |
| Phase 2 | ⏳ Blocked | 0% |
| Phase 3 | ⏳ Future | 0% |
| Phase 4 | ⏳ Future | 0% |
| Phase 5 | ⏳ Future | 0% |
| Phase 6 | ⏳ Future | 0% |

---

**Last Updated:** 2026-10-23  
**Next Review:** After Task 1.1 completion
