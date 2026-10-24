# PowerShell Script - Em tạo repo GitHub + push code tự động

# BƯỚC 1: Anh tạo repo trên GitHub (web)
# Link: https://github.com/new
# - Repo name: daiminh-video-studio
# - Public
# - Không init (để trống)

# BƯỚC 2: Copy URL repo (dạng: https://github.com/USERNAME/daiminh-video-studio.git)

# BƯỚC 3: Chạy các command dưới đây:

# ===== BẮT ĐẦU =====

cd "D:\Nhà máy sản xuất app\Chỉnh sửa Video"

# NHẬP REPO URL (anh thay bằng URL thực)
$REPO_URL = Read-Host "Nhập GitHub repo URL (https://github.com/USERNAME/daiminh-video-studio.git)"

# Setup remote
git remote add origin $REPO_URL

# Push code lên main branch
git branch -M main
git push -u origin main

Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host "Next: Import vào Vercel" -ForegroundColor Cyan
