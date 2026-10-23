# ARCHITECTURE - DAIMINH AI VIDEO STUDIO

**Phiên bản:** 1.0  
**Ngày tạo:** 2026-10-23

---

## I. TỔNG QUAN KIẾN TRÚC

```
┌─────────────────────────────────────────────────────┐
│          FRONTEND (Next.js + React)                 │
│  - Web UI (Tailwind CSS)                            │
│  - Real-time preview                                │
│  - Timeline editor                                  │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────▼──────────────────────────────────┐
│       BACKEND API GATEWAY (FastAPI)                 │
│  - Authentication & Authorization                   │
│  - REST API                                         │
│  - WebSocket for real-time updates                  │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    ┌────────┐┌────────┐┌──────────┐
    │ Database│ Cache   │Job Queue  │
    │PostgreSQL│ Redis   │ (Redis)  │
    └────────┘└────────┘└──────────┘
        │          │          │
        └──────────┼──────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    ┌──────────┐       ┌──────────┐
    │ AI Workers│      │Render    │
    │(Whisper,  │      │Workers   │
    │ OpenAI,   │      │(FFmpeg)  │
    │Stable     │      │          │
    │Diffusion) │      └──────────┘
    └──────────┘
        │
        ▼
    ┌──────────────────┐
    │ Object Storage   │
    │ (S3-compatible)  │
    └──────────────────┘
```

---

## II. PHÂN TÁCH MODULES

### 2.1 Frontend Layer (Next.js)

**Thư mục cấu trúc:**

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── logout/
│   ├── (app)/
│   │   ├── dashboard/
│   │   ├── projects/
│   │   │   ├── [id]/
│   │   │   │   ├── editor/
│   │   │   │   ├── review/
│   │   │   │   └── settings/
│   │   │   └── new/
│   │   ├── admin/
│   │   └── layout.tsx
│   └── api/ (optional, for edge functions)
├── components/
│   ├── common/
│   ├── auth/
│   ├── project/
│   ├── editor/
│   │   ├── Timeline/
│   │   ├── Preview/
│   │   └── Tools/
│   └── admin/
├── hooks/
├── services/ (API clients)
├── store/ (Zustand/Redux state)
├── types/
├── styles/
└── public/
```

**Tech Stack:**

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui or Ant Design
- Zustand (state management)
- axios / fetch (HTTP)
- React Query (server state)
- Framer Motion (animations)

---

### 2.2 Backend API (FastAPI)

**Thư mục cấu trúc:**

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py (FastAPI app initialization)
│   ├── config.py
│   ├── dependencies.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py (login, logout, refresh)
│   │   │   ├── videos.py (upload, list, detail)
│   │   │   ├── projects.py (CRUD projects)
│   │   │   ├── transcripts.py (STT)
│   │   │   ├── auto_studio.py (AI analysis)
│   │   │   ├── editor.py (timeline save)
│   │   │   ├── render.py (export)
│   │   │   ├── admin.py (dashboard)
│   │   │   └── health.py
│   │   └── ws/ (WebSocket endpoints)
│   ├── models/ (Pydantic schemas)
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── media.py
│   │   ├── transcript.py
│   │   ├── timeline.py
│   │   └── job.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── session.py (SQLAlchemy session)
│   │   ├── base.py
│   │   └── models/ (ORM models)
│   │       ├── user.py
│   │       ├── project.py
│   │       ├── media.py
│   │       ├── transcript.py
│   │       ├── timeline.py
│   │       ├── job.py
│   │       └── audit_log.py
│   ├── services/ (Business logic)
│   │   ├── auth_service.py
│   │   ├── video_service.py
│   │   ├── transcription_service.py
│   │   ├── analysis_service.py
│   │   ├── render_service.py
│   │   ├── storage_service.py
│   │   └── email_service.py
│   ├── workers/ (Background jobs)
│   │   ├── transcription_worker.py
│   │   ├── analysis_worker.py
│   │   ├── render_worker.py
│   │   └── ai_worker.py
│   ├── tasks/ (Celery/RQ tasks)
│   │   ├── transcribe.py
│   │   ├── analyze.py
│   │   ├── render.py
│   │   └── cleanup.py
│   ├── middleware/
│   │   ├── auth.py
│   │   ├── cors.py
│   │   └── error_handler.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── validators.py
│   │   ├── ffmpeg_utils.py
│   │   └── storage_utils.py
│   └── exceptions.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── migrations/ (Alembic)
├── requirements.txt
├── .env.example
└── main.py (entry point)
```

