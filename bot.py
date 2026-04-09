#!/usr/bin/env python3
"""
Trading Mindset Bot v7 — AI-powered
Konten dinamis dari Claude API setiap pengiriman
"""

import os, random, logging, json
import httpx
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Bot
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN    = os.environ.get("BOT_TOKEN",    "8626750521:AAFlZjiXQCrcb-p13S8HRuv-qVhqn7etLv0")
CHAT_ID      = os.environ.get("CHAT_ID",      "5488406480")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY", "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")
WIB          = ZoneInfo("Asia/Jakarta")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

# ── Konteks trading plan — dikirim ke Claude setiap request ──────────────────
TRADING_CONTEXT = """
Kamu adalah trading coach personal untuk seorang trader XAUUSD Indonesia.

Profil trader:
- Pair: XAUUSD (Gold vs USD)
- Session: NY Session (20:30–22:30 WIB)
- Balance saat ini: Rp 311.300.000
- Target: Rp 1 Miliar (Oktober 2026)
- Win Rate Maret 2026: 35.3%
- Profit Factor Maret 2026: 2.60
- P&L Maret: +Rp 11.300.000
- RR Target: 1:4
- TP: Fibonacci 1.618
- SL: 25–30 pip
- Max trade per malam: 2
- Risk per trade: Rp 500rb (1-11 Apr) → Rp 1jt (12 Apr+)
- Tujuan: Umroh untuk 4 orang (orang tua & mertua)

Pelajaran penting Maret:
- Rabu: hindari karena Crude Oil Report
- Jumat: WR terbaik ~62.5%
- Overtrading terjadi 23 Maret & 1 April — jadi pelajaran besar
- DST aktif: NY session jam 20:30 WIB

Drawdown framework:
- -5%: review
- -10%: kurangi size 50%
- -15%: stop 3 hari
- -20%: stop 1 minggu

Tulis dalam Bahasa Indonesia yang personal, hangat, dan memotivasi.
Gunakan kata "kamu" bukan nama orang.
Gunakan emoji secukupnya.
Format Telegram Markdown (bold dengan *teks*, italic dengan _teks_).
Jangan terlalu panjang — maksimal 200 kata.
"""

SESI_PROMPT = {
    "pagi": "Buat pesan motivasi pagi hari untuk trader ini. Fokus pada mindset positif, semangat memulai hari, dan pengingat tujuan Umroh. Sertakan satu insight tentang trading plan-nya.",

    "quotes": "Buat satu quotes inspiratif tentang trading (bisa dari tokoh terkenal atau original) lalu hubungkan langsung dengan situasi trader ini — WR 35.3%, PF 2.60, target Rp 1M. Topik boleh: risk management, compounding, disiplin, atau mindset.",

    "quotes2": "Buat konten motivasi siang hari tentang salah satu topik ini (pilih random): disiplin trading, manajemen emosi, pentingnya jurnal trading, atau cara menghadapi loss streak. Hubungkan dengan data nyata trader ini.",

    "statistik": """Buat visualisasi statistik atau simulasi angka yang menarik dan relevan untuk trader ini. 
Pilih salah satu (random):
- Simulasi compound 5%/bulan dari Rp 311jt
- Analisis probabilitas loss streak dengan WR 35.3%
- Perbandingan RR 1:4 vs RR 1:1 dalam jangka panjang
- Progress bar menuju Rp 1 Miliar
- Dampak 1 overtrading terhadap compound bulanan
- Statistik per hari (Rabu vs Jumat)
Sajikan dengan angka nyata dan insight yang actionable.""",

    "malam": "Buat pesan evaluasi malam yang reflektif dan menenangkan. Ingatkan untuk jurnal, syukuri proses hari ini, dan motivasi untuk istirahat yang baik. Sertakan pengingat tentang Umroh keluarga.",
}

# ── Fallback pesan jika API gagal ────────────────────────────────────────────
FALLBACK = {
    "pagi": "🌅 *Selamat pagi!*\n\nHari baru, kesempatan baru untuk konsisten.\nSistem sudah terbukti (PF 2.60) — tinggal dijalankan.\n\n🕌 _Umroh 4 orang menunggu di Oktober 2026._",
    "quotes": "💡 *Quote Hari Ini*\n\n_\"The goal is not to be right — the goal is to make money.\"_\n\nDengan RR 1:4, kamu tidak perlu sering benar. Cukup konsisten.",
    "quotes2": "🧠 *Mindset*\n\n_\"Disiplin adalah jembatan antara goal dan pencapaian.\"_\n\nRp 1 Miliar dicapai satu malam konsisten dalam satu waktu.",
    "statistik": "📊 *Statistik*\n\nBalance: Rp 311.3jt → Target: Rp 1M\nCompound 5%/bulan → Oktober 2026 ✅\nWR 35.3% + PF 2.60 = Sistem yang profitable\n\n_Modal dijaga = compound bekerja._",
    "malam": "🌙 *Selamat malam.*\n\nApapun yang terjadi malam ini — kalau plan diikuti, itu sudah kemenangan.\n\nIstirahat yang baik. Besok kita mulai lagi.\n\n🕌 _Umroh keluarga semakin dekat._",
}

