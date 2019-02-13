#从SNOMED CT_ID 去匹配 Classifications_Map 的referencedComponentId
# 提取 effectiveTime,referencedComponentId,mapBlock,mapGroup,mapPriority,mapRule,mapTarget
# 每个mapGroup 会有一个mapTarget，此时 去查Classification_Map_Rule 中该referencedComponentId是否存在结果
#如果存在结果 提取出mapRule为TRUE的mapTarget
#如果不存在结果 提取出mapPriority最大值的Target
import xlrd
import csv
import xlwt
from collections import defaultdict
def map():
    ID = xlrd.open_workbook('SNOMED CT ID_new.xlsx')
    data_ID=ID.sheet_by_name("Full Subset")
    nrow1 = data_ID.nrows
    file_map=open('Classifications_Map.csv')
    data_map=csv.reader(file_map)
    file_map_rule=open('mapRule_True.csv','r')
    data_map_rule = csv.reader(file_map_rule)
    dict2={}        #用于保存maprule
    dict3={}        #用于保存map
    #遍历data_map数据
    #将存在于mapRule中的group拿出来
    #将不存在于mapRule中的group选取pri最大的那个target
    #将map数据写入dict3 并只保留最高的最高pri和target
    for i1 in data_map:
        temp4=str(i1[1])+"_"+str(i1[3])
        if(temp4 in dict3):
            target1=dict3[temp4]
            target2=[i1[4],i1[6]]
            res=compare(target1,target2)
            dict3[temp4]=res
        dict3[temp4]=[i1[4],i1[6]]
    #去除dict3中的pri
    for i2 in dict3.keys():
        dict3[i2]=dict3[i2][1]

    #将maprule中的target拿出来
    for ii in data_map_rule:
        temp=str(ii[1])+"_"+str(ii[2])
        if(temp in dict2):
            date=dict2[temp].split("_")[0]
            code=dict2[temp].split("_")[1]
            new_date=compare_time(date,ii[0])
            dict2[temp]=new_date+"_"+code
        key2=str(ii[1])+"_"+str(ii[2])
        dict2[key2]=str(ii[0])+"_"+str(ii[5])

    for ii2 in dict2:
        dict2[ii2]=dict2[ii2].split("_")[1]

    #对整个dict3中的每一项遍历
    #如果dict3中的key在dict2中存在，则把dict3的value设置为dict2中的value
    for iii1 in dict3.keys():
        if iii1 in dict2:
            if(dict2!=None):            #因为此时Rule对应的Target可能为空
                dict3[iii1]=dict2[iii1]
            else:
                dict3[iii1]=""

    dict4=defaultdict(list)
    #再将id和group分离一次 后面写一个list
    for iii2 in dict3.keys():
        temp5=iii2.split("_")
        id=temp5[0]
        group=temp5[1]
        if(id in dict4):
            dict4[id].append(group)
            dict4[id].append(dict3[iii2])
        else:
            dict4[id]=[group,dict3[iii2]]

    #遍历snomed ct中id 去查找map
    map_new=open("map_new.csv","w+")
    writer=csv.writer(map_new)
    for i in range(nrow1):
        if(i==0):
            continue
        data=str(data_ID.row_values(i)[0]).replace(".0","")
        if(data in dict4):
            temp=[data,str(data_ID.row_values(i)[1])]
            for m in range(len(dict4[data])):
                temp.append(dict4[data][m])
            writer.writerow(temp)
        else:
            temp=[data,str(data_ID.row_values(i)[1])]
            writer.writerow(temp)
    map_new.close()

#比较新进入hashmap的target是否优先级是否比之前的高，选pri最大的那个
def compare(target1,target2):
    #加一个判断
    #因为target不可能为Z开头
    word1=str(target1[1])
    word2=str(target2[1])
    if(word1[0]=='Z' and word2[0]!='Z'):
        return target2
    elif(word2[0]=='Z' and word1[0]!='Z'):
        return target1

    if(int(target1[0])>=int(target2[0])):
        return target1
    else:
        return target2


#比较时间
def compare_time(time1,time2):
    time1_year=time1[0:4]
    time2_year=time2[0:4]
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


def compare_diff():
    ID1 = xlrd.open_workbook('SNOMED CT ID map_original.xlsx')
    data_ID1=ID1.sheet_by_name("Full Set")
    nrow1=data_ID1.nrows

    ID2=xlrd.open_workbook('map_new.xlsx')
    data_ID2=ID2.sheet_by_name("Full Set")
    nrow2=data_ID2.nrows
    count=0

    output=xlwt.Workbook(encoding='ascii')
    worksheet1=output.add_sheet('Sheet1')
    for i in range(nrow2):
        if(i==0):
            continue
        else:
            i1=3
            temp=[]
            while(i1<=14):
                if(data_ID1.row_values(i)[i1]!='' and data_ID2.row_values(i)[i1]!=''):
                    word1=data_ID1.row_values(i)[i1]
                    word2=data_ID2.row_values(i)[i1]
                    #print(word1)
                    #print(word2)
                    if(word1!=word2):
                        for i2 in range(len(data_ID2.row_values(i))):
                            temp.append(data_ID2.row_values(i)[i2])
                        break
                i1=i1+2
            #print(temp)
            if(len(temp)!=0):
                i2=3
                while(i2<len(temp)):
                    if(len(temp[i2])!=0):
                        temp[i2]=temp[i2][:3]+"."+temp[i2][3:]
                        #print(temp[i2])
                    i2=i2+2
                temp= [x for x in temp if x != '']

                #print(len(temp))
                temp2=[]
                if(len(temp)<=4):
                    temp2.append(temp[0])
                    temp2.append(temp[3])
                else:
                    temp2.append(temp[0])
                    temp2.append(temp[3])
                    temp3=''
                    for i3 in range(3,len(temp),2):
                        temp3=temp3+temp[i3]+"\n"
                    temp2.append(temp3)

                for i4 in range(len(temp2)):
                     worksheet1.write(i,i4,label=temp2[i4])

    output.save("map_diff_new.xls")


def map_combine():
    data=xlrd.open_workbook('map_new.xlsx')
    table=data.sheet_by_name('Full Set')
    nrow=table.nrows

    output=xlwt.Workbook(encoding='ascii')
    worksheet1=output.add_sheet('Sheet1')
    for i in range(nrow):
        if(i==0):
            continue
        else:
            id=table.row_values(i)[0]
            length=len(table.row_values(i))
            charge_id=table.row_values(i)[3]
            if(charge_id!=''):
                charge_id=charge_id[:-1]+"."+charge_id[3:]
            ii=5
            id_list=''
            while(ii<=length-1):
                if(table.row_values(i)[ii]!=''):
                    id_temp=table.row_values(i)[ii][:-1]+"."+table.row_values(i)[ii][3:]
                    id_list=id_list+id_temp+"\n"
                ii=ii+2

        worksheet1.write(i, 0, label=id)
        worksheet1.write(i,1,label=id_list)
        worksheet1.write(i,2,label=charge_id)

    output.save("map_new_output.xls")


if __name__ == '__main__':
    compare_diff()