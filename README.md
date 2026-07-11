# Webot Agentligi — Telegram Bot

Bu bot [webot-agenligi.netlify.app](https://webot-agenligi.netlify.app/) saytidagi xizmatlar va narxlarni
Telegram orqali ko'rsatadi hamda foydalanuvchidan buyurtma (ism + telefon) qabul qilib,
admin akkauntga (`7450764374`) yuboradi.

## 📁 Loyiha tuzilishi

```
webot_bot/
├── main.py            # botni ishga tushiruvchi asosiy fayl (polling + health-check server)
├── config.py           # token va admin ID .env orqali o'qiladi
├── data.py             # xizmatlar va narxlar (saytdagi bilan bir xil)
├── keyboards.py         # inline/reply klaviaturalar
├── handlers.py          # barcha buyruq va tugma logikasi + buyurtma FSM
├── requirements.txt
├── render.yaml          # Render.com uchun tayyor konfiguratsiya
├── .env.example
└── .gitignore
```

## 1️⃣ Bot tokenini olish

1. Telegramda [@BotFather](https://t.me/BotFather) ga o'ting.
2. `/newbot` buyrug'ini yuboring, bot nomi va username bering.
3. BotFather sizga token beradi, masalan: `123456789:AAExampleToken...`
4. Bu tokenni saqlab qo'ying — keyingi qadamlarda kerak bo'ladi.

## 2️⃣ Lokal test qilish (ixtiyoriy)

```bash
git clone <sizning-repo-url>
cd webot_bot
python -m venv venv
source venv/bin/activate   # Windowsda: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env faylini ochib, BOT_TOKEN qiymatini haqiqiy tokenga almashtiring
python main.py
```

Agar hammasi to'g'ri bo'lsa, konsolda `Bot polling rejimida ishga tushdi...` deb chiqadi.
Botga Telegramda `/start` yuboring.

## 3️⃣ GitHub'ga joylash

```bash
cd webot_bot
git init
git add .
git commit -m "Webot telegram bot"
git branch -M main
git remote add origin https://github.com/<username>/<repo-nomi>.git
git push -u origin main
```

⚠️ `.env` fayli `.gitignore` orqali yashiringan — tokeningiz GitHub'ga tushmaydi. Bu xavfsizlik uchun muhim.

## 4️⃣ Render.com'da deploy qilish (Web Service, polling + health-check)

⚠️ **Muhim:** Render'ning bepul tarifida Background Worker mavjud emas — u faqat pullik tarifda ochiladi.
Shuning uchun botni **Web Service** sifatida joylaymiz: bot Telegram'dan xabarlarni **polling** orqali
o'qiydi, shu bilan birga kichik bir HTTP server (`/healthz`) ham ishlab turadi — Render buni "tirik"
xizmat deb hisoblaydi.

1. [render.com](https://render.com) ga kiring, ro'yxatdan o'ting/kiring.
2. **New +** → **Web Service** ni tanlang.
3. GitHub repongizni ulang.
4. Render `render.yaml` faylini avtomatik topadi va sozlamalarni taklif qiladi:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Health Check Path:** `/healthz`
5. **Environment Variables** bo'limida quyidagilarni kiriting:
   - `BOT_TOKEN` — BotFather'dan olgan haqiqiy tokeningiz
   - `ADMIN_CHAT_ID` — `7450764374` (allaqachon `render.yaml`da bor, lekin tekshirib qo'ying)
6. **Create Web Service** tugmasini bosing.
7. Render loyihani build qilib, ishga tushiradi. Loglar bo'limida
   `Bot polling rejimida ishga tushdi...` va `Health-check server ...portda ishga tushdi` yozuvlarini ko'rasiz.
8. Deploy tugagach, Render sizga bitta manzil beradi, masalan:
   `https://webot-telegram-bot.onrender.com`

## 5️⃣ UptimeRobot bilan botni "uxlab qolishdan" saqlash

Render'ning bepul Web Service'lari **15 daqiqa** harakatsizlikdan keyin uxlab qoladi. Buning oldini olish uchun:

1. [uptimerobot.com](https://uptimerobot.com) ga kiring, bepul ro'yxatdan o'ting.
2. **+ Add New Monitor** tugmasini bosing.
3. Sozlamalar:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Webot Bot
   - **URL:** `https://<sizning-render-manzilingiz>.onrender.com/healthz`
   - **Monitoring Interval:** 5 daqiqa (bepul tarifdagi eng qisqa interval)
4. **Create Monitor** tugmasini bosing.

✅ Shu bilan UptimeRobot har 5 daqiqada botingizga "ping" yuborib turadi, Render esa doimiy faoliyat
deb hisoblab, bot va uning polling jarayonini uxlatib qo'ymaydi. Natijada bot deyarli 24/7 ishlaydi —
va bu **pullik hech qanday tarifsiz**, faqat ozgina "hiyla" orqali amalga oshiriladi.

> 💡 Eslatma: bu — rasman Render tomonidan tasdiqlangan usul emas, ko'plab dasturchilar
> qo'llaydigan keng tarqalgan workaround. Agar loyiha jiddiylashsa (masalan, mijozlaringiz ko'payib,
> uzilishlarga toqat qilib bo'lmasa), Render'ning pullik Starter tarifiga (~$7/oy) o'tish tavsiya etiladi —
> u holda uxlab qolish muammosi umuman bo'lmaydi.

## 🤖 Bot qanday ishlaydi

- `/start` — asosiy menyu (Narxlar, Aloqa)
- **Narxlar** → Veb-sayt narxlari / Bot narxlari → 3 ta tarif (Boshlang'ich, Biznes ⭐, Premium)
- Har bir tarif tafsilotlari ko'rsatiladi + **"Buyurtma berish"** tugmasi
- Tugma bosilganda: ism → telefon raqam (tugma orqali yoki qo'lda) so'raladi
- To'ldirilgach, buyurtma sizning shaxsiy Telegram akkauntingizga (ID: `7450764374`) yuboriladi
- Foydalanuvchiga "Buyurtmangiz qabul qilindi" xabari ko'rsatiladi

## ✏️ Narxlarni keyinchalik o'zgartirish

Barcha xizmat, tarif va narxlar `data.py` faylida — shu faylni tahrirlab, sayt bilan
sinxronlab turishingiz mumkin.
