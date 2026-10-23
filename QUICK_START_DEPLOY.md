# 🚀 QUICK START - Đóng Gói & Deploy DaiMinh

## ⚡ 5 Phút - Deploy Web App Ngay

### Cách 1: Vercel (DỄ NHẤT - Khuyến Nghị)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy
cd frontend
vercel --prod

# XONG! App live ở: https://daiminh.vercel.app
```

**Lợi ích:**
- ✅ Deploy 1 command
- ✅ Miễn phí
- ✅ Auto HTTPS
- ✅ Global CDN
- ✅ Custom domain

---

## 🐳 Docker - Deploy Anywhere

```bash
# Build Docker image
docker build -f Dockerfile.prod -t daiminh:1.0 .

# Run locally để test
docker run -p 3000:3000 daiminh:1.0

# Deploy to your server/cloud:
# 1. Push image to Docker Hub / AWS ECR / etc
# 2. Pull on your server
# 3. docker run -p 3000:3000 daiminh:1.0
```

---

## 📱 Mobile App - Capacitor Setup

### iOS + Android (Trên Mac)

```bash
cd frontend

# 1. Build web
npm run build

# 2. Setup Capacitor
npm install @capacitor/core @capacitor/cli
npm install @capacitor/ios @capacitor/android
npx cap init "DaiMinh" "com.daiminh.video"

# 3. Build iOS
npx cap add ios
npx cap copy ios
npx cap open ios
# → Xcode opens → Product → Archive → Upload to App Store

# 4. Build Android
npx cap add android
npx cap copy android
npx cap open android
# → Android Studio opens → Build → Upload to Google Play
```

### Android (Trên Linux/Windows)

```bash
cd frontend

# 1. Setup
npm run build
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "DaiMinh" "com.daiminh.video"
npx cap add android

# 2. Build APK
npx cap open android
# → Android Studio → Build → Generate Signed Bundle/APK

# 3. Upload to Google Play
# → Google Play Console → Upload AAB file
```

---

## 📋 Deployment Checklist

### Before Deploy (5 mins)
- [ ] `npm run build` succeeds
- [ ] No TypeScript errors
- [ ] Environment variables set
- [ ] Images optimized

### During Deploy (varies by method)
- [ ] Vercel: `vercel --prod`
- [ ] Docker: build & push
- [ ] App Store: upload archive
- [ ] Google Play: upload AAB

### After Deploy (10 mins)
- [ ] Test production URL
- [ ] Check all pages load
- [ ] Forms work correctly
- [ ] No 404 errors

---

## 🌍 Custom Domain Setup

### On Vercel
1. Go to Vercel dashboard
2. Settings → Domains
3. Add custom domain
4. Follow DNS instructions
5. Done! HTTPS automatic

### On Your Server
```bash
# Get SSL cert (free with Let's Encrypt)
sudo apt install certbot nginx

# Get cert
sudo certbot certonly --standalone -d yourdomain.com

# Configure Nginx (see nginx.prod.conf)
# Restart Nginx

sudo systemctl restart nginx
```

---

## 📊 Monitoring After Deploy

### Vercel
- Dashboard shows: Deployments, Analytics, Real-time logs

### Docker / Self-hosted
```bash
# View logs
docker logs daiminh-frontend-prod

# Monitor resources
docker stats daiminh-frontend-prod

# Check health
curl http://localhost:3000
```

---

## 🔄 Update Strategy

### Deploy New Version
```bash
# 1. Update code
git add .
git commit -m "v1.0.1: Bug fixes"

# 2. Deploy (Vercel auto-deploys from main)
# Or manually:
vercel --prod

# 3. Monitor for 1 hour
# 4. Rollback if needed:
vercel rollback
```

---

## 💰 Estimated Costs (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| **Vercel** | Free - $20 | Free tier enough for startup |
| **Domain** | $10-15 | namecheap.com, godaddy.com |
| **SSL** | Free | Included with Vercel |
| **PostgreSQL** | $10-50 | Managed: Railway, Render, etc |
| **Redis** | $0-10 | Free or managed option |
| **MinIO Storage** | Variable | Self-hosted or AWS S3 |
| **Monitoring** | $0-50 | Free: Sentry, Datadog trial |
| **Total** | **$20-145** | Depends on scale |

---

## 🎯 Recommended Path

### For MVP (Just launched)
1. ✅ **Vercel** - Deploy web app (FREE)
2. ✅ **GitHub** - Store code (FREE)
3. ✅ **Railway/Render** - Backend API ($10-30)
4. ✅ **Capacitor** - Build iOS/Android app locally

### For Scaling (Growth phase)
1. Docker + own server
2. Database managed service (Supabase, PlanetScale)
3. CDN (Cloudflare)
4. CI/CD (GitHub Actions)

---

## 📞 Need Help?

### Troubleshooting

**App won't build:**
```bash
# Clear cache & reinstall
rm -rf node_modules .next
npm install
npm run build
```

**Deploy fails:**
```bash
# Check environment variables
# Check build logs in Vercel/Docker
# Run locally first: npm run dev
```

**Mobile app crashes:**
- Check Android logcat: `adb logcat`
- Check iOS console: Xcode → Console
- Enable debug mode in Capacitor

---

## 🎉 Success Checklist

After deploy, confirm:
- [ ] ✅ Web app accessible
- [ ] ✅ All pages load
- [ ] ✅ API endpoints work
- [ ] ✅ Database connected
- [ ] ✅ Images loading
- [ ] ✅ No console errors
- [ ] ✅ Mobile responsive
- [ ] ✅ iOS app in App Store
- [ ] ✅ Android app in Google Play
- [ ] ✅ Custom domain working

---

## 📈 Next Steps

1. **Week 1:** Monitor production
2. **Week 2:** Gather user feedback
3. **Week 3:** Plan v1.0.1 fixes
4. **Week 4:** Plan v1.1.0 features

**Chúc mừng anh đã launch! 🚀**
