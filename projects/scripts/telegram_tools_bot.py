#!/usr/bin/env python3
"""
MULTIFUNGSI TOOLS BOT - Telegram Bot
Koleksi tool online yang bisa diakses lewat Telegram
Author: Hermes Support
"""

import os
import json
import random
import string
import hashlib
import base64
import qrcode
import io
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ============== KONFIGURASI ==============
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ============== MENU UTAMA ==============
def main_menu_keyboard():
    """Buat keyboard menu utama"""
    keyboard = [
        [
            InlineKeyboardButton("🔐 Password Generator", callback_data="pwd_gen"),
            InlineKeyboardButton("📱 QR Code Generator", callback_data="qr_gen"),
        ],
        [
            InlineKeyboardButton("🔄 Base64 Encode/Decode", callback_data="base64"),
            InlineKeyboardButton("🌐 Cek IP Address", callback_data="cek_ip"),
        ],
        [
            InlineKeyboardButton("🔢 Hash Generator", callback_data="hash_gen"),
            InlineKeyboardButton("📅 Timestamp Converter", callback_data="timestamp"),
        ],
        [
            InlineKeyboardButton("🎲 Random Number", callback_data="random_num"),
            InlineKeyboardButton("📝 Text to Speech", callback_data="tts"),
        ],
        [
            InlineKeyboardButton("🔍 Web Search", callback_data="web_search"),
            InlineKeyboardButton("📊 Bitcoin Price", callback_data="btc_price"),
        ],
        [
            InlineKeyboardButton("🌍 Weather Info", callback_data="weather"),
            InlineKeyboardButton("📚 Dictionary", callback_data="dictionary"),
        ],
        [
            InlineKeyboardButton("🔄 Text Reverser", callback_data="reverse"),
            InlineKeyboardButton("🔡 Word/Char Count", callback_data="charcount"),
        ],
        [
            InlineKeyboardButton("💡 About Bot", callback_data="about"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ============== HANDLER Komando ==============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start"""
    welcome = (
        "🔧 *MULTIFUNGSI TOOLS BOT*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Halo! 👋 Selamat datang di bot tools multifungsi.\n\n"
        "Pilih tool yang ingin kamu gunakan:"
    )
    await update.message.reply_text(
        welcome, reply_markup=main_menu_keyboard(), parse_mode="Markdown"
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /menu"""
    await update.message.reply_text(
        "🔧 *MULTIFUNGSI TOOLS*\nPilih tool:", 
        reply_markup=main_menu_keyboard(), 
        parse_mode="Markdown"
    )


# ============== TOOL: PASSWORD GENERATOR ==============
async def pwd_gen_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("12 Karakter", callback_data="pwd_12"),
            InlineKeyboardButton("16 Karakter", callback_data="pwd_16"),
        ],
        [
            InlineKeyboardButton("24 Karakter", callback_data="pwd_24"),
            InlineKeyboardButton("32 Karakter", callback_data="pwd_32"),
        ],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "🔐 *PASSWORD GENERATOR*\nPilih panjang password:", 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )


async def generate_password(update: Update, context: ContextTypes.DEFAULT_TYPE, length: int):
    """Generate password random"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choices(chars, k=length))
    
    # Hitung strength
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)
    
    strength = sum([has_upper, has_lower, has_digit, has_special])
    strength_text = ["Lemah 😕", "Sedang 😐", "Kuat 💪", "Sangat Kuat 🔥"][strength - 1]
    
    text = (
        "🔐 *PASSWORD GENERATED*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"`{password}`\n\n"
        f"📏 Panjang: *{length} karakter*\n"
        f"💪 Strength: *{strength_text}*\n"
        f"📅 Dibuat: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        "⚠️ Simpan password ini di tempat aman!"
    )
    return text


async def pwd_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    length_map = {"pwd_12": 12, "pwd_16": 16, "pwd_24": 24, "pwd_32": 32}
    length = length_map.get(query.data, 16)
    
    text = await generate_password(update, context, length)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Lagi", callback_data=query.data)],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    await query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ============== TOOL: QR CODE GENERATOR ==============
async def qr_gen_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📱 *QR CODE GENERATOR*\n\n"
        "Kirim teks/URL yang ingin dijadikan QR code:",
        parse_mode="Markdown"
    )
    context.user_data["awaiting_qr"] = True


async def handle_qr_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle input untuk QR code"""
    if context.user_data.get("awaiting_qr"):
        text = update.message.text
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Simpan ke buffer
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        
        await update.message.reply_photo(
            photo=bio,
            caption=f"📱 *QR Code Generated*\nuntuk: `{text[:50]}...`" if len(text) > 50 else f"📱 *QR Code Generated*\nuntuk: `{text}`",
            parse_mode="Markdown"
        )
        
        context.user_data["awaiting_qr"] = False
        return True
    return False


# ============== TOOL: BASE64 ENCODE/DECODE ==============
async def base64_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🔐 Encode", callback_data="b64_encode"),
            InlineKeyboardButton("🔓 Decode", callback_data="b64_decode"),
        ],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "🔄 *BASE64 ENCODE/DECODE*\nPilih operasi:", 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )


