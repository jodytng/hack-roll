import logging
import pyrebase
from main import *

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

NAME, PHOTO, RELIGION, STYLE, CASKET, MENU, SONG, SPEAKERS, PARTING_WORDS, REPLAN, ARRANGEMENT, ADD_FRIEND = range(12)

#global dictionary to store users
users = {}

## to upload photos onto firestore db
config = {
    "apiKey": "AIzaSyCYUi7-aoID4y4tc1c3kpDZ8vgUq5__abY",
    "authDomain": "jodofiofe.firebaseapp.com",
    "databaseURL": "https://jodofiofe-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "jodofiofe",
    "storageBucket": "jodofiofe.appspot.com",
    "messagingSenderId": "81826383063",
    "appId": "1:81826383063:web:d4ed506b8b30da70d69c92",
    "serviceAccountKey": "serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for user's name."""
    ## MAKE SURE THE USER IS NOT PREEXISTING IN THE DATABASE
    user = update.message.from_user
    username = user.username # unique username of telegram user
    doc_ref = db.collection('Dead').document(username)
    doc = doc_ref.get()

    #store user in global space so that we can send messages later
    users[username] = user.id

    if not doc.exists:
        await update.message.reply_text(
            "Hi! My name is everybodyDiesBot. I will help you plan your virtual funeral. "
            "Send /cancel to stop talking to me.\n\n"
            "What is your full name?"
        )

        return NAME
    else:
        reply_keyboard = [["Yes", "No"]]
        await update.message.reply_text(
            "It seems that you have already planned your funeral. Do you want to re-plan your funeral?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Re-plan?"
                ),
        )

        return REPLAN

async def replan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Deletes data entry if user wants to replan, else end conversation"""
    user = update.message.from_user
    username = user.username
    if update.message.text == "Yes":
        db.collection('Dead').document(username).delete()
        chat_id = update.message.chat_id
        job_removed = remove_job_if_exists(str(chat_id), context)
        await update.message.reply_text(
            "Your previous plan has been deleted! /start again to plan your funeral again.",
            reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("Sure! Your previous plan will be kept.")
        
    return ConversationHandler.END

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores user's name and asks for photo"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    fullname = update.message.text # full name entered by telegram user

    db.collection('Dead').document(username).set({'name': fullname}) ## enter name into db
    await update.message.reply_text(
        "Great! Now, send me your photo please."
    )

    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo of user and asks for religion"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    
    ## enter photo into db
    storage.child(username).put("user_photo.jpg")

    reply_keyboard = [["Buddhist", "Christian"], ["Roman Catholic", "Taoist"], ["Others"]]
    await update.message.reply_text(
        "Next, what is your religion?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Religion?"
        ),
    )

    return RELIGION

async def religion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores religion of user and asks for style"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Religion of %s: %s", user.first_name, update.message.text)
    religion = update.message.text # religion entered by telegram user
    db.collection('Dead').document(username).update({'religion': religion}) ## enter religion into db


    reply_keyboard = [["Default", "Dark Mode"], ["Party", "Tropical"]]
    await update.message.reply_text(
        "I see! What style would you like your funeral to be?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Style?"
        ),
    )
    return STYLE

async def style(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores funeral style and asks for flower arrangement"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Funeral Style of %s: %s", user.first_name, update.message.text)
    style = update.message.text # style entered by telegram user
    db.collection('Dead').document(username).update({'style': style}) ## enter style into db

    reply_keyboard = [["Yellow", "Red"], ["White", "Colorful"], ["Pink", "Blue"]]
    await update.message.reply_text(
        "Great taste! What kind of flower arrangement will you like?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Flower Arrangement?"
        ),
    )
    return ARRANGEMENT

async def arrangement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores flower arrangement and asks for casket"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Flower Arrangement of %s: %s", user.first_name, update.message.text)
    arrgmt = update.message.text # flower arrangement entered by telegram user
    db.collection('Dead').document(username).update({'arrangement': arrgmt}) ## enter arrangement into db

    reply_keyboard = [["One", "Two"], ["Three", "Four"]]
    await update.message.reply_text(
        "Great taste! Which casket do you like?\n\n"
        "Check out our caskets here (do give us some time to load):",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Casket Number?"
        ),
    )
    await update.message.reply_photo("caskets_reg/one.png", caption = "One")
    await update.message.reply_photo("caskets_reg/two.png", caption = "Two")
    await update.message.reply_photo("caskets_reg/three.png", caption = "Three")
    await update.message.reply_photo("caskets_reg/four.png", caption = "Four")
    return CASKET

async def casket(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores casket type and asks for menu"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Casket of %s: %s", user.first_name, update.message.text)

    casket = update.message.text # casket entered by telegram user
    db.collection('Dead').document(username).update({'casket': casket}) ## enter casket into db

    reply_keyboard = [["Western", "Chinese"], ["Vegetarian", "Halal"]]
    await update.message.reply_text(
        "That's a very nice casket! Next, what kind of menu do you want to offer to attendees?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Menu Choice?"
        ),
    )
    return MENU

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores user's menu choice and asks for song choice"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Menu choice of %s: %s", user.first_name, update.message.text)

    menu = update.message.text # menu entered by telegram user
    db.collection('Dead').document(username).update({'menu': menu}) ## enter menu into db

    await update.message.reply_text(
        "Now, what song do you want to be played at your funeral? "
        "Reply with a Spotify link, or /skip to skip",
        reply_markup=ReplyKeyboardRemove(),
    )

    return SONG

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores user's song choice and asks for Eulogy speakers"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Song choice of %s: %s", user.first_name, update.message.text)

    song = update.message.text # song entered by telegram user
    db.collection('Dead').document(username).update({'song': song}) ## enter song into db

    await update.message.reply_text(
        "Great song! Next, who do you want as your eulogy speakers?",
    )

    return SPEAKERS

async def skip_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips song choice and asks for Eulogy speakers"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("User %s did not send a song choice.", user.first_name)

    db.collection('Dead').document(username).update({'song': None}) ## enter empty song into db

    await update.message.reply_text(
        "Next, who do you want as your eulogy speakers?"
    )

    return SPEAKERS

async def speakers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores string of eulogy speakers and asks for final parting words"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Eulogy speakers for %s: %s", user.first_name, update.message.text)

    speakers = update.message.text # speakers entered by telegram user
    db.collection('Dead').document(username).update({'speakers': speakers}) ## enter speakers into db

    await update.message.reply_text(
        "Lastly, what are your parting words?"
    )

    return PARTING_WORDS

async def parting_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores string parting words and asks for friends"""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("Parting words for %s: %s", user.first_name, update.message.text)

    partingWords = update.message.text # parting words entered by telegram user
    db.collection('Dead').document(username).update({'partingWords': partingWords}) ## enter parting words into db

    await update.message.reply_text(
        "Who do you want to send the invitation to? (Enter the telehandles without '@', separated with empty space)\n\n"
        "Take note that invitees should be users of this bot"
    )
    return ADD_FRIEND

