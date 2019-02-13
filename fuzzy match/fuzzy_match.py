import csv
import random
import xlrd
import xlwt
from datetime import datetime
import pandas as pd
import os

def input_termdata():
    file1 = open('sct2_Description_Full_20180731_only_term_conceptId.csv')
    term_list = list()
    date_list = list()
    snomedId_list = list()
    data = csv.reader(file1)
    for item in data:
        term = item[2]
        date = item[0]
        id = item[1]
        snomedId_list.append(id)
        date_list.append(date)
        term_list.append(term)

    return term_list, date_list, snomedId_list


def input_datedata():
    file1 = open('sct2_Description_Full_20180731_only_term_conceptId.csv')
    data = csv.reader(file1)
    date_list = list()

    for item in data:
        date = item[0]
        date_list.append(date)
    return date_list


def input_iddata():
    file1 = open('sct2_Description_Full_20180731_only_term_conceptId.csv')
    data = csv.reader(file1)
    snomedId_list = list()

    for item in data:
        id = item[1]
        snomedId_list.append(id)
    return snomedId_list


# Put data in a 2 dim list
def readIn():
    reference_data,date_data,id_data= input_termdata()
    #date_data = list(input_datedata())
    #id_data = list(input_iddata())
    # print(len(reference_data))
    des_full_data = []

    for row in range(len(reference_data)):
        des_full_data.append([])
        des_full_data[row].append(id_data[row])
        des_full_data[row].append(date_data[row])
        des_full_data[row].append(reference_data[row])
    # print(des_full_data[row])
    return des_full_data

def fuzzy_match():
    des_full_data = readIn()  # read the formatted data
    reference_data = [column[2] for column in des_full_data]  # read term data
    excel = xlrd.open_workbook('dataset for automated mapping.xlsx')
    table1 = excel.sheet_by_name(u'Sheet1')
    nrow1 = table1.nrows
    count = 0
    file2 = open('fuzzy_match_new.txt', 'a+')
    i = 0

    # sort_index_list = list()
    # sort_index_list.append(0)

    while (i < nrow1):
        list_name = list()  # the term list after the filter
        list_ID = list()  # the SNOMETed ID list after the filter
        list_date = list()  # the date list after the filter
        list_ratio = list()  # the ratio after fuzzy match
        seen_ID = list()  # the SNOMTED ID list of the final results
        seen_date = list()  # the date list of the final results
        seen_name = list()  # the term name list of the final results
        seen_ratio = list()  # the ratio list of the final results
        seen_input = list()
        if (i == 0):
            i = i + 1
        time1 = datetime.now()
        # print(time1)
        input = table1.row_values(i)[2]

        for index in range(len(reference_data)):
            likehood = compute_likehood(input, reference_data[index])
            if likehood > 0.4:
                list_name.append(reference_data[index])
                list_ratio.append(likehood)
                list_date.append(des_full_data[index][1])
                list_ID.append(des_full_data[index][0])

        # Update the ID with the newest date
        for index2 in range(len(list_ID)):
            if list_name[index2] not in seen_name:  # If the name appears the first time, it should be added in the list
                seen_input.append(input)
                seen_ID.append(list_ID[index2])
                seen_date.append(list_date[index2])
                seen_name.append(list_name[index2])
                seen_ratio.append(list_ratio[index2])

            else:  # If it is already appeared, do the comparison
                dup_list = [j for j, x in enumerate(seen_name) if x == list_name[index2]]
                dup_list_index = dup_list[0]  # find the dup_index in the formal list
                if seen_date[dup_list_index] < list_date[index2]:  # if the date is bigger,replace with the new object
                    seen_input[dup_list_index] = input
                    seen_ID[dup_list_index] = list_ID[index2]
                    seen_date[dup_list_index] = list_date[index2]
                    seen_name[dup_list_index] = list_name[index2]
                    seen_ratio[dup_list_index] = list_ratio[index2]
        # print(seen_name)
        len_fuzzy_match = len(seen_name)
        time2 = datetime.now()
        count += len_fuzzy_match  # locate the index of the last fuzzy match
        # sort_index_list.append(count-1)
        print("input:" + input)
        print("sum:" + str(count))
        # print("now i:"+str(i))
        print("time:" + str((time2 - time1).seconds))
        return_Matrix = []
        return_Matrix = ratio_range(seen_ID, seen_date, seen_name, seen_ratio)

        seen_ID = [x[0] for x in return_Matrix]
        # seen_date=[x[1] for x in return_Matrix]
        seen_name = [x[2] for x in return_Matrix]
        seen_ratio = [x[3] for x in return_Matrix]
        print(seen_ratio)

        if (len_fuzzy_match != 0 and str(seen_ratio[0]) == '1.0'):
            len_fuzzy_match = 1

        for m in range(len_fuzzy_match):
            file2.write(str(input) + "///")
            # file2.write(str(seen_date[m])+"/")
            file2.write(str(seen_ID[m]) + "///")
            file2.write(str(seen_name[m]) + "///")
            file2.write(str(seen_ratio[m]) + '\n')

        i = i + 1
    file2.close()


