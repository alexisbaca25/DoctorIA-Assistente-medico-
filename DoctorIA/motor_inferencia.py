# Archivo: motor_inferencia.py
from base_conocimiento import ENFERMEDADES

def diagnosticar(sintomas_paciente):
    """
    Recibe un conjunto (set) o lista de síntomas del paciente.
    Devuelve un diccionario con el diagnóstico más probable y detalles.
    """
    max_coincidencias = 0
    diagnostico_final = None
    detalles = []

    # Convertimos a set por si viene como lista
    sintomas_set = set(sintomas_paciente)

    for enfermedad, sintomas_enfermedad in ENFERMEDADES.items():
        # Intersección: síntomas que tiene el paciente Y la enfermedad
        coincidencias = len(sintomas_set.intersection(sintomas_enfermedad))
        total_sintomas_enfermedad = len(sintomas_enfermedad)
        
        # Calcular porcentaje
        porcentaje = 0
        if total_sintomas_enfermedad > 0:
            porcentaje = (coincidencias / total_sintomas_enfermedad) * 100

        detalles.append({
            "enfermedad": enfermedad,
            "coincidencias": coincidencias,
            "porcentaje": porcentaje
        })

        # Buscar el ganador (debe tener al menos 1 síntoma)
        if coincidencias > max_coincidencias and coincidencias > 0:
            max_coincidencias = coincidencias
            diagnostico_final = enfermedad

    # Ordenar detalles de mayor a menor porcentaje
    detalles.sort(key=lambda x: x["porcentaje"], reverse=True)

    return {
        "diagnostico": diagnostico_final,
        "detalles": detalles
    }