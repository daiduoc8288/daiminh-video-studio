# 📱 BUILD ANDROID APP - HƯỚNG DẪN CHI TIẾT

**DaiMinh AI Video Studio - Bản Android**

---

## ✅ CÁ BẬC CHUẨN BỊ (EM ĐÃ LÀMBƯỚC 1-3)

- ✅ **Bước 1:** Build Next.js app - DONE
- ✅ **Bước 2:** Setup Capacitor - DONE  
- ✅ **Bước 3:** Add Android platform - DONE
- ✅ **Bước 4:** Copy web assets - DONE
- 🔜 **Bước 5:** Build APK (anh làm)

---

## 📥 TẢI CẦN THIẾT

### **1. Tải Android Studio**

**Link:** https://developer.android.com/studio

**Bước tải:**
1. Click "Download Android Studio"
2. Chọn Windows version
3. Install (làm theo hướng dẫn default)
4. Khởi động Android Studio

**Setup:**
- First launch sẽ hỏi cài SDK
- Click "Next" tất cả
- Chờ khoảng 10-15 phút để tải SDK

---

## 🔧 BUILD ANDROID APP

### **Bước 1: Mở Project**

1. Mở Android Studio
2. Click "Open an existing Android Studio project"
3. Chọn folder: `D:\Nhà máy sản xuất app\Chỉnh sửa Video\frontend\android`
4. Click "OK"

**Chờ Gradle sync (khoảng 2-3 phút)**

---

### **Bước 2: Build Signed APK**

**Menu trên cùng:**
1. Click **"Build"** → **"Build Bundle(s) / APK(s)"** → **"Build APK(s)"**

**Hoặc nếu muốn signed APK:**
1. Click **"Build"** → **"Generate Signed Bundle/APK"**
2. Chọn **"APK"** (không chọn Bundle)
3. Click "Create new..."

---

### **Bước 3: Tạo Signing Key**

**Dialog "New Key Store":**

| Field | Giá trị |
|-------|--------|
| Key Store Path | Để mặc định (sẽ lưu ở desktop) |
| Password | `daiminh2024` |
| Confirm | `daiminh2024` |
| Key Alias | `daiminh` |
| Password | `daiminh2024` |
| Confirm | `daiminh2024` |
| First and Last Name | `DaiMinh` |
| Organizational Unit | `DaiMinh` |
| Organization | `DaiMinh` |
| City or Locality | `HaNoi` |
| State or Province | `HaNoi` |
| Country Code | `VN` |

**Nhấn "OK"**

---

### **Bước 4: Build APK**

**Dialog "Generate Signed APK":**
- Build Variant: Chọn **"release"**
- Destination folder: Để mặc định
- Click **"Finish"**

**Chờ build hoàn thành (khoảng 1-2 phút)**

✅ **APK file sẽ được tạo ở:**
```
D:\Nhà máy sản xuất app\Chỉnh sửa Video\frontend\android\app\release\app-release.apk
```

---

## 🚀 UPLOAD LÊN GOOGLE PLAY

### **Bước 1: Tạo Google Play Account**

1. Vào https://play.google.com/console
2. Login bằng Google account
3. Click "Create app"
4. Nhập tên: **"DaiMinh AI Video Studio"**
5. Chọn category: **"Productivity" hoặc "Video Editors"**
6. Click "Create app"

**Lần đầu cần trả phí $25** (một lần)

---

### **Bước 2: Upload APK**

**Bên trái menu:**
1. Click **"Releases"** → **"Production"**
2. Click **"Create new release"**
3. Chọn APK file: `app-release.apk` (từ bước trên)
4. Click "Review release"

---

### **Bước 3: Điền Thông Tin App**

**Phía trái:**

**1. App content (Nội dung app)**
- Content rating: Chọn phù hợp
- Target audience: Chọn phù hợp

**2. Pricing & distribution (Giá & Phân phối)**
- Countries: Chọn các nước muốn phát hành
- Free/Paid: Chọn "Free"

**3. Screenshots & Images**
- Upload ít nhất 2 screenshots
- Upload app icon (512x512px)
- Upload feature graphic (1024x500px)

**4. Store listing**
- App name: "DaiMinh AI Video Studio"
- Short description: "Professional video editing for everyone"
- Full description: Viết mô tả chi tiết
- Privacy policy URL: (nếu có)

---

### **Bước 4: Submit**

1. Quay lại **"Releases"** → **"Production"**
2. Click **"Review release"**
3. Xem lại thông tin
4. Click **"Start rollout to Production"**

✅ **XONG!**

App sẽ được duyệt trong **2-4 giờ** thường là instant.

---

## 📊 KIỂM TRA BUILD

### **Test APK trên điện thoại:**

1. Connect Android phone qua USB
2. Bật "Developer Mode" (Settings → About → tap Build Number 7 lần)
3. Bật "USB Debugging"
4. Mở Android Studio
5. Click "Run" → Chọn device
6. App sẽ cài và chạy trên điện thoại

---

## 🆘 TROUBLESHOOTING

### **Build fails?**
```
Bước 1: File → Invalidate Caches → Restart
Bước 2: Build → Clean Project
Bước 3: Build → Rebuild Project
```

### **Cannot find SDK?**
```
File → Project Structure → SDK Location
Chọn SDK folder (thường: C:\Users\YOUR_NAME\AppData\Local\Android\Sdk)
```

### **Gradle sync failed?**
```
File → Settings → Gradle
Chọn: Use local gradle distribution
Đảm bảo Gradle path đúng
```

---

## ✨ TÓẠT CẢ XONG!

| Bước | Status |
|------|--------|
| Build web app | ✅ EM LÀM |
| Setup Capacitor | ✅ EM LÀM |
| Setup Android | ✅ EM LÀM |
| Build APK | 🔜 ANH LÀM (dễ - 10 phút) |
| Upload Google Play | 🔜 ANH LÀM (dễ - 10 phút) |

**Tổng cộng:** Anh chỉ cần 20 phút để build + upload!

---

**Khi cần giúp, hãy nhắn tin cho em!** 💪
