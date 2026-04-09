#!/usr/bin/env python3
"""
Trading Mindset Bot
5x notifikasi harian otomatis + quotes trading
"""

import os, random, logging
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Bot
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ISI_TOKEN_BARU_DISINI")
CHAT_ID   = os.environ.get("CHAT_ID",   "5488406480")
WIB       = ZoneInfo("Asia/Jakarta")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# QUOTES BANK
# ═══════════════════════════════════════════════════════════════════════════════
QUOTES = {

  "risk_management": [
    "💡 *Risk Management*\n\n"
    "_\"The first rule of trading: never lose more than you planned to lose.\"_\n\n"
    "SL 25–30 pip sudah ditetapkan.\n"
    "Risk Rp 500rb–1jt per trade sudah dihitung.\n\n"
    "Aturan itu bukan batasan — itu *pelindung* menuju Rp 1 Miliar.",

    "🛡️ *Risk Management*\n\n"
    "_\"Amateurs focus on profits. Professionals focus on risk.\"_\n\n"
    "WR hanya 35.3%, tapi *Profit Factor 2.60.*\n\n"
    "Artinya risk management yang benar *mengalahkan* winrate tinggi.\n"
    "Sistem sudah terbukti. Percayai.",

    "⚖️ *Risk Management*\n\n"
    "_\"It's not about being right or wrong —_\n"
    "_it's about how much you make when right_\n"
    "_and how little you lose when wrong.\"_\n"
    "— George Soros\n\n"
    "RR 1:4 dengan Fibonacci 1.618.\n"
    "Setiap 1 loss = butuh 1 win untuk cover + profit.\n"
    "Sistem ini *bekerja.*",

    "🔐 *Risk Management*\n\n"
    "_\"Survival is the most important thing in trading._\n"
    "_You can't trade if you're out of capital.\"_\n\n"
    "Framework drawdown:\n"
    "• -5%  → Review\n"
    "• -10% → Kurangi size\n"
    "• -15% → Stop 3 hari\n"
    "• -20% → Stop 1 minggu\n\n"
    "Ini bukan kelemahan — ini *kecerdasan bisnis.*",

    "📉 *Risk Management*\n\n"
    "_\"The key to trading success is emotional discipline._\n"
    "_If intelligence were the key, there would be_\n"
    "_a lot more people making money.\"_\n"
    "— Victor Sperandeo\n\n"
    "IQ bukan penentu profit.\n"
    "Disiplin menjalankan plan adalah penentu profit.",
  ],

  "compounding": [
    "📈 *Compounding*\n\n"
    "_\"Compound interest is the eighth wonder of the world._\n"
    "_He who understands it, earns it._\n"
    "_He who doesn't, pays it.\"_\n"
    "— Albert Einstein\n\n"
    "Rp 311 juta + 5%/bulan × 6 bulan = *~Rp 417 juta*\n"
    "Rp 311 juta + 5%/bulan × 12 bulan = *~Rp 557 juta*\n\n"
    "Compound tidak butuh keajaiban — butuh *konsistensi.*",

    "🧮 *Compounding*\n\n"
    "Simulasi balance:\n\n"
    "Apr → Rp 327 juta\n"
    "Mei → Rp 343 juta\n"
    "Jun → Rp 360 juta\n"
    "Jul → Rp 378 juta\n"
    "Agu → Rp 397 juta\n"
    "Sep → Rp 417 juta\n"
    "Okt → *Rp 438 juta* 📈\n\n"
    "_(asumsi 5%/bulan)_\n\n"
    "Satu syarat: *modal tidak dirusak overtrading.*",

    "💰 *Compounding*\n\n"
    "_\"The stock market is a device for transferring money_\n"
    "_from the impatient to the patient.\"_\n"
    "— Warren Buffett\n\n"
    "Market mentransfer uang dari trader *impulsif*\n"
    "ke trader yang *sabar menunggu setup.*\n\n"
    "Kesabaranmu = profit jangka panjang.",

    "🌱 *Compounding*\n\n"
    "_\"Small consistent gains compound into massive wealth._\n"
    "_You don't need home runs — just don't strike out.\"_\n\n"
    "Profit Factor 2.60 di Maret adalah bukti:\n"
    "Tidak perlu win besar setiap malam.\n"
    "Cukup *konsisten, disiplin, dan jaga modal.*",

    "⏳ *Compounding*\n\n"
    "_\"Time in the market beats timing the market.\"_\n\n"
    "Untuk trader: *Konsistensi mengalahkan strategi sempurna.*\n\n"
    "Tidak perlu:\n"
    "❌ Setup sempurna setiap malam\n"
    "❌ Win setiap trade\n\n"
    "Hanya perlu:\n"
    "✅ Jalankan sistem\n"
    "✅ Jaga modal\n"
    "✅ Biarkan compound bekerja",
  ],

  "mindset": [
    "🧠 *Mindset*\n\n"
    "_\"The most important quality for an investor is temperament,_\n"
    "_not intellect.\"_\n"
    "— Warren Buffett\n\n"
    "Trader yang berhasil bukan yang paling pintar analisis.\n"
    "Tapi yang paling *stabil emosinya* saat market bergerak liar.",

    "💪 *Mindset*\n\n"
    "_\"The goal of a successful trader is to make the best trades._\n"
    "_Money is secondary.\"_\n"
    "— Alexander Elder\n\n"
    "Kalau malam ini skip karena tidak ada setup —\n"
    "itu adalah *trade terbaik* yang bisa dibuat.\n\n"
    "Uang mengikuti keputusan yang benar.",

    "🔥 *Mindset*\n\n"
    "_\"Trading is 10% strategy and 90% psychology.\"_\n\n"
    "Sistem XAUUSD sudah terbukti (PF 2.60).\n"
    "Strategi sudah 90% selesai.\n\n"
    "Yang menentukan Oktober 2026:\n"
    "Apakah *psikologi* bisa konsisten\n"
    "menjalankan sistem itu malam demi malam.",

    "🌟 *Mindset*\n\n"
    "_\"Every loss is a tuition fee for your trading education._\n"
    "_The question is: are you learning from it?\"_\n\n"
    "7 pelajaran Maret sudah didokumentasi.\n"
    "Overtrading sudah dianalisis.\n"
    "Protokol Rabu sudah ditetapkan.\n\n"
    "Sudah *belajar.* Sekarang saatnya *menerapkan.*",

    "⚡ *Mindset*\n\n"
    "_\"The market is not your enemy._\n"
    "_Your biggest enemy is yourself.\"_\n\n"
    "Musuh utama bukan:\n"
    "❌ Market yang sulit\n"
    "❌ Spread yang besar\n\n"
    "Musuh utama adalah:\n"
    "⚠️ FOMO\n"
    "⚠️ Revenge trade\n"
    "⚠️ Overtrading",
  ],

  "disiplin": [
    "📌 *Disiplin*\n\n"
    "_\"Discipline is the bridge between goals and accomplishment.\"_\n"
    "— Jim Rohn\n\n"
    "Goal: Rp 1 Miliar — Oktober 2026\n"
    "Accomplishment: Umroh untuk 4 orang keluarga\n\n"
    "Jembatan di antara keduanya:\n"
    "*Disiplin setiap malam, satu trade dalam satu waktu.*",

    "🎖️ *Disiplin*\n\n"
    "_\"The harder the conflict, the more glorious the triumph.\"_\n"
    "— Thomas Paine\n\n"
    "Malam yang skip saat tidak ada setup —\n"
    "Malam yang stop setelah 2 trade —\n"
    "Malam yang tahan dari revenge trade —\n\n"
    "Semua itu adalah *kemenangan yang tidak terlihat*\n"
    "yang membangun Rp 1 Miliar secara diam-diam.",

    "🔑 *Disiplin*\n\n"
    "_\"We are what we repeatedly do._\n"
    "_Excellence, then, is not an act, but a habit.\"_\n"
    "— Aristotle\n\n"
    "Bukan trader yang kadang-kadang disiplin.\n"
    "Tapi trader yang *terbiasa* disiplin.\n\n"
    "Setiap malam yang konsisten membangun identitas itu.\n"
    "Dan identitas itu yang menghasilkan *Rp 1 Miliar.*",

    "⏰ *Disiplin Waktu*\n\n"
    "_\"The secret of your future is hidden in your daily routine.\"_\n"
    "— Mike Murdock\n\n"
    "Rutinitas trading:\n"
    "• 20:00 — Siapkan chart XAUUSD\n"
    "• 20:30 — NY session buka, scan setup\n"
    "• 20:30–22:30 — Window trading\n"
    "• 22:30 — Tutup platform, jurnal\n\n"
    "*Rutinitas ini = sistem yang menghasilkan Rp 1 Miliar.*",
  ],

  "umroh": [
    "🕌 *Untuk Keluarga*\n\n"
    "Di balik setiap malam trading dengan disiplin —\n"
    "ada 4 orang yang belum tahu betapa kerasnya perjuangan ini.\n\n"
    "👴 Bapak\n"
    "👩 Ibu\n"
    "👴 Mertua laki-laki\n"
    "👩 Mertua perempuan\n\n"
    "Mereka akan tahu saat tiket Umroh itu ada di tangan mereka.\n\n"
    "_Setiap pip yang dijaga = selangkah lebih dekat ke momen itu._",

    "🌙 *Motivasi Terdalam*\n\n"
    "Rp 1 Miliar bukan sekadar angka.\n"
    "Itu adalah:\n\n"
    "🕌 Umroh untuk orang tua\n"
    "🕌 Umroh untuk mertua\n"
    "📈 Modal untuk masa depan keluarga\n\n"
    "_Bayangkan momen itu setiap kali ingin revenge trade._",

    "✨ *Visi Oktober 2026*\n\n"
    "Pertengahan 2026 — mulai withdrawal pertama.\n"
    "Bukan untuk dipakai sendiri.\n"
    "Tapi untuk ditabung ke dana Umroh.\n\n"
    "Setiap bulan, sedikit demi sedikit.\n"
    "Sampai 4 tiket Umroh itu terbeli.\n\n"
    "Dan semua ini dimulai dari *malam ini.*",
  ],
}