async def base64_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    is_encode = query.data == "b64_encode"
    context.user_data["awaiting_base64"] = "encode" if is_encode else "decode"
    
    action = "encode" if is_encode else "decode"
    await query.edit_message_text(
        f"🔄 *BASE64 {action.upper()}*\n\n"
        f"Kirim teks yang ingin di-{action}:",
        parse_mode="Markdown"
    )


async def handle_base64_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle input untuk base64"""
    action = context.user_data.get("awaiting_base64")
    if action:
        text = update.message.text
        
        try:
            if action == "encode":
                result = base64.b64encode(text.encode()).decode()
                emoji = "🔐"
            else:
                result = base64.b64decode(text.encode()).decode()
                emoji = "🔓"
            
            await update.message.reply_text(
                f"{emoji} *BASE64 {action.upper()}*\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"Input:\n`{text[:100]}`\n\n"
                f"Result:\n`{result[:500]}`",
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        
        context.user_data["awaiting_base64"] = None
        return True
    return False


# ============== TOOL: CEK IP ADDRESS ==============
async def cek_ip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        # Dapatkan IP user dari Telegram (fallback ke public IP)
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip = response.json()["ip"]
        
        # Dapatkan info detail
        info = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        
        text = (
            "🌐 *IP ADDRESS INFO*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 IP: `{info.get('query', 'N/A')}`\n"
            f"📍 Lokasi: {info.get('country', 'N/A')}, {info.get('regionName', 'N/A')}\n"
            f"🏙️ Kota: {info.get('city', 'N/A')}\n"
            f"📮 ZIP: {info.get('zip', 'N/A')}\n"
            f"🌐 ISP: {info.get('isp', 'N/A')}\n"
            f"🏢 Org: {info.get('org', 'N/A')}\n"
            f"🛰️ AS: {info.get('as', 'N/A')}\n"
            f"🕐 Timezone: {info.get('timezone', 'N/A')}\n"
            f"📐 Lat: {info.get('lat', 'N/A')}, Lon: {info.get('lon', 'N/A')}"
        )
    except:
        text = "❌ Gagal mengambil info IP. Coba lagi nanti."
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")]]
    await query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ============== TOOL: HASH GENERATOR ==============
async def hash_gen_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔢 *HASH GENERATOR*\n\n"
        "Kirim teks yang ingin di-hash:",
        parse_mode="Markdown"
    )
    context.user_data["awaiting_hash"] = True


async def handle_hash_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle input untuk hash"""
    if context.user_data.get("awaiting_hash"):
        text = update.message.text
        
        md5 = hashlib.md5(text.encode()).hexdigest()
        sha1 = hashlib.sha1(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        sha512 = hashlib.sha512(text.encode()).hexdigest()
        
        result = (
            "🔢 *HASH RESULTS*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"Input: `{text[:50]}`\n\n"
            f"*MD5:*\n`{md5}`\n\n"
            f"*SHA1:*\n`{sha1}`\n\n"
            f"*SHA256:*\n`{sha256}`\n\n"
            f"*SHA512:*\n`{sha512}`"
        )
        
        await update.message.reply_text(result, parse_mode="Markdown")
        context.user_data["awaiting_hash"] = False
        return True
    return False


# ============== TOOL: TIMESTAMP CONVERTER ==============
async def timestamp_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    now = datetime.now()
    timestamp = int(now.timestamp())
    
    keyboard = [
        [InlineKeyboardButton("🔄 Convert Custom", callback_data="ts_convert")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    
    text = (
        "📅 *TIMESTAMP CONVERTER*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"🕐 Sekarang:\n"
        f"Unix: `{timestamp}`\n"
        f"Date: `{now.strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        f"Atau kirim timestamp untuk di-convert:"
    )
    
    await query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ============== TOOL: RANDOM NUMBER ==============
async def random_num_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("1-10", callback_data="rand_10"),
            InlineKeyboardButton("1-100", callback_data="rand_100"),
        ],
        [
            InlineKeyboardButton("1-1000", callback_data="rand_1000"),
            InlineKeyboardButton("1-10000", callback_data="rand_10000"),
        ],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "🎲 *RANDOM NUMBER*\nPilih range:", 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode="Markdown"
    )


async def random_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    range_map = {"rand_10": 10, "rand_100": 100, "rand_1000": 1000, "rand_10000": 10000}
    max_num = range_map.get(query.data, 100)
    result = random.randint(1, max_num)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Roll Lagi", callback_data=query.data)],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    await query.edit_message_text(
        f"🎲 *RANDOM NUMBER*\n━━━━━━━━━━━━━━━━━━━━━\n"
        f"Hasil (1-{max_num}): *{result}*",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ============== TOOL: TEXT REVERSER ==============
async def reverse_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔄 *TEXT REVERSER*\n\nKirim teks yang ingin di-reverse:",
        parse_mode="Markdown"
    )
    context.user_data["awaiting_reverse"] = True


