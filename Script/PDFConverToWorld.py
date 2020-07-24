
# 使用百度ai开放平台中的文字设别ai功能实现提取图片中的文字( 暂时不支持设别美术字体)
# 百度ai开放平台地址：https://ai.baidu.com/
# 功能实现的主要思路为：利用百度ai中ocr提取图片中的文字，然后保存为world文件
# 具体流程：
# 1、将pdf转为png并输出到指定保存路径
# 2、读取上步中的图片文件资源
# 3、利用百度ocr提取图片中的文字，并保存为world

# 备注：保存为world时，需要考虑文字排版问题
# 目前的解决思路为：
# 1、文字left的位置 / 32(空格所占的像素值) * 2
# 2、查看world时，需要手动设置world的左右页边距为1厘米


import os
import shutil
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from Script.PDFConverToImage import PDFConverToImage
from Script.ImageConverToTextByOCR import ImageConverToTextByOCR

class PDFConverToWorld(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.InitComponent(master)

    def InitComponent(self, master):
        self.browsePath = StringVar()
        self.master = master
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        _frm_right = ttk.Frame(self.master, relief=tkinter.RIDGE)
        _frm_right.grid(row=0, column=0, sticky=tkinter.NSEW)

        ttk.Label(_frm_right, text="选择PDF文件：").grid(row=0, column=0, padx=7.5, pady=15, columnspan=3, sticky=tkinter.NSEW)
        ttk.Entry(_frm_right, width=75, textvariable=self.browsePath).grid(row=0, column=4, columnspan=10)
        Button(_frm_right, text="浏览", width=10, command=self.BrowsePDFFolder).grid(row=0, column=18, padx=5)
        Button(_frm_right, text="开始转换", width=15, command=self.StartConver).grid(row=3, column=4, padx=200)

    def BrowsePDFFolder(self):
        self.browsePath.set(filedialog.askopenfilename())

    def StartConver(self):
        if self.browsePath.get() is None or self.browsePath.get() is '':
            messagebox.showerror('提示', 'pdf文件路径不能为空！')
            return

        #  pdf转为png
        _pdf_conver = PDFConverToImage()
        _temp_folder = _pdf_conver.PDFConverToImage(self.browsePath.get())

        # 通过百度AI，提取png中的文字
        _image_text_ocr = ImageConverToTextByOCR()
        _image_text_ocr.ImageConverToTextByOCR(_temp_folder, os.path.basename(self.browsePath.get()))

        # 删除临时文件
        if os.path.exists(_temp_folder) is True:
            shutil.rmtree(_temp_folder)


root = tk.Tk()
root.title('PDF Conver To World')
root.minsize(700, 300)
root.maxsize(800, 300)
app = PDFConverToWorld(root)
root.mainloop()