STATISTIK = [
    "📊 *Statistik Trading — Maret 2026*\n\n"
    "💰 P&L      : *+Rp 11.300.000*\n"
    "📈 Balance  : *Rp 311.300.000*\n"
    "🎯 Win Rate : *35.3%*\n"
    "⚖️ Profit Factor: *2.60*\n"
    "🔢 Max Trade/malam: *2*\n"
    "🛡️ SL       : *25–30 pip*\n"
    "🎯 RR       : *1:4*\n\n"
    "_Sistem ini sudah terbukti menghasilkan profit._\n"
    "_Tugas malam ini: jalankan dengan konsisten._",

    "🧮 *Simulasi Compound — 5%/bulan*\n\n"
    "Apr 2026 → Rp 327.000.000\n"
    "Mei 2026 → Rp 343.000.000\n"
    "Jun 2026 → Rp 360.000.000\n"
    "Jul 2026 → Rp 378.000.000\n"
    "Agu 2026 → Rp 397.000.000\n"
    "Sep 2026 → Rp 417.000.000\n"
    "Okt 2026 → *Rp 438.000.000* 📈\n\n"
    "_Satu syarat: modal tidak dirusak overtrading._",

    "📉 *Probabilitas Loss Streak*\n\n"
    "Dengan WR 35.3%:\n\n"
    "Loss 2x berturut → peluang *42%* — wajar\n"
    "Loss 3x berturut → peluang *27%* — masih normal\n"
    "Loss 4x berturut → peluang *17%* — evaluasi setup\n"
    "Loss 5x berturut → peluang *11%* — stop, review total\n\n"
    "_Loss streak bukan tanda sistem rusak._\n"
    "_Tanda sistem rusak: melanggar plan saat loss._",

    "📊 *WR vs Profit Factor — Perbandingan*\n\n"
    "WR 35% + PF 2.60 → *PROFITABLE* ✅\n"
    "WR 50% + PF 1.00 → Break even ⚠️\n"
    "WR 70% + PF 0.80 → *MERUGI* ❌\n\n"
    "*WR tinggi bukan jaminan profit.*\n"
    "*RR yang baik adalah kuncinya.*\n\n"
    "_RR 1:4 dengan SL 25–30 pip sudah tepat._",

    "🎯 *Progress Rp 1 Miliar*\n\n"
    "▓▓▓▓▓▓░░░░░░░░░░░░░░ 31.1%\n\n"
    "💰 Sekarang : Rp 311.300.000\n"
    "🎯 Target   : Rp 1.000.000.000\n"
    "📈 Sisa     : Rp 688.700.000\n"
    "⏳ Waktu    : ~6 bulan\n"
    "📊 Butuh    : ~5%/bulan\n\n"
    "_Setiap malam konsisten mengisi progress ini._\n"
    "🕌 _Umroh 4 orang menunggu di ujung perjalanan._",

    "⚡ *Risk Per Trade — Dampak ke Balance*\n\n"
    "Balance: Rp 311.300.000\n\n"
    "Fase 1 (s/d 11 Apr):\n"
    "Risk Rp 500rb = *0.16% balance* — sangat aman\n\n"
    "Fase 2 (12 Apr+):\n"
    "Risk Rp 1jt = *0.32% balance* — konservatif\n\n"
    "Drawdown -20% = Rp 62.260.000\n"
    "Butuh *62 loss berturut* untuk capai itu\n\n"
    "_Sistemnya sangat terlindungi._\n"
    "_Yang perlu dijaga: disiplin, bukan keberanian._",

    "📅 *Statistik Per Hari — Maret 2026*\n\n"
    "📅 Senin    : Normal\n"
    "📅 Selasa   : Normal\n"
    "⚠️ Rabu     : Hati-hati (Crude Oil Report)\n"
    "📅 Kamis    : Normal\n"
    "🏆 Jumat    : *WR ~62.5%* — hari terbaik\n\n"
    "_Data ini adalah edge yang nyata._\n"
    "_Maksimalkan Jumat. Hati-hati Rabu._",
]

