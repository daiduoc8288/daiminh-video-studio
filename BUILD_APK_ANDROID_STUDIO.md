# 📱 Hướng dẫn Build APK bằng Android Studio

## **Bước 1: Tải Android Studio (FREE)**

👉 https://developer.android.com/studio

Chọn phiên bản Windows, tải về.

---

## **Bước 2: Cài đặt Android Studio**

1. Chạy file .exe tải về
2. Chọn "Next" -> "Next" cho đến xong
3. **Chọn "Android SDK"** khi hỏi
4. Chờ tải SDK (1-2 GB, 10-15 phút)

---

## **Bước 3: Mở project Android**

1. Mở Android Studio
2. Click **"Open"**
3. Chọn thư mục: 
   ```
   D:\Nhà máy sản xuất app\Chỉnh sửa Video\frontend-mobile\android
   ```
4. Chờ Gradle sync (lần đầu tốn 5-10 phút)

---

## **Bước 4: Build APK**

1. Trong Android Studio, click menu **"Build"**
2. Chọn **"Build Bundle(s) / APK(s)"**
3. Chọn **"Build APK(s)"**
4. Chờ build (3-5 phút)

---

## **Bước 5: Lấy APK**

Khi build xong, thư mục APK ở:
```
D:\Nhà máy sản xuất app\Chỉnh sửa Video\frontend-mobile\android\app\build\outputs\apk\debug\app-debug.apk
```

**File này chính là Android app anh!** 📦

---

## **Bước 6: Cài APK vào điện thoại**

1. **Kết nối điện thoại** vào máy tính qua USB
2. Copy file `app-debug.apk` vào điện thoại
3. Trên điện thoại, mở file APK
4. Chọn **"Cài đặt"**

Xong! App chạy trên điện thoại 🎉

---

## **Nếu gặp lỗi:**

❌ **"Gradle sync failed"**
- Chờ Android Studio tải xong SDK
- Restart Android Studio

❌ **"Build failed"**
- Đóng Android Studio
- Xóa thư mục: `android/.gradle`
- Mở lại Android Studio

❌ **"Cannot connect device"**
- Bật USB debugging trên điện thoại
  - Settings > Developer Options > USB Debugging

---

## **Chỉ cần làm 1 lần:**
Lần đầu tốn 20-30 phút (cài SDK).
Lần sau chỉ 5 phút (build APK).

**Đơn giản không?** 🚀
