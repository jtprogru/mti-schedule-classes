import datetime
import logging

from telegram import ForceReply, Update
from telegram.ext import ContextTypes
import parser
import config


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    msg = """
    /help – показать эту справку
    /today <group_number> – показать расписание на сегодня для группы
    """
    await update.message.reply_text(msg)


async def groups_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    msg = """
    /help – показать эту справку
    /today <group_number> – показать расписание на сегодня для группы
    """
    await update.message.reply_text(msg)


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    group_number = int(update.message.text.split(" ")[1])
    sched = parser.run(datetime.date.today().strftime(config.DATE_FORMAT), group_number)
    logger.debug("", sched)
    msg = f"<b>Дата: {sched['day'].strftime(config.DATE_FORMAT)}</b>\n"
    classes = ""
    for lesson in sched['classess']:
        kt = list(lesson.keys())[0]
        classes += "Время: {}\nПредмет: {}\nАудитория: {}\n".format(kt, lesson[kt]['lecture'], lesson[kt]['class_room'])
    msg += classes
    await update.message.reply_text(text=msg, parse_mode='html')