PESAN = {
  "pagi": [
    "🌅 *Selamat pagi!*\n\n"
    "Balance: *Rp 311+ juta*\n"
    "Target: *Rp 1 Miliar — Oktober 2026*\n\n"
    "Hari baru. Kesempatan baru untuk konsisten.\n\n"
    "Ingat — bukan tentang berapa banyak trade hari ini.\n"
    "Tapi seberapa *benar* eksekusinya.\n\n"
    "🕌 _Umroh 4 orang menunggu di ujung perjalanan ini._",

    "☀️ *Pagi!*\n\n"
    "📊 *Fakta sistem trading kamu:*\n"
    "• WR 35.3% — sudah profitable\n"
    "• PF 2.60 — sangat sehat\n"
    "• RR 1:4 — asimetri yang kuat\n\n"
    "Dari 10 trade, *7 bisa loss* — tapi tetap profit.\n\n"
    "Sistem ini bekerja. Tugas hari ini:\n"
    "*Jangan ganggu yang sudah terbukti.*",

    "🌄 *Pagi — compound check:*\n\n"
    "Rp 311 juta × 5%/bulan:\n"
    "• Bulan 1 → Rp 327 juta\n"
    "• Bulan 3 → Rp 360 juta\n"
    "• Bulan 6 → Rp 417 juta\n\n"
    "Satu syarat: *modal tidak dirusak overtrading.*\n\n"
    "🔑 _Disiplin hari ini = compound bulan depan._",
  ],

  "malam": [
    "🌙 *Evaluasi malam:*\n\n"
    "Ambil 5 menit untuk jurnal:\n"
    "□ Berapa trade malam ini?\n"
    "□ Setup sesuai plan?\n"
    "□ Emosi terjaga?\n"
    "□ Apa yang bisa diperbaiki?\n\n"
    "📝 Satu kalimat di jurnal sudah cukup.\n\n"
    "🕌 _Selamat istirahat. Besok kita compound lagi._",

    "⭐ *Malam ini sudah:*\n\n"
    "✅ Satu hari lebih konsisten\n"
    "✅ Satu hari lebih dekat ke Rp 1M\n"
    "✅ Satu hari lebih dekat ke Umroh keluarga\n\n"
    "Profit → Syukuri.\n"
    "Loss → Evaluasi, bukan menyesal.\n"
    "Skip → *Keputusan terbaik jika tidak ada setup.*\n\n"
    "💪 _Besok pagi kita mulai lagi._",

    "🌟 *Renungan malam:*\n\n"
    "Modal aman malam ini?\n"
    "→ *Alhamdulillah. Compound masih bekerja.*\n\n"
    "Ikut plan malam ini?\n"
    "→ *Alhamdulillah. Sistem masih berjalan.*\n\n"
    "Tidak overtrading?\n"
    "→ *Alhamdulillah. Musuh terbesar sudah dikalahkan.*\n\n"
    "Profit itu bonus.\n"
    "*Disiplin itu tujuan sesungguhnya.*\n\n"
    "🕌 _Selamat malam._",
  ],
}

