"""
Mini Projet - Extraction et Analyse des données géographiques du Burkina Faso
==============================================================================

Ce script réalise l'extraction et l'analyse des données géographiques 
du Burkina Faso depuis la base de données GeoNames.

Auteur: SAWADOGO Abdel Saïd Najib Étudiant en Fouilles de données et intelligence artificielle
Date: 15 Août 2025
"""

import pandas as pd
import numpy as np
import openpyxl
import zipfile
import requests
import os
from io import StringIO
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("MINI PROJET - ANALYSE DES DONNÉES GÉOGRAPHIQUES DU BURKINA FASO")
print("="*80)

# Configuration
GEONAMES_URL = "https://download.geonames.org/export/dump/BF.zip"
ZIP_FILENAME = "BF.zip"
TXT_FILENAME = "BF.txt"
OUTPUT_CSV = "burkina_location.csv"
GOUNGHIN_CSV = "gounghin.csv"
EXCEL_FILENAME = "mini_projet.xlsx"

print("\n🔄 ÉTAPE 1: Téléchargement des données du Burkina Faso")
print("-" * 50)

def download_burkina_data():
    """Télécharge le fichier ZIP des données du Burkina Faso"""
    try:
        print(f"📥 Téléchargement depuis: {GEONAMES_URL}")
        response = requests.get(GEONAMES_URL, stream=True)
        response.raise_for_status()
        
        with open(ZIP_FILENAME, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Téléchargement terminé: {ZIP_FILENAME}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        return False

# Télécharger les données
if download_burkina_data():
    print(f"📁 Taille du fichier téléchargé: {os.path.getsize(ZIP_FILENAME) / 1024:.1f} KB")

print("\n🔄 ÉTAPE 2: Extraction et prétraitement des données")
print("-" * 50)

def extract_and_preprocess():
    """Extrait le fichier ZIP et prétraite les données"""
    try:
        # Extraction du fichier ZIP
        with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
            zip_ref.extractall()
            print(f"✅ Fichier extrait: {TXT_FILENAME}")
        
        # Définition des colonnes selon la documentation GeoNames
        columns = [
            'geonameid', 'name', 'asciiname', 'alternatenames',
            'latitude', 'longitude', 'feature_class', 'feature_code',
            'country_code', 'cc2', 'admin1_code', 'admin2_code',
            'admin3_code', 'admin4_code', 'population', 'elevation',
            'dem', 'timezone', 'modification_date'
        ]
        
        # Lecture des données
        print("📊 Chargement des données...")
        df = pd.read_csv(TXT_FILENAME, sep='\t', names=columns, encoding='utf-8')
        print(f"✅ Données chargées: {len(df)} enregistrements")
        
        # Sélection et renommage des colonnes requises
        df_filtered = df[['geonameid', 'name', 'latitude', 'longitude']].copy()
        df_filtered = df_filtered.rename(columns={
            'geonameid': 'ID',
            'name': 'location_name',
            'latitude': 'lat',
            'longitude': 'long'
        })
        
        # Nettoyage des données
        df_filtered = df_filtered.dropna()
        df_filtered['lat'] = pd.to_numeric(df_filtered['lat'], errors='coerce')
        df_filtered['long'] = pd.to_numeric(df_filtered['long'], errors='coerce')
        df_filtered = df_filtered.dropna()
        
        # Sauvegarde en CSV
        df_filtered.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        print(f"✅ Données sauvegardées: {OUTPUT_CSV}")
        print(f"📈 Nombre d'enregistrements traités: {len(df_filtered)}")
        
        return df_filtered
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return None

# Extraction et prétraitement
burkina_data = extract_and_preprocess()

if burkina_data is not None:
    # Affichage d'un aperçu des données
    print("\n📋 Aperçu des données:")
    print(burkina_data.head(10))
    print(f"\nℹ️  Statistiques de base:")
    print(f"   - Nombre total de lieux: {len(burkina_data)}")
    print(f"   - Latitude min: {burkina_data['lat'].min():.6f}")
    print(f"   - Latitude max: {burkina_data['lat'].max():.6f}")
    print(f"   - Longitude min: {burkina_data['long'].min():.6f}")
    print(f"   - Longitude max: {burkina_data['long'].max():.6f}")

print("\n🔄 ÉTAPE 4: Opérations d'analyse sur les données")
print("-" * 50)

def analyze_burkina_data(df):
    """Effectue les analyses demandées"""
    results = {}
    
    # 4.1 - Extraction des données contenant 'gounghin'
    print("🔍 4.1 - Recherche des lieux contenant 'gounghin'...")
    gounghin_data = df[df['location_name'].str.contains('gounghin', case=False, na=False)]
    gounghin_data.to_csv(GOUNGHIN_CSV, index=False, encoding='utf-8')
    print(f"✅ Trouvé {len(gounghin_data)} lieu(x) avec 'gounghin'")
    print(f"💾 Sauvegardé dans: {GOUNGHIN_CSV}")
    if not gounghin_data.empty:
        print("   Lieux trouvés:")
        for _, row in gounghin_data.iterrows():
            print(f"   - {row['location_name']} (ID: {row['ID']}, Lat: {row['lat']:.6f}, Long: {row['long']:.6f})")
    results['gounghin'] = gounghin_data
    
    print("\n🔍 4.2 - Extraction des lieux A-P...")
    # 4.2 - Extraction des lieux dont la première lettre est entre A et P
    a_to_p_data = df[df['location_name'].str[0].str.upper().between('A', 'P', inclusive='both')]
    print(f"✅ Trouvé {len(a_to_p_data)} lieu(x) commençant par A-P")
    results['a_to_p'] = a_to_p_data
    
    print("\n🔍 4.3 - Recherche des coordonnées extrêmes...")
    # 4.3 - Coordonnées minimales et maximales
    lat_min_idx = df['lat'].idxmin()
    lat_max_idx = df['lat'].idxmax()
    long_min_idx = df['long'].idxmin()
    long_max_idx = df['long'].idxmax()
    
    print("📊 Coordonnées extrêmes:")
    print(f"   Latitude minimale: {df.loc[lat_min_idx, 'lat']:.6f} - {df.loc[lat_min_idx, 'location_name']}")
    print(f"   Latitude maximale: {df.loc[lat_max_idx, 'lat']:.6f} - {df.loc[lat_max_idx, 'location_name']}")
    print(f"   Longitude minimale: {df.loc[long_min_idx, 'long']:.6f} - {df.loc[long_min_idx, 'location_name']}")
    print(f"   Longitude maximale: {df.loc[long_max_idx, 'long']:.6f} - {df.loc[long_max_idx, 'location_name']}")
    
    results['extremes'] = {
        'lat_min': df.loc[lat_min_idx],
        'lat_max': df.loc[lat_max_idx],
        'long_min': df.loc[long_min_idx],
        'long_max': df.loc[long_max_idx]
    }
    
    print("\n🔍 4.4 - Lieux avec lat >= 11 et lon <= 0.5...")
    # 4.4 - Lieux avec coordonnées spécifiques
    specific_coords = df[(df['lat'] >= 11) & (df['long'] <= 0.5)]
    print(f"✅ Trouvé {len(specific_coords)} lieu(x) avec lat >= 11 et long <= 0.5")
    if not specific_coords.empty:
        print("   Premiers lieux trouvés:")
        for _, row in specific_coords.head(10).iterrows():
            print(f"   - {row['location_name']} (Lat: {row['lat']:.6f}, Long: {row['long']:.6f})")
    results['specific_coords'] = specific_coords
    
    return results

# Effectuer les analyses
if burkina_data is not None:
    analysis_results = analyze_burkina_data(burkina_data)

    print("\n🔄 ÉTAPE 5: Création du fichier Excel")
    print("-" * 50)

    def create_excel_file(results):
        """Crée le fichier Excel avec les différentes feuilles"""
        try:
            with pd.ExcelWriter(EXCEL_FILENAME, engine='openpyxl') as writer:
                # Feuille 1: données gounghin
                if not results['gounghin'].empty:
                    results['gounghin'].to_excel(writer, sheet_name='gounghin', index=False)
                    print(f"✅ Feuille 'gounghin' créée avec {len(results['gounghin'])} enregistrements")
                else:
                    # Créer une feuille vide si aucune donnée
                    pd.DataFrame(columns=['ID', 'location_name', 'lat', 'long']).to_excel(
                        writer, sheet_name='gounghin', index=False)
                    print("✅ Feuille 'gounghin' créée (vide)")
                
                # Feuille 2: données A-P
                results['a_to_p'].to_excel(writer, sheet_name='A_to_P', index=False)
                print(f"✅ Feuille 'A_to_P' créée avec {len(results['a_to_p'])} enregistrements")
                
                # Feuille 3: Résumé des analyses
                summary_data = []
                summary_data.append(['Analyse', 'Résultat'])
                summary_data.append(['Nombre total de lieux', len(burkina_data)])
                summary_data.append(['Lieux avec "gounghin"', len(results['gounghin'])])
                summary_data.append(['Lieux A-P', len(results['a_to_p'])])
                summary_data.append(['Lieux lat>=11 et long<=0.5', len(results['specific_coords'])])
                summary_data.append(['', ''])
                summary_data.append(['Coordonnées extrêmes', ''])
                summary_data.append(['Latitude min', f"{results['extremes']['lat_min']['lat']:.6f} - {results['extremes']['lat_min']['location_name']}"])
                summary_data.append(['Latitude max', f"{results['extremes']['lat_max']['lat']:.6f} - {results['extremes']['lat_max']['location_name']}"])
                summary_data.append(['Longitude min', f"{results['extremes']['long_min']['long']:.6f} - {results['extremes']['long_min']['location_name']}"])
                summary_data.append(['Longitude max', f"{results['extremes']['long_max']['long']:.6f} - {results['extremes']['long_max']['location_name']}"])
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Résumé', index=False, header=False)
                print("✅ Feuille 'Résumé' créée avec les statistiques")
            
            print(f"📊 Fichier Excel créé: {EXCEL_FILENAME}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du fichier Excel: {e}")
            return False

    # Créer le fichier Excel
    create_excel_file(analysis_results)

    print("\n" + "="*80)
    print("✅ TRAITEMENT TERMINÉ AVEC SUCCÈS!")
    print("="*80)
    print(f"📁 Fichiers créés:")
    print(f"   • {OUTPUT_CSV} - Données principales du Burkina Faso")
    print(f"   • {GOUNGHIN_CSV} - Lieux contenant 'gounghin'")
    print(f"   • {EXCEL_FILENAME} - Fichier Excel avec toutes les analyses")
    print(f"\n📊 Résumé des analyses:")
    print(f"   • Nombre total de lieux traités: {len(burkina_data)}")
    print(f"   • Lieux contenant 'gounghin': {len(analysis_results['gounghin'])}")
    print(f"   • Lieux commençant par A-P: {len(analysis_results['a_to_p'])}")
    print(f"   • Lieux avec lat>=11 et long<=0.5: {len(analysis_results['specific_coords'])}")

else:
    print("❌ Échec du traitement des données")
