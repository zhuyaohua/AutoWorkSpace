"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     datareader.py
@Author:   shenfan
@Time:     2021/2/6 17:04
"""
from xlrd import open_workbook
from xlwt import Style
import os
import pandas
from src.common.config import REPORT_PATH,DATA_PATH
import time
import json


class SheetTypeError(Exception):
    pass


class ExcelReader:
    #读取excel文件中的内容。返回list
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title
                params = {}
                for col in range(1, s.nrows):
                    if s.cell_value(col,17):
                        params.update(json.loads(s.cell_value(col,17)))
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
                with open(os.path.join(DATA_PATH,"params.json"),"w+") as data:
                    data.write(json.dumps(params, indent=4, ensure_ascii=False))
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data


class ExcelWrite:
    def __init__(self,streamdata):
        self.streamdata = streamdata
        file = "ApiReport-{0}.xlsx".format(time.strftime('%Y%m%d%H%M', time.localtime()))
        print(file)
        self.excel = os.path.join(REPORT_PATH,file)

    def write(self):
        dataframe = pandas.DataFrame(self.streamdata)
        writer = pandas.ExcelWriter(self.excel, engine='xlsxwriter')
        workbook = writer.book
        fmt = workbook.add_format({"font_name": u"微软雅黑",'valign': 'vcenter','align': 'left'})
        low_fmt = workbook.add_format({'bg_color': '#00CD00'})
        mid_fmt = workbook.add_format({'bg_color': '#EEE685'})
        high_fmt = workbook.add_format({'bg_color': '#FFFF00'})
        cri_fmt = workbook.add_format({'bg_color': '#FF0000'})
        border_format = workbook.add_format({'border': 1,'top':2,'left':2,'right':2,'bottom':2})
        note_fmt = workbook.add_format({'bold': True, 'font_name': u'微软雅黑', 'font_color': 'red', 'align': 'left', 'valign': 'vcenter','text_wrap':1})
        title_fmt = workbook.add_format({'bold': True, 'font_size': 12, 'font_name': u'微软雅黑','bg_color': '#9FC3D1','valign': 'vcenter', 'align': 'center', 'text_wrap':1})
        data_fmt = workbook.add_format({'bold': True, 'font_size': 10, 'font_name': u'微软雅黑','bg_color': '#CDCD00','valign': 'vcenter', 'align': 'center', 'text_wrap':1})

        l_end = len(dataframe.index) + 2
        dataframe.to_excel(writer, sheet_name=u'interface', encoding='utf8', header=False, index=False, startcol=0, startrow=2)
        worksheet = writer.sheets[u'interface']
        for col_num, value in enumerate(dataframe.columns.values):
            worksheet.write(1, col_num, value, title_fmt)
        worksheet.merge_range('A1:T1', u'测试情况统计表', note_fmt)
        # 设置列宽
        worksheet.set_column('A:T', 30, fmt)
        worksheet.conditional_format('Q3:Q%d'% l_end, {'type': 'no_blanks','format': data_fmt})
        worksheet.conditional_format('Q3:Q%d'% l_end, {'type': 'text', 'criteria': 'between', 'value': 3, 'format': low_fmt})
        worksheet.conditional_format('Q3:Q%d'% l_end,{'type': 'text', 'criteria': '>', 'value': 3, 'format': mid_fmt})
        worksheet.conditional_format('Q3:Q%d'% l_end,{'type': 'text', 'criteria': '>', 'value': 5, 'format': high_fmt})
        worksheet.conditional_format('Q3:Q%d'% l_end,{'type': 'text', 'criteria': '>', 'value': 10, 'format': cri_fmt})
        worksheet.conditional_format('O3:O%d'% l_end,{'type': 'text', 'criteria': 'containing', 'value': 'False', 'format': cri_fmt})
        # 加边框
        worksheet.conditional_format('A1:T%d' % l_end, {'type': 'blanks','format': border_format})
        worksheet.conditional_format('A1:T%d' % l_end, {'type': 'no_blanks','format': border_format})
        writer.save()


if __name__ == '__main__':  # 用于调试
    basepath = os.path.dirname(os.path.dirname(os.path.abspath(".")))
    dataexcel = os.path.join(basepath,"data","interface_data.xls")
    data = ExcelReader(dataexcel,sheet="interface").data
    # for i in data:
    #     print(i)
    # e = ExcelWrite(data)
    # print(e.write())