def ratio_range(ID, date, name, ratio):
    sortMatrix = []
    sortMatrix1 = []
    for row in range(len(ID)):
        sortMatrix.append([])
        sortMatrix[row].append(ID[row])
        sortMatrix[row].append(date[row])
        sortMatrix[row].append(name[row])
        sortMatrix[row].append(ratio[row])

    sortMatrix1 = sorted(sortMatrix, key=lambda s: s[3], reverse=True)
    # print(sortMatrix1)
    return sortMatrix1

def descrption():
    file1=open('description_gb.csv','r',encoding='utf-8-sig')
    file2=open('description_int.csv','r',encoding='utf-8')
    dict={}
    data1=csv.reader(file2)

    for item1 in data1:
        if(item1[2] in dict):
            time1=item1[0]
            time2=dict[item1[2]][0]
            new_time=compare_time(time1,time2)
            dict[item1[2]]=[new_time,item1[1]]
        else:
            dict[item1[2]]=[item1[0],item1[1]]


    for item2 in file1.readlines():
        item=item2.replace("\n",'').split(",",2)
        if(item[2] in dict):
            time3 = item[0]
            time4 = dict[item[2]][0]
            new_time2 = compare_time(time3, time4)
            dict[item[2]] = [new_time2, item[1]]
        else:
            dict[item[2]] = [str(item[0]), str(item[1])]

    dict2={}
    for item3 in dict.keys():
        dict2[dict[item3][1]]=item3

    input_data=open('fuzzy_match_new.txt','r',encoding='utf-8')
    output_data=open('fuzzy_match_descrip.txt','w+')
    for item3 in input_data.readlines():
        item4=item3.replace('\n','').split('///')
        if(item4[1] in dict2):
            output_data.write(str(item4[0])+"#")
            output_data.write(str(item4[1])+"#")
            output_data.write(str(item4[2])+"#")
            output_data.write(str(item4[3])+"#")
            output_data.write(str(dict2[item4[1]])+'\n')
        else:
            output_data.write(str(item4[0])+"#")
            output_data.write(str(item4[1])+"#")
            output_data.write(str(item4[2])+"#")
            output_data.write(str(item4[3])+"#")
            output_data.write(str('NULL')+'\n')
    output_data.close()

def descrption2():
    path=os.getcwd()
    file=open(path+"/fuzzy match/sct2_Description_Full_20190109_only_term_conceptId.csv","r")
    dict={} #len=57638
    list=[]
    for ii in file.readlines():
        if(("(procedure)" in ii)):
            list.append(ii)

    for i in list:
        data=i.strip()
        data1=data.split("$")
        if(data1[1] in dict):
            dict[data1[1]]=data1[2]
        else:
            dict[data1[1]]=data1[2]

    #print(dict2)
    data=xlrd.open_workbook(path+"/fuzzy match/fuzzy_match_preCard.xls").sheet_by_name('sheet1')
    nrow=data.nrows
    output=open("procedure_preCard.csv",'w')
    for i1 in range(nrow):
        if(i1==0):
            continue
        id=str(data.row_values(i1)[3])
        if('.0' in id):
            id=id[:-2]

        if(id in dict):
            output.write(str(dict[id])+"\n")
        else:
            output.write("None"+"\n")
    output.close()

def compare_time(time1,time2):
    time1_year=time1[0:4]
    time2_year=time2[0:4]
    #print(time1_year)
    #print(time2_year)
    #print("!!!")
    time1_month=time1[4:6]
    time2_month=time2[4:6]
    if(int(time2_year)>int(time1_year)):
        return time2
    elif(int(time2_year)<int(time1_year)):
        return time1

    if(int(time1_month)>int(time2_month)):
        return time1
    if(int(time2_month)>int(time1_month)):
        return time2

    return time1


