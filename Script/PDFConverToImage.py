# pdf 输出为 png
# pdf转换为world，提取png图片资源

import os
import fitz
import shutil

class PDFConverToImage():

    def PDFConverToImage(self, _pdf_path):
        _temp_path = self.CreateTempFolder(_pdf_path)
        self.ConverToImage(_pdf_path, _temp_path)
        return _temp_path

    #  创建临时缓存文件夹
    def CreateTempFolder(self, _pdf_path):
        _temp_floder_path = os.path.dirname(_pdf_path) + '/ConverFinishImg/'
        if os.path.exists(_temp_floder_path) is True:
            shutil.rmtree(_temp_floder_path)
        os.mkdir(_temp_floder_path)
        return _temp_floder_path

    # 将pdf转换为png，并输出
    def ConverToImage(self, _pdf_path, _temp_save_png_path):
        _pdf_doc = fitz.open(_pdf_path)
        for _page_index in range(_pdf_doc.pageCount):
            _page_data = _pdf_doc[_page_index]

            # 旋转
            _rotate = int(0)
            # 像素、画质缩放
            _zoom_x = 2
            _zoom_y = 2

            _trans = fitz.Matrix(_zoom_x, _zoom_y).preRotate(_rotate)
            _pm = _page_data.getPixmap(matrix=_trans, alpha=False)
            _pm.writePNG(os.path.dirname(_pdf_path) + '/ConverFinishImg/' + str(_page_index) + '.png')