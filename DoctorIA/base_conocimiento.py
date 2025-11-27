# base_conocimiento.py

ENFERMEDADES = {
    # RESPIRATORIAS (Diferenciadas)
    "Gripa Común": {
        "escurrimiento nasal", "estornudos", "dolor de garganta", 
        "ojos llorosos", "cuerpo cortado", "tos leve"
    },
    "Influenza (Flu)": {
        "fiebre alta repentina", "dolor muscular intenso", "dolor de cabeza fuerte", 
        "cansancio extremo", "tos seca", "escalofríos"
    },
    "COVID-19": {
        "perdida de olfato", "perdida de gusto", "dificultad para respirar", 
        "tos seca persistente", "fiebre", "fatiga"
    },
    "Bronquitis": {
        "tos con flema", "silbido al respirar", "presion en el pecho", 
        "fatiga leve", "dificultad para respirar leve"
    },
    "Amigdalitis": {
        "dolor de garganta intenso", "dificultad para tragar", "fiebre", 
        "ganglios inflamados", "placas de pus"
    },
    "Sinusitis": {
        "dolor facial", "congestion nasal", "dolor de cabeza frontal", 
        "perdida de olfato", "mal aliento"
    },

    # DIGESTIVAS
    "Gastritis": {
        "ardor estomacal", "acidez", "dolor en la boca del estomago", 
        "nauseas", "sensacion de plenitud"
    },
    "Gastroenteritis (Infección)": {
        "diarrea liquida", "vomito", "retortijones", 
        "fiebre baja", "nauseas", "deshidratacion"
    },
    "Colitis": {
        "inflamacion abdominal", "gases", "estreñimiento o diarrea", 
        "dolor abdominal punzante"
    },

    # OTRAS
    "Migraña": {
        "dolor de cabeza unilateral", "sensibilidad a la luz", 
        "nauseas", "vision borrosa", "pulsaciones en la cabeza"
    },
    "Infección Urinaria": {
        "ardor al orinar", "necesidad frecuente de orinar", 
        "orina turbia", "dolor pelvico", "sensacion de no terminar de orinar"
    },
    "Deshidratación": {
        "boca seca", "sed intensa", "orina oscura", 
        "mareo", "piel seca", "fatiga"
    },
    "Alergia Estacional": {
        "estornudos frecuentes", "picazon en nariz", 
        "ojos rojos", "lagrimeo", "goteo nasal claro"
    },
    
    "Dengue": {
        "fiebre alta", "dolor detras de los ojos", "dolor articular severo", 
        "sarpullido", "dolor muscular", "nauseas"
    },
    "Varicela": {
        "ampollas en la piel", "comezon intensa", "costras", 
        "fiebre", "cansancio", "dolor de cabeza"
    },

    # OJOS Y OÍDOS
    "Conjuntivitis": {
        "ojos rojos", "lagañas o secrecion", "sensacion de arena en ojos", 
        "parpados pegados", "lagrimeo", "picazon en ojos"
    },
    "Otitis (Oído)": {
        "dolor de oido punzante", "sensacion de oido tapado", "zumbido en oidos", 
        "fiebre", "secrecion del oido", "mareo"
    },

    # CRÓNICAS / METABÓLICAS (Signos de alarma)
    "Diabetes (Posible descontrol)": {
        "mucha sed", "orinar muy frecuente", "mucha hambre", 
        "perdida de peso repentina", "vision borrosa", "fatiga", "boca seca"
    },
    "Hipertensión (Crisis)": {
        "zumbido en oidos", "ver lucesitas", "dolor de nuca", 
        "mareo", "palpitaciones", "dolor de cabeza fuerte"
    }
}