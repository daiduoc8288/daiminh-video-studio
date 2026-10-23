# DAIMINH AI VIDEO STUDIO - DEPLOYMENT GUIDE

## Mục Lục
1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Chuẩn Bị Môi Trường](#chuẩn-bị-môi-trường)
3. [Triển Khai Cục Bộ (Development)](#triển-khai-cục-bộ)
4. [Triển Khai Sản Xuất (Production)](#triển-khai-sản-xuất)
5. [Monitoring & Logging](#monitoring--logging)
6. [Bảo Mật & Hardening](#bảo-mật--hardening)
7. [Khôi Phục & Sao Lưu](#khôi-phục--sao-lưu)

## Yêu Cầu Hệ Thống

### Cục Bộ (Development)
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+
- Node.js 20+
- PostgreSQL 15 (hoặc Docker container)
- Redis 7 (hoặc Docker container)
- MinIO S3-compatible storage

### Sản Xuất (Production)
- Server Linux (Ubuntu 20.04+ hoặc CentOS 8+)
- Docker & Docker Compose
- Nginx reverse proxy
- SSL/TLS certificates
- PostgreSQL 15
- Redis 7
- MinIO hoặc AWS S3
- Prometheus & Grafana (monitoring)
- ELK Stack (logging)
- Disk space: 100GB+ cho media storage

## Chuẩn Bị Môi Trường

### 1. Clone Repository
```bash
git clone https://github.com/your-org/daiminh-video-studio.git
cd daiminh-video-studio
```

### 2. Cấu Hình Environment Variables
```bash
cp .env.example .env.production
nano .env.production
```

**Biến quan trọng:**
```bash
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/daiminh_db
DB_USER=daiminh_user
DB_PASSWORD=secure_password_here

# Redis
REDIS_URL=redis://redis:6379

# JWT
JWT_SECRET_KEY=your-secret-key-min-32-chars

# MinIO/S3
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=secure_minio_password
MINIO_URL=http://minio:9000

# API
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
OPENAI_API_KEY=sk-xxxxxxxxxxxx

# Security
ENVIRONMENT=production
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### 3. Tạo SSL/TLS Certificates
```bash
# Tự ký (Development)
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Production (sử dụng Let's Encrypt)
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com
# Copy certs vào thư mục ssl/
```

## Triển Khai Cục Bộ

### 1. Khởi Động Services
```bash
docker-compose up -d
```

### 2. Chạy Database Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### 3. Tạo Admin User (First-time setup)
```bash
docker-compose exec backend python -c "
from app.database.session import SessionLocal
from app.database.models.user import User
from app.utils.security import hash_password

db = SessionLocal()
user = User(
    email='admin@daiminh.local',
    password_hash=hash_password('admin123'),
    role='admin'
)
db.add(user)
db.commit()
print('Admin user created')
"
```

### 4. Truy Cập Ứng Dụng
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/docs
- MinIO Console: http://localhost:9001
- Credentials MinIO: minioadmin / minioadmin

## Triển Khai Sản Xuất

### 1. Chuẩn Bị Server
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clone & Cấu Hình
```bash
cd /app
git clone https://github.com/your-org/daiminh-video-studio.git .

# Copy cấu hình
cp .env.example .env.production
nano .env.production

# Set permissions
chmod 600 .env.production
```

### 3. Khởi Động Production Stack
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Verify Services
```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Health check
curl -k https://localhost/health
```

### 5. Cấu Hình Nginx
```bash
# Nginx configuration được tự động load từ nginx.prod.conf
# Kiểm tra cấu hình
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

### 6. Khôi Phục Database (nếu cần)
```bash
# Backup hiện tại
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U daiminh_user daiminh_db > backup.sql

# Restore từ backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U daiminh_user daiminh_db < backup.sql
```

## Monitoring & Logging

### 1. Khởi Động Monitoring Stack
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

### 2. Truy Cập Dashboards
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Kibana**: http://localhost:5601

### 3. Cấu Hình Alerts
```bash
# Edit alertmanager.yml
nano monitoring/alertmanager.yml

# Thêm Slack webhook
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
docker-compose -f docker-compose.monitoring.yml exec alertmanager \
  sh -c "envsubst < /etc/alertmanager/alertmanager.yml > /tmp/alertmanager.yml && cp /tmp/alertmanager.yml /etc/alertmanager/alertmanager.yml"
```

### 4. Xem Logs
```bash
# Container logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Application logs
docker-compose -f docker-compose.monitoring.yml logs -f filebeat

# Database logs
docker-compose -f docker-compose.prod.yml logs -f postgres
```

## Bảo Mật & Hardening

### 1. Cập Nhật Security Headers
```bash
# Đã cấu hình trong nginx.prod.conf:
# - HSTS (HTTP Strict Transport Security)
# - X-Frame-Options
# - X-Content-Type-Options
# - X-XSS-Protection
# - Referrer-Policy
```

### 2. Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5432/tcp  # PostgreSQL (restricted)
sudo ufw allow 6379/tcp  # Redis (restricted)
```

### 3. Database Security
```bash
# Thay đổi mật khẩu PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U daiminh_user -c "ALTER USER daiminh_user WITH PASSWORD 'new_password';"

# Tạo user chỉ đọc cho backup
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U daiminh_user -c "CREATE USER backup_user WITH PASSWORD 'backup_password';"
```

### 4. JWT Security
```bash
# Generate strong JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env
JWT_SECRET_KEY=your_generated_secret
docker-compose -f docker-compose.prod.yml restart backend
```

### 5. File Permissions
```bash
# SSL certificates
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem

# Configuration files
chmod 600 .env.production
chmod 600 monitoring/alertmanager.yml

# Data volumes
sudo chown -R 999:999 postgres_data/
sudo chown -R 999:999 redis_data/
sudo chown -R 999:999 minio_data/
```

## Khôi Phục & Sao Lưu

### 1. Automated Backups
```bash
# Tạo script backup hàng ngày
sudo tee /usr/local/bin/daiminh-backup.sh > /dev/null <<'EOF'
#!/bin/bash
BACKUP_DIR="/backups/daiminh"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
docker-compose -f /app/docker-compose.prod.yml exec -T postgres \
  pg_dump -U daiminh_user daiminh_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# MinIO backup (sync to external storage)
aws s3 sync s3://daiminh-bucket/ s3://backup-bucket/daiminh-$DATE/ \
  --profile daiminh --region ap-southeast-1

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

# Log the backup
echo "Backup completed at $DATE" >> /var/log/daiminh-backup.log
EOF

sudo chmod +x /usr/local/bin/daiminh-backup.sh

# Add to crontab (2 AM daily)
sudo crontab -e
# 0 2 * * * /usr/local/bin/daiminh-backup.sh
```

### 2. Restore Procedure
```bash
# Stop application
docker-compose -f docker-compose.prod.yml down

# Restore database
docker-compose -f docker-compose.prod.yml up postgres -d
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U daiminh_user daiminh_db < backup_$DATE.sql

# Restore MinIO data
aws s3 sync s3://backup-bucket/daiminh-$DATE/ s3://daiminh-bucket/ \
  --profile daiminh --region ap-southeast-1

# Restart all services
docker-compose -f docker-compose.prod.yml up -d

# Verify
docker-compose -f docker-compose.prod.yml ps
curl -k https://localhost/health
```

## Troubleshooting

### Database Connection Error
```bash
# Kiểm tra PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_isready
docker-compose -f docker-compose.prod.yml logs postgres
```

### API Timeout
```bash
# Kiểm tra backend
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml exec backend curl http://localhost:8000/api/health
```

### Storage Issues
```bash
# Kiểm tra MinIO
docker-compose -f docker-compose.prod.yml exec minio curl http://localhost:9000/minio/health/live

# Check disk space
df -h
docker system df
```

### Performance Tuning
```bash
# Increase worker processes
docker-compose -f docker-compose.prod.yml down
# Edit docker-compose.prod.yml backend service:
# CMD: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
docker-compose -f docker-compose.prod.yml up -d
```

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Database Backup | Daily @ 2 AM | `daiminh-backup.sh` |
| Log Rotation | Weekly | Automatic (logrotate) |
| Security Updates | Monthly | `apt-get update && apt-get upgrade` |
| Certificate Renewal | 30 days before expiry | `certbot renew` |
| Storage Cleanup | Weekly | Manual or automated script |
| Performance Review | Monthly | Check Grafana dashboards |

## Support & Escalation

- **Critical Issues**: ops-team@daiminh.local
- **Database Issues**: dba-team@daiminh.local
- **Security Issues**: security@daiminh.local
- **On-call Rotation**: Check PagerDuty

---

**Last Updated**: 2026-10-23 | **Version**: 6.0.0