# ─────────────────────────────────────────────────────────────────────────────
def get_footer():
    now  = datetime.now(WIB)
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()]
    return f"\n\n─────────────────\n📅 {hari}, {now.strftime('%d %b %Y')} | ⏰ {now.strftime('%H:%M')} WIB"

def get_teks(sesi: str) -> str:
    if sesi in ["quotes", "quotes2"]:
        kategori = random.choice(list(QUOTES.keys()))
        return random.choice(QUOTES[kategori])
    elif sesi == "statistik":
        return random.choice(STATISTIK)
    else:
        return random.choice(PESAN[sesi])

# ── Scheduler jobs — async functions langsung ────────────────────────────────
async def job_pagi(bot):
    teks = get_teks("pagi") + get_footer()
    await bot.send_message(chat_id=CHAT_ID, text=teks, parse_mode="Markdown")
    log.info("✅ [pagi] terkirim")

async def job_quotes(bot):
    teks = get_teks("quotes") + get_footer()
    await bot.send_message(chat_id=CHAT_ID, text=teks, parse_mode="Markdown")
    log.info("✅ [quotes] terkirim")

async def job_quotes2(bot):
    teks = get_teks("quotes2") + get_footer()
    await bot.send_message(chat_id=CHAT_ID, text=teks, parse_mode="Markdown")
    log.info("✅ [quotes2] terkirim")