# ── Generate konten dari Claude API ──────────────────────────────────────────
async def generate_konten(sesi: str) -> str:
    prompt = SESI_PROMPT.get(sesi, SESI_PROMPT["quotes"])
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 400,
                    "system": TRADING_CONTEXT,
                    "messages": [{"role": "user", "content": prompt}],
                }
            )
            data = response.json()
            if response.status_code == 200:
                teks = data["content"][0]["text"].strip()
                log.info(f"✅ Claude API OK [{sesi}] — {len(teks)} chars")
                return teks
            else:
                log.error(f"❌ Claude API error: {data}")
                return FALLBACK.get(sesi, FALLBACK["quotes"])
    except Exception as e:
        log.error(f"❌ Claude API exception: {e}")
        return FALLBACK.get(sesi, FALLBACK["quotes"])

# ── Footer ────────────────────────────────────────────────────────────────────
def get_footer():
    now  = datetime.now(WIB)
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()]
    return f"\n\n─────────────────\n📅 {hari}, {now.strftime('%d %b %Y')} | ⏰ {now.strftime('%H:%M')} WIB"

# ── Kirim pesan ───────────────────────────────────────────────────────────────
async def kirim(bot: Bot, sesi: str):
    teks = await generate_konten(sesi)
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=teks + get_footer(),
            parse_mode="Markdown"
        )
        log.info(f"✅ [{sesi}] terkirim")
    except Exception as e:
        # Kalau Markdown error, kirim plain text
        try:
            await bot.send_message(chat_id=CHAT_ID, text=teks + get_footer())
            log.info(f"✅ [{sesi}] terkirim (plain)")
        except Exception as e2:
            log.error(f"❌ [{sesi}] gagal: {e2}")

# ── Scheduler jobs ────────────────────────────────────────────────────────────
async def job_pagi(bot):      await kirim(bot, "pagi")
async def job_quotes(bot):    await kirim(bot, "quotes")
async def job_quotes2(bot):   await kirim(bot, "quotes2")
async def job_statistik(bot): await kirim(bot, "statistik")
async def job_malam(bot):     await kirim(bot, "malam")

# ── Commands ──────────────────────────────────────────────────────────────────
async def cmd_start(update, context):
    await update.message.reply_text(
        "🤖 *Trading Mindset Bot* — AI Powered!\n\n"
        "Konten dibuat oleh Claude AI setiap pengiriman — tidak pernah sama!\n\n"
        "📅 *Jadwal harian (WIB):*\n"
        "• 06:00 — Motivasi & mindset pagi\n"
        "• 10:00 — Quotes trading (AI generated)\n"
        "• 14:00 — Mindset & disiplin (AI generated)\n"
        "• 20:00 — Statistik & angka (AI generated)\n"
        "• 22:00 — Evaluasi & renungan malam\n\n"
        "📌 *Commands:*\n"
        "/quote — Quotes AI random sekarang\n"
        "/risk — Quotes risk management\n"
        "/compound — Simulasi compound\n"
        "/mindset — Quotes mindset\n"
        "/statistik — Statistik & angka\n"
        "/plan — Trading plan lengkap\n"
        "/progress — Progress Rp 1M\n"
        "/test — Pesan AI random sekarang\n\n"
        "🎯 *Target: Rp 1 Miliar — Oktober 2026*\n"
        "🕌 Umroh untuk 4 orang keluarga",
        parse_mode="Markdown"
    )

async def cmd_test(update, context):
    await update.message.reply_text("⏳ Generating dari Claude AI...")
    sesi = random.choice(["pagi", "quotes", "quotes2", "statistik", "malam"])
    teks = await generate_konten(sesi)
    try:
        await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")
    except:
        await update.message.reply_text(teks + get_footer())

async def cmd_quote(update, context):
    await update.message.reply_text("⏳ Generating...")
    teks = await generate_konten("quotes")
    try:
        await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")
    except:
        await update.message.reply_text(teks + get_footer())

async def cmd_risk(update, context):
    await update.message.reply_text("⏳ Generating...")
    prompt_risk = "Buat quotes atau insight mendalam tentang risk management trading untuk trader ini. Hubungkan dengan SL 25-30 pip, RR 1:4, dan drawdown framework yang sudah ditetapkan."
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                json={"model": "claude-haiku-4-5-20251001", "max_tokens": 400, "system": TRADING_CONTEXT, "messages": [{"role": "user", "content": prompt_risk}]}
            )
            teks = response.json()["content"][0]["text"].strip()
    except:
        teks = FALLBACK["quotes"]
    try:
        await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")
    except:
        await update.message.reply_text(teks + get_footer())

