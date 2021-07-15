# -*- coding: utf-8 -*-
import pdfplumber
import re
import openpyxl
import os, sys
import time


# 获得pdf内容
def get_pdf_content(f_path):
    data = ''
    with pdfplumber.open(f_path) as pdf:
        for page in pdf.pages:
            data += page.extract_text()
    data = data.replace('\n', '')
    data = data.replace(' ', '')
    return data


# 获得pdf内字段
def regex_base():
    base_dict = {
        '姓名': '尊敬的([\u4E00-\u9FA5]{1,5})',
        '岗位': '您将工作在([\u4E00-\u9FA5]{1,30})',
        '职位': '职位为([\u4E00-\u9FA5]{1,30})',
        '上级': '您的直接汇报上级是([\u4E00-\u9FA5]{1,30})',
        '职级': '您的职级为([A-Z0-9]{0,3})',
        '工作地点': '您的工作地点将为([\u4E00-\u9FA5]{1,30})',
        '薪资': '月薪([0-9,]{1,10})',
        '绩效': '绩效工资[0-9,]{0,10}元，为月薪的([0-9%]{1,3})',
        '聘用期限': '聘用期限为(\d{1,3})年',
        '入职时间': '您的入职时间确定为([0-9（）\u4E00-\u9FA5]{1,30})',
        '市内交通费': '你将获得(\d{0,10})元市内交通费',
        '通讯费': '你每月将获得(\d{0,10})元通讯费',
        '综合津贴': '你每月将获得(\d{0,10})元综合津贴',
        '试用期': '您的试用期为([\u4E00-\u9FA5]{1,30})个月',
        '文件名': 'MayForceBeWithU'
    }
    return base_dict


def regex_get_data(content):
    base_dict = regex_base()
    data = {}
    for i, j in base_dict.items():
        aa = re.search(j, content)
        if aa:
            aa = aa.group(1)
        else:
            aa = ''
        data[i] = aa
    return data


# 写入excel
def write_excel(data):
    bk = openpyxl.Workbook()
    sheet = bk.active
    for row in data:
        sheet.append(row)
    bk.save(f'output {time.strftime("%Y-%m-%d %H%M%S", time.localtime())}.xlsx')


# 获得当前路径全部的pdf文件
def get_all_pdf_file(path=r'./pdf/'):
    filenames = []
    for i in os.listdir(path):
        if i.endswith('.pdf' or '.PDF'):
            filenames.append(path + i)
    return filenames


def get_all_pdfs_to_excel(filenames):
    data = []
    data.append(list(regex_base().keys()))
    for i in filenames:
        aa = list(regex_get_data(get_pdf_content(i)).values())
        aa[-1] = os.path.split(i)[1]
        data.append(aa)
    write_excel(data)


if __name__ == '__main__':

    # pdf文件需要放在pdf目录下
    get_all_pdfs_to_excel(get_all_pdf_file())
    print('Done')

