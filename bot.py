import database

# guarda el estado actual de cada usuario
_estados_usuarios = {}

# guarda datos temporales durante la conversacion
_sesiones_temporales = {}

def procesar_mensaje(chat_id, mensaje_usuario):

    # elimina espacios al principio y al final del mensaje
    mensaje = mensaje_usuario.strip()

    # obtiene el estado actual del usuario
    estado = _estados_usuarios.get(chat_id, "ESTADO_INICIAL")

    # estado inicial del chatbot
    if estado == "ESTADO_INICIAL":

        # cambia el estado para esperar una fecha
        _estados_usuarios[chat_id] = "ESPERANDO_FECHA"

        # obtiene las fechas disponibles desde la base de datos
        fechas = ", ".join(database.obtener_fechas_disponibles())

        return (
            "¡Hola! Bienvenido al asistente virtual del consultorio.\n"
            f"Por favor, indique la fecha para su consulta.\n"
            f"Fechas disponibles: {fechas}"
        )

    # espera que el usuario ingrese una fecha
    elif estado == "ESPERANDO_FECHA":

        # verifica que la fecha exista
        if mensaje not in database.obtener_fechas_disponibles():
            return "La fecha ingresada no es válida o no tiene turnos cargados."

        # obtiene los horarios libres para esa fecha
        horarios = database.obtener_horarios_libres(mensaje)

        # verifica si quedan horarios disponibles
        if len(horarios) == 0:
            return "No quedan horarios disponibles para esa fecha."

        # guarda temporalmente la fecha elegida
        _sesiones_temporales[chat_id] = {"fecha": mensaje}

        # cambia el estado para esperar un horario
        _estados_usuarios[chat_id] = "ESPERANDO_HORA"

        # convierte la lista de horarios en texto
        opciones = "\n".join(horarios)

        return (
            f"Horarios disponibles para {mensaje}:\n"
            f"{opciones}\n"
            "Escriba uno de los horarios."
        )

    # espera que el usuario seleccione un horario
    elif estado == "ESPERANDO_HORA":

        # recupera la fecha elegida anteriormente
        fecha = _sesiones_temporales[chat_id]["fecha"]

        # obtiene los horarios disponibles de esa fecha
        horarios = database.obtener_horarios_libres(fecha)

        # verifica que el horario ingresado sea valido
        if mensaje not in horarios:
            return "Horario inválido. Ingrese uno de los horarios mostrados."

        # guarda temporalmente el horario elegido
        _sesiones_temporales[chat_id]["hora"] = mensaje

        # cambia el estado para pedir los datos del paciente
        _estados_usuarios[chat_id] = "ESPERANDO_DATOS"

        return (
            "Horario pre-reservado.\n"
            "Ingrese sus datos en formato:\n"
            "Nombre Apellido, DNI"
        )

    # espera que el usuario ingrese sus datos
    elif estado == "ESPERANDO_DATOS":

        # verifica que los datos tengan el formato correcto
        if "," not in mensaje:
            return "Formato incorrecto. Ejemplo: Juan Perez, 20123456"

        # recupera la fecha y hora elegidas
        fecha = _sesiones_temporales[chat_id]["fecha"]
        hora = _sesiones_temporales[chat_id]["hora"]

        # intenta reservar el turno en la base de datos
        exito = database.verificar_y_reservar(fecha, hora, mensaje)

        if exito:
            # CONSISTENCIA BPMN: resetea el estado para simular el fin del proceso
            _estados_usuarios[chat_id] = "ESTADO_INICIAL"

            return (
                "¡Turno confirmado!\n"
                f"Fecha: {fecha}\n"
                f"Hora: {hora}\n"
                f"Paciente: {mensaje}\n\n"
                "Proceso finalizado con éxito. Si desea una nueva cita, envíe un mensaje."
            )
        else:
            # CONSISTENCIA BPMN: el desvío del 'no' en el diagrama vuelve a los horarios de la misma fecha
            _estados_usuarios[chat_id] = "ESPERANDO_HORA"
            horarios = database.obtener_horarios_libres(fecha)
            opciones = "\n".join(horarios)

            return (
                "Disculpe, el horario seleccionado acaba de ser reservado por otro usuario.\n"
                f"Horarios que aún quedan disponibles para el {fecha}:\n{opciones}\n"
                "Por favor, escriba otra de las opciones."
            )