#对输入数据进行处理去除特殊符号
#去除特殊词组
def process_data(term1,term2):
    # 先去掉特殊符号,不留空
    special_charater1 = ['"', "+", "+/-", "&", "(", ")",","]
    for sc in special_charater1:
        term2 = term2.replace(sc, "")
        term1 = term1.replace(sc, "")
    # 去掉但是要留空的
    special_charater2 = [" - ", " / ","/", "  ", ]
    for sc2 in special_charater2:
        term2 = term2.replace(sc2, " ")
        term1 = term1.replace(sc2, " ")
    word1 = term1.replace('"', '').split(' ')  # 去除"且用空格分离
    word2 = term2.replace('"', '').split(' ')

    # 特殊字符加入一个set
    special_word = ['and', 'or', 'with', 'of', 'surgery', 'operation', 'special acharacters',
                    'space', 'test', 'treatment', 'examination', 'from', 'to', 'using', 'left',
                    'right', 'bilateral', 'yes/no','in']
    special_word_set = set()
    for i in special_word:
        special_word_set.add(i)

    # 去除特殊字符
    for iii in word1:
        if (iii in special_word_set):
            word1.remove(iii)
        if (len(iii)==0):
            word1.remove(iii)
    for ii in word2:
        if (ii in special_word_set):
            word2.remove(ii)
        if (len(ii)==0):
            word2.remove(ii)

    #word1=list(set(word1))
    #word2=list(set(word2))
    return word1,word2


def compute_likehood(term1,term2):
    word1,word2=process_data(term1,term2)
    #计算相似度
    #比较的前提是word1和word2有交集
    #如果word1长度大于word2 则backward
    #如果word1长度小于word2 则forward
    likehood=0
    #print(word1)
    #print(word2)
    insection=check_insection(word1,word2)  #返回交集
    #print(insection)
    #交集为空
    #print(insection)
    if(len(insection)==0):
        likehood=0
    else:
        word1_len=len(word1)
        word2_len=len(word2)
        insection_len=len(insection)
        if(word1_len>=word2_len):
            likehood=insection_len/word1_len
        else:
            likehood=insection_len/word2_len

    return likehood

#查询两个词组是否有交集
def check_insection(word1,word2):
    res=[]
    temp_set=set()
    for i in word1:
        temp_set.add(i)

    for ii in word2:
        if(ii in temp_set):
            #print(ii)
            res.append(ii)

    return res

def fuzzy_match_preference_card():
    excel = xlrd.open_workbook('snomed CT ID&alias.xlsx')
    table1 = excel.sheet_by_name(u'Sheet1')
    nrow=table1.nrows
    reference_item={}
    for i in range(nrow):
        if(i==0):
            continue
        reference_item[table1.row_values(i)[0]]=table1.row_values(i)[2]
        if(table1.row_values(i)[1]!=''):
            temp=table1.row_values(i)[1].split("\n")
            for i1 in range(len(temp)-1):
                reference_item[temp[i1]]=table1.row_values(i)[2]


    excel2=xlrd.open_workbook('preference card.xls')
    table2=excel2.sheet_by_name(u"Sheet1")
    nrow2=table2.nrows

    file2 = open('fuzzy_match_preference_card_number.txt', 'a+')

    for i2 in range(nrow2):
        temp2=table2.row_values(i2)[1].strip()
        match_item=list()
        match_ratio=list()
        for reference in reference_item:
            ratio=compute_likehood(temp2,reference)
            if(ratio>0.4):
                match_item.append(reference)
                match_ratio.append(ratio)

        sortMatrix=ratio_range2(match_item,match_ratio)
        #print(sortMatrix)
        name=[x[0] for x in sortMatrix]
        ratio = [x[1] for x in sortMatrix]

        #print(ratio)
        #print(name)
        #print("input"+temp2)
        #print("sum of fuzzy match of this item "+str(len(match_item)))

        for m in range(len(match_item)):
             #file2.write(str(table2.row_values(i2)[0])+"#")
             #file2.write(str(temp2) + "#")
             # file2.write(str(seen_date[m])+"/")
             #file2.write(str(name[m]) + "#")
             file2.write(str(reference_item[name[m]]).replace(".0","")+"\n")
             #file2.write(str(ratio[m]) + "\n")

    file2.close()

def body_site_match():
    excel = xlrd.open_workbook('body site prefererence card.xlsx')
    table1 = excel.sheet_by_name(u'Sheet1')
    nrow=table1.nrows
    dict={}

    output=xlwt.Workbook(encoding='ascii')
    worksheet1=output.add_sheet('Sheet1')

    for i in range(nrow):
        if(i==0):
            continue
        dict[table1.row_values(i)[0]]=table1.row_values(i)[1]

    for i1 in range(1404):
        if(i1==0):
            continue
        temp=str(table1.row_values(i1)[2]).replace(".0","")
        if(temp in dict):
            worksheet1.write(i1,0,label=dict[temp])

    output.save("body site.xls")

def ratio_range2(name, ratio):
    sortMatrix = []
    for row in range(len(name)):
        sortMatrix.append([])
        sortMatrix[row].append(name[row])
        sortMatrix[row].append(ratio[row])

    sortMatrix1 = sorted(sortMatrix, key=lambda s: s[1], reverse=True)
    # print(sortMatrix1)
    return sortMatrix1

#这个函数将fuzzy match的结果匹配到procedure中


if __name__ == '__main__':
    descrption2()
