# config/column_config.py

COLUMN_DEFINITIONS = {
    "DATE CENTRALISATION": {
        "format": "datetime",
        "required": True,
        "description": "Date de centralisation des données"
    },
    "REGION": {
        "format": "string",
        "required": True,
        "description": "Région concernée"
    },
    "N° LIMITATION": {
        "format": "string",
        "required": True,
        "description": "Numéro de la limitation"
    },
    "IDR POSTE": {
        "format": "string",
        "required": False,
        "description": "Identifiant du poste"
    },
    # Ajoutez les autres colonnes ici...
}

# Dictionnaire des formats acceptés et leurs validations
FORMAT_TYPES = {
    "datetime": "datetime64[ns]",
    "date": "datetime64[ns]",
    "string": "object",
    "int": "int64",
    "float": "float64",
    "boolean": "bool"
}

# Règles de validation spécifiques
SPECIFIC_RULES = {
    "TYPE REQUETE": {
        "values": ["Automatique", "Manuelle"],
        "condition": lambda x: x.startswith("ALZ -"),
        "expected": "Automatique"
    },
    "STATUT LIMITATION": {
        "values": [
            "planifiée et mise en œuvre",
            "mise en œuvre en temps réel",
            "planifiée et non mise en œuvre"
        ]
    }
}