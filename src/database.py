# -*- coding: utf-8 -*-
"""
Módulo de Persistencia y Base de Datos Simulada
Cátedra: Organización Empresarial - UTN
"""

# Base de datos simulada de la agenda del psicólogo (Persistencia de estados de turnos)
# True = Disponible, False = Ocupado
_db_turnos = {
    "25/06/2026": {
        "14:00": {"disponible": True, "id": 101, "paciente": None},
        "15:30": {"disponible": True, "id": 102, "paciente": None},
        "17:00": {"disponible": False, "id": 103, "paciente": "DNI 11223344"} # Simulación turno ocupado
    },
    "26/06/2026": {
        "09:00": {"disponible": True, "id": 201, "paciente": None},
        "10:30": {"disponible": True, "id": 202, "paciente": None}
    }
}

def obtener_fechas_disponibles():
    """Devuelve las fechas configuradas en la agenda."""
    return list(_db_turnos.keys())

def obtener_horarios_libres(fecha):
    """Filtra y devuelve los horarios que están marcados como disponibles."""
    if fecha not in _db_turnos:
        return []
    return [hora for hora, datos in _db_turnos[fecha].items() if datos["disponible"]]

def verificar_y_reservar(fecha, hora, datos_paciente):
    """
    Control de concurrencia (Gateway Crítico). 
    Verifica si el turno sigue libre antes de escribir de forma atómica.
    """
    if fecha in _db_turnos and hora in _db_turnos[fecha]:
        if _db_turnos[fecha][hora]["disponible"]:
            # Escritura y persistencia de la información
            _db_turnos[fecha][hora]["disponible"] = False
            _db_turnos[fecha][hora]["paciente"] = datos_paciente
            return True
    return False