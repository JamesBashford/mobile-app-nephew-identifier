pip install python-telegram-bot

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fastai.vision.all import load_learner
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5105937010:AAGq0X4gqd6n_wMjzf8SMUPd-TaMSQcbdbw'


def start(update, context):
    update.message.reply_text(
        "Bot by Bashy \n\n "
        "Just send me a photo of Mikey or Danny and I will tell you which it is 😏"
    )


def help_command(update, context):
        update.message.reply_text('My only purpose is to tell you if a picture is of Mikey or Danny. Send a photo')



# def echo(update, context):
#     print(update)
#     print(context)
#     update.message.reply_text(update.message.text)


def load_model():
    global model
    model = load_learner('model/Mikey_Danny.pkl')
    print('Model loaded')


def detect_mask(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')

    label = model.predict('user_photo.jpg')[0]
    if label == "mikey":
        update.message.reply_text(
            "Oh yeah....that's a Marvellous Mikey alright!😉"
        )
    else:
        update.message.reply_text(
            "Clearly a Daniel Monster"
        )


def main():
    load_model()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.photo, detect_mask))

    dp.add_error_handler(error)
    
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)
    
    updater.idle()


if __name__ == '__main__':
    main()
