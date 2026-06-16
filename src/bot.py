"""
Motor Principal del Chatbot - Máquina de Estados Finitos
Cátedra: Organización Empresarial - UTN
"""

import database

# Registro transitorio de estados por usuario (Memoria del proceso administrativo)
# Mapea chat_id -> estado_actual
_estados_usuarios = {}
# Mapea chat_id -> datos_temporales_de_sesión
_sesiones_temporales = {}

def procesar_mensaje(chat_id, mensaje_usuario):
    mensaje = mensaje_usuario.strip()
    estado = _estados_usuarios.get(chat_id, "ESTADO_INICIAL")

    # ==========================================
    # GATEWAY: ESTADO INICIAL
    # ==========================================
    if estado == "ESTADO_INICIAL":
        _estados_usuarios[chat_id] = "ESPERANDO_FECHA"
        fechas = ", ".join(database.obtener_fechas_disponibles())
        return (f"¡Hola! Bienvenido al asistente virtual del consultorio.\n"
                f"Por favor, indique la fecha para su consulta. Fechas con agenda: [{fechas}]")

    # ==========================================
    # GATEWAY: ESPERANDO FECHA
    # ==========================================
    elif estado == "ESPERANDO_FECHA":
        # CAMINO INFELIZ: La fecha no existe en la base de datos o formato erróneo
        if mensaje not in database.obtener_fechas_disponibles():
            return "La fecha ingresada no es válida o no tiene turnos cargados. Por favor, intente de nuevo."
        
        # CAMINO FELIZ
        horarios = database.obtener_horarios_libres(mensaje)
        if not horarios:
            return "Lo sentimos, ya no quedan horarios disponibles para esa fecha. Indique otra."
        
        _sesiones_temporales[chat_id] = {"fecha": mensaje}
        _estados_usuarios[chat_id] = "ESPERANDO_HORA"
        
        opciones = "\n".join([f"- {h}" for h in horarios])
        return f"Para el día {mensaje}, seleccione uno de los siguientes horarios libres:\n{opciones}"

    # ==========================================
    # GATEWAY: ESPERANDO HORA
    # ==========================================
    elif estado == "ESPERANDO_HORA":
        fecha_sel = _sesiones_temporales[chat_id]["fecha"]
        horarios_libres = database.obtener_horarios_libres(fecha_sel)
        
        # CAMINO INFELIZ: Selección de un horario no listado o ya ocupado
        if mensaje not in horarios_libres:
            return "Horario inválido. Por favor, escriba exactamente una de las opciones del menú."
        
        # CAMINO FELIZ: Almacenamiento temporal en sesión
        _sesiones_temporales[chat_id]["hora"] = mensaje
        _estados_usuarios[chat_id] = "ESPERANDO_DATOS"
        return f"Horario {mensaje} pre-reservado. Para finalizar, ingrese sus datos en formato: Nombre Apellido, DNI"

    # ==========================================
    # GATEWAY: ESPERANDO DATOS
    # ==========================================
    elif estado == "ESPERANDO_DATOS":
        # CAMINO INFELIZ: Error de robustez si no ingresa la coma o datos muy cortos
        if "," not in mensaje or len(mensaje) < 10:
            return "Formato incorrecto. Por favor, ingrese: Nombre Apellido, DNI (ej: Juan Pérez, 20123456)."
        
        fecha_final = _sesiones_temporales[chat_id]["fecha"]
        hora_final = _sesiones_temporales[chat_id]["hora"]
        
        # Persistencia atómica en Base de Datos
        exito = database.verificar_y_reservar(fecha_final, hora_final, mensaje)
        
        if exito:
            _estados_usuarios[chat_id] = "TURNO_CONFIRMADO"
            return (f"¡Turno confirmado con éxito!\n"
                    f"Fecha: {fecha_final}\nHora: {hora_final} hs\nPaciente: {mensaje}\n"
                    f"¡Muchas gracias!")
            
        # CAMINO INFELIZ CONDICIONAL: Concurrencia de estrés (El turno se ocupó en ese segundo)
        else:
            _estados_usuarios[chat_id] = "ESPERANDO_FECHA"
            return "Disculpe, el turno acaba de ser tomado por otro usuario. Reiniciando selección de fecha."

    # ==========================================
    # REINICIO DEL CICLO
    # ==========================================
    elif estado == "TURNO_CONFIRMADO":
        _estados_usuarios[chat_id] = "ESTADO_INICIAL"
        return "Proceso finalizado. Si desea gestionar un nuevo turno, envíe cualquier mensaje."