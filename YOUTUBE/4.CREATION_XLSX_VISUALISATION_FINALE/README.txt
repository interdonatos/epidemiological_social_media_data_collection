1. Création du fichier json contenant tous les tweets
Entrée = collect_transcriptions_normalise_anonymsise_anno_auto_location_thematique/
Lancer la commande bash : 
for i in *.txt;do cat $i >> output.json;done
Sortie = output.json

2. Création du fichier xlsx contenant tous les tweets (fichier final pour la visualisation)
Lancer le script "json_to_xlsx.py"
Entrée = output.json
Sortie = output.xlsx