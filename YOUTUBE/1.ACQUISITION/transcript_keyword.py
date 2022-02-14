#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:51:13 2020

@author: ace
"""

#%% Installation de l'api de google 
#pip install youtube_transcript_api
#Importation de la bibliotheque YouTubeTranscriptApi
from youtube_transcript_api import YouTubeTranscriptApi 

#%% Définition d'une fonction qui va afficher True si une vidéo contient un sous titre sinon False
def is_avail(v_id):
  try:
      transcript_list = YouTubeTranscriptApi.get_transcript(v_id,languages=['en'])
      return True
  except:
    return False
is_avail("tBBjJnQpvoM")

#%%

from requests import get # module permetttant d'utiliser le http 
def get_trans(start_token=""): #Fonction permettant de récuperer le token par page 
  
  api_key = "AIzaSyDmq_KWyit_TLzHE0EbF7VU2QtNbdb2B4I" #Clé Api fournit par Youtube
  #channel_id = "UCZl9utbYlPMssMhgrGUqXZA" # Id de la chaine RTB Youtube
  #channel_id = "UCGAR1p-zHqYAKo2Y1EtMnrg" # Id de la chaine SantépubliqueFrance
  keyword = "avian influenza" #pas une chaine maisq requete youtube Grippe aviaire, test
  #channel_id"UCv6qHPwghGsyOfzEYZXcfKg" # Id de la chaine Allo Docteurs
  max_result = 25 #nombre de videos sous titrés par page #25
  datas = [] #Variable datas qui va contenir la liste des videos avec leur id
  # la condition pour commence a partir d'un token sinon commence a partir d'un token vide
  if start_token == "":
    response = get("https://www.googleapis.com/youtube/v3/search?q="+keyword+"&key="+api_key+"&part=snippet,id&order=date&maxResults="+str(max_result))
  else:
    response = get("https://www.googleapis.com/youtube/v3/search?q="+keyword+"&key="+api_key+"&part=snippet,id&order=date&maxResults="+str(max_result)+"&pageToken="+start_token)
  response_json = response.json()
  datas.append(response_json)
  nextPageToken = response_json.get("nextPageToken")
  # Récupérer tout le reste des pages
  page = 1
  while nextPageToken:
      print(nextPageToken)
      try:
        r = get("https://www.googleapis.com/youtube/v3/search?q="+keyword+"&key="+api_key+"&part=snippet,id&order=date&maxResults="+str(max_result)+"&pageToken="+nextPageToken)
        json_data = r.json()
        datas.append(json_data)
        nextPageToken = json_data.get("nextPageToken")
        page += 1
      except:
        break
  print("last page : ",page," ; token : ",nextPageToken)
  return datas,nextPageToken

import pickle,json #import de la bibliotheque json et de pickle
datas,last_token = get_trans()
pickle.dump(datas,open("datas_1000.dp","wb"))


def flattening(l):
    """ fonction permettant de rendre la liste en une seule dimension """
    d = []
    for res in l:
        for ob in res['items']:
            d.append(ob)
    return d
        

datas = pickle.load(open("datas_1000.dp","rb")) #Charger le fichier datas_1000.dp

# ud = [len(i['items']) for i in datas]
# print(ud)
# print(datas[-1])
datas = flattening(datas)


ted = 0
total = 0
data = {}
data['video'] = []
v1 = ""
v2 = ""
v3 = ""
v4 = ""
v5 = ""
v6 = ""
#v7 = ""

#OUTPUT_FILENAME = "corpus_1000_videos_newENCODE.json"
OUTPUT_FILENAME = "corpus_videos_avian influenza_2510_v3.json"

for ob in datas:
    #print(res['items'])
    #print(ob['id']['videoId']," : ",is_avail(ob['id']['videoId']))
    total += 1
    if "videoId" in ob["id"]:
      if is_avail(ob['id']['videoId']):
        trans = YouTubeTranscriptApi.get_transcript(ob['id']['videoId'],languages=['en'])
        ted += 1
        transcript = ""
        for t in trans:
          transcript +=" " + t['text']
        v1 = ob['id']['videoId']
        v2 = ob['snippet']['publishedAt']
        v3 = ob['snippet']['title']
        v4 = ob['snippet']['description']
        v5 = transcript
        #v6 = ob['snippet']['channelTitle']
        v7 = ''
        #v7 = ob['snippet']['country']
        #localized = results['items'][0]['snippet']['localized']  #ESSAYEZ CA COURAGE
        #localizations = results['items'][0]['localizations'] #ET ça
        #v7 = ob['snippet'].get('country')
        print(ob['snippet']['publishedAt'])
        data['video'].append({
      'id': v1,
      'date': v2,
      'title': v3,
      'description': v4,
      'transcript': v5,
      #'channel_title' : v6,
      'end_video' : v7
      #'country source' : v7
      })

with open(OUTPUT_FILENAME, 'a', encoding="utf-8") as outfile: # Ecrire le fichier de notre corpus
    #json.dump(data, outfile, ensure_ascii=False).encode('utf-8')
    json.dump(data, outfile, ensure_ascii=False)



#%%