async def job_statistik(bot):
    teks = get_teks("statistik") + get_footer()
    await bot.send_message(chat_id=CHAT_ID, text=teks, parse_mode="Markdown")
    log.info("✅ [statistik] terkirim")

async def job_malam(bot):
    teks = get_teks("malam") + get_footer()
    await bot.send_message(chat_id=CHAT_ID, text=teks, parse_mode="Markdown")
    log.info("✅ [malam] terkirim")

# ── Commands ──────────────────────────────────────────────────────────────────
async def cmd_start(update, context):
    await update.message.reply_text(
        "🤖 *Trading Mindset Bot* aktif!\n\n"
        "📅 *Jadwal harian (WIB):*\n"
        "• 06:00 — Motivasi & mindset pagi\n"
        "• 10:00 — Quotes trading random\n"
        "• 14:00 — Quotes mindset & disiplin\n"
        "• 20:00 — Statistik & gambaran angka\n"
        "• 22:00 — Evaluasi & renungan malam\n\n"
        "📌 *Commands:*\n"
        "/quote — Quotes random\n"
        "/risk — Quotes risk management\n"
        "/compound — Simulasi compound\n"
        "/mindset — Quotes mindset\n"
        "/disiplin — Quotes disiplin\n"
        "/umroh — Motivasi Umroh\n"
        "/statistik — Angka & statistik\n"
        "/plan — Trading plan lengkap\n"
        "/progress — Progress Rp 1M\n"
        "/test — Pesan random sekarang\n\n"
        "🎯 *Target: Rp 1 Miliar — Oktober 2026*\n"
        "🕌 Umroh untuk 4 orang keluarga",
        parse_mode="Markdown"
    )

