from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys

def split_pdf(path, start=0, end=0, name='output'):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(open(path, 'rb'))
    outfn = path.split('.pdf')
    if not os.path.exists(outfn[0]):
        os.mkdir(outfn[0])
    outfn = outfn[0] + '/' + name + '.pdf'
    for i in range(start - 1, end):
        pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))

# def single_page(path,start):
#     pdf_output = PdfFileWriter()
#     pdf_input = PdfFileReader(open(path, 'rb'))
#     outfn = path.split('.pdf')
#     if not os.path.exists(outfn[0]):
#         os.mkdir(outfn[0])
#     outfn = outfn[0] + '/' + str(start) + '.pdf'
#     pdf_output.addPage(pdf_input.getPage(start))
#     pdf_output.write(open(outfn, 'wb'))

# 页面计算
def pagecount(path):
    pdf_input = PdfFileReader(open(path, 'rb'))
    return pdf_input.getNumPages()


# 每页分页
def split_every_page(path):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(open(path, 'rb'))
    outfn = path.split('.pdf')
    if not os.path.exists(outfn[0]):
        os.mkdir(outfn[0])
    # 获取 pdf 共用多少页
    page_count = pdf_input.getNumPages()
    for i in range(page_count):
        pdf_output.addPage(pdf_input.getPage(i))
        out_path = outfn[0] + '/' + str(i) + '.pdf'
        pdf_output.write(open(out_path, 'wb'))
        pdf_output = PdfFileWriter()


def main():
    path = sys.argv[1]
    # path = 'C:/Users/sunzhongshan-pc/Desktop/国家基本公共服务标准（2021年版）.pdf'
    pgcounts = pagecount(path)
    print(f'{path} \n共 {pgcounts} 页')
    pages = input('开始结束页面编号示例：1-2;7-13;7-11;19;21-;【如果是每页分页输入0】 \n请输入:')
    if pages == '0':
        print('开始分页')
        split_every_page(path)
        print('已完成')
    else:
        pages = pages.split(';')
        print(pages)
        for i in range(len(pages)):
            # print(se)
            se = pages[i].split('-')
            print(se)
            if len(se) == 1 and se != '':
                end = int(se[0])
                split_pdf(path, start=int(se[0]), end=end, name=se[0])
            elif len(se) == 2 and se[1] != '':
                split_pdf(path, start=int(se[0]), end=int(se[1]), name=se[0] + '-' + se[1])
            else:
                split_pdf(path, start=int(se[0]), end=pgcounts, name=se[0] + '-' + str(pgcounts))


if __name__ == '__main__':
    # split_every_page()
    main()
