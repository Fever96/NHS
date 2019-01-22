import xlrd
import xlwt
import os

path=os.getcwd()+'/preference card/'
#preference_card
def precedure_surgeon():
    sur=''
    procedure=''
    xlsfile=path+"Final-merged preference card.xlsx"
    book=xlrd.open_workbook(xlsfile)
    sheet=[]
    for i in book.sheets():
        sheet.append(i.name)

    output=xlwt.Workbook(encoding='ascii')
    worksheet1=output.add_sheet('Sheet1')

    for index,sheet_item in enumerate(sheet):
        surgeon_set=list()
        procedure_set=list()
        table=book.sheet_by_name(sheet_item)
        print(sheet_item)
        if(len(table.row_values(0)[0])!=0):
            if(table.row_values(0)[0]!='Preference Card: Surgeon Mr A'):
                temp=''
                if(table.row_values(0)[0][:25]=="Preference Card: Surgeon "):
                    temp=table.row_values(0)[0].split("Surgeon ")[1]
                else:
                    temp=table.row_values(0)[0][17:]
                surgeon_set.append(temp)
                temp7=table.row_values(4)
                procedure3 = ''
                for iiiiiii in range(8):
                    if (len(temp7[iiiiiii]) != 0):
                        procedure3 = procedure3 +" "+ str(temp7[iiiiiii])
                procedure_set.append(procedure3)
            elif(table.row_values(0)[0]=='Preference Card: Surgeon Mr A'):
                temp1=table.row_values(2)
                #print(temp1)
                for ii in range(len(temp1)):
                    if(len(temp1[ii])!=0):
                        if(temp1[ii]=='SPR'):
                            continue
                        #print(temp1[ii])
                        surgeon_set.append(temp1[ii])
                if(table.row_values(3)[0]!='Procedures'):
                    temp2 = table.row_values(3)
                    #print(temp2)
                    for iii in range(len(temp2)):
                        if (len(temp2[iii]) != 0):
                            if (temp2[iii] == 'SPR'):
                                continue
                            #print(temp2[iii])
                            surgeon_set.append(temp2[iii])
                    if(table.row_values(4)[0]=='Procedures'):
                        temp5=table.row_values(5)
                        procedure1 = ''
                        for iiiii in range(8):
                            if (len(temp5[iiiii]) != 0):
                                procedure1 = procedure1 + " "+str(temp5[iiiii])
                        procedure_set.append(procedure1)
                    else:
                        print("Error 1")
                elif(table.row_values(3)[0]=='Procedures'):
                    temp6 = table.row_values(4)
                    procedure2 = ''
                    for iiiiii in range(8):
                        if (len(temp6[iiiiii]) != 0):
                            procedure2 = procedure2 + " "+str(temp6[iiiiii])
                    procedure_set.append(procedure2)

        else:
            temp3=table.row_values(2)
            for iii in range(len(temp3)):
                if(len(temp3[iii])!=0):
                    if (temp3[iii] == 'SPR'):
                        continue
                    #print(temp3[iii])
                    surgeon_set.append(temp3[iii])
            temp4=table.row_values(4)
            #print(temp4)
            procedure=''
            for iiii in range(8):
                if(len(temp4[iiii])!=0):
                    procedure=procedure+" "+str(temp4[iiii])
            procedure_set.append(procedure)

        for i1 in range(len(surgeon_set)):
            sur+=surgeon_set[i1]+"$"

        for i2 in range(len(procedure_set)):
            procedure=procedure_set[i2]

        #worksheet1.write(index,0,label=sur)
        #worksheet1.write(index,1,label=procedure)

    #output.save("preference card.xls")



def supplies():
    xlsfile=path+"Final-merged preference card.xlsx"
    book=xlrd.open_workbook(xlsfile)
    sheet=[]
    for i in book.sheets():
        sheet.append(i.name)

    output=xlwt.Workbook(encoding='ascii')
    worksheet1=output.add_sheet('Sheet1')

    for index,sheet_item in enumerate(sheet):
        table = book.sheet_by_name(sheet_item)
        print(sheet_item)
        rows=table.nrows
        supplies=list()
        temp1=table.row_values(7)[0] #supplies  #regularly supplier row in 7
        #but sometimes in 6 row or 8 row
        flag=7
        if(temp1!='Supplies'):    # Shai JJ-Grommets    Khai-Grommets  Han JJ-Grommets  And-Grommets
            #print(sheet_item)
            temp1=table.row_values(8)[0]
            flag=8
            if temp1!='Supplies':      #McD-OPEN MYOMECTOMY
                #print("6"+sheet_item)
                temp1=table.row_values(6)[0]
                flag=6

        flag=flag+3  #skip open&avaliable row and code&amount&item&alias
        #extract all supplies by iteration
        #print("flag:"+str(flag))
        standby_output=[]
        output=[]
        while(flag<rows):
            if(table.row_values(flag)[0]=='Drugs'):
                break
            else:
                first_row=table.row_values(flag)[:3]
                second_row=table.row_values(flag)[4:7]

                #判断是否为空
                if(check_empty(first_row)!=True):
                    output.append(first_row)
                    #print()
                #    print(first_row)
                if(check_empty(second_row)!=True):
                    #print()
                    #判断standby的情况
                    if(table.row_values(flag)[4]=='Have Standby'):
                        flag_standby=flag+2
                        while(flag_standby<rows):
                            if (table.row_values(flag_standby)[0] == 'Drugs'):
                                break
                            else:
                                standby_row = table.row_values(flag_standby)[4:7]
                                if(check_empty(standby_row)!=True):
                                    standby_output.append(standby_row)
                                flag_standby+=1
                    else:
                        output.append(second_row)
                flag+=1

        print("sheet item " + sheet_item)
        print("Open")
        open_new=delete_standby_in_open(output,standby_output)

        #print(open_new)
        print("Standby")
        #print(standby_output)

        #print(len(standby_output))


#在open里 去除standby
def delete_standby_in_open(open,standby):
    open_new=[]
    i=0
    while(i<len(open)):
        if(open[i][0]!='Code' and open[i] not in standby):
            open_new.append(open[i])
            i=i+1
        else:
            i=i+1
    return open_new

def check_empty(test):      #check a list empty or not
                            # empty return True
                            # otherwise return False
    length=len(test)
    for i in range(length):
        if(test[i]!=''):
            return False
    return True

def drugs():
    print()

if __name__ == '__main__':
    print("test")
