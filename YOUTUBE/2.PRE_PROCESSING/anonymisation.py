"""
This script allows to anonymize the names and pseudos of users present in the texts of tweets in English.
As input, we have a .txt file containing the text of a tweet
In output, we have a .txt file containing the anonymized text of the input tweet

To anonymize the twitter pseudos in the text, we use a simple regex, to substitute "@pseudo" to "USER".

To anonymize the names present in the texts, we use the named entity recognition of the Flair tool. We first tag the entities in the text, then with the help of a regex, we substitute the entities labeled PER to "NAME". Finally, we remove any other labels (like location, etc).

NB: There may be some errors in the recognition of named entities found by Flair.

Example tweet :
"@josh25 Kristien Van Reeth, a professor of virology at Ghent University in Belgium, and Sarah Gregory discuss a case of avian-like swine influenza in a pig farmer in the Netherlands"

Example anonymise tweet :
USER NAME Van NAME , a professor of virology at Ghent University in Belgium , and NAME NAME discuss a case of avian-like swine influenza in a pig farmer in the Netherlands 
"""

#import of the librairies
from tqdm import tqdm
import os, glob
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
from segtok.segmenter import split_single
import shutil
import re
import spacy
nlp = spacy.load("en_core_web_sm")
import numpy as np

"""
#input text
input_file="tweet.txt"
#output text
output_file="tweet_anonymise.txt"

#open file and read it
fi=open(input_file, "r", encoding="utf-8").read()
"""

#Variables des données
chemin_dossier_transcriptions_normalisees="dossier_txt_transcriptions_v2_100_normalise"
chemin_dossier_transcriptions_normalisees_anonymisation="dossier_txt_transcriptions_v2_100_normalise_anonymise"

#copier le dossier original, afin de pouvoir faire les traitements sur un nouveau dossier
if not os.path.exists(chemin_dossier_transcriptions_normalisees_anonymisation):
    shutil.copytree(chemin_dossier_transcriptions_normalisees, chemin_dossier_transcriptions_normalisees_anonymisation)

folder_path = (chemin_dossier_transcriptions_normalisees_anonymisation)

for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    #anonymise user name
    text=re.sub("@[a-zA-Z0-9-_]+","<NAME>",text)
    
    doc=nlp(text)
    #final,ch,f="","",False

        
    tags =np.array( [[token.text_with_ws, token.pos_] for token in doc])
    for ent in doc.ents:
        #1 : pour colonne 2
        tags[ent.start:ent.end,1] = ent.label_    
    #print(tags)

    #Afficher les entités nommés tagués dans le texte, sans problème de tokenisation et d'espace en trop
    final,ch,f,i ="","",False,0 # final = Texte finale, ch = chaine de caractère tampon, f = si une entité nommé a été détéctée, i = position dans les parcours de 'tags'

    while i < len(doc): #tant que not end of file
        if tags[i,1]== "PERSON": #si le mot est tagué "LOC"
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
                final+="<NAME> ".format(ch) #annotation de la loc
                f=False             
            final+=tags[i,0] #concaténation du résultat dans final
        i+=1

    #ECRITURE SUR LES FICHIERS
    open(filename,'w',encoding="utf-8").write(final) #les articles sont tagués par spacy et écrits dans les fichiers
    print(final)
    
    """
    #anonymise user name
    fi=re.sub("@[a-zA-Z0-9-_]+","<USER>",text)

    #detect entities "PERSON" and tag text
    sentences = Sentence(fi, use_tokenizer=True)
    # Run NER over sentence
    tagger.predict(sentences)
    #tag the text
    tag=sentences.to_tagged_string()
    
    #anonymise entities that have label "PERSON"
    tag=re.sub("[\w'-]+ <(B|E|S)-PERSON>","<NAME>",tag)
    
    #remove tags from other labels entities
    tag=re.sub("<[A-Z-]+-[A-Z-]+>","",tag)
    tag=re.sub("  ", " ", tag) #remove blank space in plus
    print(tag)
    
    #write the result in the ouput file (append mode)
    fo=open(text, "a", encoding="utf-8").write(tag)
    """
    

