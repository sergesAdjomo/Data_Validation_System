# src/type_validator.py

import pandas as pd
from typing import List, Dict
import numpy as np
from datetime import datetime
from config.column_config import COLUMN_DEFINITIONS, FORMAT_TYPES

class TypeValidator:
    """Classe responsable de la validation des types de données"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialise le validateur de types
        
        Args:
            data (pd.DataFrame): DataFrame à valider
        """
        self.data = data
        self.errors: List[Dict] = []
        
    def validate_column_types(self) -> List[Dict]:
        """
        Vérifie les types de données pour chaque colonne
        
        Returns:
            List[Dict]: Liste des erreurs de type trouvées
        """
        self.errors = []
        
        for col, properties in COLUMN_DEFINITIONS.items():
            if col not in self.data.columns:
                continue
                
            expected_format = properties.get('format', 'string')
            
            # Ignore les valeurs nulles dans la validation
            non_null_mask = self.data[col].notna()
            values_to_check = self.data.loc[non_null_mask, col]
            
            if expected_format == 'datetime':
                self._validate_datetime(col, values_to_check)
            elif expected_format == 'int':
                self._validate_integer(col, values_to_check)
            elif expected_format == 'float':
                self._validate_float(col, values_to_check)
            elif expected_format == 'boolean':
                self._validate_boolean(col, values_to_check)
                
        return self.errors
    
    def _validate_datetime(self, col: str, values: pd.Series) -> None:
        """Valide les valeurs de type datetime"""
        for idx, value in values.items():
            if not isinstance(value, (pd.Timestamp, datetime)):
                try:
                    pd.to_datetime(value)
                except:
                    self.errors.append({
                        'colonne': col,
                        'ligne': idx,
                        'valeur': value,
                        'type_erreur': 'type_invalide',
                        'message': f"La valeur '{value}' n'est pas une date valide"
                    })
    
    def _validate_integer(self, col: str, values: pd.Series) -> None:
        """Valide les valeurs de type entier"""
        for idx, value in values.items():
            if not isinstance(value, (int, np.integer)) or pd.isna(value):
                try:
                    int_value = int(float(value))
                    if float(value) != int_value:
                        raise ValueError
                except:
                    self.errors.append({
                        'colonne': col,
                        'ligne': idx,
                        'valeur': value,
                        'type_erreur': 'type_invalide',
                        'message': f"La valeur '{value}' n'est pas un entier valide"
                    })
    
    def _validate_float(self, col: str, values: pd.Series) -> None:
        """Valide les valeurs de type float"""
        for idx, value in values.items():
            if not isinstance(value, (float, int, np.integer, np.float)):
                try:
                    float(value)
                except:
                    self.errors.append({
                        'colonne': col,
                        'ligne': idx,
                        'valeur': value,
                        'type_erreur': 'type_invalide',
                        'message': f"La valeur '{value}' n'est pas un nombre décimal valide"
                    })
    
    def _validate_boolean(self, col: str, values: pd.Series) -> None:
        """Valide les valeurs de type boolean"""
        valid_values = [True, False, 'VRAI', 'FAUX', 1, 0]
        for idx, value in values.items():
            if value not in valid_values:
                self.errors.append({
                    'colonne': col,
                    'ligne': idx,
                    'valeur': value,
                    'type_erreur': 'type_invalide',
                    'message': f"La valeur '{value}' n'est pas une valeur booléenne valide"
                })
    
    def suggest_column_types(self) -> Dict:
        """
        Suggère les types de données appropriés pour chaque colonne
        
        Returns:
            Dict: Dictionnaire des types suggérés
        """
        suggestions = {}
        
        for col in self.data.columns:
            if col in COLUMN_DEFINITIONS:
                expected_format = COLUMN_DEFINITIONS[col]['format']
                suggested_type = FORMAT_TYPES.get(expected_format, 'object')
                suggestions[col] = suggested_type
        
        return suggestions