**Tech Stack:**

- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic (validation)
- Redis (caching + job queue)
- RQ or Celery (background jobs)
- APScheduler (scheduled tasks)
- Python-Jose (JWT)
- Pytest (testing)
- FFmpeg (video processing)
- Whisper (STT)

---

### 2.3 Database (PostgreSQL)

**Schema tổng quát:**

```
users
├─ id (UUID, PK)
├─ email (varchar, unique)
├─ password_hash (varchar)
├─ full_name (varchar)
├─ role (enum: admin, editor, reviewer)
├─ created_at
└─ updated_at

projects
├─ id (UUID, PK)
├─ user_id (FK users)
├─ title (varchar)
├─ status (enum: draft, reviewing, approved, published)
├─ created_at
└─ updated_at

media_assets
├─ id (UUID, PK)
├─ project_id (FK projects)
├─ original_filename (varchar)
├─ file_size (bigint)
├─ duration (float)
├─ width (int)
├─ height (int)
├─ status (enum: uploading, ready, processing, error)
├─ original_path (varchar)
├─ proxy_path (varchar)
├─ thumbnail_path (varchar)
├─ metadata (jsonb)
├─ created_at
└─ updated_at

transcripts
├─ id (UUID, PK)
├─ media_asset_id (FK media_assets)
├─ content (text)
├─ segments (jsonb[])
├─ language (varchar)
├─ status (enum: pending, processing, completed, error)
├─ created_at
└─ updated_at

timelines
├─ id (UUID, PK)
├─ project_id (FK projects)
├─ duration (float)
├─ fps (int)
├─ width (int)
├─ height (int)
├─ data (jsonb) -- timeline structure
├─ version (int)
├─ created_at
└─ updated_at

render_jobs
├─ id (UUID, PK)
├─ project_id (FK projects)
├─ aspect_ratio (enum: 9:16, 16:9)
├─ status (enum: pending, processing, completed, error)
├─ progress (float)
├─ output_path (varchar)
├─ retry_count (int)
├─ error_message (text)
├─ started_at
├─ completed_at
└─ created_at

review_requests
├─ id (UUID, PK)
├─ project_id (FK projects)
├─ requested_by (FK users)
├─ assigned_to (FK users)
├─ status (enum: pending, approved, rejected)
├─ comments (text)
├─ created_at
└─ updated_at

audit_logs
├─ id (UUID, PK)
├─ user_id (FK users)
├─ action (varchar)
├─ resource_type (varchar)
├─ resource_id (UUID)
├─ changes (jsonb)
└─ created_at
```

**Indexes:**

```
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_media_assets_project_id ON media_assets(project_id);
CREATE INDEX idx_media_assets_status ON media_assets(status);
CREATE INDEX idx_transcripts_media_asset_id ON transcripts(media_asset_id);
CREATE INDEX idx_timelines_project_id ON timelines(project_id);
CREATE INDEX idx_render_jobs_project_id ON render_jobs(project_id);
CREATE INDEX idx_render_jobs_status ON render_jobs(status);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

### 2.4 Cache & Queue (Redis)

**Redis Keys Naming:**

```
# User sessions
session:user:{user_id}

# Cache
cache:video:{video_id}:metadata
cache:transcript:{transcript_id}
cache:project:{project_id}

