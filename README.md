# Documentation du Système de Validation de Données

## Introduction

Le Système de Validation de Données est une application Python conçue pour automatiser et standardiser le processus de validation des données de limitation électrique. 

Ce système permet de vérifier la conformité des données selon un ensemble de règles métier prédéfinies, assurant ainsi la qualité et la cohérence des informations avant leur intégration dans les systèmes de production.

### Objectifs du Projet

Notre système répond à plusieurs objectifs critiques :

1. Automatiser la validation des fichiers de données pour réduire les erreurs humaines
2. Standardiser le processus de contrôle selon des règles métier définies
3. Générer des rapports détaillés et exploitables
4. Faciliter l'identification et la correction des anomalies
5. Assurer la traçabilité des contrôles effectués

## Architecture du Projet

### Structure des Dossiers

```
projet_validation/
├── config/
│   └── column_config.py     # Configuration des règles de validation
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Chargement des données
│   ├── null_validator.py    # Validation des valeurs nulles
│   ├── type_validator.py    # Validation des types de données
│   ├── rules_validator.py   # Validation des règles métier
│   ├── report_generator.py  # Génération des rapports
│   └── utils.py            # Fonctions utilitaires
├── data/
│   └── test.xlsx           # Fichiers de données à valider
├── rapports/
│   ├── markdown/           # Rapports au format Markdown
│   ├── html/              # Rapports au format HTML
│   └── validation_results.json
├── main.py                 # Point d'entrée du programme
└── requirements.txt        # Dépendances du projet
```

### Composants Principaux

1. **Data Loader (data_loader.py)**
   - Gère le chargement des fichiers de données
   - Effectue les conversions de format nécessaires
   - Vérifie l'intégrité basique des données

2. **Validateurs (null_validator.py, type_validator.py, rules_validator.py)**
   - Null Validator : Vérifie les contraintes de non-nullité
   - Type Validator : Valide les types de données
   - Rules Validator : Applique les règles métier spécifiques

3. **Générateur de Rapports (report_generator.py)**
   - Crée des rapports détaillés en plusieurs formats
   - Organise les résultats de manière structurée
   - Génère des statistiques et des recommandations

## Fonctionnement du Système

### Processus de Validation

1. **Chargement des Données**
   - Lecture du fichier Excel source
   - Vérification de la présence des colonnes requises
   - Préparation des données pour la validation

2. **Validations**
   - Contrôle des valeurs nulles obligatoires
   - Vérification des types de données
   - Application des règles métier spécifiques

3. **Génération des Rapports**
   - Création de rapports Markdown pour la lisibilité
   - Génération de versions HTML pour la consultation web
   - Production d'un fichier JSON pour l'intégration système

### Types de Contrôles Effectués

1. **Contrôles de Nullité**
   - Vérification des champs obligatoires
   - Identification des données manquantes
   - Analyse de la complétude des données

2. **Contrôles de Type**
   - Validation des formats de date
   - Vérification des types numériques
   - Contrôle des formats de chaîne

3. **Règles Métier**
   - Validation des statuts de limitation
   - Contrôle des types de requête
   - Vérification des conditions NAZA

## Utilisation du Système

### Prérequis

- Python 3.8 ou supérieur
- Dépendances listées dans requirements.txt

### Installation

```bash
# Création de l'environnement virtuel
python -m venv venv

# Activation de l'environnement
source venv/bin/activate  # Unix/MacOS
venv\Scripts\activate     # Windows

# Installation des dépendances
pip install -r requirements.txt
```

### Exécution

```bash
python main.py
```

### Format des Données d'Entrée

Le système attend un fichier Excel (.xlsx) contenant les colonnes suivantes :
- DATE CENTRALISATION
- REGION
- N° LIMITATION
- Et autres colonnes définies dans la configuration...

## Rapports Générés

### 1. Rapport de Synthèse (summary.md)
- Vue d'ensemble des validations
- Statistiques globales
- Points d'attention principaux

### 2. Rapport de Validation des Valeurs Nulles (null_validation.md)
- Liste des champs obligatoires manquants
- Statistiques de complétude
- Recommandations de correction

### 3. Rapport de Validation des Types (type_validation.md)
- Erreurs de format détectées
- Suggestions de correction
- Impact sur la qualité des données

### 4. Rapport de Validation des Règles (rules_validation.md)
- Violations des règles métier
- Analyse détaillée par type d'erreur
- Recommandations de correction

## Maintenance et Extension

### Ajout de Nouvelles Règles

Pour ajouter de nouvelles règles de validation :
1. Mettre à jour column_config.py avec les nouvelles règles
2. Ajouter les méthodes de validation correspondantes dans rules_validator.py
3. Mettre à jour la génération des rapports si nécessaire

### Personnalisation des Rapports

Les rapports peuvent être personnalisés en modifiant :
1. Les templates dans report_generator.py
2. Le format de sortie des validateurs
3. La structure du fichier JSON de résultats

## Support et Contact

Pour toute question ou problème :
1. Consulter les logs dans le fichier debug.log
2. Vérifier la documentation des règles métier
3. Contacter l'équipe de support

## Conclusion

Ce système de validation offre une solution robuste et extensible pour assurer la qualité des données avant leur intégration. 

Sa structure modulaire permet une maintenance facile et des extensions futures selon les besoins évolutifs de l'entreprise.# Data_Validation_System
