# Mini Projet - Analyse des Données Géographiques du Burkina Faso

## 📋 Description du Projet

Ce projet consiste à extraire et analyser des données géographiques du Burkina Faso depuis la base de données **GeoNames** (http://www.geonames.org/). L'objectif est de créer une application qui traite les informations de localisation avec coordonnées géographiques.

## 🎯 Objectifs

1. **Extraction des données** depuis GeoNames pour le Burkina Faso
2. **Prétraitement** et filtrage des données
3. **Analyses spécifiques** sur les données géographiques
4. **Export** vers différents formats (CSV, Excel)

## 🔧 Étapes Réalisées

### Étape 1: Extraction de la Base de Données
- ✅ Identification du code ISO du Burkina Faso: **BF**
- ✅ Téléchargement du fichier `BF.zip` depuis https://download.geonames.org/export/dump/
- ✅ Extraction et lecture des données au format TSV

### Étape 2: Prétraitement des Données
- ✅ Sélection des colonnes pertinentes:
  - `geonameid` → `ID`
  - `name` → `location_name` 
  - `latitude` → `lat`
  - `longitude` → `long`
- ✅ Nettoyage et validation des données
- ✅ Sauvegarde dans `burkina_location.csv`

### Étape 3: Opérations d'Analyse
- ✅ **4.1** - Extraction des lieux contenant "gounghin" → `gounghin.csv`
- ✅ **4.2** - Filtrage des lieux A-P (ordre alphabétique)
- ✅ **4.3** - Identification des coordonnées extrêmes (min/max)
- ✅ **4.4** - Localisation des lieux avec `lat >= 11` et `lon <= 0.5`

### Étape 4: Export Excel
- ✅ Création du fichier `mini_projet.xlsx` avec:
  - Feuille **"gounghin"** - Données contenant "gounghin"
  - Feuille **"A_to_P"** - Lieux de A à P
  - Feuille **"Résumé"** - Statistiques des analyses

## 📁 Structure du Repository

```
mini_projet_data_analysis/
├── README.md                    # Ce fichier
├── burkina_geo_analysis.py      # Script Python principal
├── burkina_geo_analysis.ipynb   # Notebook Jupyter
└── data/
    ├── BF.txt                  # Données initiales
    ├── burkina_location.csv    # Données principales
    ├── gounghin.csv            # Lieux avec "gounghin"
    └── mini_projet.xlsx        # Fichier Excel final
```

## 🚀 Installation et Utilisation

### Prérequis
```bash
pip install pandas requests openpyxl numpy
```

### Exécution
```bash
python burkina_geo_analysis.py
```

### Google Colab
1. Ouvrez le fichier `burkina_geo_analysis.ipynb` dans Google Colab
2. Exécutez toutes les cellules
3. Téléchargez les fichiers générés

## 📊 Résultats Obtenus

### Statistiques Générales
- **Nombre total de lieux**: ~12,000 enregistrements
- **Étendue géographique**:
  - Latitude: 9.4° N à 15.1° N
  - Longitude: -5.5° W à 2.4° E

### Analyses Spécifiques
1. **Lieux "Gounghin"**: Plusieurs quartiers identifiés (principalement à Ouagadougou)
2. **Lieux A-P**: ~69% des données
3. **Zone spécifique**: (lat≥11, lon≤0.5)

## 🛠️ Technologies Utilisées

- **Python 3.8+**
- **Pandas** - Manipulation de données
- **Requests** - Téléchargement de fichiers
- **OpenPyXL** - Export Excel
- **NumPy** - Calculs numériques

## 📈 Méthodologie

1. **Acquisition**: Téléchargement automatisé depuis GeoNames
2. **Preprocessing**: Nettoyage, validation, renommage
3. **Analyse**: Filtrage conditionnel, recherche de patterns
4. **Export**: Formats multiples pour différents usages

## 🌍 Sources de Données

- **GeoNames.org**: Base de données géographique mondiale
- **License**: Creative Commons Attribution 4.0
- **Format**: Tab-separated values (TSV) UTF-8
- **Mise à jour**: Données actualisées quotidiennement

## 👥 Contribution

Ce projet a été réalisé dans le cadre d'un exercice d'analyse de données géographiques. Les contributions sont les bienvenues pour:

- Améliorer l'efficacité du code
- Ajouter de nouvelles analyses
- Optimiser la visualisation des résultats

## 📞 Contact

Pour toute question ou suggestion concernant ce projet, n'hésitez pas à ouvrir une issue ou à contribuer directement.

---

**Date de création**: 15 Août 2025  
**Dernière mise à jour**: 15 Août 2025  
**Status**: ✅ Terminé