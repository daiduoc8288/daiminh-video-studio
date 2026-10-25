# 📱 Build Android APK - DaiMinh Video App

**Status:** Capacitor project ready ✅
**Need:** Android SDK to build APK

---

## **Option 1: Install Android Studio (20 min)**

1. **Download Android Studio**
   - https://developer.android.com/studio
   
2. **Install**
   - Open Android Studio
   - Follow setup wizard
   - Install Android SDK (API 34+)
   
3. **Build APK**
   ```bash
   cd "D:\Nhà máy sản xuất app\Chỉnh sửa Video\frontend-mobile"
   npx cap build android
   ```

4. **Find APK**
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

---

## **Option 2: Use Fiverr (5 min payment)**

Pay someone to build APK:
- Upload `frontend-mobile` folder
- They build APK
- Cost: ~$20-50

---

## **Option 3: Use Expo (easiest)**

```bash
npm install -g eas-cli
cd frontend-mobile
eas build --platform android
```

---

## **For iOS:**
- Requires **Mac** (cannot build on Windows)
- Either:
  - Use Mac to build
  - Pay Fiverr for iOS build
  - Use EAS (online service)

---

**Which option anh prefer?** 🚀
