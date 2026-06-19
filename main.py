import bot

# identificador del usuario que interactua con el chatbot
chat_id = 1

# mensaje inicial del programa
print("=== chatbot del consultorio ===")
print("Escriba 'salir' para terminar.\n")

# bucle principal del chatbot
while True:

    # lee el mensaje ingresado por el usuario
    mensaje = input("Vos: ")

    # permite finalizar la conversacion
    if mensaje.lower() == "salir":
        print("Bot: Hasta luego.")
        break

    # envia el mensaje al chatbot para que lo procese
    respuesta = bot.procesar_mensaje(chat_id, mensaje)

    # muestra la respuesta generada por el bot
    print("\nBot:", respuesta)
    print()

