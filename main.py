import tkinter
from tkinter.filedialog import (askopenfilename, askopenfilenames, askdirectory, asksaveasfilename)
import os
import shutil
import configparser

config_path = 'config.ini'
config = configparser.ConfigParser()
config.read(config_path, encoding='GBK')

npk_list = []
dnf_list = []
npk_dir = ''
dnf_dir = ''


# 读取配置 初始化
def config_init(entry1_val, listbox1_val, entry2_val, listbox2_val):
    # 读取配置并渲染
    render_form(entry1_val, listbox1_val, 'npk', config.get('base', 'npk_dir'))
    render_form(entry2_val, listbox2_val, 'dnf', config.get('base', 'dnf_dir'))


# 初始化 构建界面
def init():
    # 创建窗体
    win = tkinter.Tk()
    win.title('DNF补丁安装器')
    win.geometry('600x500')

    button0 = tkinter.Button(win, text='功能说明', command=lambda: tkinter.messagebox.showinfo('提示', "功能说明: 把需要安装的补丁，放在公共目录下，方便统一管理。\r\n" +
                          "使用说明：\r\n" +
                          "0. 使用前先把自己的补丁都放在公共目录，支持次级目录(可以把一套补丁，放在同一个目录下，再放进公共目录)\r\n" +
                          "1. 选择存放补丁的公共目录\r\n" +
                          "2. 选择dnf目录下的imagePacks2\r\n" +
                          "注意：\r\n" +
                          "1. 该项目只支持补丁追加，不支持替换，即同名补丁安装时，不会替换(建议用次级目录区分)\r\n" +
                          "2. 公共目录下最多支持次级目录，太深的没写"),
                             width=10,
                             height=2)
    button0.pack()

    # 窗体左
    fm1 = tkinter.Frame(win)

    # npk目录
    label1 = tkinter.Label(fm1, text='npk目录(统一存放补丁)', width=20, height=2, anchor='w')
    label1.pack()

    entry1_val = tkinter.Variable()
    entry1 = tkinter.Label(fm1, textvariable=entry1_val, width=30, height=2, anchor='w')
    entry1.pack()

    listbox1_val = tkinter.Variable()
    listbox1 = tkinter.Listbox(fm1, listvariable=listbox1_val)
    listbox1.pack()

    button1 = tkinter.Button(fm1, text='选择文件夹', command=lambda: set_npk_directory(entry1_val, listbox1_val, 'npk'), width=10,
                             height=2)
    button1.pack()

    fm1.pack(side='left', padx=10)

    # 窗体右
    fm2 = tkinter.Frame(win)

    # dnf目录
    label2 = tkinter.Label(fm2, text='dnf目录(imagePacks2)', width=20, height=2, anchor='w')
    label2.pack()

    entry2_val = tkinter.Variable()
    entry2 = tkinter.Label(fm2, textvariable=entry2_val, width=30, height=2, anchor='w')
    entry2.pack()

    listbox2_val = tkinter.Variable()
    listbox2 = tkinter.Listbox(fm2, listvariable=listbox2_val)
    listbox2.pack()

    button2 = tkinter.Button(fm2, text='选择文件夹', command=lambda: set_npk_directory(entry2_val, listbox2_val, 'dnf'), width=10,
                             height=2)
    button2.pack()

    fm2.pack(side='right', padx=10)

    # 安装 卸载 npk 按钮

    button3 = tkinter.Button(fm1, text='安装', command=lambda: install_npk(listbox1, listbox2_val), width=10,
                             height=2)
    button3.pack()

    button4 = tkinter.Button(fm2, text='卸载', command=lambda: uninstall_npk(listbox2, listbox2_val), width=10,
                             height=2)
    button4.pack()

    # button_quit = tkinter.Button(win, text='退出', command=lambda: win.quit(), width=10, height=2)
    # button_quit.pack()

    # 读取配置文件 并渲染数据
    config_init(entry1_val, listbox1_val, entry2_val, listbox2_val)

    win.mainloop()


# 读取当前目录下的文件和目录
def load_directory_name(path):
    try:
        if path:
            return os.listdir(path)
        return []
    except Exception as e:
        print(e)
        return []


# 设置补丁路径并显示
def set_npk_directory(select_path, listbox_val, _label):
    # 选择文件夹
    path = select_directory()

    # 写入配置
    if path:
        config.set('base', _label + '_dir', path)
        config.write(open(config_path, 'w'))
        # 渲染
        render_form(select_path, listbox_val, _label, path)