async def cmd_quote(update, context):
    k = random.choice(list(QUOTES.keys()))
    await update.message.reply_text(random.choice(QUOTES[k]) + get_footer(), parse_mode="Markdown")

async def cmd_risk(update, context):
    await update.message.reply_text(random.choice(QUOTES["risk_management"]) + get_footer(), parse_mode="Markdown")

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
    teks = f"🧮 *Simulasi Compound 5%/bulan*\n_(dari Rp {bal:,.0f})_\n\n{rows}\n💡 Compound bekerja kalau modal dijaga.\n🛡️ Jaga drawdown = jaga compounding." + get_footer()
    await update.message.reply_text(teks, parse_mode="Markdown")

async def cmd_mindset(update, context):
    await update.message.reply_text(random.choice(QUOTES["mindset"]) + get_footer(), parse_mode="Markdown")

async def cmd_disiplin(update, context):
    await update.message.reply_text(random.choice(QUOTES["disiplin"]) + get_footer(), parse_mode="Markdown")

async def cmd_umroh(update, context):
    await update.message.reply_text(random.choice(QUOTES["umroh"]) + get_footer(), parse_mode="Markdown")

async def cmd_statistik(update, context):
    await update.message.reply_text(random.choice(STATISTIK) + get_footer(), parse_mode="Markdown")

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
        "• -5%  → Review & evaluasi\n"
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

async def cmd_test(update, context):
    semua = list(QUOTES.keys()) + ["statistik", "pagi", "malam"]
    pilihan = random.choice(semua)
    if pilihan in QUOTES:
        teks = random.choice(QUOTES[pilihan])
    elif pilihan == "statistik":
        teks = random.choice(STATISTIK)
    else:
        teks = random.choice(PESAN[pilihan])
    await update.message.reply_text(teks + get_footer(), parse_mode="Markdown")

# ── Setup scheduler — pakai coroutine langsung, bukan lambda ─────────────────
def setup_scheduler(app):
    bot = app.bot
    scheduler = AsyncIOScheduler(timezone=WIB)

    scheduler.add_job(job_pagi,      "cron", hour=6,  minute=0,  args=[bot], id="pagi")
    scheduler.add_job(job_quotes,    "cron", hour=10, minute=0,  args=[bot], id="quotes")
    scheduler.add_job(job_quotes2,   "cron", hour=14, minute=0,  args=[bot], id="quotes2")
    scheduler.add_job(job_statistik, "cron", hour=20, minute=0,  args=[bot], id="statistik")
    scheduler.add_job(job_malam,     "cron", hour=22, minute=0,  args=[bot], id="malam")

    scheduler.start()
    log.info("✅ Scheduler aktif — 5 sesi terdaftar")
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
        ("disiplin",  cmd_disiplin),
        ("umroh",     cmd_umroh),
        ("statistik", cmd_statistik),
        ("plan",      cmd_plan),
        ("progress",  cmd_progress),
    ]:
        app.add_handler(CommandHandler(cmd, handler))

    setup_scheduler(app)
    log.info("✅ Bot siap — polling aktif")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
