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
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
p = Punctuator('INTERSPEECH-T-BRNN.pcl')
#Variables des données
chemin_dossier_transcriptions_bruts="dossier_txt_transcriptions_v2_100"
chemin_dossier_transcriptions_normalisees="dossier_txt_transcriptions_v2_100_normalise"

#copier le dossier original, afin de pouvoir faire les traitements sur un nouveau dossier
if not os.path.exists(chemin_dossier_transcriptions_normalisees):
    shutil.copytree(chemin_dossier_transcriptions_bruts, chemin_dossier_transcriptions_normalisees)

folder_path = (chemin_dossier_transcriptions_normalisees)

#Etape 1: suppression des bruits retranscrits, eg. [Music], [Laugh], etc.
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    text_etape_1=re.sub("(\[Music\] |\[Laugh\] |\[ __ \] |\[Applause\] )","",text) #ok

    #ECRITURE SUR LES FICHIERS
    #with open(chemin_dossier_transcriptions_normalisees, 'w', encoding="utf-8") as outfile: # Ecrire 
    #    json.dump(text_etape_1, outfile)
    open(filename,'w',encoding="utf-8").write(text_etape_1)

#Etape 2: ajout de la ponctuation
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()

    text_etape_1_2=p.punctuate(text)
    
    #nettoyage
    text_etape_1_2=re.sub("(:,|:\.)",":",text_etape_1_2)
    text_etape_1_2=re.sub("&,","&",text_etape_1_2)
    text_etape_1_2=re.sub("(,,|\.,|~,|,\.)",",",text_etape_1_2)
    text_etape_1_2=re.sub("\"\.","\"",text_etape_1_2)
    
    #text_etape_1_2=re.sub("(\"”|)","\"",text_etape_1_2)

    #ECRITURE SUR LES FICHIERS
    #with open(chemin_dossier_transcriptions_normalisees, 'w', encoding="utf-8") as outfile: # Ecrire 
    #    json.dump(text_etape_1_2, outfile)
    open(filename,'w',encoding="utf-8").write(text_etape_1_2)
    

#Etape 3: ajout des capitales
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 150000000 # or even higher
    doc = nlp(text) #tokenise
    #tagged_sent = [(w.text, w.pos_,w.tag_) for w in doc] 
    tagged_sent = [(w.text, w.pos_) for w in doc] #pos tag des mots
    #print(tagged_sent)
    normalized_sent = [w.capitalize() if t in ["PROPN"] else w for (w,t) in tagged_sent]
    normalized_sent[0] = normalized_sent[0].capitalize() #ajout majuscule au premier mot de la phrase
    text_etape_1_2_3 = re.sub(" (?=[\[\(\]\).,'!?:;]) ?", "", ' '.join(normalized_sent))
    text_etape_1_2_3=re.sub(" \/ ","/",text_etape_1_2_3)
    
    #ECRITURE SUR LES FICHIERS
    #with open(chemin_dossier_transcriptions_normalisees, 'w', encoding="utf-8") as outfile: # Ecrire 
    #    json.dump(text_etape_1_2_3, outfile)
    open(filename,'w',encoding="utf-8").write(text_etape_1_2_3)

#Etape 4: correction des erreurs spécifiques
#sur google collab, pour utiliser BERT, méthode 1, mais coupe les documents

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