# Job Queue
job:queue:transcription
job:queue:rendering
job:queue:analysis

# Real-time updates
ws:project:{project_id}
ws:user:{user_id}

# Rate limiting
rate_limit:user:{user_id}:{endpoint}
```

---

### 2.5 Object Storage (S3-compatible)

**Bucket Structure:**

```
daiminh-videos/
├── originals/
│   └── {year}/{month}/{video_id}/video.mp4
├── proxies/
│   └── {year}/{month}/{video_id}/proxy.mp4
├── thumbnails/
│   └── {year}/{month}/{video_id}/thumb.jpg
├── exports/
│   └── {project_id}/{render_job_id}/export.mp4
├── templates/
│   └── {template_id}/
│       ├── intro.mp4
│       ├── outro.mp4
│       └── logo.png
└── uploads/
    └── {user_id}/{temporary_files}
```

---

### 2.6 AI Workers

**Worker Types:**

1. **Transcription Worker**
   - Input: video_id
   - Process: Whisper STT
   - Output: transcript JSON

2. **Analysis Worker**
   - Input: video_id, transcript_id
   - Process: NLP analysis, silence detection
   - Output: highlights, suggestions

3. **Render Worker**
   - Input: project_id, timeline_data, aspect_ratio
   - Process: FFmpeg render
   - Output: MP4 video

**Queue Management:**

```
Job Queue (Redis):
- TRANSCRIPTION (priority: high)
- ANALYSIS (priority: medium)
- RENDERING (priority: high)
- CLEANUP (priority: low)
```

---

## III. DEPLOYMENT & INFRASTRUCTURE

### 3.1 Local Development (Docker Compose)

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    ports: ["5432:5432"]
    env_file: .env
    
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    
  minio:
    image: minio/minio:latest
    ports: ["9000:9000", "9001:9001"]
    env_file: .env
    
  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [postgres, redis]
    env_file: .env
    volumes:
      - ./backend:/app
      
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]
```

### 3.2 Cloud Architecture (AWS/GCP)

```
┌─────────────────────────────┐
│   Kubernetes Cluster        │
├─────────────────────────────┤
│  FastAPI Deployment (k8s)   │
├─────────────────────────────┤
│  Worker Pods:               │
│  - Transcription (2-5)      │
│  - Analysis (2-5)           │
│  - Rendering (3-10)         │
└────────────┬────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
  RDS    ElastiCache S3
  (PostgreSQL) (Redis)
```

---

## IV. SECURITY

### 4.1 Authentication & Authorization

- JWT tokens (access + refresh)
- Role-based access control (RBAC)
- Session management via Redis

### 4.2 Data Protection

- Encrypted passwords (bcrypt)
- HTTPS only
- No secrets in code (use env vars)
- Input validation (Pydantic)
- SQL injection protection (SQLAlchemy ORM)

### 4.3 File Security

- File type validation
- File size limits
- Virus scan (optional)
- Restrict file access

### 4.4 Logging & Monitoring

- Audit logs for all operations
- Request/response logging
- Error tracking (Sentry)
- Performance monitoring

---

## V. SCALABILITY

### Horizontal Scaling

```
// Thêm AI workers
$ kubectl scale deployment ai-worker --replicas=10

// Thêm render workers
$ kubectl scale deployment render-worker --replicas=5

// Thêm API pods
$ kubectl scale deployment backend-api --replicas=3
```

### Database Optimization

- Read replicas
- Connection pooling
- Query optimization
- Index optimization

---

## VI. MONITORING & LOGGING

**Stack:**

- Prometheus (metrics)
- Grafana (dashboards)
- ELK Stack (logs)
- Sentry (errors)

**Key Metrics:**

- API response time
- Video processing duration
- Job queue size
- Database connection count
- Storage usage
- Error rate

---

**Next Step:** Tạo Database Schema & API Contracts chi tiết
