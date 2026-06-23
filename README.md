# 🛒 E-Shop - Django E-Commerce Loyihasi

## 📦 O'rnatish va Ishga Tushirish

### 1. Virtual muhit yarating
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 2. Kerakli kutubxonalarni o'rnating
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini tayyorlang
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Superuser yarating (admin panel uchun)
```bash
python manage.py createsuperuser
```

### 5. Serverni ishga tushiring
```bash
python manage.py runserver
```

### 6. Brauzerda oching
- **Bosh sahifa:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

---

## 📁 Loyiha Tuzilishi

```
ecommerce/
├── core/               # Asosiy konfiguratsiya
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/              # Foydalanuvchi ilovasi
│   ├── models.py       # User, Profile modellari
│   ├── views.py        # Login, Register, Profil
│   ├── forms.py
│   ├── urls.py
│   └── signals.py
├── products/           # Mahsulotlar ilovasi
│   ├── models.py       # Product, Category, Cart, Order
│   ├── views.py        # Savat, Buyurtma, Mahsulot
│   ├── urls.py
│   └── admin.py
├── templates/          # HTML shablonlar
│   ├── base.html
│   ├── users/
│   └── products/
├── static/
│   └── css/style.css
├── media/              # Yuklangan fayllar
├── requirements.txt
└── manage.py
```

---

## ✅ Funksiyalar

- 👤 **Foydalanuvchilar:** Ro'yxatdan o'tish, kirish, profil tahrirlash
- 🏪 **Mahsulotlar:** Kategoriyalar, qidirish, mahsulot sahifasi
- 🛒 **Savat:** Qo'shish, o'chirish, miqdor yangilash
- 📦 **Buyurtmalar:** Buyurtma berish, holat kuzatish
- 👨‍💼 **Admin panel:** Mahsulot, kategoriya, buyurtma boshqaruvi

---

## 🗄️ PostgreSQL ga o'tish (ixtiyoriy)

`core/settings.py` faylida SQLite ni izohga olib, PostgreSQL ni yoqing:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'postgres',
        'PASSWORD': 'sizning_parolingiz',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Keyin `pip install psycopg2-binary` o'rnating.
