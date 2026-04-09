# 🤖 Trading Mindset Bot

Bot Telegram motivasi harian menuju Rp 1 Miliar.

## Jadwal Notifikasi (WIB)
| Waktu | Sesi | Konten |
|-------|------|--------|
| 06:00 | Pagi | Mindset awal hari |
| 10:00 | Siang | Pengingat fokus & istirahat |
| 14:00 | Sore | Pre-session preparation |
| 20:00 | Pre-session | 30 menit sebelum NY session |
| 23:00 | Malam | Evaluasi & istirahat |

## Commands
- `/start` — Aktifkan bot & lihat info
- `/test` — Coba pesan random sekarang
- `/progress` — Lihat progress menuju Rp 1M

## Setup

### 1. Buat Bot Telegram
1. Chat @BotFather di Telegram
2. Ketik `/newbot`
3. Ikuti instruksi, simpan **BOT_TOKEN**
4. Chat bot kamu, lalu buka:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Ambil **chat.id** dari response JSON = **CHAT_ID**

### 2. Deploy ke Railway (gratis)
1. Buat akun di https://railway.app
2. New Project → Deploy from GitHub
3. Upload folder ini ke GitHub dulu
4. Di Railway → Variables → tambahkan:
   - `BOT_TOKEN` = token dari BotFather
   - `CHAT_ID` = chat ID kamu
5. Deploy → selesai, bot jalan 24 jam!

### 3. Test lokal
```bash
pip install -r requirements.txt
export BOT_TOKEN="token_kamu"
export CHAT_ID="chat_id_kamu"
python bot.py
```
