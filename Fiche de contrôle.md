# README : Fiche de Description des Contrôles

## Introduction
Ce document décrit les contrôles à appliquer aux colonnes d'un fichier de données. Chaque colonne est associée à un format attendu, 
des règles de validation et des conditions spécifiques. 
L'objectif est de garantir la qualité et la cohérence des données pour un traitement efficace.

---

## Colonnes et Détails des Contrôles

### 1. DATE CENTRALISATION
- **Format attendu** : DateTime
- **Obligatoire** : Oui
- **Contrôles** : notNull

### 2. REGION
- **Format attendu** : String
- **Obligatoire** : Oui
- **Contrôles** : NotNull

### 3. N° LIMITATION
- **Format attendu** : String
- **Obligatoire** : Oui
- **Contrôles** :
  - Si "CONSIGNE LIMITATION (MW)", "DATE DEBUT REALISE", "DATE FIN REALISE" et "IDR POSTE" sont identiques sur deux ou plusieurs "N° LIMITATION", alors ces limitations sont considérées comme des doublons.

### 4. IDR POSTE
- **Format attendu** : String

### 5. LIBELLE POSTE
- **Format attendu** : String
- **Obligatoire** : Oui
- **Contrôles** : NotNull

### 6. NOM CLIENT
- **Format attendu** : String
- **Obligatoire** : Oui
- **Contrôles** : NotNull

### 7. N° TRANSFO
- **Format attendu** : String

### 8. CONSIGNE LIMITATION (MW)
- **Format attendu** : Int

### 9. TYPE REQUETE
- **Format attendu** : String
- **Obligatoire** : Oui
- **Contrôles** :
  - Si "N° LIMITATION" commence par "ALZ –", alors la limitation est **Automatique**.
  - Sinon, la limitation est **Manuelle**.

### 10. MOTIF
- **Format attendu** : String
- **Obligatoire** : Oui
- **Contrôles** :
  - Le motif doit respecter l’une des trois valeurs autorisées et être sensible à la casse.

### 11. DATE ENVOI PLANIFICATION
- **Format attendu** : DateTime
- **Obligatoire** : Non

### 12. DATE DEBUT PREVUE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre", sinon peut être null.

### 13. HEURE DEBUT PREVUE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre", sinon peut être null.

### 14. DATE FIN PREVUE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre", sinon peut être null.

### 15. HEURE FIN PREVUE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre", sinon peut être null.

### 16. DATE DEBUT DEMANDEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 17. HEURE DEBUT DEMANDEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 18. DATE DEBUT REALISEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 19. HEURE DEBUT REALISEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 20. DATE FIN DEMANDEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 21. HEURE FIN DEMANDEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 22. DATE FIN REALISEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 23. HEURE FIN REALISEE
- **Format attendu** : DateTime
- **Obligatoire** : Oui si "STATUT LIMITATION" = "planifiée et mise en œuvre" ou "mise en œuvre en TR".

### 24. RETRAIT URGENT (OUI/NON)
- **Format attendu** : Booléen
- **Obligatoire** : Oui si "Motif" = "Aléa réseau/Fortuit".

### 25. IDR OUVRAGE EN DEFAUT
- **Format attendu** : String

### 26. COMMENTAIRE CE
- **Format attendu** : String

### 27. TYPE CLIENT
- **Format attendu** : String

### 28. CODE EIC
- **Format attendu** : String

### 29. ANNEE LIVRAISON
- **Format attendu** : Date
- **Obligatoire** : Oui

### 30. REQUETE NAZA (VRAI/FAUX)
- **Format attendu** : Booléen
- **Contrôles** :
    -Si "N° LIMITATION" commence par "ALZ -", alors la valeur doit être "VRAI".
    -Sinon, la valeur doit être "FAUX".

### 31. NOM SITE RTE
- **Format attendu** : String

### 32. ZONE NAZA
- **Format attendu** : String

### 33. VAGUE NAZA
- **Format attendu** : Date

### 34. TYPE MODULATION
- **Format attendu** : String

### 35. STATUT LIMITATION
- **Format attendu** : String
- **Contrôles** :
    - Si "DATE DEBUT DEMANDEE" n'est pas vide et "DATE DEBUT PREVUE" est vide, alors la valeur est "Mise en œuvre en temps réel".
    - Si "DATE DEBUT DEMANDEE" est vide et "DATE DEBUT PREVUE" n'est pas vide, alors la valeur est "Planifiée et non mise en œuvre".
    - Si "DATE DEBUT DEMANDEE" n'est pas vide et "DATE DEBUT PREVUE" n'est pas vide, alors la valeur est "Planifiée et mise en œuvre".
    - Si "DATE DEBUT DEMANDEE" n'est pas vide et "DATE DEBUT PREVUE" est vide, alors le champ doit être vide.

