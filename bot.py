
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

CANDLES = {
    "свежие": [
        ("Лимоный бриз", "🍋 мята, лимонный лист"),
        ("Солнечный мандарин", "🍊 бергамот, нероли, мандарин, морская соль"),
        ("Туманный рассвет", "🌫 озон, лимон, яблоко, шалфей, эвкалипт"),
        ("День в SPA", "💆 лемонграсс, чёрная смородина, пачули"),
        ("Солнечные цветы (верхние)", "☀️ бергамот, лимон, зелень")
    ],
    "травяные": [
        ("День в парке", "🌿 трава, базилик, шалфей, инжир"),
        ("Лес в полнолуние", "🌲 шалфей, кориандр, мох, ромашка"),
        ("Сандал и цветы", "🌼 лаванда, кувшинка, ромашка, сандал")
    ],
    "цветочные": [
        ("Солнечные цветы (сердце)", "🌸 иланг, гардения, тубероза, жасмин"),
        ("Морской туман (сердце)", "🌊 гардения, тубероза, жасмин самбак"),
        ("Лавандовый вечер", "💜 лаванда, мускатный орех, ваниль")
    ],
    "гурманские": [
        ("Абсент из черной смородины", "🍇 яблоко, смородина, ежевика, амбра, кедр"),
        ("Пряная роза", "🌹 розы, специи, бобы тонка, пачули"),
        ("Морской туман (база)", "🥥 кокос, миндаль, ладан"),
        ("День в парке (база)", "🪵 бобы тонка, гвоздика, сандал")
    ],
    "древесные": [
        ("Лес в полнолуние (база)", "🪵 дерево, бальзам, специи"),
        ("Пряная роза (база)", "🌶 пачули, бобы тонка"),
        ("Сандал и цветы", "🪵 сандал"),
        ("Лавандовый вечер (база)", "🍦 ваниль")
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕯 Привет! Я помогу тебе выбрать свечу.

"
        "🧠 Вопрос 1: А для какого настроения или момента вы хотите свечу?
"
        "(например: для сна, уюта, работы, романтики и т.д.)"
    )
    context.user_data["step"] = 1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step", 1)

    if step == 1:
        context.user_data["purpose"] = update.message.text
        context.user_data["step"] = 2
        keyboard = [
            [InlineKeyboardButton("🍋 Свежие", callback_data="свежие")],
            [InlineKeyboardButton("🌿 Травяные", callback_data="травяные")],
            [InlineKeyboardButton("🌸 Цветочные", callback_data="цветочные")],
            [InlineKeyboardButton("🍇 Гурманские", callback_data="гурманские")],
            [InlineKeyboardButton("🪵 Древесные", callback_data="древесные")],
        ]
        await update.message.reply_text(
            "👃 Вопрос 2: Какие ароматы вам больше по душе?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    response = f"✨ Подборка свечей категории *{category}* (2680₽ каждая):

"
    for name, desc in CANDLES[category]:
        response += f"• {name} — {desc}
"
    response += "
🛍 Заказать можно у @Kamilla_Chrome"
    await query.edit_message_text(response, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()

if __name__ == "__main__":
    main()
