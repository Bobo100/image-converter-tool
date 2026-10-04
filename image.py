from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import logging
from tkinter import ttk

# create UI
root = Tk()
root.title("File Selector")

root.geometry("600x400")

# input files control
input_files = []
input_files_listbox = Listbox(root, selectmode=MULTIPLE)
input_files_listbox.pack(fill=BOTH, expand=1)

# set the filetypes to .jpg, .png and .tiff
filetypes = [("all" ,"*.*"),
            ("JPEG", "*.jpg"), ("PNG", "*.png"), 
             ("TIFF", "*.tiff"), ("jfif", "*.jfif"), 
             ("bmp", "*.bmp"), ("gif", "*.gif")]


def add_files():
    
    # show file dialog
    files = filedialog.askopenfilenames(
        filetypes=filetypes, title="Select files to convert")
    

    # add files to listbox
    for file in files:        
        if file not in input_files:        
            input_files.append(file)
            input_files_listbox.insert(END, os.path.basename(file))


# add files button
add_files_button = Button(root, text="Add Files", command=add_files)
add_files_button.pack(pady=10)


def image_resize():
    """
    将原始图片的宽高比例调整到跟目标图的宽高比例一致，所以需要：
    1. 切图，缩小原始图片的宽度或者高度
    2. 将切图后的新图片生成缩略图
    :param src_filename: 原始图片的名字
    :param dst_width: 目标图片的宽度
    :param dst_height: 目标图片的高度
    """

    if (Comboxlist.get() == ''):
        return

    value = Comboxlist.get().split('x')
    dst_width = int(value[0])
    dst_height = int(value[1])
    # 「600x900」沒有第三段名稱，輸出成 _small_image
    size_type = value[2] if len(value) > 2 else ''

    for index in input_files_listbox.curselection():
        src_filename = input_files[index]
        print(src_filename)
        # 取得祖父親資料夾的名稱
        parent_dir = os.path.basename(os.path.dirname(os.path.dirname(src_filename)))
        # 目标图片（缩略图）的命名
        if (size_type=='Big'):
            thumbnail_filename = os.path.join(os.path.dirname(src_filename), parent_dir + "_big_image.png")
        elif (size_type=='Slide'):
            flag = True
            count = 1
            while(flag):
                str_count = str(count)
                thumbnail_filename = os.path.join(os.path.dirname(src_filename), parent_dir + "_slides_image_0" + str_count + ".png")
            
                if(os.path.exists(thumbnail_filename)):
                    count = count + 1
                else:
                    flag = False
        elif (size_type=='Title'):
            thumbnail_filename = os.path.join(os.path.dirname(src_filename), parent_dir + "_title_image.png")
        else:
            thumbnail_filename = os.path.join(os.path.dirname(src_filename), parent_dir + "_small_image.png")
 

        # 打开原始图片
        src_image = Image.open(src_filename)
        # 原始图片的宽度和高度
        src_width, src_height = src_image.size
        # 原始图片的宽高比例，保留2位小数
        src_ratio = float('%.2f' % (src_width / src_height))
        # 目标图片的宽高比例，保留2位小数
        dst_ratio = float('%.2f' % (dst_width / dst_height))

        # 如果原始图片的宽高比例大，则将原始图片的宽度缩小
        if src_ratio >= dst_ratio:
            # 切图后的新高度
            if src_height < dst_height:
                logging.warning('目标图片的高度({0} px)超过原始图片的高度({1} px)，最终图片的高度为 {1} px'.format(
                    dst_height, src_height))
            new_src_height = src_height
            # 切图后的新宽度
            new_src_width = int(new_src_height * dst_ratio)  # 向下取整
            # 比如原始图片(1280*480)和目标图片(800*300)的比例完全一致时，此时new_src_width=1281，可能四周会有一条黑线
            if new_src_width > src_width:
                logging.warning('切图的宽度({0} px)超过原始图片的宽度({1} px)，最终图片的宽度为 {1} px'.format(
                    new_src_width, src_width))
                new_src_width = src_width
            blank = int((src_width - new_src_width) / 2)  # 左右两边的空白。向下取整
            # 左右两边留出同样的宽度，计算出新的 box: The crop rectangle, as a (left, upper, right, lower)-tuple
            box = (blank, 0, blank + new_src_width, new_src_height)
        # 如果原始图片的宽高比例小，则将原始图片的高度缩小
        else:
            # 切图后的新宽度
            if src_width < dst_width:
                logging.warning('目标图片的宽度({0} px)超过原始图片的宽度({1} px)，最终图片的宽度为 {1} px'.format(
                    dst_width, src_width))
            new_src_width = src_width
            # 切图后的新高度
            new_src_height = int(new_src_width / dst_ratio)  # 向下取整
            if new_src_height > src_height:
                logging.warning('切图的高度({0} px)超过原始图片的高度({1} px)，最终图片的高度为 {1} px'.format(
                    new_src_height, src_height))
                new_src_height = src_height
            blank = int((src_height - new_src_height) / 2)  # 上下两边的空白。向下取整
            # 上下两边留出同样的高度，计算出新的 box: The crop rectangle, as a (left, upper, right, lower)-tuple
            box = (0, blank, new_src_width, blank + new_src_height)

        # 切图
        new_src_image = src_image.crop(box)
        # 生成目标缩略图
        new_src_image.thumbnail((dst_width, dst_height))
        # 保存到磁盘上
        new_src_image.save(thumbnail_filename, format='png', quality=100)

        logging.info('目标图片已生成: {}'.format(thumbnail_filename))

        input_files_listbox.delete(index)


# add files button
resize_button = Button(root, text="Resize Images", command=image_resize)
resize_button.pack(pady=10)


def validate_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False


# input_frame = Frame(root)
# input_frame.pack()

# width_frame = Frame(input_frame)
# width_frame.pack(side='top')

# input_width_label = Label(width_frame, text="Width")
# input_width_label.pack(side='left')

# input_width = Entry(width_frame, validate='key', validatecommand=(
#     root.register(validate_input), '%P'))
# input_width.insert(0, "2560")
# input_width.pack(side='left')

# height_frame = Frame(input_frame)
# height_frame.pack(side='top')

# input_height_label = Label(height_frame, text="Height")
# input_height_label.pack(side='left')
# input_height = Entry(height_frame, validate='key',
#                      validatecommand=(root.register(validate_input), '%P'))
# input_height.insert(0, "1440")
# input_height.pack(side='left')


Comboxlist_label = Label(root, text="選擇要變更的大小")
Comboxlist_label.pack()
Comboxlist = ttk.Combobox(root, values=[
    "2560x1440xBig", "2560x1440xSlide", "600x900", "960x540xTitle"])  # 初始化
Comboxlist.pack(pady=10)


root.mainloop()
