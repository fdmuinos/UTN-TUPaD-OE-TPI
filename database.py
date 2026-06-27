import csv

# nombre del archivo csv que se usa como base de datos
ARCHIVO = "turnos.csv"

def cargar_turnos():

    # diccionario donde se guardan los turnos cargados
    turnos = {}

    # abre el archivo csv en modo lectura
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:

        # lee el csv usando la primera fila como encabezado
        lector = csv.DictReader(archivo)

        for fila in lector:

            # obtiene la fecha y hora de cada fila
            fecha = fila["fecha"].strip()
            hora = fila["hora"].strip()

            # si la fecha no existe en el diccionario se crea
            if fecha not in turnos:
                turnos[fecha] = {}

            # guarda la informacion del turno
            turnos[fecha][hora] = {
                "disponible": fila["disponible"].strip().upper() == "TRUE",
                "id": int(fila["id"]),
                "paciente": fila["paciente"].strip() if fila["paciente"] else None
            }

    # devuelve todos los turnos cargados
    return turnos


def guardar_turnos(turnos):

    # abre el csv en modo escritura para actualizarlo
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:

        campos = ["fecha", "hora", "disponible", "id", "paciente"]

        escritor = csv.DictWriter(archivo, fieldnames=campos)

        # escribe los encabezados del csv
        escritor.writeheader()

        # recorre todos los turnos y los guarda
        for fecha in turnos:
            for hora in turnos[fecha]:

                datos = turnos[fecha][hora]

                escritor.writerow({
                    "fecha": fecha,
                    "hora": hora,
                    "disponible": datos["disponible"],
                    "id": datos["id"],
                    "paciente": datos["paciente"] if datos["paciente"] else ""
                })


def obtener_fechas_disponibles():

    # carga los turnos y devuelve las fechas
    turnos = cargar_turnos()

    return list(turnos.keys())


def obtener_horarios_libres(fecha):

    # carga los turnos desde el csv
    turnos = cargar_turnos()

    # si la fecha no existe devuelve lista vacia
    if fecha not in turnos:
        return []

    # devuelve solo los horarios disponibles
    return [
        hora
        for hora, datos in turnos[fecha].items()
        if datos["disponible"]
    ]


def verificar_y_reservar(fecha, hora, datos_paciente):

    # carga los turnos actuales
    turnos = cargar_turnos()

    # verifica que la fecha y hora existan
    if fecha in turnos and hora in turnos[fecha]:

        # verifica que el turno siga libre
        if turnos[fecha][hora]["disponible"]:

            # cambia el estado a ocupado
            turnos[fecha][hora]["disponible"] = False

            # guarda los datos del paciente
            turnos[fecha][hora]["paciente"] = datos_paciente

            # actualiza el csv con los nuevos datos
            guardar_turnos(turnos)

            return True

    # devuelve false si no pudo reservar
    return False

