from PIL import Image, ImageEnhance, ImageFilter
import os, sys
import shutil
import openpyxl
import json


def open_image(path):
    im = Image.open(path)
    print(im.format, im.size, im.mode)
    return im


# 创建缩略图
def create_thumbnail(path, outpath='', px=128):
    size = (px, px)
    file_name, file_suffix = os.path.splitext(os.path.basename(path))
    outfile = outpath + '/' + file_name + "_thumbnail" + ".jpg"
    try:
        with Image.open(path) as im:
            im.thumbnail(size)
            im = im.convert("RGB")  # JPG压缩,尺寸更小
            im.save(outfile, "JPEG")
            return outfile
    except OSError:
        if not '.db' in path:
            print("cannot create thumbnail for", path)


# 处理一系列图片
def create_thumbnails(lists, px=128):
    for infile in lists:
        create_thumbnail(infile, px)


# 图像平移
def roll(path, delta):
    """Roll an image sideways."""
    image = Image.open(path)
    xsize, ysize = image.size
    print(image.size)

    delta = delta % xsize
    print(delta)
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part1, (xsize - delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize - delta, ysize))

    return image


# 变成黑白
def change_color(path):
    with Image.open(path) as im:
        im = im.convert('L')
    return im


# 增加对比度
def enhance_contrast(path, delta=1.3):
    enh = ImageEnhance.Contrast(Image.open(path))
    enh.enhance(delta).show("30% more contrast")


# 图片大小调整
def image_resize(path, scale=1):
    im = Image.open(path)
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)))


# 打包exe直接拖入cmd，获得文件列表
def get_list():
    aa = sys.argv[1:]
    print(aa)


# 滤镜
def pic_filter(path):
    with Image.open(path) as im:
        # 高斯模糊
        # im1 = im.filter(ImageFilter.GaussianBlur)
        # 普通模糊
        # im2 = im.filter(ImageFilter.BLUR)
        # 边缘增强
        # im2 = im.filter(ImageFilter.EDGE_ENHANCE)
        # 找到边缘
        im1 = im.filter(ImageFilter.FIND_EDGES)
        # 浮雕
        # im.filter(ImageFilter.EMBOSS)
        # 轮廓
        # im3 = im.filter(ImageFilter.CONTOUR)
        # 锐化
        # im.filter(ImageFilter.SHARPEN)
        # 平滑
        # im.filter(ImageFilter.SMOOTH)
        # 细节
        # im.filter(ImageFilter.DETAIL)
        # im1.show()
        aa = im.histogram()
        im1.show()
        print(aa)


###################################################################################################

# 获得路径下所有文件及路径
def get_all_file(filepath):
    lists = []
    for root, dirs, files in os.walk(filepath, topdown=False):
        for name in files:
            lists.append(root + '/' + name)
        # for name in dirs:
        #     print(os.path.join(root, name))
    # print(f'####{lists}')
    return lists


# 1、将当下路径中origin文件夹下所有文件复制到 origin_thumbnail
# 2、同时将源文件路径和新文件路径添加到dict写入list,保存到data.txt文件
def from_raw_to_thumbnail(outputfilename='origin_thumbnail', thumbnail_px=2000):
    datum = []
    basepath = os.path.split(sys.argv[0])[0] + '/'
    origin_path = os.path.join(basepath, 'origin/')
    if not os.path.isdir(origin_path):
        os.mkdir(origin_path)
    print('当前路径:' + basepath)
    file_lists = get_all_file(origin_path)  # 获得路径下所有文件
    count_file_lists = len(file_lists)
    # 如果列表不为空
    if count_file_lists:
        # 判断是否有导出文件夹目录
        outpath = os.path.join(basepath, outputfilename)
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        i = 1
        for inpath in file_lists:
            outfilename = create_thumbnail(inpath, outpath, thumbnail_px)
            datum.append((inpath, outfilename))
            # 显示照片压缩进度
            sys.stdout.write(f'\r照片压缩中 {i}/{count_file_lists}')
            i = i + 1
        print(f"照片已压缩,共 {count_file_lists} 张")
        File_W_R(basepath, filename='dict_data.txt').write_file(str(init_pic_dict(datum)))
    else:
        print("请将照片复制到origin文件夹下,再重新运行软件")
        os.startfile(origin_path)


