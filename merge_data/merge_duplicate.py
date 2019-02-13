import csv
import random
import xlrd
import xlwt
import numpy as np
from collections import defaultdict 
import pandas as pd

def read_data(path):
    file=open(path)
    data = csv.reader(file)
    return data

def merge_concept():
    file = open('../database/merge_con_gb_int_z.csv','w+')
    data_gb=read_data('../database/concept_gb.csv')
    data_int=read_data('../database/concept_int.csv')
    id_list=list()
    effectiveTime_list=list()
    active_list=list()
    moduleId_list=list()
    definitionStatusId_list=list()
    merge_list=list()

 #id, effectiveTime, active, moduleId, definitionStatusId
    for item in data_gb:
        id_list.append(item[0])
        effectiveTime_list.append(item[1])
        active_list.append(item[2])
        moduleId_list.append(item[3])
        definitionStatusId_list.append(item[4])

    for item in data_int:
        id_list.append(item[0])
        effectiveTime_list.append(item[1])
        active_list.append(item[2])
        moduleId_list.append(item[3])
        definitionStatusId_list.append(item[4])

    seen_list=list()
    for index1 in range(len(id_list)):
        merge=id_list[index1]+'$'+effectiveTime_list[index1]+'$'+active_list[index1]+'$'+moduleId_list[index1]+'$'+definitionStatusId_list[index1]
        merge_list.append(merge)
        print(merge)

    for merge in merge_list:
        if merge not in seen_list:
            #seen_list.append(merge_list[index3])
            file.write(merge+"\n")


    file.close()

def merge_description():
    file = open('../database/merge_des_gb_int_z.csv','w+')
    data_gb=read_data('../database/description_gb.csv')
    data_int=read_data('../database/description_int.csv')
    id_list=list()
    effectiveTime_list=list()
    active_list=list()
    moduleId_list=list()
    conceptId_list=list()
    languageCode_list=list()
    typeId_list=list()
    term_list=list()
    caseSign_list=list()

    merge_list=list()


 #id, effectiveTime, active, moduleId, conceptId, languageCode,typeId,term,caseSign
    for item in data_gb:
        id_list.append(item[0])
        effectiveTime_list.append(item[1])
        active_list.append(item[2])
        moduleId_list.append(item[3])
        conceptId_list.append(item[4])
        languageCode_list.append(item[5])
        typeId_list.append(item[6])
        term_list.append(item[7])
        caseSign_list.append(item[8])


    for item in data_int:
        id_list.append(item[0])
        effectiveTime_list.append(item[1])
        active_list.append(item[2])
        moduleId_list.append(item[3])
        conceptId_list.append(item[4])
        languageCode_list.append(item[5])
        typeId_list.append(item[6])
        term_list.append(item[7])
        caseSign_list.append(item[8])


    seen_list=list()
    for index1 in range(len(id_list)):
        merge=id_list[index1]+'$'+effectiveTime_list[index1]+'$'+active_list[index1]+'$'+moduleId_list[index1]+'$'+conceptId_list[index1]+'$'+languageCode_list[index1]+'$'+typeId_list[index1]+'$'+term_list[index1]+'$'+caseSign_list[index1]
        merge_list.append(merge)

    for merge in merge_list:
        if merge not in seen_list:
            #seen_list.append(merge_list[index3])
            file.write(merge+"\n")
            
    
    file.close()


def active_filter_con():
    #id_list=list()
    #effectiveTime_list=list()
    #active_list=list()
    #moduleId_list=list()
    #definitionStatusId_list=list()
    full_data=list()
    active_l=list()


    indexTWO=0
    file=open('../database/concept_gb_int_activelist.csv','w+')
    merge_con_data = read_data('../database/merge_con_gb_int_z.csv')
    for item in merge_con_data:
        
        id = item[0].split('$')[0]
        effectiveTime = item[0].split('$')[1]
        active = item[0].split('$')[2]
        moduleId = item[0].split('$')[3]
        definitionStatusId = item[0].split('$')[4]
        full_data.append([])
        full_data[indexTWO].append(id)
        full_data[indexTWO].append(effectiveTime)
        full_data[indexTWO].append(active)
        full_data[indexTWO].append(moduleId)
        full_data[indexTWO].append(definitionStatusId)
        indexTWO=indexTWO+1

    full_data_sort=sorted(full_data,key=lambda s:s[1],reverse=False)
    
    #timeDict=defaultdict(list)
    activeDict=defaultdict(list)
    #moduleIdDict=defaultdict(list)
    #definitionSDict=defaultdict(list)

    for row in range(len(full_data_sort)):
        active_l.append([])
        active_l[row].append(full_data_sort[row][0])
        active_l[row].append(full_data_sort[row][2])

    for k,v in active_l:
        activeDict[k].append(v)

    for i in range(len(full_data_sort)):
        if full_data_sort[i][0] in activeDict:
            #print(activeDict[full_data_sort[i][0]])
            len_ac=len(activeDict[full_data_sort[i][0]])-1
            if activeDict[full_data_sort[i][0]][len_ac]=='1':
                file.write(str(full_data_sort[i][0])+"$")
                file.write(str(full_data_sort[i][1])+"$")
                file.write(str(full_data_sort[i][2])+"$")
                file.write(str(full_data_sort[i][3])+"$")
                file.write(str(full_data_sort[i][4])+"\n")
                print(str(full_data_sort[i][0]))
    file.close()
    

