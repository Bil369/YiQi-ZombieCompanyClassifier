import pandas as pd
import numpy as np
import joblib

class CompanyClassifier:
    
    '''
    Input: Four Pandas DataFrame: base_test_sum, knowledge_test_sum, money_report_test_sum, year_report_test_sum
    Output: Pandas DataFrame: ID, flag
    '''
    
    def __init__(self, base_test_sum, knowledge_test_sum, money_report_test_sum, year_report_test_sum):
        self.base_test_sum = base_test_sum
        self.knowledge_test_sum = knowledge_test_sum
        self.money_report_test_sum = money_report_test_sum
        self.year_report_test_sum = year_report_test_sum
    
        self.base_test_sum['ID'] = self.base_test_sum['ID'].astype('int')
        self.knowledge_test_sum['ID'] = self.knowledge_test_sum['ID'].astype('int')
        self.money_report_test_sum['ID'] = self.money_report_test_sum['ID'].astype('int')
        self.year_report_test_sum['ID'] = self.year_report_test_sum['ID'].astype('int')
    
    def preprocess(self):
        base_test_sum = self.base_test_sum
        knowledge_test_sum = self.knowledge_test_sum
        money_report_test_sum = self.money_report_test_sum
        year_report_test_sum = self.year_report_test_sum
        condition = year_report_test_sum['资产总额'].isnull() & ~year_report_test_sum['负债总额'].isnull() \
                    & ~year_report_test_sum['所有者权益合计'].isnull()
        year_report_test_sum.loc[condition, '资产总额'] = year_report_test_sum.loc[condition, '负债总额'] \
                                                        + year_report_test_sum.loc[condition, '所有者权益合计']
        condition = ~year_report_test_sum['资产总额'].isnull() & year_report_test_sum['负债总额'].isnull() \
                    & ~year_report_test_sum['所有者权益合计'].isnull()
        year_report_test_sum.loc[condition, '负债总额'] = year_report_test_sum.loc[condition, '资产总额'] \
                                                        - year_report_test_sum.loc[condition, '所有者权益合计']
        condition = ~year_report_test_sum['资产总额'].isnull() & ~year_report_test_sum['负债总额'].isnull() \
                    & year_report_test_sum['所有者权益合计'].isnull()
        year_report_test_sum.loc[condition, '所有者权益合计'] = year_report_test_sum.loc[condition, '资产总额'] \
                                                            - year_report_test_sum.loc[condition, '负债总额']
        
        base_test_sum = base_test_sum.fillna({'注册时间': 2002.0,
                                                '注册资本': 5023.133934462283,
                                                '行业': '交通运输业',
                                                '区域': '江西',
                                                '企业类型': '农民专业合作社',
                                                '控制人类型': '企业法人',
                                                '控制人持股比例': 0.7547409850483776})
        knowledge_test_sum = knowledge_test_sum.fillna({'专利': 0,
                                                        '商标': 0,
                                                        '著作权': 0})
        money_report_test_sum = money_report_test_sum.fillna({'year': 2017.0,
                                                              '债权融资额度': 3334.498497772306,
                                                              '债权融资成本': 267.0109897520844,
                                                              '股权融资额度': 5130.455030707215,
                                                              '股权融资成本': 205.22738362924534,
                                                              '内部融资和贸易融资额度': 26228.413307054252,
                                                              '内部融资和贸易融资成本': 1570.9729908071383,
                                                              '项目融资和政策融资额度': 1024.4001114320456,
                                                              '项目融资和政策融资成本': 61.52766412986071})
        year_report_test_sum = year_report_test_sum.fillna({'year': 2016.0,
                                                            '从业人数': 509,
                                                            '资产总额': 135072.24229404208,
                                                            '负债总额': 162285.30989636254,
                                                            '营业总收入': 344766.79090349167,
                                                            '主营业务收入': 206568.3004228836,
                                                            '利润总额': 103109.60091887777,
                                                            '净利润': 22053.03948918005,
                                                            '纳税总额': 75595.39170910012,
                                                            '所有者权益合计': -27210.262594444728})
        
        year_report_test_sum['纳税/净利'] = year_report_test_sum['纳税总额'] / (year_report_test_sum['净利润'] + 1)
        year_report_test_sum['负债/资产'] = year_report_test_sum['负债总额'] / (year_report_test_sum['资产总额'] + 1)
        year_report_test_sum['主收/营收'] = year_report_test_sum['主营业务收入'] / (year_report_test_sum['营业总收入'] + 1)
        year_report_test_sum['净利/资产'] = year_report_test_sum['净利润'] / (year_report_test_sum['资产总额'] + 1)
        year_report_test_sum['净利/营收'] = year_report_test_sum['净利润'] / (year_report_test_sum['营业总收入'] + 1)
        year_report_test_sum['纳税/营收'] = year_report_test_sum['纳税总额'] / (year_report_test_sum['营业总收入'] + 1)
        money_report_test_sum['融资额度'] = money_report_test_sum['债权融资额度'] + money_report_test_sum['股权融资额度'] +\
                                  money_report_test_sum['内部融资和贸易融资额度'] + money_report_test_sum['项目融资和政策融资额度']
        year_report_test_sum['利润/营收'] = year_report_test_sum['利润总额'] / (year_report_test_sum['营业总收入'] + 1)
        year_report_test_sum['净利/利润'] = year_report_test_sum['净利润'] / (year_report_test_sum['利润总额'] + 1)
        year_report_test_sum['所得税'] = year_report_test_sum['利润总额'] - year_report_test_sum['净利润']
        year_report_test_sum['所得税/纳税'] = year_report_test_sum['所得税'] / (year_report_test_sum['纳税总额'] + 1)
        year_report_test_sum['净利/负债'] = year_report_test_sum['净利润'] / (year_report_test_sum['负债总额'] + 1)
        year_report_test_sum['纳税/负债'] = year_report_test_sum['纳税总额'] / (year_report_test_sum['负债总额'] + 1)
        year_report_test_sum['负债/所有者'] = year_report_test_sum['负债总额'] / (year_report_test_sum['所有者权益合计'] + 1)
        year_report_test_sum['费用'] = year_report_test_sum['营业总收入'] - year_report_test_sum['利润总额']
        year_report_test_sum['费用/营收'] = year_report_test_sum['费用'] / (year_report_test_sum['营业总收入'] + 1)
        year_report_test_sum['利润/费用'] = year_report_test_sum['利润总额'] / (year_report_test_sum['费用'] + 1)
        year_report_test_sum['净利/融资额度'] = year_report_test_sum['净利润'] / (money_report_test_sum['融资额度'] + 1)
        year_report_test_sum['纳税/融资额度'] = year_report_test_sum['纳税总额'] / (money_report_test_sum['融资额度'] + 1)
        year_report_test_sum['营收/资产'] = year_report_test_sum['营业总收入'] / (year_report_test_sum['资产总额'] + 1)
        year_report_test_sum['所有者/资产'] = year_report_test_sum['所有者权益合计'] / (year_report_test_sum['资产总额'] + 1)
        year_report_test_sum['净利/所有者'] = year_report_test_sum['净利润'] / (year_report_test_sum['所有者权益合计'] + 1)
        year_report_test_sum['政策/净利'] = money_report_test_sum['项目融资和政策融资额度'] / (year_report_test_sum['净利润'] + 1)
        year_report_test_sum['融资/负债'] = money_report_test_sum['融资额度'] / (year_report_test_sum['负债总额'] + 1)
        year_report_test_sum['政策/负债'] = money_report_test_sum['项目融资和政策融资额度'] / (year_report_test_sum['负债总额'] + 1)
        year_report_test_sum['接受补助'] = [0] * len(year_report_test_sum)
        condition = ((year_report_test_sum['政策/净利'] < -0.5) | (year_report_test_sum['政策/净利'] > 1)) & (year_report_test_sum['负债/资产'] > 0.5)
        year_report_test_sum.loc[condition, '接受补助'] = 1
        
        def jinglijudge(x):
            if len(x) == 3:
                return int(x.iloc[0] < 0 and x.iloc[1] < 0 and x.iloc[2] < 0)
            elif len(x) == 2:
                return int(x.iloc[0] < 0 and x.iloc[1] < 0)
            elif len(x) == 1:
                return int(x.iloc[0] < 0)
        year_report_groupby_sum1 = pd.DataFrame(year_report_test_sum['净利润'].groupby(year_report_test_sum['ID']).apply(jinglijudge).reset_index())
        year_report_groupby_sum1.columns = ['ID', '净三小0']
        year_report_groupby_sum7 = year_report_test_sum.groupby('ID').mean().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(year_report_groupby_sum7.columns)):
            if i == 0:
                newcol.append(year_report_groupby_sum7.columns[i])
                continue
            newcol.append(year_report_groupby_sum7.columns[i] + '_mean')
        year_report_groupby_sum7.columns = newcol
        year_report_groupby_sum8 = year_report_test_sum.groupby('ID').min().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(year_report_groupby_sum8.columns)):
            if i == 0:
                newcol.append(year_report_groupby_sum8.columns[i])
                continue
            newcol.append(year_report_groupby_sum8.columns[i] + '_min')
        year_report_groupby_sum8.columns = newcol
        year_report_groupby_sum9 = year_report_test_sum.groupby('ID').max().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(year_report_groupby_sum9.columns)):
            if i == 0:
                newcol.append(year_report_groupby_sum9.columns[i])
                continue
            newcol.append(year_report_groupby_sum9.columns[i] + '_max')
        year_report_groupby_sum9.columns = newcol
        year_report_groupby_sum10 = year_report_test_sum.groupby('ID').std().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(year_report_groupby_sum10.columns)):
            if i == 0:
                newcol.append(year_report_groupby_sum10.columns[i])
                continue
            newcol.append(year_report_groupby_sum10.columns[i] + '_std')
        year_report_groupby_sum10.columns = newcol
        def growth(x):
            x.drop('ID', axis=1, inplace=True)
            res = ((x.iloc[1] - x.iloc[0]) / (x.iloc[0] + 1) + (x.iloc[2] - x.iloc[1]) / (x.iloc[1] + 1)) / 2
            return res
        year_report_groupby_sum11 = year_report_test_sum[['ID', '从业人数', '资产总额', '负债总额', '营业总收入', '主营业务收入', 
                                                          '利润总额', '净利润', '纳税总额', '所有者权益合计', '负债/资产', 
                                                          '负债/所有者', '所有者/资产', '净利/所有者', '政策/净利']].groupby('ID').apply(growth).reset_index()
        newcol = []
        for i in range(len(year_report_groupby_sum11.columns)):
            if i == 0:
                newcol.append(year_report_groupby_sum11.columns[i])
                continue
            newcol.append(year_report_groupby_sum11.columns[i] + '_growth')
        year_report_groupby_sum11.columns = newcol
        year_report_groupby_sum = pd.merge(year_report_groupby_sum1, year_report_groupby_sum7, on='ID', how='left')
        year_report_groupby_sum = pd.merge(year_report_groupby_sum, year_report_groupby_sum8, on='ID', how='left')
        year_report_groupby_sum = pd.merge(year_report_groupby_sum, year_report_groupby_sum9, on='ID', how='left')
        year_report_groupby_sum = pd.merge(year_report_groupby_sum, year_report_groupby_sum10, on='ID', how='left')
        year_report_groupby_sum = pd.merge(year_report_groupby_sum, year_report_groupby_sum11, on='ID', how='left')
        
        money_report_groupby_sum1 = money_report_test_sum.groupby('ID').mean().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(money_report_groupby_sum1.columns)):
            if i == 0:
                newcol.append(money_report_groupby_sum1.columns[i])
                continue
            newcol.append(money_report_groupby_sum1.columns[i] + '_mean')
        money_report_groupby_sum1.columns = newcol
        money_report_groupby_sum2 = money_report_test_sum.groupby('ID').max().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(money_report_groupby_sum2.columns)):
            if i == 0:
                newcol.append(money_report_groupby_sum2.columns[i])
                continue
            newcol.append(money_report_groupby_sum2.columns[i] + '_max')
        money_report_groupby_sum2.columns = newcol
        money_report_groupby_sum3 = money_report_test_sum.groupby('ID').min().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(money_report_groupby_sum3.columns)):
            if i == 0:
                newcol.append(money_report_groupby_sum3.columns[i])
                continue
            newcol.append(money_report_groupby_sum3.columns[i] + '_min')
        money_report_groupby_sum3.columns = newcol
        money_report_groupby_sum4 = money_report_test_sum.groupby('ID').std().reset_index().drop('year', axis=1)
        newcol = []
        for i in range(len(money_report_groupby_sum4.columns)):
            if i == 0:
                newcol.append(money_report_groupby_sum4.columns[i])
                continue
            newcol.append(money_report_groupby_sum4.columns[i] + '_std')
        money_report_groupby_sum4.columns = newcol
        money_report_groupby_sum = pd.merge(money_report_groupby_sum1,money_report_groupby_sum2, on='ID', how='left')
        money_report_groupby_sum = pd.merge(money_report_groupby_sum,money_report_groupby_sum3, on='ID', how='left') 
        money_report_groupby_sum = pd.merge(money_report_groupby_sum,money_report_groupby_sum4, on='ID', how='left') 
        
        total_data = pd.merge(base_test_sum, knowledge_test_sum, on='ID', how='left')
        total_data = pd.merge(total_data, money_report_groupby_sum, on='ID', how='left')
        total_data = pd.merge(total_data, year_report_groupby_sum, on='ID', how='left')
        total_data = total_data.fillna(0)
        
        return total_data
    
    def predict(self):
        data = self.preprocess()
        X = data[['净三小0', '净利润_mean', '纳税总额_mean', '纳税/净利_mean', '净利/资产_mean', '净利/营收_mean',
          '纳税/营收_mean', '净利/利润_mean', '净利/负债_mean', '纳税/负债_mean', '纳税/融资额度_mean', 
          '纳税/净利_min', '所得税_min', '所得税/纳税_min', '净利润_max', '纳税总额_max', '纳税/净利_max', 
          '净利/资产_max', '净利/营收_max', '纳税/营收_max', '净利/利润_max', '净利/负债_max', '纳税/负债_max', 
          '净利/融资额度_max', '纳税/融资额度_max', '融资/负债_max', '纳税总额_std', '纳税/净利_std', 
          '净利/营收_std', '纳税/营收_std', '所得税/纳税_std', '纳税/负债_std', '纳税/融资额度_std', 
          '净利/所有者_mean',  '政策/净利_mean', '融资/负债_mean' ,'政策/负债_mean', '接受补助_mean', 
          '从业人数_min', '资产总额_min', '负债总额_min', '营业总收入_min', '主营业务收入_min', '利润总额_min',
          '净利润_min', '纳税总额_min', '所有者权益合计_min', '负债/资产_min', '主收/营收_min', '净利/资产_min',
          '净利/营收_min', '纳税/营收_min', '利润/营收_min', '净利/利润_min', '净利/负债_min', '纳税/负债_min', 
          '负债/所有者_min', '费用_min', '费用/营收_min', '利润/费用_min', '净利/融资额度_min', 
          '纳税/融资额度_min', '营收/资产_min', '所有者/资产_min', '净利/所有者_min', '政策/净利_min', 
          '融资/负债_min', '政策/负债_min', '接受补助_min', '资产总额_max', '负债总额_max', '营业总收入_max',
          '主营业务收入_max','利润总额_max', '所有者权益合计_max', '负债/资产_max', '主收/营收_max', 
          '利润/营收_max', '所得税_max', '所得税/纳税_max', '负债/所有者_max', '费用_max', '费用/营收_max', 
          '利润/费用_max', '营收/资产_max', '所有者/资产_max', '净利/所有者_max', '政策/净利_max', 
          '政策/负债_max', '接受补助_max', '从业人数_std', '资产总额_std', '负债总额_std', '营业总收入_std', 
          '主营业务收入_std', '利润总额_std', '净利润_std', '所有者权益合计_std', '负债/资产_std', '主收/营收_std', 
          '净利/资产_std', '利润/营收_std', '净利/利润_std', '所得税_std', '净利/负债_std', '负债/所有者_std', '费用_std',
          '费用/营收_std', '利润/费用_std', '净利/融资额度_std', '营收/资产_std', '所有者/资产_std',
          '净利/所有者_std', '政策/净利_std', '融资/负债_std', '政策/负债_std', '接受补助_std', '从业人数_growth',
          '资产总额_growth', '负债总额_growth', '营业总收入_growth', '主营业务收入_growth', '利润总额_growth',
          '净利润_growth', '纳税总额_growth', '所有者权益合计_growth', '负债/资产_growth', '负债/所有者_growth',
          '所有者/资产_growth', '净利/所有者_growth', '政策/净利_growth'
         ]]
        eclf = joblib.load('classifier/eclf.joblib')
        y_pred = eclf.predict(X)
        
        return pd.DataFrame({'ID': data['ID'], 'flag': y_pred})