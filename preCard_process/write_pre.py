import csv
import random
import xlrd
import xlwt
import numpy as np


def write_pre():
    file=open('preCard.txt','w+')
    xlsfile='OUTPUT.xls'
    book = xlrd.open_workbook(xlsfile)
    table = book.sheet_by_name('Sheet1')
    nrow = table.nrows
    for i in range(nrow):
        j=i+1
        if i ==0:
            i=i+1
        if i == nrow-1:
            exit()
        if i >= 1:
            file.write('Preference Card '+'%04d' %j )
        

       
        
        file.write('\n')
        file.write('Surgeon:'+'\n')
        file.write(table.cell(j,0).value+'\n')
        file.write('Procedure:'+'\n')
        temp1=table.cell(j,1).value
        procedure=temp1.split('$')
        for index in range(len(procedure)-1):
            file.write(procedure[index+1]+'\n')
        file.write('Location:'+'\n')
        file.write(table.cell(j,2).value+'\n')
        file.write('Instructions:'+'\n')
        file.write('Scheduling Instructions:'+'\n')
        if (table.cell(j,3).value.strip()=='Leave this blank'):
            file.write('\n')
        else:
            file.write(table.cell(j,3).value+'\n')
        file.write('Patient Instructions:'+'\n')
        if (table.cell(j,4).value.strip()=='Leave this blank'):
            file.write('\n')
        else:
            file.write(table.cell(j,4).value+'\n')
        file.write('Nursing Instructions:'+'\n')
        if (table.cell(j,5).value.strip()=='Leave this blank'):
            file.write('\n')
        else:
            file.write(table.cell(j,5).value+'\n')
        file.write('Scrub Notes:'+'\n')
        file.write(table.cell(j,6).value+'\n')
        file.write('Pre-procedure Prep Instructions:'+'\n')
        file.write(table.cell(j,7).value+'\n')
        file.write('Positioning Instructions:'+'\n')
        file.write(table.cell(j,8).value+'\n')
        file.write('Other Info:'+'\n')
        file.write(table.cell(j,9).value+'\n')
        file.write('\n')
        
        




if __name__ == '__main__':
    write_pre()        








