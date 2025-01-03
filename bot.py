import telebot
import pyotp

# Masukkan API Token dari BotFather
API_TOKEN = '8044025494:AAE7l_jFu3N80e73bsE6VAsXtzr9B9M5T3E'  # Ganti dengan token bot Anda
bot = telebot.TeleBot(API_TOKEN)

# Handle perintah /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Selamat datang di 2FA Bot!\n\n"
        "Kirimkan secret key Anda untuk mendapatkan kode OTP.\n"
        "Contoh: `JBSWY3DPEHPK3PXP` (tanpa tanda kutip).",
        parse_mode="Markdown"
    )

# Handle pesan teks (untuk menerima secret key)
@bot.message_handler(func=lambda message: True)
def generate_otp(message):
    try:
        # Ambil secret key dari pesan pengguna
        secret_key = message.text.strip()

        # Validasi panjang secret key (biasanya 16 karakter untuk TOTP)
        if len(secret_key) < 16:
            bot.reply_to(message, "Secret key terlalu pendek. Pastikan Anda mengirimkan secret key yang valid.")
            return

        # Buat TOTP menggunakan pyotp
        totp = pyotp.TOTP(secret_key)

        # Hasilkan kode OTP
        otp_code = totp.now()

        # Kirimkan kode OTP ke pengguna
        bot.reply_to(message, f"Kode OTP Anda adalah: `{otp_code}`", parse_mode="Markdown")
    except Exception as e:
        # Tangani error jika secret key tidak valid
        bot.reply_to(message, "Terjadi kesalahan. Pastikan Anda mengirimkan secret key yang valid.")

# Jalankan bot
print("Bot sedang berjalan...")
bot.polling()