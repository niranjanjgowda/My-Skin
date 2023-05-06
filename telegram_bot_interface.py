import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow import keras

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Send me a picture!')

def photo_handler(update: Update, context: CallbackContext) -> None:
    #add disease names in the order you are training them
    disease_names = {'Acne and Rosacea Photos': 0,
                     'Atopic Dermatitis Photos': 1,
                     'Melanoma Skin Cancer Nevi and Moles': 2,
                    'Warts Molluscum and other Viral Infections': 3
                    }
    photo = update.message.photo[-1]
    file_id = photo.file_id
    new_file = context.bot.get_file(file_id)
    new_file.download('image.jpg')
    img_path = "image.jpg"
    model = keras.models.load_model("model_path")
    img = image.load_img(img_path, target_size=(300, 300))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 300
    pred = model.predict(img_array)
    result = np.argmax(pred[0])
    print(result)
    print([i for i,j in disease_names.items() if j == result])
    context.bot.send_message(chat_id=update.effective_chat.id, text=str([i for i,j in disease_names.items() if j == result][0]))
    os.remove("image.jpg")

def main():
    updater = Updater(token='your_telegram_api_key', use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    photo_handle = MessageHandler(Filters.photo, photo_handler)
    dispatcher.add_handler(photo_handle)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()