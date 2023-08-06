import json
import os
import sys

import pandas as pd
import requests
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.log import slog, sprint, hide, show
    from .Stock import StockData
except:
    from log.log import slog, sprint, hide, show
    from Stock import StockData


class IndustryAnalysis(object):

    def __init__(self, names=['贵州茅台', '隆基股份']):
        self.names = names
        self.codes = [i['code'] for i in StockData(
            names=self.names).stocks_info().values()]
        self.url = 'http://f10.eastmoney.com/IndustryAnalysis/IndustryAnalysisAjax?'
        self.headers = {
            "Host": "f10.eastmoney.com",
            "Referer": "http://f10.eastmoney.com/IndustryAnalysis/Index?type=web&code=SZ300059",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
            "X-Requested-With": "XMLHttpRequest"
        }

    def params_list(self, codes):
        params_list = []
        for code in codes:
            params_list.append({"code": code[0:2].upper()+code[3:],
                                "icode": "447"})
        return params_list

    def request(self, params):
        response = requests.get(
            self.url, headers=self.headers, params=params, timeout=5)
        response.encoding = response.apparent_encoding
        return json.loads(response.text)

    def get_data(self):
        data_list = []
        for params in tqdm(self.params_list(codes=self.codes)):
            data_list.append(self.request(params=params))
        return data_list

    @property
    def info(self):
        sprint('Getting industry analysis data...')
        industry_info = []
        growth_info = []
        valuation_info = []
        dupont_info = []
        market_size = []
        i = 0
        for data in self.get_data():
            industry_info.append({self.names[i]: data['hyzx']})  # 行业资讯
            growth_info.append(data['czxbj']['data'])  # 成长性比较
            valuation_info.append({self.names[i]: data['gzbj']['data']})  # 估值
            dupont_info.append({self.names[i]: data['dbfxbj']['data']})  # 杜邦
            market_size.append(
                {self.names[i]+'——'+'按总市值排名': data['gsgmzsz']})  # 总市值
            market_size.append(
                {self.names[i]+'——'+'按流通市值排名': data['gsgmltsz']})  # 流通市值
            market_size.append(
                {self.names[i]+'——'+'按营业收入排名': data['gsgmyysr']})  # 营业收入
            market_size.append(
                {self.names[i]+'——'+'按净利润排名': data['gsgmjlr']})  # 净利润
            i += 1
        return {
            'industry_info': industry_info,
            'growth_info': growth_info,
            'valuation_info': valuation_info,
            'dupont_info': dupont_info,
            'market_size': market_size,
        }

    def industry_info(self):
        lists = []
        for i in self.info['industry_info']:
            for j, k in i.items():
                for l in k:
                    lists.append([j, l['date'], l['title']])
        return pd.DataFrame(lists, columns=['stock', 'date', 'advisory'])

    def growth_info(self):
        lists = []
        for i in self.info['growth_info']:
            lists.append([i[0]['jc']])
            for j in i:
                lists.append(j.values())
        T1 = ['基本每股收益增长率(%)', '营业收入增长率(%)', '净利润增长率(%)']
        T2 = ['3年复合', '19A', 'TTM', '20E', '21E', '22E']
        columns = ['排名', '代码', '简称']
        for t1 in T1:
            for t2 in T2:
                columns.append(t2+'--'+t1)
        return pd.DataFrame(lists, columns=columns)

    def valuation_info(self):
        '''
        (1)MRQ市净率=上一交易日收盘价/最新每股净资产
        (2)市现率①=总市值/现金及现金等价物净增加额
        (3)市现率②=总市值/经营活动产生的现金流量净额
        '''
        columns = ['排名', '代码', '简称', 'PEG']
        T = {'市盈率': ['19A', 'TTM', '20E', '21E', '22E'],
             '市销率': ['19A', 'TTM', '20E', '21E', '22E'],
             '市净率': ['19A', 'MRQ'],
             '市现率①': ['19A', 'TTM'],
             '市现率②': ['19A', 'TTM'],
             'EV/EBITDA': ['19A', 'TTM']}
        for i, j in T.items():
            for k in j:
                columns.append(k+'--'+i)
        lists = []
        for i in self.info['valuation_info']:
            lists.append(i.keys())
            for j in i.values():
                for k in j:
                    lists.append(k.values())
        return pd.DataFrame(lists, columns=columns)

    def dupont_info(self):
        T1 = ['ROE(%)', '净利率(%)', '总资产周转率(%)', '权益乘数(%)']
        T2 = ['3年平均', '17A', '18A', '19A']
        columns = ['排名', '代码', '简称']
        for t1 in T1:
            for t2 in T2:
                columns.append(t2+'--'+t1)
        lists = []
        for i in self.info['dupont_info']:
            lists.append(i.keys())
            for j in i.values():
                for k in j:
                    lists.append(k.values())
        return pd.DataFrame(lists, columns=columns)

    def market_size(self):
        columns = ['排名', '代码', '简称',
                   '总市值(元)', '流通市值(元)', '营业收入(元)', '净利润(元)', '报告期']
        lists = []
        for i in self.info['market_size']:
            lists.append(i.keys())
            for j in i.values():
                for k in j:
                    lists.append(k.values())
        return pd.DataFrame(lists, columns=columns)


if __name__ == '__main__':
    ia = IndustryAnalysis()
    test = ia.market_size()
    print(test)