def active_filter_des():

    full_data=list()
    active_l=list()

    merge_con_data=list()
    indexTWO=0
    file=open('../database/description_gb_int_activelist.csv','w+')
    for line in open("../database/merge_des_gb_int_z.csv","r"):
        merge_con_data.append(line) 
    #merge_con_data = read_data('../database/merge_des_gb_int_z.csv')
    for item in merge_con_data:
        #print(item)
        id = item.split('$')[0]
        effectiveTime = item.split('$')[1]
        active = item.split('$')[2]
        moduleId = item.split('$')[3]
        conceptId = item.split('$')[4]
        languageCode = item.split('$')[5]
        typeId = item.split('$')[6]
        term = item.split('$')[7]
        caseSign = item.split('$')[8]
        full_data.append([])
        full_data[indexTWO].append(id)
        full_data[indexTWO].append(effectiveTime)
        full_data[indexTWO].append(active)
        full_data[indexTWO].append(moduleId)
        full_data[indexTWO].append(conceptId)
        full_data[indexTWO].append(languageCode)
        full_data[indexTWO].append(typeId)
        full_data[indexTWO].append(term)
        full_data[indexTWO].append(caseSign)
        indexTWO=indexTWO+1

    full_data_sort=sorted(full_data,key=lambda s:s[1],reverse=False)
    
    #timeDict=defaultdict(list)
    activeDict=defaultdict(list)
    #moduleIdDict=defaultdict(list)
    #definitionSDict=defaultdict(list)

    for row in range(len(full_data_sort)):
        active_l.append([])
        active_l[row].append(full_data_sort[row][0])
        active_l[row].append(full_data_sort[row][2])

    for k,v in active_l:
        activeDict[k].append(v)

    num=0
    for i in range(len(full_data_sort)):
        if full_data_sort[i][0] in activeDict:
            #print(activeDict[full_data_sort[i][0]])
            len_ac=len(activeDict[full_data_sort[i][0]])-1
            if activeDict[full_data_sort[i][0]][len_ac]=='1':  
                file.write(str(full_data_sort[i][0])+"$")
                file.write(str(full_data_sort[i][1])+"$")
                file.write(str(full_data_sort[i][2])+"$")
                file.write(str(full_data_sort[i][3])+"$")
                file.write(str(full_data_sort[i][4])+"$")
                file.write(str(full_data_sort[i][5])+"$")
                file.write(str(full_data_sort[i][6])+"$")
                file.write(str(full_data_sort[i][7])+"$")
                file.write(str(full_data_sort[i][8]))
                if '"' in full_data_sort[i][7]:
                    print(full_data_sort[i][7])
                
    print(num)
    file.close()


def merge_relationship():
    data_gb=pd.read_csv('../database/relationship_gb.csv')
    data_int=pd.read_csv('../database/relationship_int.csv')
    print(len(data_gb))
    print(len(data_int))
    linked_list=pd.concat([data_gb,data_int],axis=0)
    print(len(linked_list))
    linked_list=linked_list.drop_duplicates()
    print(len(linked_list))
    #linked_list.to_csv('../database/relationship.csv',index=False)

def active_filter_rela():
    data=pd.read_csv('../database/relationship.csv')
    dict={}
    for index,row in data.iterrows():
        print(index)
        key=str(row['id'])+"_"+str(row['moduleId'])+"_"+str(row['sourcedId'])\
            +"_"+str(row['destinationId'])+"_"+str(row['relationshipGroup'])\
            +"_"+str(row['typeId'])+"_"+str(row['chracteristicTypeId'])+"_"+str(row['modifierId'])
        value=str(row['effectivetime'])+"_"+str(row['active'])
        if(key in dict):
            storage=dict[key]
            time1,active_flag1=storage.split("_") #time in dict
            time2,active_flag2=value.split("_")  #time new input
            if(int(time1)>=int(time2)):
                if(active_flag1=='0' and active_flag2!='0'):
                    dict.pop(key)
                elif(active_flag1=='0' and active_flag2=='0'):
                    dict.pop(key)
                else:
                    dict[key]=storage
            elif(int(time2)>int(time1)):
                if(active_flag1=='0' and active_flag2=='0'):
                    dict.pop(key)
                elif(active_flag2=='0' and active_flag1=='1'):
                    dict.pop(key)
                else:
                    dict[key]=value
            else:
                dict[key]=value
        else:
            dict[key]=value

    dict_res={}
    for key,value in dict.items():
        effectivetime,active=value.split("_")
        id, moduleId, sourcedId, destinationId, relationshipGroup, typeId, chracteristicTypeId, modifierId=key.split("_")
        if(active!='0'):
            list=[]
            list.append(effectivetime)
            list.append(active)
            list.append(moduleId)
            list.append(sourcedId)
            list.append(destinationId)
            list.append(relationshipGroup)
            list.append(typeId)
            list.append(chracteristicTypeId)
            list.append(modifierId)
            dict_res[id]=list

    res=pd.DataFrame.from_dict(dict_res,orient='index')
    res.to_csv('../database/relationship_gb_int_activelist.csv')

if __name__ == '__main__':
    #active_filter_rela()
    merge_relationship()
    

