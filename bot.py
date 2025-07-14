import logging
from datetime import datetime
from pathlib import Path
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ======= ЛОГИРОВАНИЕ ==========
BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "easycash_bot.log"

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8', mode='a')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)

    logger.info("✅ Логирование включено. Лог-файл: %s", LOG_FILE)
    return logger

logger = setup_logging()

# ======= КОНФИГ ==========
TOKEN = "7640066117:AAE9YxmQylPm2F63BOjEn8vxMQHfNLKvB7A"
ADMIN_ID = 752119100
WELCOME_IMAGE = BASE_DIR / "images/welcome.png"
SIGNAL_IMAGE = BASE_DIR / "images/welcome.png"

bot_stats = {
    "total_users": set(),
    "active_sessions": set(),
    "signals_sent": 0,
    "help_requests": 0,
    "stats_requests": 0
}

# ======= ОБРАБОТЧИКИ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        logger.info(f"Новый пользователь: ID={user.id}, Имя={user.first_name}")
        bot_stats["total_users"].add(user.id)
        bot_stats["active_sessions"].add(update.effective_chat.id)

        keyboard = [
            [InlineKeyboardButton("📚 Инструкция", callback_data="instruction")],
            [InlineKeyboardButton("🚀 Получить сигнал", callback_data="get_signal")],
            [InlineKeyboardButton("🆘 Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(WELCOME_IMAGE, 'rb') as photo:
            await update.message.reply_photo(
                photo=InputFile(photo),
                caption=f"👋{user.first_name}, Добро пожаловать в <b>EASYCASH SOFT BOT</b>!\n\n"
                        "💣 В боте представлено 20 игр: Mines, Luckyjet, Coinflip и другие с разнообразным геймплеем, где можно испытать удачу.\n\n"
                        "🤖 Этот бот основан на передовой технологии искусственного интеллекта - Chat GPT 4o, предсказывая ходы с высокой точностью.",
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error(f"Ошибка в start: {str(e)}", exc_info=True)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        logger.info(f"Обработка callback: {query.data} от {query.from_user.id}")
        if query.data == "get_signal":
            bot_stats["signals_sent"] += 1
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="menu")]]
            
            with open(SIGNAL_IMAGE, 'rb') as photo:
                await query.message.reply_photo(
                    photo=InputFile(photo),
                    caption=(
                        "👑 Привет! Для активации бота пройди быструю <a href='https://1wilib.life/casino/list?open=register&p=1vph'>регистрацию на 1WIN (CLICK)</a>.\n\n"
                        "⚠️ Важно создать <b>новый аккаунт</b> по ссылке — по ранее неиспользованному номеру телефона, "
                        "а также <b>без социальных сетей</b>. Если у тебя уже есть аккаунт на <a href='https://1wilib.life/casino/list?open=register&p=1vph'>1WIN</a>, выйди из него.\n\n"
                        "1. Нажми на слово <a href='https://1wilib.life/casino/list?open=register&p=1vph'>Зарегистрироваться</a>, включи режим <b>инкогнито</b> и перейди на сайт.\n"
                        "2. При регистрации обязательно введи промо-код <b>EASYCASINO</b>.\n"
                        "3. Пополни баланс (рекомендуется от 2000 ₽).\n"
                        "4. Перейди в раздел 1WIN Games и выбери игру.\n"
                        "5. Нажми «Получить сигнал» в меню.\n"
                        "(⚠️ Если вы зарегестрировались, но бот вас не видит - попробуйте сделать несколько ставок или написать хелперу)"
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="HTML"
                )

        elif query.data == "instruction":
            bot_stats["help_requests"] += 1
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="menu")]]
            await query.message.reply_text(
                text=(
                    "📝 <b>Инструкция по сигналам</b>\n\n"
                    "1. Зайдите в раздел 1win games и выберите игру нужную вам.\n"
                    "2. Установите количество ловушек: зависит от игры. Это очень важно!\n"
                    "3. Запросите сигнал в боте, указав, сколько ловушек вы поставили.\n"
                    "4. Если сигнал оказался неудачным, советуем увеличить ставку в два раза (Х²), чтобы компенсировать потери.\n\n"
                    "⚠️ <b>Важно</b>: не всегда стоит удваивать ставку. Иногда прогнозы имеют много звёздочек, и можно потерять банк, если не соблюдать дисциплину.\n\n"
                    "Попробуйте использовать нашего бота уже сегодня и посмотрите, как ваш капитал будет расти! 💹"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )

        elif query.data == "help":
            bot_stats["help_requests"] += 1
            keyboard = [
                [InlineKeyboardButton("📞 Написать хелперу", url="https://t.me/easycash_helper")],
                [InlineKeyboardButton("🔙 Назад", callback_data="menu")]
            ]
            await query.message.reply_text(
                text="🆘 Помощь\n\nПо всем вопросам обращайтесь к @easycash_helper",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=None
            )

        elif query.data == "menu":
            user = query.from_user
            keyboard = [
                [InlineKeyboardButton("📚 Инструкция", callback_data="instruction")],
                [InlineKeyboardButton("🚀 Получить сигнал", callback_data="get_signal")],
                [InlineKeyboardButton("🆘 Помощь", callback_data="help")]
            ]
            with open(WELCOME_IMAGE, 'rb') as photo:
                await query.message.reply_photo(
                    photo=InputFile(photo),
                    caption=f"👋{user.first_name}, Добро пожаловать в <b>EASYCASH SOFT BOT</b>!\n\n"
                            "💣 В боте представлено 20 игр: Mines, Luckyjet, Coinflip и другие с разнообразным геймплеем, где можно испытать удачу.\n\n"
                            "🤖 Этот бот основан на передовой технологии искусственного интеллекта - Chat GPT 4o, предсказывая ходы с высокой точностью.",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="HTML"
                )
            await query.message.delete()

    except Exception as e:
        logger.error(f"Ошибка обработки callback: {str(e)}", exc_info=True)
        await query.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if user.id != ADMIN_ID:
            await update.message.reply_text("🚫 Доступ запрещен")
            return

        stats_text = (
            "<b>📊 Статистика бота:</b>\n\n"
            f"👥 Пользователей: {len(bot_stats['total_users'])}\n"
            f"🟢 Активных чатов: {len(bot_stats['active_sessions'])}\n"
            f"📨 Отправлено сигналов: {bot_stats['signals_sent']}\n"
            f"🆘 Запросов помощи: {bot_stats['help_requests']}\n\n"
            f"🕒 Последнее обновление: {datetime.now().strftime('%H:%M:%S')}"
        )
        await update.message.reply_text(stats_text, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Ошибка в stats: {str(e)}")

# ======= ЗАПУСК ==========
def main():
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("stats", stats))
        app.add_handler(CallbackQueryHandler(button_handler))
        logger.info("🔄 Бот запущен, ожидаем команды...")
        app.run_polling()
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
        print(f"🔴 Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()
