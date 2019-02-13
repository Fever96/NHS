import xlwt
import xlrd
from collections import defaultdict

def merge():
    excel = xlrd.open_workbook('fuzzy_match_preCard_v2-upload15012019-nonmatch-Leilei comment.xlsx')
    table1 = excel.sheet_by_name(u'highlight 1')
    table2 = excel.sheet_by_name(u'fuzzy_match_update')

    dict1={}
    rows1=table1.nrows
    rows2=table2.nrows

    dict2=defaultdict(list)

    for i in range(rows2):
        if(i==0):
            continue
        dict1[table2.row_values(i)[1].strip()]=table2.row_values(i)[2]

    for i1 in range(rows1):
            dict2[table1.row_values(i1)[1].strip()].append(table1.row_values(i1)[2])
            dict2[table1.row_values(i1)[1].strip()].append(table1.row_values(i1)[3])

    for key,value in dict2.items():
        if(key in dict1):
            dict1[key]=dict2[key]

    #去重
    for key1,value1 in dict1.items():
        if(type(value1)==list):
            value1_temp = list(set(value1))
            value1_temp.sort(key=value1.index)
            dict1[key1]=value1_temp

    #print(dict1)
    excel2= xlrd.open_workbook('OUTPUT.xls')
    table3=excel2.sheet_by_name(u'Sheet1')
    dict3=defaultdict(list)
    nrow3=table3.nrows
    ncol1=table3.ncols

    output=open('output_windows.txt','w+')
    for i2 in range(nrow3):
        if(i2==0):
            continue
        procedure=table3.row_values(i2)[1].strip()[1:]
        surgeon=table3.row_values(i2)[0].strip()
        location=table3.row_values(i2)[2].strip()
        Scheduling_Instructions=table3.row_values(i2)[3].strip()
        Patient_Instructions=table3.row_values(i2)[4].strip()
        Nusing_Instructions=table3.row_values(i2)[5].strip()
        Scurb_Notes=table3.row_values(i2)[6].strip()
        Pre_procedure=table3.row_values(i2)[7].strip()
        Positioning_Instructions=table3.row_values(i2)[8].strip()
        Other_Info=table3.row_values(i2)[9].strip()
        Suppliers=table3.row_values(i2)[10]
        Drugs=table3.row_values(i2)[11]
        Equipment=table3.row_values(i2)[12]
        Staff=table3.row_values(i2)[13]
        concept_id=list()
        procedure_temp= list()
        if(procedure in dict1.keys()):
            if(type(dict1[procedure])==list):
                for index,value in enumerate(dict1[procedure]):
                    if(index%2==0):
                        procedure_temp.append(dict1[procedure][index])
                    else:
                        concept_id.append(dict1[procedure][index])
            else:
                procedure_temp.append(procedure)
        else:
            procedure_temp.append(procedure)

        if(i2<10):
            output.writelines("Preference card "+"000"+str(i2)+'\r\n')
        elif(i2>=10 and i2<100):
            output.writelines("Preference card "+"00"+str(i2)+'\r\n')
        elif(i2>=100 and i2<1000):
            output.writelines("Preference card "+"0"+str(i2)+'\r\n')
        else:
            output.writelines("Preference card "+str(i2)+'\r\n')
        output.writelines("Surgeon:"+'\r\n')
        output.writelines(surgeon+'\r\n')
        output.writelines("Concept ID: "+'\r\n')
        if(len(concept_id)==0):
            print(i2)
            output.writelines('\r\n')
        for i4 in concept_id:
            output.writelines(i4+"\r\n")
        output.writelines("Procedure: "+'\r\n')
        for i5 in procedure_temp:
            output.writelines(i5+"\r\n")
        output.writelines("Location: "+'\r\n')
        output.writelines(location+"\r\n")

        output.writelines("Supplies: "+'\r\n')
        output.writelines("Code|Amount|Item|Open|Available (Standby) "+'\r\n')
        output.writelines(Suppliers)

        output.writelines("Drugs: "+'\r\n')
        output.writelines("Name|Open|Available "+'\r\n')
        output.writelines(Drugs)
        output.writelines("(Surgical) Equipment:"+'\r\n')
        output.writelines(Equipment)
        output.writelines("Intruments:"+'\r\n')
        output.writelines("Code|Name|Open|Available (Standby)"+'\r\n')
        output.writelines('\r\n')
        output.writelines("Implant Trays:"+'\r\n')
        output.writelines("\r\n")
        output.writelines("Positioning Information: "+'\r\n')
        output.writelines(Positioning_Instructions)
        output.writelines("Instructions:"+'\r\n')
        output.writelines("Scheduling Instructions"+'\r\n')
        output.writelines(Scheduling_Instructions+'\r\n')
        output.writelines("Patient Instructions"+'\r\n')
        output.writelines(Patient_Instructions+"\r\n")
        output.writelines("Pre-procedure Prep Instructions"+'\r\n')
        output.writelines(Pre_procedure+'\r\n')
        output.writelines("Positioning Instructions"+"\r\n")
        output.writelines(Positioning_Instructions+'\r\n')
        output.writelines("Other info"+'\r\n')
        output.writelines(Other_Info+'\r\n')

        output.writelines("\r\n")
        output.writelines("\r\n")

    output.close()

if __name__ == '__main__':
    merge()