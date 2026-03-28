import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ১. আপনার বটের টোকেন
TOKEN = '8597619890:AAHiuToAT6mBiq661qd11doBRhchR2LpxQc'

# ২. আপনার টেলিগ্রাম ইউজারনেম
MY_USERNAME = 'nurzxcvbnm' 

SHOE_DATA = {
    'sports': {
        'name': 'Nike Air Max 270',
        'price': '৪৫০০ টাকা',
        'sizes': '৪০, ৪১, ৪২, ৪৩',
        'image': 'https://i.postimg.cc/xCCv0LKg/IMG-20260321-150621-969.jpg',
        'details': 'রানিং বা ক্যাজুয়াল ব্যবহারের জন্য এটি সেরা আরামদায়ক জুতা।'
    },
    'formal': {
        'name': 'Bata Executive Leather',
        'price': '৩২০০ টাকা',
        'sizes': '৩৯, ৪০, ৪১',
        'image': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4',
        'details': '১০০% অরিজিনাল লেদার জুতা। অফিসিয়াল ব্যবহারের জন্য সেরা পছন্দ।'
    }
}

def main_menu():
    keyboard = [['সব জুতা দেখুন 👟'], ['ডেলিভারি চার্জ ও নিয়ম 🚚', 'আমাদের লোকেশন 📍'], ['অর্ডার পদ্ধতি 🛒', 'যোগাযোগ ও রিভিউ 📞']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম! 🙏\nআমাদের শপে আপনাকে স্বাগতম।", reply_markup=main_menu())

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'সব জুতা দেখুন 👟':
        keyboard = [[InlineKeyboardButton("স্পোর্টস জুতা 👟", callback_data='sports')], [InlineKeyboardButton("ফর্মাল জুতা 👞", callback_data='formal')]]
        await update.message.reply_text("কোন ধরণের জুতা দেখতে চাচ্ছেন?", reply_markup=InlineKeyboardMarkup(keyboard))
    elif text == 'ডেলিভারি চার্জ ও নিয়ম 🚚':
        await update.message.reply_text("🚚 *ডেলিভারি চার্জ:*\n\n📍 বগুড়া শহর: ৮০ টাকা\n📍 সারা বাংলাদেশ: ১৫০ টাকা", parse_mode='Markdown')
    elif text == 'আমাদের লোকেশন 📍':
        await update.message.reply_text("📍 *আমাদের প্রধান কেন্দ্র:*\nবগুড়া সদর, বগুড়া।", parse_mode='Markdown')
    elif text == 'অর্ডার পদ্ধতি 🛒':
        await update.message.reply_text("🛒 পছন্দের জুতা সিলেক্ট করে 'অর্ডার করুন' বাটনে ক্লিক করে তথ্যগুলো দিন।")
    elif text == 'যোগাযোগ ও রিভিউ 📞':
        await update.message.reply_text(f"📞 মেসেজ দিন: @{MY_USERNAME}")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'back_to_menu':
        await query.message.delete()
        keyboard = [[InlineKeyboardButton("স্পোর্টস জুতা 👟", callback_data='sports')], [InlineKeyboardButton("ফর্মাল জুতা 👞", callback_data='formal')]]
        await query.message.reply_text("কোন ধরণের জুতা দেখতে চাচ্ছেন?", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    shoe = SHOE_DATA.get(query.data)
    if shoe:
        caption = f"👟 *মডেল:* {shoe['name']}\n💰 *দাম:* {shoe['price']}\n📏 *সাইজ:* {shoe['sizes']}\n\n📝 {shoe['details']}"
        keyboard = [[InlineKeyboardButton("🛒 অর্ডার করুন", url=f"https://t.me/{MY_USERNAME}")], [InlineKeyboardButton("⬅️ ব্যাকে যান", callback_data='back_to_menu')]]
        await query.message.reply_photo(photo=shoe['image'], caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        await query.message.delete()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messages))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()
