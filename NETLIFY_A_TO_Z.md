# 🚀 NETLIFY DEPLOYMENT - HƯỚNG DẪN CHI TIẾT A TỚI Z

**Anh chỉ cần 5 phút, click vài nút là xong!**

---

## **BƯỚC 1: MỞ NETLIFY**

👉 **Vào link này:** https://app.netlify.com

---

## **BƯỚC 2: LOGIN / SIGNUP**

### Nếu chưa có account:
1. Click **"Sign up"**
2. Chọn **"Sign up with GitHub"**
3. Authorize Netlify truy cập GitHub
4. Xong!

### Nếu đã có account:
1. Click **"Log in"**
2. Login bằng GitHub
3. Xong!

---

## **BƯỚC 3: TẠO PROJECT MỚI**

**Sau khi login, anh sẽ thấy dashboard Netlify**

1. Click nút **"Add new site"** (hoặc **"New site from Git"**)
2. Chọn **"Import an existing project"**

---

## **BƯỚC 4: KẾT NỐI GITHUB**

1. Chọn **"GitHub"**
2. Click **"Authorize Netlify"** (nếu cần)
3. Chọn repo: **`daiduoc8288/daiminh-video-studio`**
4. Click **"Install & Authorize"**

---

## **BƯỚC 5: CẤU HÌNH BUILD**

**Netlify sẽ hiển thị form cấu hình:**

| Field | Giá trị |
|-------|--------|
| **Branch to deploy** | `main` |
| **Build command** | `npm run build` |
| **Publish directory** | `.next` |
| **Base directory** | `frontend` |

✅ **Nhập đúng các giá trị trên!**

---

## **BƯỚC 6: DEPLOY**

1. Kiểm tra lại các cài đặt
2. Click nút **"Deploy site"** (màu xanh lá)
3. **Chờ 5-10 phút để Netlify build & deploy**

**Anh sẽ thấy:**
- Build log chạy (dòng text xanh)
- Status: "Building..." → "Deploying..." → "Published" ✅

---

## **BƯỚC 7: LẤY NETLIFY URL**

**Sau khi deploy xong:**

1. Anh sẽ thấy URL Netlify (dạng: `https://daiminh-video-studio.netlify.app`)
2. **Copy URL này!**
3. **Cho Em!**

---

## **BƯỚC 8: SETUP CUSTOM DOMAIN (Em làm)**

Sau khi anh cho em Netlify URL:

Em sẽ:
1. ✅ Vào Netlify settings
2. ✅ Add custom domain: `video.daiminh365.vn`
3. ✅ Update DNS (CNAME pointing)
4. ✅ **Web LIVE!** 🎉

---

## **NẾU CÓ LỖIBAO GIỜ:**

### Build Failed?
- Check build log (red error text)
- Báo em error message

### Deploy không xong?
- Chờ thêm 5 phút
- Refresh page
- Check "Deploys" tab

### Không thấy repo GitHub?
- Logout Netlify
- Logout GitHub
- Login lại

---

## **TÓNG TẮT:**

1. ✅ Vào netlify.com
2. ✅ Login GitHub
3. ✅ Click "Add new site"
4. ✅ Chọn repo: `daiduoc8288/daiminh-video-studio`
5. ✅ Build command: `npm run build`
6. ✅ Publish: `.next`
7. ✅ Base: `frontend`
8. ✅ Click Deploy
9. ✅ Chờ 5-10 phút
10. ✅ Copy URL → Cho Em

**Xong!** 🎉

---

**ANH LÀM THEO HƯỚNG DẪN NÀY, CHẮC CHẮN THÀNH CÔNG!**

**Anh làm xong, báo Em Netlify URL!** 💪
