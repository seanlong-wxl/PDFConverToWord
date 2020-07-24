
# 通过百度ocr，提取图片中的文字并输出为world

import os
from tkinter import messagebox
from aip import AipOcr
from Script.ConfigData import ConfigData

class ImageConverToTextByOCR():

    ocrClient = None
    converContent = []
    converFilePath = ''
    converFileName = ''

    def ImageConverToTextByOCR(self, _img_folder_path, _pdf_name):

        self.converFileName = os.path.splitext(_pdf_name)[0]
        self.converFilePath = os.path.abspath(os.path.join(_img_folder_path, '..'))
        self.converContent.clear()
        self.ocrClient = AipOcr(ConfigData.APP_ID, ConfigData.APP_KEY, ConfigData.SECRET_KEY)

        _img_datas = []
        _img_datas = self.LoadLocalImageData(_img_folder_path)
        if _img_datas is None or len(_img_datas) is 0:
            return
        _result = self.OcrImageText(_img_datas)
        if _result is False:
            return
        self.SaveConverData()

    # 加载本地图片数据
    def LoadLocalImageData(self, _folder_path):
        if os.path.exists(_folder_path) is False:
            messagebox.showerror('提示', '当前图片资源路径:' + _folder_path + ' 不存在!')
            return

        _image_data_array = []
        for _png_file in os.listdir(_folder_path):
            _file_path = _folder_path + _png_file
            with open(_file_path, 'rb') as _files_data:
                _image_data_array.append(_files_data.read())
        return _image_data_array

    # 提取图片中的文字
    def OcrImageText(self, _img_datas):
        for _data in _img_datas:
            _ocrReturnData = self.ocrClient.accurate(_data)

            if 'error_code' in _ocrReturnData:
                messagebox.showerror('错误', '错误码：' + str(_ocrReturnData['error_code']) + '\n\n错误信息：' + _ocrReturnData['error_msg'] + '\n\n请联系开发人员QQ: 380363027')
                return False

            _result = _ocrReturnData['words_result']
            for _contents in _result:
                _left_val = 0
                _insert_space_num = 0
                if 'location' in _contents and 'left' in _contents['location']:
                    _left_val = _contents['location']['left']
                    _insert_space_num = _left_val / 32
                _content = str(' ' * int(_insert_space_num)*2) + _contents['words']
                self.converContent.append(_content)
                print(_content)
        return True

    # 保存提取内容为world
    def SaveConverData(self):
        if len(self.converContent) is 0:
            messagebox.showerror('提示', '提取文字的长度为0！')
            return

        _result_content = ''
        for _content in self.converContent:
            _result_content += _content + '\n'

        _save_file_path = self.converFilePath + '/' + self.converFileName + '.doc'
        if os.path.exists(_save_file_path) is True:
            os.remove(_save_file_path)

        with open(_save_file_path, 'a', encoding='utf-8') as sf:
            sf.write(_result_content)

        messagebox.showinfo('完成', '转换已完成，保存路径为：' + _save_file_path)