# 文件读写
class File_W_R:
    def __init__(self, base_path, filename='dict_data.txt', ):
        self.base_path = base_path
        self.filename = filename
        self.file_path = self.base_path + self.filename
        self.encoding = 'gbk'
        self.creat_empty_file()

    def show_path(self):
        print(self.base_path)

    def creat_empty_file(self):
        if not os.path.isfile(self.file_path):
            print('Create New')
            self.write_file("''")
        else:
            self.read_file()

    def read_file(self):
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            aa = f.read()
            if aa:
                self.data = eval(aa)
            else:
                self.data = ''

    def write_file(self, data):
        self.data = data
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            f.write(str(self.data))
            print(f'已写入 {self.filename}')

    def read_excel_raw(self, sheetname='taglists.xlsx'):
        wb = openpyxl.load_workbook('taglists.xlsx')
        # sheet = wb[sheetname]
        sheet = wb.active
        a = []
        for column in sheet.columns:
            b = []
            for cell in column:
                if cell.value:
                    b.append(cell.value)
            a.append(b)
        return a

    def read_excel(self, sheetname='Sheet1'):
        a = self.read_excel_raw(sheetname=sheetname)
        bb = []
        for i in range(len(a)):
            ff = {}
            ff['name'] = a[i][1]
            ff['type'] = a[i][0]
            ff['tags'] = a[i][2:]
            bb.append(ff)
        self.write_file(bb)
        return a

    def get_data(self):
        return self.data

    def create_folder(self, new_path):
        if not os.path.isdir(new_path):
            os.makedirs(new_path, mode=0o777)

    # 1 读取tag，创建文件夹
    # 2 复制图片并重命名
    def pic_copy_rename(self, out_put_folder_name='000分类000'):
        for key, value in self.data.items():
            new_path = f'./{out_put_folder_name}/' + '/'.join(value['sort_tags'].split('-'))
            self.create_folder(new_path)
            fsrc_path = value['origin_path']
            fdst_path = new_path + '/' + value['sort_tags'] + '-' + os.path.split(fsrc_path)[1]
            shutil.copy(fsrc_path, fdst_path)


# 初始化图片列表，添加原始路径，添加压缩图片路径
def init_pic_lists(datum):
    pic_lists = []

    def add_item(name, origin_path, thumbnail_path):
        pic_item = {
            'name': name,
            'origin_path': origin_path,
            'thumbnail_path': thumbnail_path,
            'sort_tags': '',
            'update_time': '',
            'useless': False
        }
        return pic_item

    for origin_path, thumbnail_path in datum:
        name = os.path.split(thumbnail_path)[1]
        pic_lists.append(add_item(name=name, origin_path=origin_path, thumbnail_path=thumbnail_path))
    # print(f'数量：{len(pic_lists)}')
    # print(pic_lists)
    print(f'已创建 {len(pic_lists)} 条记录')
    return pic_lists


# 初始化图片字典，id:{}，添加原始路径，添加压缩图片路径
def init_pic_dict(datum):
    pic_dict = {}

    def add_item(name, origin_path, thumbnail_path):
        pic_item = {
            'name': name,
            'origin_path': origin_path,
            'thumbnail_path': thumbnail_path,
            'sort_tags': '',
            'update_time': '',
            'useless': False
        }
        return pic_item

    for index, item in enumerate(datum):
        origin_path, thumbnail_path = item
        name = os.path.split(thumbnail_path)[1]
        pic_dict[index] = (add_item(name=name, origin_path=origin_path, thumbnail_path=thumbnail_path))
    # print(f'数量：{len(pic_lists)}')
    # print(pic_lists)
    print(f'已创建 {len(pic_dict)} 条记录')
    return pic_dict


# TODO 将来可以支持tags的手动添加，如批量导入
import time, sys

if __name__ == '__main__':
    # print('没有呈现在运行')
    from_raw_to_thumbnail()
    # TODO 所有照片都会被重新压缩，暂时不做处理，不能保证不会用同名同大小的文件被替换,或者读取exif数据，再讨论
    input('按回车键退出')
    # id = 0
    # data = '拖后腿呢好屯'
    # res = File_W_R(base_path='./', filename='dict_data.txt').get_data()
    # res = eval(res)
    # print(res[id])
    # res[id]['sort_tags'] = data
    # print('after' + str(res))
    # File_W_R(base_path='./', filename='dict_data.txt').write_file(str(res))

    # tagslists = [{'name': '安全', 'type': 'success', 'tags': ['系统', '数据', '安防', '隐私', '网络']},
    #              {'name': '分类', 'type': 'warning', 'tags': ['命名', '分类', '多版本']},
    #              {'name': '效率', 'type': 'primary', 'tags': ['统计', '存放', '工具使用']},
    #              {'name': '资产', 'type': 'info', 'tags': ['硬件', '软件', '闲置', '机房']},
    #              {'name': '呈现', 'type': 'danger', 'tags': ['不一致', '不规范', '错误', '广告']}]
    # File_W_R(base_path='./').pic_copy_rename()
