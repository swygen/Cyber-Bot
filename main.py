import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

TOKEN = "7977910185:AAGUKUbL1gGflrwYn4ZmDMn0V0CXeoN0XIg"  # <-- এখানে আপনার বটের টোকেন বসান
bot = telebot.TeleBot(TOKEN)

# Agreement Start Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    agreement = """🛡️ *Agreement*

এই বট ব্যবহার করে আপনি সম্মত হচ্ছেন:
- বটের অপব্যবহার করবেন না
- ভুল তথ্য দেবেন না
- নিরাপত্তার জন্য সীমিত তথ্য সংগ্রহ করা হয়
- আপনার গোপনীয়তা রক্ষা করা হয়
- অপব্যবহারে সীমাবদ্ধতা আরোপিত হতে পারে
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ I Agree This Agreement", callback_data="agree"))
    bot.send_message(message.chat.id, agreement, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "agree")
def agreement_accepted(call):
    welcome_msg = f"""🤖 *Welcome to CYBER SECURITY BD*

আমরা টেলিগ্রামে নিরাপদ এবং সচেতন কমিউনিটি গঠনে কাজ করছি।
"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("MY PROFILE", "SERVICE")
    markup.add("POLICY", "SUBMIT INFORMATION")
    markup.add("SUPPORT TEAM")
    bot.send_message(call.message.chat.id, welcome_msg, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "MY PROFILE")
def my_profile(message):
    profile_text = f"""👤 *Your Profile Info*

🪪 Name: {message.from_user.first_name}
🆔 User ID: {message.from_user.id}

📡 Part of the Telegram Clean Network
🚀 Actively securing communities
    """
    bot.send_message(message.chat.id, profile_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "SERVICE")
def service_info(message):
    service_text = "🇧🇩 বাংলাদেশের সকল সেবা সমূহ নিচে উল্লেখ রয়েছে:"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📞 জাতীয় তথ্যসেবা হটলাইন (333)", url="tel:333"))
    markup.add(InlineKeyboardButton("🚨 জরুরি সেবা (999)", url="tel:999"))
    markup.add(InlineKeyboardButton("🏥 স্বাস্থ্য বাতায়ন (16263)", url="tel:16263"))
    markup.add(InlineKeyboardButton("👩‍👧 নারী ও শিশু সহায়তা হটলাইন (109)", url="tel:109"))
    markup.add(InlineKeyboardButton("⚖️ দুর্নীতি দমন কমিশন (106)", url="tel:106"))
    markup.add(InlineKeyboardButton("🔐 ডিজিটাল নিরাপত্তা হেল্পলাইন (105)", url="tel:105"))
    bot.send_message(message.chat.id, service_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "POLICY")
def policy_info(message):
    text = """🔍 Collaborating with cyber police to detect, report, and remove:

🚫 Illegal 18+ content
⚠️ Scams
🛡️ Abuse

Dedicated to making Telegram a safer place for everyone.
    """
    bot.send_message(message.chat.id, text)

# Submit Info Workflow
user_reports = {}

@bot.message_handler(func=lambda message: message.text == "SUBMIT INFORMATION")
def submit_info_start(message):
    bot.send_message(message.chat.id, "📝 আপনি কোন দুর্নীতি বা অনিয়মের তথ্য দিতে চাইলে, দয়া করে গ্রুপ লিংক পাঠান:")
    user_reports[message.chat.id] = {}

@bot.message_handler(func=lambda message: message.chat.id in user_reports and "group_link" not in user_reports[message.chat.id])
def get_group_link(message):
    user_reports[message.chat.id]["group_link"] = message.text
    bot.send_message(message.chat.id, "📄 এখন আপনার অভিযোগটি লিখুন:")

@bot.message_handler(func=lambda message: message.chat.id in user_reports and "complaint" not in user_reports[message.chat.id])
def get_complaint(message):
    user_reports[message.chat.id]["complaint"] = message.text
    name = message.from_user.first_name
    user_reports[message.chat.id]["name"] = name
    bot.send_message(message.chat.id, "📨 তথ্য জমা দেওয়ার জন্য নিচের বাটনে ক্লিক করুন।", reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ তথ্য জমা দিন", callback_data="submit_info")
    ))

@bot.callback_query_handler(func=lambda call: call.data == "submit_info")
def submit_final(call):
    data = user_reports.get(call.message.chat.id, {})
    report_message = f"""📥 *নতুন রিপোর্ট প্রাপ্ত হয়েছে*

👤 নাম: {data.get("name")}
🔗 গ্রুপ লিংক: {data.get("group_link")}
📝 অভিযোগ: {data.get("complaint")}
🆔 ইউজার আইডি: {call.from_user.id}
"""
    # অ্যাডমিন চ্যাট আইডি দিয়ে এখানে রিপোর্ট পাঠান (example: -1001234567890)
    admin_chat_id = "6243881362"
    bot.send_message(admin_chat_id, report_message, parse_mode="Markdown")

    bot.send_message(call.message.chat.id, "✅ ধন্যবাদ! তথ্য দিয়ে সাহায্য করার জন্য। আপনার তথ্য সঠিক হলে আমরা দ্রুত Action নিব ।")

    del user_reports[call.message.chat.id]

@bot.message_handler(func=lambda message: message.text == "SUPPORT TEAM")
def support_team(message):
    support_msg = """🤖 *Cyber Security BD Support Team*

Hi there! 👋
We’re here to help with any issues, questions, or reports related to illegal content, scams, or abuse on Telegram.

Please describe your concern clearly. Our support team will review it as soon as possible.

🔒 All reports are confidential.
📩 Response time: within 24 hours.

Thank you for helping make Telegram safer! 💙
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📩 CONTACT NOW", url="https://t.me/Swygen_bd"))
    bot.send_message(message.chat.id, support_msg, parse_mode="Markdown", reply_markup=markup)

# Keep Alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

# Start the bot
keep_alive()
bot.polling()