# 渲染
def render_form(select_path, listbox_val, _label, path):
    arr = load_directory_name(path)

    # 选择文件夹时保存到全局变量
    global npk_list
    global dnf_list
    global npk_dir
    global dnf_dir

    if _label == 'npk':
        if path:
            npk_dir = path + '/'
            select_path.set(path)
            # 保留 npk NPK 和文件夹
            new_arr = []
            for item in arr:
                _file = npk_dir + item
                if os.path.isfile(_file):
                    file_ext = os.path.splitext(_file)[-1]
                    if file_ext in ['.npk', '.NPK']:
                        new_arr.append(item)
                else:
                    new_arr.append(item)
            listbox_val.set(new_arr)
            npk_list = new_arr

    else:
        if npk_dir == '':
            tkinter.messagebox.showinfo('提示', '请先设置npk目录')
            return

        if path:
            dnf_dir = path + '/'
            select_path.set(path)
            load_dnf_list(listbox_val)


# 目录选择框
def select_directory():
    return askdirectory()


# 安装npk
def install_npk(listbox, listbox2_val):
    # 判断文件夹或文件 把对应文件复制到dnf中 防止
    # print(listbox.curselection())
    if listbox.curselection():

        if dnf_dir == '':
            tkinter.messagebox.showinfo('提示', '请设置dnf目录下的imagePacks2目录')
            return
        # 获取文件 复制到 目标文件夹
        filename = listbox.get(listbox.curselection())
        _path = npk_dir + filename
        myCopyFile(_path, dnf_dir)

        # 重新加载目录
        load_dnf_list(listbox2_val)

        tkinter.messagebox.showinfo('提示', '安装成功')
    else:
        tkinter.messagebox.showinfo('提示', '请在npk目录选择要安装的补丁')


# 卸载npk
def uninstall_npk(listbox, listbox2_val):
    # 判断文件夹或文件 把对应文件从dnf移除 比对
    if listbox.curselection():

        # 删除所选
        filename = listbox.get(listbox.curselection())

        # 判断结尾没有后缀 匹配删除
        _path = dnf_dir + filename

        if os.path.isfile(_path):
            os.remove(_path)
        else:
            for _file in os.listdir(dnf_dir):
                file_ext = os.path.splitext(_file)[-1]

                if file_ext in ['.npk', '.NPK']:
                    if _file.endswith('@' + filename + '@' + file_ext):
                        _path = dnf_dir + _file
                        os.remove(_path)

        # 重新加载目录
        load_dnf_list(listbox2_val)

        tkinter.messagebox.showinfo('提示', '卸载成功')
    else:
        tkinter.messagebox.showinfo('提示', '请在dnf目录选择要卸载的补丁')


# 复制文件
def myCopyFile(srcFile, toPath):  # 复制函数

    if not os.path.exists(toPath):
        tkinter.messagebox.showinfo('提示', '目标目录不存在')
        return

    if not os.path.isfile(srcFile):
        # print("%s not exist!" % srcfile)
        if os.path.isdir(srcFile):
            # 遍历目录下的文件
            _list = os.listdir(srcFile)
            for _file in _list:
                # 获取后缀 npk 或 NPK
                _srcFile = srcFile + '/' + _file
                if os.path.isfile(_srcFile):
                    file_ext = os.path.splitext(_srcFile)[-1]
                    if file_ext in ['.npk', '.NPK']:
                        toFile = toPath + _file.replace(file_ext, '@' + os.path.basename(srcFile) + '@' + file_ext)
                        if not os.path.isfile(toFile):
                            shutil.copy(_srcFile, toFile)  # 复制文件
                            # print("copy %s -> %s" % (srcFile, toFile))

    else:
        fpath, fname = os.path.split(srcFile)  # 分离文件名和路径
        toFile = toPath + fname
        if not os.path.exists(toFile):
            shutil.copy(srcFile, toFile)  # 复制文件
            # print("copy %s -> %s" % (srcFile, toFile))


# 加载dnf中已安装的补丁 对应我的补丁列表 取交集
def load_dnf_list(listbox_val):
    # 文件夹内的文件
    arr = load_directory_name(dnf_dir)

    new_arr = []
    for item in arr:
        new_item = item.split('@')
        if len(new_item) == 3:
            new_arr.append(new_item[1])
        else:
            new_arr.append(new_item[0])

    # 比较两边的文件 取交集
    list(set(npk_list) & set(new_arr))
    new_arr = list(set(npk_list).intersection(set(new_arr)))

    listbox_val.set(new_arr)
    global dnf_list
    dnf_list = new_arr


if __name__ == "__main__":
    init()
