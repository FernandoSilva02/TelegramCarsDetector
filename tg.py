from telegram.ext import Updater, MessageHandler, filters
import cv2

# Función para procesar las imágenes recibidas
def process_image(update, context):
    # Obtener la imagen del mensaje
    file = context.bot.getFile(update.message.photo[-1].file_id)
    image_path = file.download('image.jpg')  # Guardar la imagen localmente

    # Cargar la imagen con OpenCV y aplicar detección de objetos con YOLOv5
    image = cv2.imread(image_path)
    # Aquí deberías integrar tu lógica para utilizar YOLOv5 en 'image'

    # Enviar respuesta al usuario con los resultados de la detección (por ejemplo, texto con objetos detectados)
    context.bot.send_message(chat_id=update.message.chat_id, text="Objetos detectados: [Lista de objetos detectados]")

def main():
    # Inicializar el bot con tu token
    updater = Updater(token='6742866921:AAHVjdEXLKuI9sc1KUO7juxeQDIkGZL_Tdg', use_context=True)
    dispatcher = updater.dispatcher

    # Manejar mensajes con imágenes
    photo_handler = MessageHandler(filters.photo, process_image)
    dispatcher.add_handler(photo_handler)

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
