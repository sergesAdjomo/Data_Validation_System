# src/rules_validator.py

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config.column_config import SPECIFIC_RULES

class RulesValidator:
    """
    Classe responsable de la validation des règles métier spécifiques.
    Implémente les contrôles complexes décrits dans la documentation.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialise le validateur de règles spécifiques
        
        Args:
            data (pd.DataFrame): DataFrame à valider
        """
        self.data = data
        self.errors: List[Dict] = []
        
    def validate_all_rules(self) -> List[Dict]:
        """
        Exécute toutes les validations de règles spécifiques
        
        Returns:
            List[Dict]: Liste complète des erreurs trouvées
        """
        self.errors = []
        
        # Validation des règles pour chaque ligne
        for idx, row in self.data.iterrows():
            # Validation du numéro de limitation
            self._validate_limitation_number(row, idx)
            
            # Validation du type de requête
            self._validate_request_type(row, idx)
            
            # Validation du statut de limitation
            self._validate_limitation_status(row, idx)
            
            # Validation de la requête NAZA
            self._validate_naza_request(row, idx)
            
            # Validation de l'indemnisation
            self._validate_compensation(row, idx)
            
            # Validation des durées
            self._validate_durations(row, idx)
            
        return self.errors
    
    def _validate_limitation_number(self, row: pd.Series, idx: int) -> None:
        """Valide les règles spécifiques au numéro de limitation"""
        if pd.isna(row.get('N° LIMITATION')):
            return
            
        # Vérification des doublons selon les critères spécifiés
        duplicate_mask = (
            (self.data['CONSIGNE LIMITATION (MW)'] == row['CONSIGNE LIMITATION (MW)']) &
            (self.data['DATE DEBUT REALISEE'] == row['DATE DEBUT REALISEE']) &
            (self.data['DATE FIN REALISEE'] == row['DATE FIN REALISEE']) &
            (self.data['IDR POSTE'] == row['IDR POSTE'])
        )
        
        if duplicate_mask.sum() > 1:
            self.errors.append({
                'colonne': 'N° LIMITATION',
                'ligne': idx,
                'type_erreur': 'doublon',
                'message': f"Doublon détecté pour la limitation {row['N° LIMITATION']}"
            })
    
    def _validate_request_type(self, row: pd.Series, idx: int) -> None:
        """Valide les règles concernant le type de requête"""
        num_limitation = str(row.get('N° LIMITATION', ''))
        type_requete = row.get('TYPE REQUETE')
        
        if pd.isna(type_requete):
            return
            
        if num_limitation.startswith('ALZ -'):
            if type_requete != 'Automatique':
                self.errors.append({
                    'colonne': 'TYPE REQUETE',
                    'ligne': idx,
                    'type_erreur': 'type_invalide',
                    'message': "Le type de requête doit être 'Automatique' pour une limitation ALZ"
                })
        else:
            if type_requete != 'Manuelle':
                self.errors.append({
                    'colonne': 'TYPE REQUETE',
                    'ligne': idx,
                    'type_erreur': 'type_invalide',
                    'message': "Le type de requête doit être 'Manuelle' pour une limitation non-ALZ"
                })
    
    def _validate_limitation_status(self, row: pd.Series, idx: int) -> None:
        """Valide les règles concernant le statut de limitation"""
        status = row.get('STATUT LIMITATION')
        if pd.isna(status):
            return
            
        date_debut_demandee = pd.notna(row.get('DATE DEBUT DEMANDEE'))
        date_debut_prevue = pd.notna(row.get('DATE DEBUT PREVUE'))
        
        expected_status = None
        if date_debut_demandee and not date_debut_prevue:
            expected_status = 'mise en œuvre en temps réel'
        elif not date_debut_demandee and date_debut_prevue:
            expected_status = 'planifiée et non mise en œuvre'
        elif date_debut_demandee and date_debut_prevue:
            expected_status = 'planifiée et mise en œuvre'
            
        if expected_status and status != expected_status:
            self.errors.append({
                'colonne': 'STATUT LIMITATION',
                'ligne': idx,
                'type_erreur': 'statut_invalide',
                'message': f"Le statut devrait être '{expected_status}'"
            })
    
    def _validate_naza_request(self, row: pd.Series, idx: int) -> None:
        """Valide les règles concernant les requêtes NAZA"""
        num_limitation = str(row.get('N° LIMITATION', ''))
        requete_naza = row.get('REQUETE NAZA (VRAI/FAUX)')
        
        if pd.isna(requete_naza):
            return
            
        if num_limitation.startswith('ALZ -'):
            if requete_naza != 'VRAI':
                self.errors.append({
                    'colonne': 'REQUETE NAZA (VRAI/FAUX)',
                    'ligne': idx,
                    'type_erreur': 'valeur_invalide',
                    'message': "La requête NAZA doit être VRAI pour une limitation ALZ"
                })
        else:
            if requete_naza != 'FAUX':
                self.errors.append({
                    'colonne': 'REQUETE NAZA (VRAI/FAUX)',
                    'ligne': idx,
                    'type_erreur': 'valeur_invalide',
                    'message': "La requête NAZA doit être FAUX pour une limitation non-ALZ"
                })
    
    def _validate_compensation(self, row: pd.Series, idx: int) -> None:
        """Valide les règles concernant l'indemnisation"""
        status = row.get('STATUT LIMITATION')
        indemnisable = row.get('INDEMNISABLE (VRAI/FAUX)')
        
        if pd.isna(indemnisable):
            return
            
        if status == 'planifiée et mise en œuvre':
            if indemnisable != 'VRAI':
                self.errors.append({
                    'colonne': 'INDEMNISABLE (VRAI/FAUX)',
                    'ligne': idx,
                    'type_erreur': 'valeur_invalide',
                    'message': "L'indemnisation doit être VRAI pour une limitation planifiée et mise en œuvre"
                })
        else:
            if indemnisable != 'FAUX':
                self.errors.append({
                    'colonne': 'INDEMNISABLE (VRAI/FAUX)',
                    'ligne': idx,
                    'type_erreur': 'valeur_invalide',
                    'message': "L'indemnisation doit être FAUX pour les autres statuts"
                })
    
    def _validate_durations(self, row: pd.Series, idx: int) -> None:
        """Valide les règles concernant les durées"""
        status = row.get('STATUT LIMITATION')
        
        if status in ['planifiée et mise en œuvre', 'planifiée et non mise en œuvre']:
            if pd.isna(row.get('DUREE PREVUE (HEURES)')):
                self.errors.append({
                    'colonne': 'DUREE PREVUE (HEURES)',
                    'ligne': idx,
                    'type_erreur': 'valeur_manquante',
                    'message': "La durée prévue est obligatoire pour ce statut"
                })
                
        if status in ['planifiée et mise en œuvre', 'mise en œuvre en temps réel']:
            if pd.isna(row.get('DUREE DEMANDEE (HEURES)')):
                self.errors.append({
                    'colonne': 'DUREE DEMANDEE (HEURES)',
                    'ligne': idx,
                    'type_erreur': 'valeur_manquante',
                    'message': "La durée demandée est obligatoire pour ce statut"
                })
            
            if pd.isna(row.get('DUREE REALISEE (HEURES)')):
                self.errors.append({
                    'colonne': 'DUREE REALISEE (HEURES)',
                    'ligne': idx,
                    'type_erreur': 'valeur_manquante',
                    'message': "La durée réalisée est obligatoire pour ce statut"
                })

    def get_validation_summary(self) -> pd.DataFrame:
        """
        Génère un résumé des erreurs de validation
        
        Returns:
            pd.DataFrame: Résumé des erreurs par type et colonne
        """
        if not self.errors:
            return pd.DataFrame()
            
        summary = pd.DataFrame(self.errors)
        grouped = summary.groupby(['colonne', 'type_erreur']).size().reset_index(name='count')
        return grouped.sort_values('count', ascending=False)