async def add_friend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Add friend and end convo"""
    handles = update.message.text
    friends = handles.split(" ")
    user = update.message.from_user
    username = user.username

    #add delayed message
    chat_id = update.effective_message.chat_id
    #in case job exists
    job_removed = remove_job_if_exists(str(chat_id), context)
    #set time in seconds
    due = 30
    context.job_queue.run_once(send, due, chat_id=chat_id, name=str(chat_id), data = [friends, f"https://jodytng.github.io/#/f{username}/"])

    await update.message.reply_text("Thank you! Here's the link to your funeral. We will send this out to all your contacts after 7 days. /refresh regularly to delay your death!")
    await update.message.reply_text(f"https://jodytng.github.io/#/{username}/")

    return ConversationHandler.END

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> list:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return []
    for job in current_jobs:
        job.schedule_removal()
    return job.data

async def send(context: ContextTypes.DEFAULT_TYPE) -> None:
    """send link"""
    job = context.job
    friends = job.data[0]
    link = job.data[1]
    count = 0
    if(friends):
        for friend in friends:
            if friend in users.keys():
                count += 1
                await context.bot.send_message(users[friend], text=f"We would like to solemnly invite you to your friend's funeral: {link}")
    if(count == 0):
        await context.bot.send_message(job.chat_id, text="You have no friends using the bot :(")
    else:
        await context.bot.send_message(job.chat_id, text="We have sent out the invitations to your funeral. Rest In Peace.")
        await context.bot.send_sticker(job.chat_id, sticker="CAACAgIAAxkBAAGZkkVjwwNGyPqGy5r2HPIN9SqYm_tEqAAC4QADUomRIznBNrZHX5TMLQQ")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reset time when user presses reset"""
    user = update.message.from_user
    username = user.username
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    #set time in seconds
    due = 30
    context.job_queue.run_once(send, due, chat_id=chat_id, name=str(chat_id), data = job_removed)
    await update.message.reply_text("You are still alive! We have resetted your timer back to 7 days.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    username = user.username # unique username of telegram user
    logger.info("User %s canceled the conversation.", user.first_name)

    ## CHECK IF USER EXISTS IN DATABASE WHEN CANCELLING
    doc_ref = db.collection('Dead').document(username)
    doc = doc_ref.get()
    if doc.exists:
        db.collection('Dead').document(username).delete() ## delete user entry from db

    await update.message.reply_text(
        "Bye! I hope you die one day", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5815995673:AAGChfC32EfvGhO1fMC1pfFhUL6DpIx4SW0").build()

    #create handlers for reset
    application.add_handler(CommandHandler("refresh", reset))

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            PHOTO: [MessageHandler(filters.PHOTO, photo)], 
            RELIGION: [MessageHandler(filters.Regex("Buddhist|Christian|Roman Catholic|Taoist|Others"), religion)],
            STYLE: [MessageHandler(filters.Regex("Default|Dark Mode|Party|Tropical"), style)],
            CASKET: [MessageHandler(filters.Regex("One|Two|Three|Four"), casket)],
            MENU: [MessageHandler(filters.Regex("Western|Chinese|Vegetarian|Halal"), menu)],
            SONG: [MessageHandler(filters.TEXT & ~filters.COMMAND, song), CommandHandler("skip", skip_song)],
            SPEAKERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, speakers)],
            PARTING_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, parting_words)],
            REPLAN: [MessageHandler(filters.Regex("Yes|No"), replan)],
            ARRANGEMENT: [MessageHandler(filters.Regex("Yellow|Red|White|Colorful|Pink|Blue"), arrangement)],
            ADD_FRIEND: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_friend)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()