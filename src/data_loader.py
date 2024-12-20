# src/data_loader.py

import pandas as pd
import logging
from pathlib import Path

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
            
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """Charge les données depuis le fichier"""
        try:
            logging.info(f"Tentative de chargement du fichier : {self.file_path}")
            
            if self.file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(self.file_path)
            elif self.file_path.suffix.lower() == '.csv':
                self.data = pd.read_csv(self.file_path)
            else:
                raise ValueError(f"Format de fichier non supporté : {self.file_path.suffix}")
                
            # Vérification des données chargées
            if self.data.empty:
                raise ValueError("Le fichier chargé ne contient aucune donnée")
                
            logging.info(f"Données chargées avec succès : {len(self.data)} lignes, {len(self.data.columns)} colonnes")
            logging.debug(f"Colonnes présentes : {self.data.columns.tolist()}")
            
            # Nettoyage basique des données
            self.data = self._clean_data(self.data)
            
            return self.data
            
        except Exception as e:
            logging.error(f"Erreur lors du chargement des données : {str(e)}")
            raise
            
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données chargées"""
        # Suppression des espaces dans les noms de colonnes
        df.columns = df.columns.str.strip()
        
        # Suppression des lignes entièrement vides
        df = df.dropna(how='all')
        
        # Conversion des colonnes de dates
        date_columns = [col for col in df.columns if 'DATE' in col.upper()]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                logging.warning(f"Impossible de convertir la colonne {col} en date")
        
        return df

    def get_data_info(self) -> dict:
        """Retourne des informations sur les données chargées"""
        if self.data is None:
            raise ValueError("Aucune donnée n'a été chargée")
            
        return {
            'nombre_lignes': len(self.data),
            'nombre_colonnes': len(self.data.columns),
            'colonnes': self.data.columns.tolist(),
            'types_donnees': self.data.dtypes.to_dict(),
            'valeurs_manquantes': self.data.isnull().sum().to_dict()
        }