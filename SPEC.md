# DaiMinh AI Video Studio - Specification

**Version:** 1.0.0  
**Status:** In Development  
**Last Updated:** 2026-10-25

---

## 1. Project Overview

**DaiMinh AI Video Studio** là nền tảng chỉnh sửa video tích hợp AI cho Nhà thuốc Đại Minh. Hệ thống cho phép:

- Tải video thô (1-60 phút)
- Tự động tạo transcript (STT via Whisper)
- AI tự động dựng video (Auto Studio)
- Chỉnh sửa chuyên sâu (Pro Editor)
- Kiểm duyệt nội dung sức khỏe
- Xuất video MP4 1080p (9:16, 16:9)

---

## 2. Core Features

### 2.1 AI Auto Studio Module
**Mục đích:** Tự động tạo draft video từ video thô

**Workflow:**
1. User upload video (max 1 hour)
2. System extract audio → Whisper STT
3. Generate Vietnamese transcript
4. AI analyze content → suggest edits
5. Auto create draft video layout
6. Apply AI effects & transitions
7. Export 1080p MP4 (both ratios)

**Inputs:**
- Raw video file (MP4, MOV, AVI)
- Video metadata (title, description)

**Outputs:**
- Transcript (VTT, JSON)
- Draft video (MP4 1080p)
- AI suggestions JSON

---

### 2.2 Pro Video Editor Module
**Mục đích:** Manual video editing cho chuyên sâu

**Features:**
- Timeline editor (import draft or raw video)
- Trim, cut, merge segments
- Add text overlays
- Apply effects (fade, scale, rotate)
- Adjust speed, volume
- Generate AI images (Stable Diffusion)
- Preview real-time
- Save project (draft mode)
- Export final (MP4 1080p, 9:16 + 16:9)

**Toolbar:**
- Trim tool, Cut tool, Merge tool
- Text editor, Effects panel
- Image generator button
- Speed/Volume controls
- Preview/Export buttons

---

### 2.3 Content Review Module
**Mục đích:** Health policy compliance check

**Review Checklist:**
- ✓ Medical claims accuracy
- ✓ Regulatory compliance
- ✓ Harmful content filter
- ✓ Accessibility check

**Workflow:**
1. User submit video
2. AI auto-scan → flag issues
3. Pharmacist manual review
4. Approve/Reject/Request changes
5. If approved → publish
6. If rejected → return to editor

---

## 3. User Interface Design

### 3.1 Landing Page
- **Hero:** Title, subtitle, CTA button
- **Features:** 4 feature cards with icons
- **Call-to-action:** "Get Started" button

### 3.2 Main Dashboard (After Login)
- **Left Sidebar:** Navigation menu
- **Main Area:** Project list / Editor workspace
- **Top Bar:** User profile, settings

### 3.3 Editor Interface
- **Left Panel:** Tools (trim, cut, merge, text, effects)
- **Center:** Timeline editor / Preview
- **Right Panel:** Properties, export options

---

## 4. Technical Stack

### Frontend
- **Framework:** Next.js 15, React 19
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **State:** React Context / Zustand
- **UI Components:** Custom components + shadcn/ui
- **Video Preview:** Video.js / Plyr

### Backend
- **Framework:** Python FastAPI
- **Database:** PostgreSQL
- **Cache:** Redis
- **Queue:** Celery + Redis
- **Video Processing:** FFmpeg
- **AI Services:**
  - Whisper (STT)
  - Stable Diffusion (Image Gen)
  - OpenAI/Claude (Content Analysis)
- **Storage:** AWS S3 / MinIO

### DevOps
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **Frontend Hosting:** Vercel
- **Backend Hosting:** AWS EC2 / Digital Ocean
- **Database:** AWS RDS
- **Storage:** AWS S3
- **CI/CD:** GitHub Actions

---

## 5. Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  role ENUM('admin', 'editor', 'pharmacist'),
  created_at TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  title VARCHAR,
  status ENUM('draft', 'in_review', 'published'),
  created_at TIMESTAMP
);
```

### Videos Table
```sql
CREATE TABLE videos (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects,
  file_url VARCHAR,
  duration INTEGER,
  format VARCHAR,
  created_at TIMESTAMP
);
```

### Transcripts Table
```sql
CREATE TABLE transcripts (
  id UUID PRIMARY KEY,
  video_id UUID REFERENCES videos,
  content TEXT,
  language VARCHAR,
  created_at TIMESTAMP
);
```

---

## 6. API Endpoints (to be implemented)

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Current user info

### Projects
- `GET /api/projects` - List user projects
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Videos
- `POST /api/videos/upload` - Upload raw video
- `GET /api/videos/{id}` - Get video info
- `DELETE /api/videos/{id}` - Delete video

### Processing
- `POST /api/processing/auto-studio` - Start auto studio
- `POST /api/processing/export` - Start export
- `GET /api/processing/{job_id}` - Job status

### Content Review
- `POST /api/review/submit` - Submit for review
- `GET /api/review/{id}` - Get review status
- `POST /api/review/{id}/approve` - Approve
- `POST /api/review/{id}/reject` - Reject

---

## 7. Navigation Structure

```
Landing Page
├── Get Started Button
└── Learn React Link

Dashboard (After Login)
├── Auto Studio
│   ├── Upload Video
│   ├── View Transcript
│   └── Download Draft
├── Pro Editor
│   ├── Load Project
│   ├── Edit Timeline
│   └── Export Video
├── Review Queue
│   ├── Pending Reviews
│   └── Review Details
└── Settings
    ├── Profile
    └── Preferences
```

---

## 8. Deployment Checklist

- [ ] Frontend deployed to Vercel
- [ ] Domain configured (video.daiminh365.vn)
- [ ] Backend API running
- [ ] Database connected
- [ ] S3 storage configured
- [ ] Redis cache running
- [ ] Docker images built
- [ ] Environment variables set
- [ ] HTTPS/SSL enabled
- [ ] Monitoring & logging setup

---

## 9. Roadmap

### Phase 1 (Current)
- ✅ Landing page deployed
- 🔄 Mobile app (APK) in testing
- [ ] Basic dashboard UI
- [ ] Project management

### Phase 2
- [ ] Auto Studio AI integration
- [ ] Video upload & STT
- [ ] Basic timeline editor

### Phase 3
- [ ] Advanced editing tools
- [ ] AI image generation
- [ ] Content review workflow

### Phase 4
- [ ] Health policy engine
- [ ] Analytics dashboard
- [ ] Team collaboration

---

## 10. Success Metrics

- Landing page load time: < 2s
- Video upload: < 30s (100MB)
- Transcript generation: < 2min (1 hour video)
- Export time: < 5min (1080p MP4)
- User satisfaction: 4.5/5 stars
- System uptime: 99.9%

---

**Document Author:** DaiMinh Development Team  
**Last Review:** 2026-10-25
