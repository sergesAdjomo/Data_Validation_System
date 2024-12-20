# src/utils.py

from typing import Any, Dict, List
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
import logging

class ValidationUtils:
    """Classe utilitaire pour les fonctions communes de validation"""
    
    @staticmethod
    def format_error_message(column: str, row_index: int, value: Any, message: str) -> Dict:
        """Formate un message d'erreur de manière standardisée"""
        return {
            'colonne': column,
            'ligne': row_index,
            'valeur': str(value),
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

    @staticmethod
    def export_errors_to_excel(errors: List[Dict], output_path: str) -> None:
        """Exporte les erreurs dans un fichier Excel avec mise en forme"""
        df = pd.DataFrame(errors)
        
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Erreurs', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Erreurs']
            
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'bg_color': '#D9E1F2',
                'border': 1
            })
            
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 15)

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse une chaîne de date dans différents formats possibles"""
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S'
        ]
        
        for date_format in formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        raise ValueError(f"Format de date non reconnu: {date_str}")

    @staticmethod
    def calculate_duration_hours(start_date: datetime, end_date: datetime) -> float:
        """Calcule la durée en heures entre deux dates"""
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError("Les dates doivent être au format datetime")
        
        duration = end_date - start_date
        return duration.total_seconds() / 3600

class ReportUtils:
    """Classe utilitaire pour la génération et la manipulation des rapports"""
    
    @staticmethod
    def create_report_directories(base_path: str = "rapports") -> Dict[str, Path]:
        """Crée la structure des dossiers pour les rapports"""
        paths = {
            'base': Path(base_path),
            'templates': Path(base_path) / "templates",
            'output_markdown': Path(base_path) / "output" / "markdown",
            'output_html': Path(base_path) / "output" / "html"
        }
        
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
            
        return paths

    @staticmethod
    def setup_report_logging(log_path: Path) -> None:
        """Configure le système de logging pour les rapports"""
        logging.basicConfig(
            filename=log_path / "report_generation.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )