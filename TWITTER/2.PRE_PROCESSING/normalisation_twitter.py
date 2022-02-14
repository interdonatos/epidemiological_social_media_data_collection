"""
Normalisation des données de YouTube
Entrée : dossier de fichiers .txt représentant les transcriptions bruts
Sortie : dossier de fichiers .txt représentant les transcriptions normalisées

Quatre étapes :
- suppression des bruits retranscrits
- ajout de la ponctuation
- ajout des capitales
- correction des erreurs spécifiques
"""

#importation des librairies python
import re
import sys 
import os, glob
from tqdm import tqdm 
from punctuator import Punctuator
import spacy 
import en_core_web_sm
import shutil
from redditscore.tokenizer import CrazyTokenizer
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


#Variables des données
chemin_dossier_transcriptions_bruts="dossier_txt_tweets_238-2"
chemin_dossier_transcriptions_normalisees="dossier_txt_tweets_238-2_normalise"

#copier le dossier original, afin de pouvoir faire les traitements sur un nouveau dossier
if not os.path.exists(chemin_dossier_transcriptions_normalisees):
    shutil.copytree(chemin_dossier_transcriptions_bruts, chemin_dossier_transcriptions_normalisees)

folder_path = (chemin_dossier_transcriptions_normalisees)

#Etape 1: suppression des hashtags et des caractères non unicodes
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    
    text=re.sub("#","",text) #suppression des hashtags
    text=re.sub(r"\\n"," ",text) #suppression dex \n
    text=re.sub(r"\\x[0-9a-z]+","",text) #suppression des caractères non unicode
    text= text.encode("ascii", "ignore") #suppression des caractères non ascii
    
    #ECRITURE SUR LES FICHIERS
    open(filename,'wb').write(text)

#Etape 2: correction des erreurs spécifiques
#sur google collab, pour utiliser BERT
#METHODE 2 : Utilisation de règles
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    regles_check=re.sub("birth flu","bird flu",text) #birth flu
    regles_check=re.sub("[a]?h5n1","H5N1",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?5 (and |n|N)1","H5N1",regles_check) #(h|H)5 and 1 OU (h|H)5 (n|N)1
    regles_check=re.sub("[a]?h5n8","H5N8",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?5 (and |n|N)8","H5N8",regles_check) #(h|H)5 and 8 OU (h|H)5 (n|N)8
    regles_check=re.sub("(h810|hyn8)","H5N8",regles_check) #h810 ou hyn8
    regles_check=re.sub("[a]?h7n9","H7N9",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?7 (and |n|N)9","H7N9",regles_check)
    regles_check=re.sub("[a]?h3n2","H3N2",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?3 (and |n|N)2","H3N2",regles_check)
    regles_check=re.sub("[a]?h9n2","H9N2",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?9 (and |n|N)2","H9N2",regles_check)
    regles_check=re.sub("[a]?h7n10","H7N10",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?7 (and |n|N)10","H7N10",regles_check)
    regles_check=re.sub("[a]?h10n3","H10N3",regles_check) #ajout majuscule, meilleure reconnaissance de l'entité
    regles_check=re.sub("(h|H) ?10 (and |n|N)3","H10N3",regles_check)
    regles_check=re.sub("h103","H10N3",regles_check)
    regles_check=re.sub("avian ?fluor","avian flu",regles_check) #avian ?fluor
    regles_check=re.sub("avian flu Enza","avian influenza",regles_check) #avian flu Enza
    regles_check=re.sub("avon flu","avian flu",regles_check) #avon flu

    open(filename,'w',encoding="utf-8").write(regles_check)