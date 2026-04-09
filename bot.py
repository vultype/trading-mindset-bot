#!/usr/bin/env python3
"""
Trading Mindset Bot — Candra
Motivasi harian menuju Rp 1 Miliar | XAUUSD | NY Session
"""

import os, asyncio, random, logging
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8626750521:AAGWL7IZqHg62hxrbDPiVzN_jMzrwr4v6v4")
CHAT_ID   = os.environ.get("CHAT_ID",   "5488406480")
WIB       = ZoneInfo("Asia/Jakarta")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

SCHEDULE = [
    {"hour": 6,  "minute": 0,  "sesi": "pagi"},
    {"hour": 10, "minute": 0,  "sesi": "siang"},
    {"hour": 14, "minute": 0,  "sesi": "sore"},
    {"hour": 20, "minute": 0,  "sesi": "pre_session"},
    {"hour": 23, "minute": 0,  "sesi": "malam"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# PESAN — Semua berdasarkan trading plan Candra yang nyata
# ═══════════════════════════════════════════════════════════════════════════════
PESAN = {

# ─────────────────────────────────────────────────────────────────────────────
  "pagi": [

    "🌅 *Selamat pagi, Candra!*\n\n"
    "Balance hari ini: *Rp 311 juta lebih.*\n"
    "Target Oktober 2026: *Rp 1 Miliar.*\n\n"
    "Jarak itu ditempuh bukan dengan 1 trade besar —\n"
    "tapi dengan *ratusan malam yang konsisten.*\n\n"
    "Malam ini cukup 1–2 trade yang sesuai plan.\n"
    "Itu sudah cukup. Itu sudah *luar biasa.*\n\n"
    "🕌 _Umroh untuk Bapak, Ibu, dan mertua — bayangkan wajah mereka._",

    "☀️ *Pagi, Candra!*\n\n"
    "📊 *Fakta sistem kamu (Maret 2026):*\n"
    "• WR: 35.3% — sudah profitable\n"
    "• Profit Factor: 2.60 — sangat sehat\n"
    "• RR 1:4 dengan Fibonacci 1.618\n\n"
    "Artinya: dari 10 trade, *7 bisa loss* — tapi kamu tetap profit.\n\n"
    "💡 Sistem ini bekerja. Tugas kamu hari ini hanya *satu:*\n"
    "Jangan ganggu sistem yang sudah terbukti.\n\n"
    "🛡️ _Jaga modal = jaga compounding = jaga impian._",

    "🌄 *Compound itu ajaib, Candra.*\n\n"
    "Kalau setiap bulan tumbuh 5% saja:\n"
    "• April 2026: ~Rp 327 juta\n"
    "• Juli 2026: ~Rp 380 juta\n"
    "• Oktober 2026: *~Rp 1 Miliar* ✅\n\n"
    "Tapi compound bekerja dengan satu syarat:\n"
    "*Modal tidak boleh dibakar oleh overtrading.*\n\n"
    "Ingat 23 Maret dan 1 April — overtrading adalah musuh terbesar.\n\n"
    "🔑 _Disiplin hari ini = compound bulan depan._",

    "🌞 *Selamat pagi!*\n\n"
    "📌 *7 Pelajaran Maret yang sudah kamu dokumentasi:*\n\n"
    "Kamu sudah tahu masalahnya.\n"
    "Kamu sudah tahu solusinya.\n"
    "Kamu sudah pasang app blocker.\n"
    "Kamu sudah buat trading plan.\n\n"
    "Sekarang hanya butuh satu hal:\n"
    "*Eksekusi konsisten — hari demi hari.*\n\n"
    "Trader yang menang bukan yang paling pintar,\n"
    "tapi yang paling *konsisten.*\n\n"
    "🕌 _4 tiket Umroh menunggu di Oktober 2026._",

    "🌤️ *Pagi ini, satu quotes untuk kamu:*\n\n"
    "_\"Seorang trader profesional bukan yang tidak pernah loss —_\n"
    "_tapi yang sudah menerima loss sebagai biaya berbisnis.\"_\n\n"
    "SL kamu 25–30 pip.\n"
    "Risk per trade: Rp 500rb (fase 1) → Rp 1jt (fase 2).\n"
    "Itu sudah dihitung. Itu sudah *direncanakan.*\n\n"
    "Kalau malam ini loss — itu bukan kegagalan.\n"
    "Kegagalan hanya terjadi kalau kamu:\n"
    "❌ Tidak pasang SL\n"
    "❌ Revenge trade setelah loss\n"
    "❌ Trade lebih dari 2x malam itu\n\n"
    "🛡️ _Hindari 3 itu — kamu sudah menang._",

    "☀️ *Candra, ingat ini setiap pagi:*\n\n"
    "Kamu bukan trader yang sedang *mencoba.*\n"
    "Kamu adalah trader yang sedang *membangun bisnis.*\n\n"
    "Bisnis kamu:\n"
    "• Produk: Eksekusi XAUUSD\n"
    "• Modal kerja: Rp 311 juta\n"
    "• Target revenue: Rp 1 Miliar\n"
    "• Deadline: Oktober 2026\n"
    "• Sistem: NY Session, max 2 trade, RR 1:4\n\n"
    "Bisnis yang baik tidak butuh *keberuntungan.*\n"
    "Butuh *sistem yang dijalankan dengan konsisten.*\n\n"
    "🎯 _Jalankan bisnismu malam ini._",

  ],

# ─────────────────────────────────────────────────────────────────────────────
  "siang": [

    "🔔 *Pengingat siang, Candra!*\n\n"
    "NY Session masih *8 jam lagi.*\n\n"
    "Jangan buka chart sekarang untuk cari setup —\n"
    "itu hanya menguras energi mental untuk malam nanti.\n\n"
    "💡 *Yang bisa dilakukan siang ini:*\n"
    "□ Review jurnal kemarin\n"
    "□ Cek kalender ekonomi malam ini\n"
    "□ Istirahat dan isi energi\n\n"
    "Trader terbaik tahu kapan harus *tidak* di depan chart.\n\n"
    "🕐 _Simpan fokus untuk jam 20:30 WIB._",

    "☀️ *Siang hari — saatnya evaluasi singkat:*\n\n"
    "📅 *Statistik Candra berdasarkan hari:*\n"
    "• Jumat: WR ~62.5% ← *terbaik*\n"
    "• Rabu: Hati-hati (Crude Oil Report)\n"
    "• Senin–Kamis: Normal, ikuti setup\n\n"
    "Kalau hari ini Rabu → pertimbangkan skip atau perketat filter.\n"
    "Kalau hari ini Jumat → *ini peluang terbaik mingguan.*\n\n"
    "Data tidak berbohong. Gunakan ini.\n\n"
    "🎯 _Trading berdasarkan data, bukan feeling._",

    "💭 *Quote siang untuk Candra:*\n\n"
    "_\"The goal of a successful trader is to make the best trades._\n"
    "_Money is secondary.\"_\n"
    "— Alexander Elder\n\n"
    "Terjemahan untuk plan kamu:\n"
    "Kalau malam ini kamu *skip* karena tidak ada setup bagus —\n"
    "itu adalah *trade terbaik* yang bisa kamu buat.\n\n"
    "Profit otomatis mengikuti keputusan yang benar.\n\n"
    "📊 _WR 35.3% dengan PF 2.60 — buktinya sudah ada._",

    "🌿 *Istirahat sebentar, Candra.*\n\n"
    "Perjalanan ke Rp 1 Miliar adalah *marathon,* bukan sprint.\n\n"
    "Bayangkan:\n"
    "• Mei 2026: Mulai scaling risk ke 0.5% equity\n"
    "• Juni 2026: Mulai partial TP strategy\n"
    "• Juli 2026: Evaluasi London session\n"
    "• Pertengahan 2026: *Mulai withdrawals untuk Umroh*\n"
    "• Oktober 2026: Target Rp 1 Miliar tercapai\n\n"
    "Setiap hari yang kamu jalani dengan disiplin\n"
    "adalah satu hari dalam peta perjalanan ini.\n\n"
    "🕌 _Kamu sedang dalam perjalanan yang benar._",

    "📊 *Komponen sistem Candra (reminder):*\n\n"
    "⏰ Entry: NY Session 20:30–22:30 WIB\n"
    "🎯 TP: Fibonacci 1.618\n"
    "🛡️ SL: 25–30 pip\n"
    "⚖️ RR Target: 1:4\n"
    "🔢 Max trade: 2 per malam\n"
    "💰 Risk/trade: Rp 500rb (s/d 11 Apr) → Rp 1jt (12 Apr+)\n\n"
    "Sistem ini sudah *menghasilkan +Rp 11.3jt di Maret.*\n\n"
    "Tugas kamu bukan menemukan sistem baru.\n"
    "Tugas kamu adalah *menjalankan sistem ini dengan sempurna.*\n\n"
    "🔑 _Jangan ubah yang sudah terbukti bekerja._",

    "💡 *Siang ini, hitung bareng:*\n\n"
    "Balance: Rp 311.3 juta\n"
    "Target: Rp 1 Miliar\n"
    "Sisa: Rp 688.7 juta\n\n"
    "Dengan compound 5%/bulan:\n"
    "Bulan 1 → Rp 327jt\n"
    "Bulan 2 → Rp 343jt\n"
    "Bulan 3 → Rp 360jt\n"
    "Bulan 4 → Rp 378jt\n"
    "Bulan 5 → Rp 397jt\n"
    "Bulan 6 → *Rp 417jt* 🎯\n\n"
    "Konsisten 5%/bulan = *Oktober 2026 tercapai.*\n\n"
    "🧮 _Matematika tidak berbohong kalau sistemnya dijaga._",

  ],

# ─────────────────────────────────────────────────────────────────────────────
  "sore": [

    "🌇 *4 jam lagi NY Session buka!*\n\n"
    "⚡ *Pre-session checklist Candra:*\n\n"
    "□ Cek higher timeframe XAUUSD\n"
    "□ Tandai support & resistance kunci\n"
    "□ Identifikasi zona entry Fibonacci\n"
    "□ Set alert harga — jangan nonton chart terus\n"
    "□ Hitung lot size sesuai risk hari ini\n"
    "□ Pastikan Trading Block extension aktif\n\n"
    "Kalau semua done → *istirahat, nonton chart pas 20:30 WIB.*\n\n"
    "🎯 _Persiapan 30 menit = ketenangan 2 jam trading._",

    "🌆 *Sore hari — reminder plan April Candra:*\n\n"
    "📅 *Fase 1 (1–11 April):* Risk Rp 500rb/trade\n"
    "📅 *Fase 2 (12–30 April):* Risk Rp 1jt/trade\n\n"
    "Kenapa bertahap? Karena:\n"
    "✅ Bangun kembali kepercayaan diri\n"
    "✅ Buktikan konsistensi dulu\n"
    "✅ Baru scale up dengan tenang\n\n"
    "Ini bukan kelemahan — ini *kecerdasan manajemen risiko.*\n\n"
    "💪 _Trader smart scale up setelah terbukti, bukan sebelumnya._",

    "🏆 *Visualisasi sore hari:*\n\n"
    "Pertengahan 2026 — Candra mulai withdrawal pertama.\n"
    "Bukan untuk dipakai — tapi untuk ditabung ke dana Umroh.\n\n"
    "4 orang:\n"
    "👴 Bapak\n"
    "👩 Ibu\n"
    "👴 Mertua laki-laki\n"
    "👩 Mertua perempuan\n\n"
    "Mereka belum tahu seberapa keras Candra bekerja malam-malam ini.\n"
    "Tapi hasilnya akan berbicara sendiri.\n\n"
    "💫 _Setiap trade yang disiplin = selangkah lebih dekat ke momen itu._",

    "⚙️ *Framework 4 level drawdown Candra:*\n\n"
    "🟡 -5%   → Review setup, evaluasi 1 hari\n"
    "🟠 -10%  → Kurangi size 50%, cari penyebab\n"
    "🔴 -15%  → Stop trading 3 hari, review total\n"
    "⛔ -20%  → Stop trading 1 minggu, konsultasi\n\n"
    "Ini bukan aturan yang mempersulit —\n"
    "ini adalah *pelindung* yang menjaga Candra tetap di game.\n\n"
    "Trader yang survive adalah trader yang bisa *bertahan* di drawdown.\n\n"
    "🛡️ _Jaga drawdown = jaga masa depan._",

    "📈 *Sore ini, ingat: Jumat adalah harimu.*\n\n"
    "WR Candra di hari Jumat: *~62.5%*\n\n"
    "Kalau hari ini Jumat → *ini adalah setup terbaik minggu ini.*\n"
    "Fokus maksimal. Persiapan matang. Eksekusi tenang.\n\n"
    "Kalau hari ini bukan Jumat → simpan energi untuk Jumat.\n\n"
    "_\"Trade the best, skip the rest.\"_\n\n"
    "🎯 _Selektivitas adalah senjata trader yang profitable._",

  ],

# ─────────────────────────────────────────────────────────────────────────────
  "pre_session": [

    "🔔 *20:00 WIB — NY SESSION 30 MENIT LAGI!*\n\n"
    "⚡ *Final checklist sebelum eksekusi:*\n\n"
    "□ Setup XAUUSD sudah jelas?\n"
    "□ Entry zone sudah ditandai?\n"
    "□ SL 25–30 pip sudah dihitung?\n"
    "□ TP di Fibonacci 1.618 sudah di-set?\n"
    "□ Max 2 trade malam ini — sudah diingat?\n"
    "□ Trading Block extension aktif?\n\n"
    "✅ Semua siap → *Execute sesuai plan*\n"
    "❌ Ada keraguan → *Skip dulu, tunggu setup lebih jelas*\n\n"
    "🕌 _Bismillah — untuk keluarga, untuk Umroh, untuk masa depan._",

    "⏰ *Pre-session reminder:*\n\n"
    "Jam 20:30 WIB — NY session buka (DST aktif).\n\n"
    "Ingat protokol entry Candra:\n"
    "• *Jangan entry sebelum 20:30 WIB*\n"
    "• Window terbaik: 20:30–22:30 WIB\n"
    "• Setelah 22:30 → pertimbangkan skip jika belum dapat setup\n\n"
    "Disiplin waktu entry = salah satu edge terbesar yang kamu punya.\n\n"
    "⏱️ _Waktu yang salah = setup yang salah, meski chart terlihat bagus._",

    "🌙 *Mindset pre-session:*\n\n"
    "_\"Saya tidak perlu profit malam ini._\n"
    "_Saya hanya perlu menjalankan plan malam ini.\"_\n\n"
    "Profit adalah *hasil* dari eksekusi yang benar —\n"
    "bukan tujuan per trade.\n\n"
    "Tujuan per trade Candra:\n"
    "✅ Entry sesuai setup\n"
    "✅ SL terpasang\n"
    "✅ TP di 1.618 Fibonacci\n"
    "✅ Max 2 trade\n\n"
    "Kalau 4 itu terpenuhi — *malam ini sudah sukses,*\n"
    "apapun hasilnya.\n\n"
    "💪 _PF 2.60 itu nyata. Sistemnya bekerja. Percaya._",

    "⚠️ *Cek hari ini — protokol khusus:*\n\n"
    "📅 *Kalau hari ini RABU:*\n"
    "→ Crude Oil Report malam ini\n"
    "→ Tunda entry atau perketat filter\n"
    "→ Kalau tidak yakin → *skip, ini keputusan terbaik*\n\n"
    "📅 *Kalau hari ini JUMAT:*\n"
    "→ WR historis kamu 62.5%\n"
    "→ Fokus maksimal, ini hari terbaikmu\n\n"
    "📅 *Hari lainnya:*\n"
    "→ Follow setup normal, ikuti sistem\n\n"
    "🎯 _Data adalah panduan. Feeling adalah musuh._",

    "💫 *30 menit sebelum market buka:*\n\n"
    "Bayangkan dua versi dirimu malam ini:\n\n"
    "*Versi A:* Dapat 2 setup bagus, eksekusi tenang,\n"
    "profit sesuai RR 1:4, tutup laptop jam 22:30.\n\n"
    "*Versi B:* Tidak dapat setup bagus, sabar menunggu,\n"
    "akhirnya *skip* malam ini, tidur lebih awal.\n\n"
    "Kedua versi itu adalah *kemenangan.*\n\n"
    "Yang kalah hanya satu:\n"
    "❌ Overtrading karena bosan atau FOMO\n\n"
    "🛡️ _Jaga diri dari Versi C — itulah tugas utama malam ini._",

  ],

# ─────────────────────────────────────────────────────────────────────────────
  "malam": [

    "🌙 *Evaluasi malam — selesai trading?*\n\n"
    "Ambil 10 menit untuk jurnal:\n\n"
    "□ Berapa trade malam ini?\n"
    "□ Win atau loss?\n"
    "□ Setup sesuai plan?\n"
    "□ Ada yang bisa diperbaiki?\n"
    "□ Emosi terjaga?\n\n"
    "📝 Tulis di jurnal — satu kalimat saja sudah cukup.\n\n"
    "_Trader yang tidak jurnal tidak tahu kenapa mereka profit —_\n"
    "_dan tidak tahu kenapa mereka loss._\n\n"
    "🕌 _Selamat istirahat. Besok market buka lagi._",

    "⭐ *Malam ini kamu sudah:*\n\n"
    "✅ Menjalani satu hari lagi dalam perjalanan ke Rp 1M\n"
    "✅ Menjaga modal dari keputusan impulsif\n"
    "✅ Satu langkah lebih dekat ke Umroh keluarga\n\n"
    "Apakah profit malam ini? → Syukuri.\n"
    "Apakah loss malam ini? → Evaluasi, bukan menyesal.\n"
    "Apakah skip malam ini? → *Ini keputusan terbaik jika tidak ada setup.*\n\n"
    "Semua skenario di atas adalah *progress* —\n"
    "selama kamu tidak melanggar plan.\n\n"
    "💪 _Besok pagi kita mulai lagi. Konsisten._",

    "🌟 *Renungan malam — compound Candra:*\n\n"
    "Rp 311 juta hari ini.\n\n"
    "Kalau bulan ini +5% → Rp 327 juta\n"
    "Kalau 3 bulan konsisten → Rp 360 juta\n"
    "Kalau 6 bulan konsisten → Rp 417 juta\n"
    "Kalau sampai Oktober konsisten → *Rp 1 Miliar* 🎯\n\n"
    "Angka ini nyata. Matematika ini bekerja.\n"
    "Tapi hanya kalau satu syarat terpenuhi:\n"
    "*Modal tidak dirusak oleh keputusan buruk.*\n\n"
    "Malam ini sudah selesai. Modal aman?\n"
    "Kalau iya — *Alhamdulillah. Kamu menang malam ini.*\n\n"
    "🕌 _Tidur yang cukup — besok kita compound lagi._",

    "💰 *Progress tracker malam ini:*\n\n"
    "🏁 Start April: Rp 311.3 juta\n"
    "🎯 Target Oktober 2026: Rp 1 Miliar\n"
    "📅 Sisa waktu: ~6 bulan\n\n"
    "Yang perlu dijaga:\n"
    "• Drawdown maksimal -20% (= Rp 62 juta)\n"
    "• Loss streak 2x berturut → evaluasi, jangan lanjut\n"
    "• Withdrawal mulai pertengahan 2026 untuk dana Umroh\n\n"
    "_\"Kekayaan sejati bukan dibangun dalam semalam —_\n"
    "_tapi dalam satu kebiasaan baik yang diulang setiap malam.\"_\n\n"
    "🛌 _Istirahat. Besok adalah hari baru untuk compound._",

    "🙏 *Sebelum tidur, syukuri 3 hal ini:*\n\n"
    "1️⃣ *Modal masih aman?*\n"
    "   → Alhamdulillah — compound masih bekerja\n\n"
    "2️⃣ *Ikut plan malam ini?*\n"
    "   → Alhamdulillah — sistem masih berjalan\n\n"
    "3️⃣ *Tidak overtrading?*\n"
    "   → Alhamdulillah — musuh terbesar sudah dikalahkan\n\n"
    "Profit itu bonus yang menyenangkan.\n"
    "*Disiplin itu tujuan yang sesungguhnya.*\n\n"
    "🕌 _Selamat malam, Candra._\n"
    "_Bapak, Ibu, dan mertua bangga dengan prosesmu —_\n"
    "_bahkan sebelum Umroh itu terjadi._",

    "🌙 *Quote penutup malam:*\n\n"
    "_\"Jangan hitung profit hari ini._\n"
    "_Hitung apakah kamu lebih baik dari kemarin._\"\n\n"
    "Kemarin kamu sudah:\n"
    "• Dokumentasi 7 pelajaran Maret\n"
    "• Pasang Trading Block extension\n"
    "• Buat plan April yang terstruktur\n"
    "• Tetap trading meski ada tantangan\n\n"
    "Candra yang sekarang *sudah lebih baik* dari sebelumnya.\n\n"
    "Teruslah tumbuh — satu malam dalam satu waktu.\n\n"
    "🎯 _Rp 1 Miliar. Oktober 2026. Umroh 4 orang._\n"
    "_Bukan mimpi — ini *rencana yang sedang berjalan.*_",

  ],
}

# ─────────────────────────────────────────────────────────────────────────────
def get_footer():
    now  = datetime.now(WIB)
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()]
    return f"\n\n─────────────────\n📅 {hari}, {now.strftime('%d %b %Y')} | ⏰ {now.strftime('%H:%M')} WIB"

async def kirim(bot: Bot, sesi: str):
    teks = random.choice(PESAN[sesi]) + get_footer()
    try:
        await bot.send_message(chat_id=CHAT_ID, text=teks, parse_mode="Markdown")
        log.info(f"✅ [{sesi}] terkirim")
    except Exception as e:
        log.error(f"❌ [{sesi}] gagal: {e}")

# ── Commands ──────────────────────────────────────────────────────────────────
async def cmd_start(update, context):
    await update.message.reply_text(
        "🤖 *Trading Mindset Bot — Candra* aktif!\n\n"
        "📅 *Jadwal notifikasi harian:*\n"
        "• 06:00 — Mindset pagi\n"
        "• 10:00 — Fokus siang\n"
        "• 14:00 — Pre-session sore\n"
        "• 20:00 — 30 menit sebelum NY session\n"
        "• 23:00 — Evaluasi & istirahat\n\n"
        "📌 *Commands:*\n"
        "/test — Coba pesan random sekarang\n"
        "/progress — Cek progress Rp 1M\n"
        "/plan — Review trading plan kamu\n"
        "/compound — Simulasi compound\n\n"
        "🎯 Target: *Rp 1 Miliar — Oktober 2026*\n"
        "🕌 Umroh untuk 4 orang keluarga",
        parse_mode="Markdown"
    )

async def cmd_test(update, context):
    sesi = random.choice(list(PESAN.keys()))
    teks = random.choice(PESAN[sesi]) + get_footer()
    await update.message.reply_text(teks, parse_mode="Markdown")

async def cmd_progress(update, context):
    bal    = 311_300_000
    target = 1_000_000_000
    pct    = bal / target * 100
    bar    = "█" * int(pct/5) + "░" * (20 - int(pct/5))
    await update.message.reply_text(
        f"📊 *Progress Rp 1 Miliar*\n\n"
        f"💰 Balance : Rp {bal:>15,.0f}\n"
        f"🎯 Target  : Rp {target:>15,.0f}\n"
        f"📈 Progress: [{bar}] {pct:.1f}%\n\n"
        f"📅 Target bulan  : Oktober 2026\n"
        f"⏳ Estimasi sisa : ~6 bulan\n"
        f"📈 Butuh/bulan   : ~5% compound\n\n"
        f"🕌 *Umroh 4 orang — tetap di jalur!*",
        parse_mode="Markdown"
    )

async def cmd_plan(update, context):
    await update.message.reply_text(
        "📋 *Trading Plan Candra — April 2026*\n\n"
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

async def cmd_compound(update, context):
    bal    = 311_300_000
    target = 1_000_000_000
    rate   = 0.05
    rows   = ""
    b      = bal
    now    = datetime.now(WIB)
    for i in range(1, 10):
        b *= (1 + rate)
        m  = (now.month - 1 + i) % 12 + 1
        y  = now.year + (now.month - 1 + i) // 12
        bln = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"][m-1]
        flag = " ✅" if b >= target else ""
        rows += f"• {bln} {y}: Rp {b:,.0f}{flag}\n"
        if b >= target:
            break
    await update.message.reply_text(
        f"🧮 *Simulasi Compound 5%/bulan*\n"
        f"_(dari Rp {bal:,.0f})_\n\n"
        f"{rows}\n"
        f"💡 Compound bekerja kalau modal dijaga.\n"
        f"🛡️ Jaga drawdown = jaga compounding.",
        parse_mode="Markdown"
    )

# ── Scheduler ─────────────────────────────────────────────────────────────────
def setup_scheduler(app):
    scheduler = AsyncIOScheduler(timezone=WIB)
    for j in SCHEDULE:
        s = j["sesi"]
        scheduler.add_job(
            lambda sesi=s: asyncio.create_task(kirim(app.bot, sesi)),
            trigger="cron", hour=j["hour"], minute=j["minute"], id=f"sesi_{s}"
        )
    scheduler.start()
    log.info("✅ Scheduler aktif")

def main():
    log.info("🚀 Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",    cmd_start))
    app.add_handler(CommandHandler("test",     cmd_test))
    app.add_handler(CommandHandler("progress", cmd_progress))
    app.add_handler(CommandHandler("plan",     cmd_plan))
    app.add_handler(CommandHandler("compound", cmd_compound))
    setup_scheduler(app)
    log.info("✅ Bot siap")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
