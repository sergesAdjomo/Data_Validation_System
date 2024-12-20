# main.py

import logging
from pathlib import Path
from src.data_loader import DataLoader
from src.null_validator import NullValidator
from src.type_validator import TypeValidator
from src.rules_validator import RulesValidator
from src.report_generator import ReportGenerator

class DataValidationPipeline:
    """
    Cette classe orchestre l'ensemble du processus de validation des données.
    Elle coordonne le chargement des données, l'exécution des validations,
    et la génération des rapports détaillés.
    """
    
    def __init__(self, file_path: str):
        """
        Initialise le pipeline de validation avec le chemin du fichier à analyser.
        
        Args:
            file_path (str): Chemin vers le fichier de données à valider
        """
        self.file_path = file_path
        self.report_generator = ReportGenerator()
        
    def run_validation(self):
        """
        Exécute le processus complet de validation et génère les rapports.
        
        Returns:
            tuple: (nombre total d'erreurs, résultats détaillés)
        """
        try:
            # Chargement des données depuis le fichier source
            loader = DataLoader(self.file_path)
            data = loader.load_data()
            
            # Exécution des trois types de validation
            null_validator = NullValidator(data)
            type_validator = TypeValidator(data)
            rules_validator = RulesValidator(data)
            
            # Compilation des résultats de toutes les validations
            results = {
                'total_rows': len(data),
                'null_validation': null_validator.validate_required_fields(),
                'type_validation': type_validator.validate_column_types(),
                'rules_validation': rules_validator.validate_all_rules()
            }
            
            # Génération des rapports détaillés
            self.report_generator.generate_all_reports(results)
            
            # Calcul du nombre total d'erreurs toutes catégories confondues
            total_errors = (
                len(results['null_validation']) +
                len(results['type_validation']) +
                len(results['rules_validation'])
            )
            
            return total_errors, results
            
        except Exception as e:
            logging.error(f"Erreur lors de la validation : {str(e)}")
            raise

def main():
    """
    Point d'entrée principal du programme.
    Configure le logging, lance le pipeline de validation
    et affiche un résumé des résultats.
    """
    # Configuration du système de logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Chemin vers le fichier de données à valider
    input_file = "data/test.xlsx"
    
    try:
        # Création et exécution du pipeline de validation
        pipeline = DataValidationPipeline(input_file)
        total_errors, results = pipeline.run_validation()
        
        # Affichage des résultats dans la console
        print("\nRésultats de la validation :")
        print(f"Status : {'success' if total_errors == 0 else 'warnings'}")
        print(f"Nombre total d'erreurs : {total_errors}")
        print("\nLes rapports détaillés ont été générés dans le dossier 'rapports' :")
        print("- rapports/markdown/ : Rapports en format Markdown")
        print("- rapports/html/    : Rapports en format HTML")
        print("- rapports/validation_results.json : Rapport complet au format JSON\n")
        
    except Exception as e:
        print(f"\nErreur lors de l'exécution : {str(e)}")
        logging.error(f"Erreur fatale : {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()