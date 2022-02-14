# -*- coding: utf-8 -*-
"""
Ce script permet d'annoter automatiquement les entités spatiales (GPE, LOC et FAC) d'un dossier de fichier .txt avec Spacy
"""

import spacy
import os, glob
import numpy as np
from tqdm import tqdm
import shutil
import re
import sys
import numpy as np
import csv
import itertools
import pandas as pd

#Variables chemin textes
chemin_dossier_articles="dossier_txt_transcriptions_normalise_anonmysisation_100"
chemin_dossier_articles_spacy="dossier_txt_transcriptions_normalise_anonmysisation_100_anno_auto_location"

#text="While the European Meat and Poultry Market is Hampered by Avian Influenza, British Producers Struggle with Brexit Shocks CRYPTO CRYPTO NEWS - https://t.co/aknaWAINeg"

#######SPACY#######
print("Traitement spacy")

nlp = spacy.load("en_core_web_sm")

################################# ANNOTATION DES ENTITES SPATIALES - GPE #################################

#copier le dossier original, afin de pouvoir faire les traitements sur un nouveau dossier
if not os.path.exists(chemin_dossier_articles_spacy):
    shutil.copytree(chemin_dossier_articles, chemin_dossier_articles_spacy)

folder_path = (chemin_dossier_articles_spacy) #à changer
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    open(filename,'a',encoding="utf-8").write(', "Spatial Entities": "')
    doc=nlp(text)
    #tableau mot + tag
    tags =np.array( [[token.text_with_ws, token.pos_] for token in doc])
    for ent in doc.ents:
        tags[ent.start:ent.end,1] = ent.label_ 
        
        if ent.label_ in ['LOC', 'GPE', 'FAC']:
            ent="('"+ent.text+"', "+ent.label_+")"
            print(ent)
            #print(basename(filename),ent.text, ent.label_,j) 
            open(filename,'a',encoding="utf-8").write(ent)
    open(filename,'a',encoding="utf-8").write('" ')
    
    """
    for ent in doc.ents:
        #1 : pour colonne 2
        tags[ent.start:ent.end,1] = ent.label_    
    #print(tags)

    #Afficher les entités nommés tagués dans le texte, sans problème de tokenisation et d'espace en trop
    final,ch,f,i ="","",False,0 # final = Texte finale, ch = chaine de caractère tampon, f = si une entité nommé a été détéctée, i = position dans les parcours de 'tags'

    while i < len(doc): #tant que not end of file
        if tags[i,1]== "GPE": #si le mot est tagué "LOC"
            if not f: #si n'a pas été détecté comme une entité nommée
                #ch=ch.strip()
                ch = tags[i,0] #on écrit le mot
                
                f= True
            elif f: #si a été détectée en tant que LOC
                #ch=ch.strip()
                ch+=tags[i,0] #concaténation du mot annoté comme LOC dans ch
                
        else:
            if f: #si a été détectée en tant que LOC
                ch=ch.strip(" ")
                final+="['{0}', 'GPE'] ".format(ch) #annotation de la loc
                f=False             
            final+=tags[i,0] #concaténation du résultat dans final
        i+=1

    #ECRITURE SUR LES FICHIERS
    open(filename,'w',encoding="utf-8").write(final) #les articles sont tagués par spacy et écrits dans les fichiers
    print(final)


################################# ANNOTATION DES ENTITES SPATIALES - LOC #################################

folder_path = (chemin_dossier_articles_spacy)
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    #text=open(filename,encoding="utf-8").read()
    doc=nlp(text)
    #tableau mot + tag
    tags =np.array( [[token.text_with_ws, token.pos_] for token in doc])
    for ent in doc.ents:
        #1 : pour colonne 2
        tags[ent.start:ent.end,1] = ent.label_    
    #print(tags)

    #Afficher les entités nommés tagués dans le texte, sans problème de tokenisation et d'espace en trop
    final,ch,f,i ="","",False,0 # final = Texte finale, ch = chaine de caractère tampon, f = si une entité nommé a été détéctée, i = position dans les parcours de 'tags'

    while i < len(doc): #tant que not end of file
        if tags[i,1]== "LOC": #si le mot est tagué "LOC"
            if not f: #si n'a pas été détecté comme une entité nommée
                #ch=ch.strip()
                ch = tags[i,0] #on écrit le mot
                
                f= True
            elif f: #si a été détectée en tant que LOC
                #ch=ch.strip()
                ch+=tags[i,0] #concaténation du mot annoté comme LOC dans ch
                
        else:
            if f: #si a été détectée en tant que LOC
                ch=ch.strip(" ")
                final+="['{0}', 'LOC'] ".format(ch) #annotation de la loc
                f=False             
            final+=tags[i,0] #concaténation du résultat dans final
        i+=1
        
    #ECRITURE SUR LES FICHIERS
    open(filename,'w',encoding="utf-8").write(final) #les articles sont tagués par spacy et écrits dans les fichiers 
    print(final)
    
################################# ANNOTATION DES ENTITES SPATIALES - FAC #################################
  
folder_path = (chemin_dossier_articles_spacy)
for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    #text=open(filename,encoding="utf-8").read()
    doc=nlp(text)
    #tableau mot + tag
    tags =np.array( [[token.text_with_ws, token.pos_] for token in doc])
    for ent in doc.ents:
        #1 : pour colonne 2
        tags[ent.start:ent.end,1] = ent.label_    
    #print(tags)

    #Afficher les entités nommés tagués dans le texte, sans problème de tokenisation et d'espace en trop
    final,ch,f,i ="","",False,0 # final = Texte finale, ch = chaine de caractère tampon, f = si une entité nommé a été détéctée, i = position dans les parcours de 'tags'

    while i < len(doc): #tant que not end of file
        if tags[i,1]== "FAC": #si le mot est tagué "LOC"
            if not f: #si n'a pas été détecté comme une entité nommée
                #ch=ch.strip()
                ch = tags[i,0] #on écrit le mot
                
                f= True
            elif f: #si a été détectée en tant que LOC
                #ch=ch.strip()
                ch+=tags[i,0] #concaténation du mot annoté comme LOC dans ch
                
        else:
            if f: #si a été détectée en tant que LOC
                ch=ch.strip(" ")
                final+="['{0}', 'FAC'] ".format(ch) #annotation de la loc
                f=False             
            final+=tags[i,0] #concaténation du résultat dans final
        i+=1
        
    #ECRITURE SUR LES FICHIERS
    open(filename,'w',encoding="utf-8").write(final) #les articles sont tagués par spacy et écrits dans les fichiers 
    print(final)"""