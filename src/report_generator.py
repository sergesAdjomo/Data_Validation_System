# src/report_generator.py

import pandas as pd
from pathlib import Path
import json
import markdown
from datetime import datetime
from typing import Dict, List, Any

class ReportGenerator:
    """
    Classe responsable de la génération de rapports détaillés à partir des résultats de validation.
    Cette classe s'occupe de formater et d'organiser les résultats dans différents formats (MD, HTML, JSON).
    """
    
    def __init__(self, base_path: str = "rapports"):
        """Initialise le générateur de rapports avec le chemin de base pour les sorties"""
        self.base_path = Path(base_path)
        self._setup_directories()
        self.start_time = datetime.now()
    
    def _setup_directories(self):
        """Crée la structure des dossiers nécessaires pour les rapports"""
        self.base_path.mkdir(exist_ok=True)
        (self.base_path / 'markdown').mkdir(exist_ok=True)
        (self.base_path / 'html').mkdir(exist_ok=True)

    def generate_summary_report(self, results: Dict) -> str:
        """
        Génère le rapport de synthèse avec des statistiques détaillées et des recommandations.
        """
        # Calcul des statistiques
        total_rows = results.get('total_rows', 0)
        rules_errors = results.get('rules_validation', [])
        type_errors = results.get('type_validation', [])
        null_errors = results.get('null_validation', [])
        
        # Création du contenu du rapport
        content = [
            "# Rapport de Validation Complet\n",
            f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## 1. Résumé Général\n",
            "### Statistiques Globales\n",
            f"- Nombre total de lignes analysées : {total_rows}",
            f"- Nombre total d'erreurs détectées : {len(rules_errors) + len(type_errors) + len(null_errors)}\n",
            "### Répartition des Erreurs par Type\n"
        ]

        # Analyse des erreurs par type
        error_types = self._analyze_error_types(rules_errors)
        for error_type, count in error_types.items():
            content.append(f"- {error_type}: {count} erreurs")

        return '\n'.join(content)

    def generate_null_validation_report(self, null_validation: List) -> str:
        """
        Génère le rapport de validation des valeurs nulles avec des statistiques de complétude.
        """
        if not null_validation:
            content = [
                "# Rapport de Validation des Valeurs Nulles\n",
                f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                "## Résultat Global\n",
                "✅ Aucune erreur de valeur nulle détectée\n"
            ]
        else:
            content = [
                "# Rapport de Validation des Valeurs Nulles\n",
                f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                "## Erreurs Détectées\n"
            ]
            for error in null_validation:
                content.append(f"- Colonne: {error['colonne']}")
                content.append(f"  Ligne: {error['ligne']}")
                content.append(f"  Message: {error['message']}\n")

        return '\n'.join(content)

    def generate_type_validation_report(self, type_validation: List) -> str:
        """
        Génère le rapport de validation des types avec des suggestions de correction.
        """
        if not type_validation:
            content = [
                "# Rapport de Validation des Types\n",
                f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                "## Résultat Global\n",
                "✅ Aucune erreur de type détectée\n"
            ]
        else:
            content = [
                "# Rapport de Validation des Types\n",
                f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                "## Erreurs Détectées\n"
            ]
            for error in type_validation:
                content.extend([
                    f"- Colonne: {error['colonne']}",
                    f"  Type attendu: {error.get('type_attendu', 'N/A')}",
                    f"  Type trouvé: {error.get('type_trouve', 'N/A')}",
                    f"  Message: {error['message']}\n"
                ])

        return '\n'.join(content)

    def generate_rules_validation_report(self, rules_validation: List) -> str:
        """
        Génère le rapport de validation des règles métier avec des analyses détaillées.
        """
        if not rules_validation:
            return "# Rapport de Validation des Règles Métier\n\n✅ Aucune violation de règle détectée"

        # Groupement des erreurs par type
        errors_by_type = {}
        for error in rules_validation:
            error_type = error['type_erreur']
            if error_type not in errors_by_type:
                errors_by_type[error_type] = []
            errors_by_type[error_type].append(error)

        content = [
            "# Rapport de Validation des Règles Métier\n",
            f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "## Résumé des Erreurs par Type\n"
        ]

        for error_type, errors in errors_by_type.items():
            content.extend([
                f"### {error_type.title()} ({len(errors)} erreurs)",
                "Détails des erreurs :\n"
            ])
            
            for error in errors:
                content.extend([
                    f"- Colonne: {error['colonne']}",
                    f"  Ligne: {error['ligne']}",
                    f"  Message: {error['message']}\n"
                ])

        return '\n'.join(content)

    def _analyze_error_types(self, rules_errors: List) -> Dict:
        """Analyse et compte les différents types d'erreurs"""
        error_types = {}
        for error in rules_errors:
            error_type = error.get('type_erreur', 'inconnu')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        return error_types

    def generate_all_reports(self, results: Dict):
        """
        Génère tous les rapports et les sauvegarde dans les formats appropriés.
        """
        reports = {
            'summary': self.generate_summary_report(results),
            'null_validation': self.generate_null_validation_report(results.get('null_validation', [])),
            'type_validation': self.generate_type_validation_report(results.get('type_validation', [])),
            'rules_validation': self.generate_rules_validation_report(results.get('rules_validation', []))
        }

        # Sauvegarde des rapports en Markdown
        for name, content in reports.items():
            md_path = self.base_path / 'markdown' / f'{name}.md'
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Conversion en HTML
            self._convert_to_html(md_path, content)

        # Sauvegarde du rapport JSON enrichi
        self._save_json_report(results)

    def _convert_to_html(self, md_path: Path, content: str):
        """Convertit le contenu Markdown en HTML avec un style amélioré"""
        html_content = markdown.markdown(content)
        html_path = self.base_path / 'html' / md_path.with_suffix('.html').name

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(self._get_html_template().format(
                title=md_path.stem.replace('_', ' ').title(),
                content=html_content
            ))

    def _save_json_report(self, results: Dict):
        """Sauvegarde un rapport JSON enrichi avec des métadonnées"""
        enriched_results = {
            'metadata': {
                'date_generation': datetime.now().isoformat(),
                'version_validateur': '1.0.0',
                'duree_execution': str(datetime.now() - self.start_time)
            },
            'resultats': results,
            'statistiques': self._calculate_statistics(results)
        }

        json_path = self.base_path / 'validation_results.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(enriched_results, f, indent=2, ensure_ascii=False)

    def _calculate_statistics(self, results: Dict) -> Dict:
        """Calcule des statistiques détaillées sur les résultats"""
        total_errors = len(results.get('rules_validation', [])) + \
                      len(results.get('type_validation', [])) + \
                      len(results.get('null_validation', []))

        return {
            'total_lignes': results.get('total_rows', 0),
            'total_erreurs': total_errors,
            'repartition_erreurs': self._analyze_error_types(results.get('rules_validation', [])),
            'score_qualite': self._calculate_quality_score(results)
        }

    def _calculate_quality_score(self, results: Dict) -> float:
        """Calcule un score de qualité global des données"""
        total_rows = results.get('total_rows', 0)
        if total_rows == 0:
            return 0.0

        total_errors = len(results.get('rules_validation', [])) + \
                      len(results.get('type_validation', [])) + \
                      len(results.get('null_validation', []))

        return round((1 - (total_errors / (total_rows * 3))) * 100, 2)

    def _get_html_template(self) -> str:
        """Retourne le template HTML pour les rapports"""
        return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
            margin-top: 1.5em;
        }}
        .error {{
            color: #e74c3c;
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #e74c3c;
        }}
        .success {{
            color: #27ae60;
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #27ae60;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #f5f6fa;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>
"""