async def cmd_compound(update, context):
    bal, target, rate = 311_300_000, 1_000_000_000, 0.05
    rows, b = "", bal
    now = datetime.now(WIB)
    for i in range(1, 13):
        b *= (1 + rate)
        m   = (now.month - 1 + i) % 12 + 1
        y   = now.year + (now.month - 1 + i) // 12
        bln = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"][m-1]
        flag = " ✅" if b >= target else ""
        rows += f"• {bln} {y}: Rp {b:,.0f}{flag}\n"
        if b >= target: break
    teks = (f"🧮 *Simulasi Compound 5%/bulan*\n_(dari Rp {bal:,.0f})_\n\n{rows}\n"
            f"💡 Compound bekerja kalau modal dijaga.\n🛡️ Jaga drawdown = jaga compounding.")
    await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")

async def cmd_mindset(update, context):
    await update.message.reply_text("⏳ Generating...")
    teks = await generate_konten("quotes2")
    try:
        await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")
    except:
        await update.message.reply_text(teks + get_footer())

async def cmd_statistik(update, context):
    await update.message.reply_text("⏳ Generating...")
    teks = await generate_konten("statistik")
    try:
        await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")
    except:
        await update.message.reply_text(teks + get_footer())

async def cmd_plan(update, context):
    await update.message.reply_text(
        "📋 *Trading Plan — April 2026*\n\n"
        "⏰ *Session:* NY Session (20:30–22:30 WIB)\n"
        "💹 *Pair:* XAUUSD\n"
        "🎯 *TP:* Fibonacci 1.618\n"
        "🛡️ *SL:* 25–30 pip\n"
        "⚖️ *RR:* 1:4\n"
        "🔢 *Max trade:* 2 per malam\n\n"
        "💰 *Risk per trade:*\n"
        "• 1–11 Apr: Rp 500.000\n"
        "• 12–30 Apr: Rp 1.000.000\n\n"
        "📅 *Protokol hari:*\n"
        "• Rabu → hati-hati crude oil\n"
        "• Jumat → WR terbaik (~62.5%)\n\n"
        "⚠️ *Drawdown framework:*\n"
        "• -5%  → Review\n"
        "• -10% → Kurangi size 50%\n"
        "• -15% → Stop 3 hari\n"
        "• -20% → Stop 1 minggu\n\n"
        "📊 *Maret 2026:* WR 35.3% | PF 2.60 | +Rp 11.3jt",
        parse_mode="Markdown"
    )

async def cmd_progress(update, context):
    bal, target = 311_300_000, 1_000_000_000
    pct = bal / target * 100
    bar = "█" * int(pct/5) + "░" * (20 - int(pct/5))
    await update.message.reply_text(
        f"📊 *Progress Rp 1 Miliar*\n\n"
        f"💰 Sekarang : Rp {bal:,.0f}\n"
        f"🎯 Target   : Rp {target:,.0f}\n"
        f"📈 Progress : [{bar}] {pct:.1f}%\n\n"
        f"📅 Target   : Oktober 2026\n"
        f"⏳ Sisa     : ~6 bulan\n"
        f"📊 Butuh    : ~5%/bulan\n\n"
        f"🕌 *Umroh 4 orang — tetap di jalur!*",
        parse_mode="Markdown"
    )

# ── Scheduler ─────────────────────────────────────────────────────────────────
def setup_scheduler(app):
    bot = app.bot
    scheduler = AsyncIOScheduler(timezone=WIB)
    scheduler.add_job(job_pagi,      "cron", hour=6,  minute=0,  args=[bot], id="pagi")
    scheduler.add_job(job_quotes,    "cron", hour=10, minute=0,  args=[bot], id="quotes")
    scheduler.add_job(job_quotes2,   "cron", hour=14, minute=0,  args=[bot], id="quotes2")
    scheduler.add_job(job_statistik, "cron", hour=20, minute=0,  args=[bot], id="statistik")
    scheduler.add_job(job_malam,     "cron", hour=22, minute=0,  args=[bot], id="malam")
    scheduler.start()
    log.info("✅ Scheduler aktif — 5 sesi")
    return scheduler

def main():
    log.info("🚀 Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    for cmd, handler in [
        ("start",     cmd_start),
        ("test",      cmd_test),
        ("quote",     cmd_quote),
        ("risk",      cmd_risk),
        ("compound",  cmd_compound),
        ("mindset",   cmd_mindset),
        ("statistik", cmd_statistik),
        ("plan",      cmd_plan),
        ("progress",  cmd_progress),
    ]:
        app.add_handler(CommandHandler(cmd, handler))
    setup_scheduler(app)
    log.info("✅ Bot siap")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
