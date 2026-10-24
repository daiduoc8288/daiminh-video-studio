# 🌐 SETUP DNS SUBDOMAIN - video.daiminh365.vn

**Anh cần làm những bước này để web app chạy ở video.daiminh365.vn**

---

## 📋 HƯỚNG DẪN CHI TIẾT (5 PHÚT)

### **Bước 1: Vào Matbao Dashboard**
1. Vào https://manage.matbao.net/ (anh đã mở rồi)
2. Login bằng tài khoản anh

---

### **Bước 2: Tìm mục Quản Lý Tên Miền**

**Bên menu trái, tìm và click:**
- Tìm icon "🌐 Tên miền" hoặc "Domain" 
- Hoặc tìm "Quản lý tên miền"

---

### **Bước 3: Chọn Domain daiminh365.vn**

1. Tìm **daiminh365.vn** trong danh sách
2. Click vào nó để vào chi tiết domain
3. Tìm tab **"DNS"** hoặc **"Nameserver"**

---

### **Bước 4: Thêm CNAME Record**

**Click nút "Thêm Record" hoặc "Add DNS Record"**

**Nhập thông tin:**
- **Type:** CNAME
- **Name/Subdomain:** video
- **Value/Points to:** cname.vercel-dns.com
- **TTL:** 3600 (hoặc để mặc định)

**Sau đó:**
- Click "Lưu" hoặc "Save"
- Chờ 5-10 phút để DNS cập nhật

---

### **Bước 5: Deploy Web App lên Vercel**

**Nếu chưa deploy:**

1. Vào https://vercel.com
2. Click "New Project"
3. Import GitHub repo của anh (hoặc upload code)
4. Click "Deploy"
5. Vercel sẽ cho URL (ví dụ: daiminh.vercel.app)

**Sau đó, vào Project Settings → Domains**
- Thêm custom domain: **video.daiminh365.vn**
- Vercel sẽ cho DNS instructions
- HTTPS tự động

---

## ✅ XONG!

**Bây giờ:**
- Web app sẽ chạy ở: **https://video.daiminh365.vn** ✨

---

## 🆘 NẾU CÓ VẤN ĐỀ

### DNS không cập nhật?
- Chờ 10-15 phút (DNS cập nhật chậm)
- Hoặc clear browser cache (Ctrl+Shift+Delete)

### Không tìm thấy tab DNS?
- Vào "Quản lý DNS" từ menu
- Hoặc click "Manage DNS" button

### Muốn kiểm tra DNS?
```
Vào: https://dnschecker.org
Nhập: video.daiminh365.vn
Nên thấy: cname.vercel-dns.com
```

---

**Em đã chuẩn bị mọi thứ. Anh chỉ cần làm 5 bước này!** 🚀