async def handle_reverse_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle input untuk reverse"""
    if context.user_data.get("awaiting_reverse"):
        text = update.message.text
        reversed_text = text[::-1]
        
        await update.message.reply_text(
            "🔄 *TEXT REVERSED*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"Original:\n`{text}`\n\n"
            f"Reversed:\n`{reversed_text}`",
            parse_mode="Markdown"
        )
        context.user_data["awaiting_reverse"] = False
        return True
    return False


# ============== TOOL: WORD/CHAR COUNT ==============
async def charcount_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔡 *WORD/CHAR COUNT*\n\nKirim teks untuk dihitung:",
        parse_mode="Markdown"
    )
    context.user_data["awaiting_charcount"] = True


async def handle_charcount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle input untuk char count"""
    if context.user_data.get("awaiting_charcount"):
        text = update.message.text
        
        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.split("\n"))
        space_count = text.count(" ")
        
        await update.message.reply_text(
            "🔡 *TEXT STATISTICS*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 Characters: *{char_count}*\n"
            f"📚 Words: *{word_count}*\n"
            f"📄 Lines: *{line_count}*\n"
            f"⬜ Spaces: *{space_count}*",
            parse_mode="Markdown"
        )
        context.user_data["awaiting_charcount"] = False
        return True
    return False


# ============== TOOL: ABOUT ==============
async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = (
        "💡 *ABOUT THIS BOT*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🔧 *MULTIFUNGSI TOOLS BOT*\n\n"
        "Bot ini menyediakan berbagai tools online yang bisa diakses "
        "langsung dari Telegram.\n\n"
        "*Tools yang tersedia:*\n"
        "🔐 Password Generator\n"
        "📱 QR Code Generator\n"
        "🔄 Base64 Encode/Decode\n"
        "🌐 IP Address Checker\n"
        "🔢 Hash Generator\n"
        "📅 Timestamp Converter\n"
        "🎲 Random Number\n"
        "🔄 Text Reverser\n"
        "🔡 Word/Char Counter\n\n"
        "Made with ❤️ by Hermes Support"
    )
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")]]
    await query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ============== CALLBACK ROUTER ==============
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Router untuk semua callback"""
    query = update.callback_query
    data = query.data
    
    # Back to main menu
    if data == "back_main":
        await query.answer()
        await query.edit_message_text(
            "🔧 *MULTIFUNGSI TOOLS*\nPilih tool:",
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # Tool callbacks
    callback_map = {
        "pwd_gen": pwd_gen_callback,
        "qr_gen": qr_gen_callback,
        "base64": base64_callback,
        "cek_ip": cek_ip_callback,
        "hash_gen": hash_gen_callback,
        "timestamp": timestamp_callback,
        "random_num": random_num_callback,
        "reverse": reverse_callback,
        "charcount": charcount_callback,
        "about": about_callback,
        # Password lengths
        "pwd_12": lambda u, c: generate_password_callback(u, c, 12),
        "pwd_16": lambda u, c: generate_password_callback(u, c, 16),
        "pwd_24": lambda u, c: generate_password_callback(u, c, 24),
        "pwd_32": lambda u, c: generate_password_callback(u, c, 32),
        # Random numbers
        "rand_10": random_callback,
        "rand_100": random_callback,
        "rand_1000": random_callback,
        "rand_10000": random_callback,
        # Base64
        "b64_encode": base64_handler,
        "b64_decode": base64_handler,
    }
    
    if data in callback_map:
        await callback_map[data](update, context)


async def generate_password_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, length: int):
    query = update.callback_query
    await query.answer()
    
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choices(chars, k=length))
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)
    
    strength = sum([has_upper, has_lower, has_digit, has_special])
    strength_text = ["Lemah 😕", "Sedang 😐", "Kuat 💪", "Sangat Kuat 🔥"][strength - 1]
    
    text = (
        "🔐 *PASSWORD GENERATED*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"`{password}`\n\n"
        f"📏 Panjang: *{length} karakter*\n"
        f"💪 Strength: *{strength_text}*\n"
        f"📅 Dibuat: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        "⚠️ Simpan password ini di tempat aman!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Lagi", callback_data=f"pwd_{length}")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")],
    ]
    await query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ============== MESSAGE HANDLER ==============
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle semua pesan text"""
    # Cek apakah ada input yang ditunggu
    if await handle_qr_input(update, context):
        return
    if await handle_base64_input(update, context):
        return
    if await handle_hash_input(update, context):
        return
    if await handle_reverse_input(update, context):
        return
    if await handle_charcount_input(update, context):
        return
    
    # Default: tampilkan menu
    await update.message.reply_text(
        "🔧 *MULTIFUNGSI TOOLS*\nPilih tool:",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


# ============== MAIN ==============
def main():
    """jalankan bot"""
    print("🚀 Starting Multifungsi Tools Bot...")
    
    # Buat application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Jalankan bot
    print("✅ Bot is running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
