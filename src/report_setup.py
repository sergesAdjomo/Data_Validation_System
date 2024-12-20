# report_setup.py

import os
import markdown
import shutil
from datetime import datetime
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader

class ReportManager:
    """Gestionnaire de rapports pour le système de validation"""
    
    def __init__(self, base_path: str = "rapports"):
        """
        Initialise le gestionnaire de rapports
        
        Args:
            base_path: Chemin du dossier principal des rapports
        """
        self.base_path = Path(base_path)
        self.templates_path = self.base_path / "templates"
        self.output_path = self.base_path / "output"
        self._setup_directories()
        self._setup_logging()
        
    def _setup_directories(self):
        """Crée la structure des dossiers nécessaires"""
        # Création des dossiers principaux
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.templates_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        
        # Création des sous-dossiers pour différents formats
        os.makedirs(self.output_path / "markdown", exist_ok=True)
        os.makedirs(self.output_path / "html", exist_ok=True)
        
    def _setup_logging(self):
        """Configure le système de logging"""
        logging.basicConfig(
            filename=self.base_path / "report_generation.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def create_markdown_report(self, report_data: dict, report_type: str):
        """
        Crée un rapport Markdown à partir des données
        
        Args:
            report_data: Données du rapport
            report_type: Type de rapport (summary, null_validation, etc.)
        """
        # Création du nom de fichier avec horodatage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type}_{timestamp}.md"
        
        # Chemin complet du fichier
        output_file = self.output_path / "markdown" / filename
        
        try:
            # Écriture du rapport
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Rapport de {report_type}\n\n")
                f.write(f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Écriture du contenu spécifique selon le type
                if report_type == "summary":
                    self._write_summary_content(f, report_data)
                elif report_type == "null_validation":
                    self._write_null_validation_content(f, report_data)
                # Ajoutez d'autres types de rapports ici...
                
            logging.info(f"Rapport Markdown créé : {filename}")
            return output_file
            
        except Exception as e:
            logging.error(f"Erreur lors de la création du rapport Markdown : {str(e)}")
            raise
            
    def convert_to_html(self, markdown_file: Path):
        """
        Convertit un fichier Markdown en HTML
        
        Args:
            markdown_file: Chemin du fichier Markdown à convertir
        """
        try:
            # Lecture du contenu Markdown
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Conversion en HTML
            html_content = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code', 'toc']
            )
            
            # Création du fichier HTML
            html_file = self.output_path / "html" / markdown_file.with_suffix('.html').name
            
            # Application du template HTML
            env = Environment(loader=FileSystemLoader(self.templates_path))
            template = env.get_template('report_template.html')
            
            rendered_html = template.render(
                content=html_content,
                title=markdown_file.stem,
                generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            # Sauvegarde du fichier HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
                
            logging.info(f"Conversion HTML réussie : {html_file}")
            return html_file
            
        except Exception as e:
            logging.error(f"Erreur lors de la conversion en HTML : {str(e)}")
            raise

    def _write_summary_content(self, file, data):
        """Écrit le contenu d'un rapport de synthèse"""
        file.write("## Statistiques Globales\n\n")
        file.write(f"Nombre total de lignes analysées : {data.get('total_rows', 0)}\n")
        file.write(f"Nombre total d'erreurs : {data.get('total_errors', 0)}\n")
        # etc...

    def _write_null_validation_content(self, file, data):
        """Écrit le contenu d'un rapport de validation des valeurs nulles"""
        file.write("## Analyse des Valeurs Nulles\n\n")
        for column, errors in data.get('null_errors', {}).items():
            file.write(f"### Colonne : {column}\n")
            file.write(f"Nombre d'erreurs : {len(errors)}\n\n")
        # etc...
