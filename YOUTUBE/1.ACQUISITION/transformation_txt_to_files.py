import re
import os, glob
from tqdm import tqdm 


#couper le fichier json en plusieurs fichiers txt


json_transcription="file-name_jsonformat_238.json"
dossier_txt_transcriptions="dossier_txt_tweets_238-2/"
#text=open(chemin_dossier_articles,encoding="utf-8").read()
#text=re.sub("\n","\nxxxxx\n",text)
#open(chemin_dossier_articles,"w",encoding="utf-8").write(text)

if not os.path.exists(dossier_txt_transcriptions):
 os.makedirs(dossier_txt_transcriptions)

with open(json_transcription,'r', encoding="utf-8") as fo:
    start=0
    op=''
    cntr=1
    for x in fo.read().split('"end_video": ""},'):
        #print(x)
        
        #if(x=='end_video'):
        if(start==0):
            #Création et écriture des fichiers
            opf=open(dossier_txt_transcriptions+str(cntr)+'.txt','w', encoding="utf-8") # !!!!! attention créer manuellement le dossier avant sinon ne marche pas !!!!!#
            opf.write(op)
            opf.write(x)
            opf.close()
            op=''
            cntr+=1
        else:
            start=1
    else:
        #ecriture de l'article
        op=op.strip() + x
fo.close()
print ('completed')

#Ouverture et Ecriture de tous les articles à la suite dans un fichier txt
#fic=open(ecriture_articles_fichier_csv, mode='w',encoding='utf-8')
#fic.write(chaine.strip())

#supprimer éléments indésirables

folder_path = (dossier_txt_transcriptions)

for filename in tqdm(glob.glob(os.path.join(folder_path, '*.txt'))):
    text=open(filename,encoding="utf-8").read()
    text=re.sub("\"{","{\"",text)
    text=re.sub("id:","id\": \"",text)
    text=re.sub("date:","\", \"date\": \"",text)
    text=re.sub("tweet:b('|\")","\", \"tweet\": \"",text)
    text=re.sub("'\"\"","\"",text)
    text=re.sub("\"tweet\": \"\"","\"tweet\": \"",text)
    text=re.sub("\"\"\"\"","\"",text)
    
    open(filename,'w',encoding="utf-8").write(text)

