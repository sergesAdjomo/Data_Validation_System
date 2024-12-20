# src/null_validator.py

import pandas as pd
from typing import List, Dict
import logging
from config.column_config import COLUMN_DEFINITIONS

class NullValidator:
    """Classe responsable de la validation des valeurs nulles"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialise le validateur de valeurs nulles
        
        Args:
            data (pd.DataFrame): DataFrame à valider
        """
        self.data = data
        self.errors: List[Dict] = []
        
    def validate_required_fields(self) -> List[Dict]:
        """
        Vérifie les champs obligatoires (non null)
        
        Returns:
            List[Dict]: Liste des erreurs trouvées
        """
        self.errors = []
        
        for col, properties in COLUMN_DEFINITIONS.items():
            if col not in self.data.columns:
                if properties.get('required', False):
                    self.errors.append({
                        'colonne': col,
                        'type_erreur': 'colonne_manquante',
                        'message': f"La colonne obligatoire '{col}' est manquante"
                    })
                continue
                
            if properties.get('required', False):
                null_indices = self.data[col].isnull()
                if null_indices.any():
                    null_rows = null_indices[null_indices].index.tolist()
                    self.errors.append({
                        'colonne': col,
                        'type_erreur': 'valeur_null',
                        'lignes_concernées': null_rows,
                        'message': f"Valeurs nulles trouvées dans la colonne obligatoire '{col}'"
                    })
        
        return self.errors
    
    def get_null_summary(self) -> pd.DataFrame:
        """
        Génère un résumé des valeurs nulles dans le DataFrame
        
        Returns:
            pd.DataFrame: Résumé des valeurs nulles
        """
        null_counts = self.data.isnull().sum()
        null_percentages = (null_counts / len(self.data)) * 100
        
        summary = pd.DataFrame({
            'Nombre_Null': null_counts,
            'Pourcentage_Null': null_percentages.round(2)
        })
        
        return summary.sort_values('Nombre_Null', ascending=False)
    
    def validate_conditional_nulls(self) -> List[Dict]:
        """
        Vérifie les règles conditionnelles pour les valeurs nulles
        
        Returns:
            List[Dict]: Liste des erreurs trouvées
        """
        # Exemple de validation conditionnelle
        if 'STATUT LIMITATION' in self.data.columns:
            mask_planifie = self.data['STATUT LIMITATION'] == 'planifiée et mise en œuvre'
            required_columns = ['DATE DEBUT PREVUE', 'DATE FIN PREVUE']
            
            for col in required_columns:
                if col in self.data.columns:
                    null_mask = self.data[col].isnull() & mask_planifie
                    if null_mask.any():
                        self.errors.append({
                            'colonne': col,
                            'type_erreur': 'valeur_null_conditionnelle',
                            'lignes_concernées': null_mask[null_mask].index.tolist(),
                            'message': f"Valeurs nulles non autorisées pour '{col}' quand le statut est 'planifiée et mise en œuvre'"
                        })
        
        return self.errors