### 36. HORODATE DEBUT MATCHING
- **Format attendu** : DateTime

### 37. HORODATE FIN MATCHING
- **Format attendu** : DateTime

### 38. DELAI PREVENANCE (JOURS)
- **Format attendu** : Int

### 39. DELAIS PREVENANCE RESPECTE (VRAI/FAUX)
- **Format attendu** : Booléen

### 40. DUREE PREVUE (HEURES)
- **Format attendu** : Int
- **Obligatoire** : Oui si "STATUT LIMITATION" = "Planifiée et mise en œuvre" ou "Planifiée et non mise en œuvre".

### 41. DUREE DEMANDEE (HEURES)
- **Format attendu** : Int
- **Obligatoire** : Oui si "STATUT LIMITATION" = "Planifiée et mise en œuvre" ou "Mise en œuvre en Temps Réel".

### 42. DUREE REALISEE (HEURES)
- **Format attendu** : Int
- **Obligatoire** : Oui si "STATUT LIMITATION" = "Planifiée et mise en œuvre" ou "Mise en œuvre en Temps Réel".

### 43. COMMENTAIRE DEXPL
- **Format attendu** : String

### 44. CONTRAT (AMONT J-1/GRE-A-GRE/SANS DEVIS)
- **Format attendu** : String
- **Obligatoire** : Oui si "STATUT LIMITATION" = "Planifiée et mise en œuvre" et "TYPE CLIENT" = "Producteur HTB".

### 45. PERIODE CORRELATION (VRAI/VIDE)
- **Format attendu** : Booléen

### 46. HORS QUOTA (VRAI/FAUX)
- **Format attendu** : Booléen
- **Obligatoire** : Oui si "MOTIF" = "Travaux Programmés".

### 47. RESEAU AMONT (VRAI/FAUX)
- **Format attendu** : Booléen
- **Obligatoire** : Oui si "MOTIF" = "Aléa réseau/Fortuit".

### 48. INDEMNISABLE (VRAI/FAUX)
- **Format attendu** : Booléen
- **Contrôles** :
    - Si "STATUT LIMITATION" = "Planifiée et mise en œuvre", alors la valeur doit être "VRAI".
    - Sinon, elle doit être "FAUX".

### 49. MODE VALORISATION
- **Format attendu** : String
- **Obligatoire** : Oui si "TYPE CLIENT" = "Producteur HTB".

### 50. TARIF INDEMNISATION (€/MWh)
- **Format attendu** : Int
- **Obligatoire** : Oui si "TYPE CLIENT" = "Producteur HTB".

### 51. INDEMNITE DEVIS (€)
- **Format attendu** : String
- **Obligatoire** : Oui si "MODE VALORISATION" = "Devis amont".

### 52. DATE COMMUNICATION ELIGIBILITE
- **Format attendu** : DateTime

### 53. ENE AU REALISE (MWh)
- **Format attendu** : Int

### 54. INDEMNITE AU REALISE (€)
- **Format attendu** : String

### 55. INDEMNITE RETENUE (€)
- **Format attendu** : String

### 56. DATE COMMUNICATION INDEMNITE
- **Format attendu** : Date

### 57. CONTESTATION CLIENT INDEMNITE (VRAI/VIDE)
- **Format attendu** : Booléen

### 58. COMMENTAIRE SGC
- **Format attendu** : String

### 59. DATE CREATION COMMANDE
- **Format attendu** : Date

### 60. N° COMMANDE
- **Format attendu** : Int

### 61. CODE GCP FOURNISSEUR
- **Format attendu** : String

### 62. DATE RECEPTION FACTURE
- **Format attendu** : Date

### 63. N° RECEPTION
- **Format attendu** : Int

### 64. COMMENTAIRE ACDC
- **Format attendu** : String

### 65. ENI ESTIMEE (MWh)
- **Format attendu** : Float

### 66. INDEMNITE ESTIMEE (€)
- **Format attendu** : Float

---

## Règles Conditionnelles

### 1. Limitation Planifiée et Mise en Œuvre
Si "STATUT LIMITATION" = "planifiée et mise en œuvre", les colonnes suivantes doivent être renseignées :
- DATE DEBUT PREVUE
- HEURE DEBUT PREVUE
- DATE FIN PREVUE
- HEURE FIN PREVUE

### 2. Limitation en Temps Réel
Si "STATUT LIMITATION" = "mise en œuvre en Temps Réel", les colonnes suivantes doivent être renseignées :
- DATE DEBUT DEMANDEE
- HEURE DEBUT DEMANDEE
- DATE DEBUT REALISEE
- HEURE DEBUT REALISEE
- DATE FIN DEMANDEE
- HEURE FIN DEMANDEE
- DATE FIN REALISEE
- HEURE FIN REALISEE

---

## Contact
Pour toute question sur l'application des contrôles, veuillez contacter l'équipe en charge.

