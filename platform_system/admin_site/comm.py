#coding:utf8
import hashlib
from datetime import datetime
import time
import os
import string
import xlsxwriter
from platform_system.settings import DOWNLOAD_FILE_DIR



def transfer_fen_2_yuan(price):
    '''
    转换分到元
    '''
    
    i_price = int(price)
    if i_price < 10:
        return "0.0"+str(price)
    elif i_price >= 10 and i_price < 100 :
        return "0."+str(price)
    else:
        num_yuan = i_price / 100
        num_other = i_price % 100
        num = "%d.%02d" % (num_yuan, num_other)
        return num
    
def transfer_yuan_2_fen(price):
    '''
    转换元到分
    '''
    
    point_price = float(price)
    return int(100*point_price)

    
    
def IsDigitData(param):
    '''
    检查是否是数字
    '''
    
    intParam = str(param)

    if not intParam.isdigit():
        return False;
    else:
        return True;
    

    
def check_input_price(price):
    '''
    检查输入金额格式是否错误
    '''
    
    if price.count(".") > 1:
        return 1

    point_index = price.find(".")
    if -1 == point_index:
        if False == IsDigitData(price):
            return 1;
        else:
            return 0;
    else:
        #检查整数部分是否都是数字
        num_1 = price[0:point_index]
        if False == IsDigitData(num_1):
            return 1;
        
        #检查小数点是否最后一位
        if point_index == len(price) - 1:
            return 1
        
        #检查小数部分是否都是数字
        num_2 = price[point_index+1]
        if False == IsDigitData(num_2):
            return 1;
    
        return 0



def create_exel(subdir, filename, ncols):
    '''
    生成一个EXCEL
    '''
    path =  DOWNLOAD_FILE_DIR + "/" + subdir + "/"
    if not os.access(path,os.F_OK):
        os.makedirs(path)
    name = path + filename
    workbook = xlsxwriter.Workbook(name) 
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, ncols, 22)          
    return workbook,worksheet


def add_row_to_exel(work, sheet, rownum, row_value_list):
    '''
    写入一行
    '''
    
    std_format = work.add_format({'border':1,'align':'center','font_size':12})
    for i in range(0, len(row_value_list)):
        sheet.write(rownum,i,row_value_list[i], std_format)      
        std_format.set_align('vcenter')
        
    return 0




def add_order_top_to_exel(work, sheet):
    '''
    写入头部 
    '''
    list_top = []
    list_top.append(u"姓名")
    list_top.append(u"联系方式")
    list_top.append(u"性别")
    list_top.append(u"购买商品名称")
    list_top.append(u"支付金额")
    list_top.append(u"支付状态")
    list_top.append(u"支付时间")

    std_format = work.add_format({'border':1,'align':'center','bg_color':'green','font_size':12})
    for i in range(0, len(list_top)):
        sheet.write(0,i,list_top[i], std_format)      
        std_format.set_align('vcenter')
        
    return 0



def add_subc_top_to_exel(work, sheet):
    '''
    写入头部 
    '''
    list_top = []
    list_top.append(u"服务员")
    list_top.append(u"顾客姓名")
    list_top.append(u"联系方式")
    list_top.append(u"性别")
    list_top.append(u"服务开始时间")
    list_top.append(u"服务结束时间")
    list_top.append(u"状态")


    std_format = work.add_format({'border':1,'align':'center','bg_color':'green','font_size':12})
    for i in range(0, len(list_top)):
        sheet.write(0,i,list_top[i], std_format)      
        std_format.set_align('vcenter')
        
    return 0



def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()
