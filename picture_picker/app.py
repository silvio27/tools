#!/usr/bin/python3
# -*- coding: gbk -*-
# @Time    : 2021/6/13 16:51
# @Author  : Silvio27
# @Email   : silviosun@outlook.com
# @File    : app.py
# @Software: PyCharm

# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/3 17:28
# @Author  : Silvio27
# @Email   : silviosun@outlook.com
# @File    : main.py
# @Software: PyCharm
import os, sys
from typing import Optional
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import time
from deal_picture import File_W_R
from starlette.responses import StreamingResponse
from deal_picture import from_raw_to_thumbnail
import multiprocessing

hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'app'
]

app = FastAPI()

# ǰ��ҳ��url
origins = ['*']

# ��̨api�������
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/message")
async def root():
    return {
        "message": "Hello World",
        "name": "Sun",
        "Gender": "male",
        "Age": "20"
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# ��ĳ���ļ�
@app.get("/file/{s}")
def root(s: str):
    with open(s, 'r') as f:
        aa = f.read()
    return eval(aa)


#
@app.get("/data/sumlists")
def get_tags_sum():
    basedata = File_W_R(base_path='./', filename='dict_data.txt').get_data()
    count_list = []
    for i in basedata.values():
        for j in i['sort_tags'].split('-'):
            count_list.append(j)

    taglists = File_W_R(base_path='./', filename='taglists.txt').read_excel_raw()
    sumLists = []
    for i in taglists:
        sumList = {}
        sumList[i[1]] = count_list.count(i[1])
        sumList['tags'] = {}
        for j in i[2:]:
            sumList['tags'][j] = count_list.count(j)
        sumLists.append(sumList)

    datum =[]
    for item in sumLists:
        data = ''
        for i, j in item.items():
            data = ''
            if not isinstance(j, dict):
                data += str(i)
                data += ':'
                data += str(j)
                datum.append(data)
            else:
                for m, n in j.items():
                    data += '    '
                    data += str(m)
                    data += ':'
                    data += str(n)
                datum.append(data)
    print(datum)
    return datum
    # return count_list


@app.get("/data/taglists/{category}")
def get_raw_tags(category: str):
    File_W_R(base_path='./', filename='taglists.txt').read_excel(sheetname=category)
    # if os.path.isfile('taglists.txt') and File_W_R(base_path='./', filename='taglists.txt').get_data():
    #     read_excel()
    # else:
    #     data = "[{'name': '��ȫ', 'type': 'success', 'tags': ['ϵͳ', '����', '����', '��˽', '����']}, {'name': '����', 'type': 'warning', 'tags': ['����', '����', '��汾']}, {'name': 'Ч��', 'type': 'primary', 'tags': ['ͳ��', '���', '����ʹ��']}, {'name': '�ʲ�', 'type': 'info', 'tags': ['Ӳ��', '���', '����', '����']}, {'name': '����', 'type': 'danger', 'tags': ['��һ��', '���淶', '����', '���']},{'name': '����', 'type': '', 'tags': ['+']}]"
    #
    #     read_excel()
    # File_W_R(base_path='./', filename='taglists.txt').write_file(data)
    return File_W_R(base_path='./', filename='taglists.txt').get_data()


# ������Ƭ�ֵ�keyֵ�б�����������
@app.get("/data/keylist")
def get_raw_data():
    data = File_W_R(base_path='./', filename='dict_data.txt').get_data()
    bkdata = []
    for i in sorted(data):
        bkdata.append(i)
    return bkdata


# ������Ƭid�����Ƭ������Ƭ��������
@app.get("/data/key/{key}")
def get_pic_thumbnail_url(key: int):
    data = File_W_R(base_path='./', filename='dict_data.txt').get_data()
    print(data)
    data = data[key]
    return data


# TODO ����ͼƬ���Ʒ���ͼƬ,Ŀǰ·����д����,�������Ż���
# TODO ��θ��ݴ򿪵��ļ����޸�·����������Ĭ��·���ϣ� + ���Ĭ��ѹ���ļ�������
@app.get("/image/{name}")
def show_pic(name):
    raw_path = os.getcwd() + '/origin_thumbnail/' + name
    file_like = open(raw_path, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")


@app.get("/data/backdata/{id}/{data}")
def get_tags(id: int, data: Optional[str] = None):
    print(id, data)
    res = File_W_R(base_path='./', filename='dict_data.txt').get_data()
    res[id]['sort_tags'] = data
    print('after' + str(res))
    File_W_R(base_path='./', filename='dict_data.txt').write_file(str(res))
    return 'ok'


# generate_pic
@app.get("/generate_pic")
def generate_pic():
    File_W_R(base_path='./').pic_copy_rename()
    return 'ok'


if __name__ == '__main__':
    # ���
    # multiprocessing.freeze_support()
    # uvicorn.run(app='app:app', host="0.0.0.0", port=8888, reload=False, debug=False, workers=2)

    # �ճ�����
    uvicorn.run(app='app:app', host="0.0.0.0", port=8888, reload=True, debug=True, workers=2)
