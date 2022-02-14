# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:46:36 2021

@author: camille.schaeffer
"""

import sys
import pprint
import xlsxwriter
import json
import re

#with open("dossier_transcriptions2411/output.json", encoding="utf-8") as infile:
#    jstring = infile.read()
#    data = json.loads(re.sub('$',']}', jstring))

#with open('dossier_transcriptions2411/output.json','w') as mon_fichier:
#    json.dump(data, mon_fichier)

class FileManagement:
    def __init__(self):
        self.json_file_name="dossier_transcriptions2411/output.json"
        self.excel_file_name="output.xlsx"
        self.array_id_=[]
        self.array_date=[]
        self.array_transcript=[]
        self.array_spatial_entities=[]
        self.array_thematic_entities=[]
        #self.array_end_video=[]
        self.array_sum=[]
        
    def read_text_file(self):
        try:
            with open(self.json_file_name, encoding="utf-8") as data_file:
                #print(data_file)
                data=json.load(data_file)
                #print(data)
                for each_axis in data['Video']:
                    id_=str(each_axis["id"])
                    date=str(each_axis["date"])
                    transcript=str(each_axis["transcript"])
                    spatial_entities=str(each_axis["Spatial Entities"])
                    thematic_entities=str(each_axis["Thematic Entities"])
                    #description=str(each_axis["description"])
                    #transcript=str(each_axis["transcript"])
                    #end_video=int(each_axis)["end_video"]
                    self.array_id_.append(id_)
                    self.array_date.append(date)
                    self.array_transcript.append(transcript)
                    self.array_spatial_entities.append(spatial_entities)
                    self.array_thematic_entities.append(thematic_entities)
                    #self.array_end_video.append(end_video)
                    self.array_sum.append(id_+date+transcript+spatial_entities+thematic_entities)
                    #pprint.pprint("date={0}".format(date))
                    #pprint.pprint("y={0}".format(y))
        except:
            print("unexcept error : ", sys.exc_info()[0])
            raise
    
    def save_to_xlsx(self):
        workbook=xlsxwriter.Workbook(self.excel_file_name)
        worksheet=workbook.add_worksheet()
        #
        for index, value in enumerate(self.array_id_):
            worksheet.write(index,0,self.array_id_[index]) #column 0
            worksheet.write(index,1,self.array_date[index])
            worksheet.write(index,2,self.array_transcript[index])
            worksheet.write(index,3,self.array_spatial_entities[index])
            worksheet.write(index,4,self.array_thematic_entities[index])
            #worksheet.write(index,5,self.array_end_video[index])
            #worksheet.write(index,5,self.array_sum[index])
        workbook.close()

if __name__ == '__main__':
    file_management = FileManagement()
    file_management.read_text_file()
    file_management.save_to_xlsx()
