from django.shortcuts import render
from .forms import UploadForm, SingleDataInputForm
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse
from .algorithm import CompanyClassifier
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts.charts import Liquid
from pyecharts.charts import Radar

# Create your views here.

def index(request):
    return render(request, 'index.html')

def multiple_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            with open('classifier/upload/base_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['base_test_sum'].chunks():
                    destination.write(chunk)
            with open('classifier/upload/knowledge_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['knowledge_test_sum'].chunks():
                    destination.write(chunk)
            with open('classifier/upload/money_report_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['money_report_test_sum'].chunks():
                    destination.write(chunk)
            with open('classifier/upload/year_report_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['year_report_test_sum'].chunks():
                    destination.write(chunk)
            return HttpResponseRedirect(reverse('multiple-result'))
    else:
        form = UploadForm()
    return render(request, 'multiple_upload.html', {'form': form})

def multiple_result(request):
    base_test_sum = pd.read_csv('classifier/upload/base_test_sum.csv', encoding='gbk')
    knowledge_test_sum = pd.read_csv('classifier/upload/knowledge_test_sum.csv', encoding='gbk')
    money_report_test_sum = pd.read_csv('classifier/upload/money_report_test_sum.csv', encoding='gbk')
    year_report_test_sum = pd.read_csv('classifier/upload/year_report_test_sum.csv', encoding='gbk')
    clf = CompanyClassifier(base_test_sum, knowledge_test_sum, money_report_test_sum, year_report_test_sum)
    result = clf.predict()
    result.to_csv('classifier/result/result.csv', encoding='gbk', index=False)
    return render(request, 'multiple_result.html')

def multiple_download(request):
    response = StreamingHttpResponse(open('classifier/result/result.csv', 'rb'), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    return response

def single_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            with open('classifier/upload/base_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['base_test_sum'].chunks():
                    destination.write(chunk)
            with open('classifier/upload/knowledge_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['knowledge_test_sum'].chunks():
                    destination.write(chunk)
            with open('classifier/upload/money_report_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['money_report_test_sum'].chunks():
                    destination.write(chunk)
            with open('classifier/upload/year_report_test_sum.csv', 'wb+') as destination:
                for chunk in request.FILES['year_report_test_sum'].chunks():
                    destination.write(chunk)
            return HttpResponseRedirect(reverse('single-result'))
    else:
        form = UploadForm()
    return render(request, 'single_upload.html', {'form': form})

def single_result(request):
    base_test_sum = pd.read_csv('classifier/upload/base_test_sum.csv', encoding='gbk')
    knowledge_test_sum = pd.read_csv('classifier/upload/knowledge_test_sum.csv', encoding='gbk')
    money_report_test_sum = pd.read_csv('classifier/upload/money_report_test_sum.csv', encoding='gbk')
    year_report_test_sum = pd.read_csv('classifier/upload/year_report_test_sum.csv', encoding='gbk')
    clf = CompanyClassifier(base_test_sum, knowledge_test_sum, money_report_test_sum, year_report_test_sum)
    result = clf.predict()
    pred = result['flag'].iloc[0]
    compony_id = result['ID'].iloc[0]
    return render(request, 'single_result.html', {'pred': pred, 'company_id': compony_id})

def single_input(request):
    if request.method == 'POST':
        form = SingleDataInputForm(request.POST)
        if form.is_valid():
            company_id = form.cleaned_data['company_id']
            zhuce_time = form.cleaned_data['zhuce_time']
            zhuce_ziben = form.cleaned_data['zhuce_ziben']
            HANGYE_DICT = dict((('UN', '未知'), ('JT', '交通运输业'), ('SY', '商业服务业'), ('GY', '工业'), ('FW', '服务业'),
                              ('SQ', '社区服务'), ('LS', '零售业')))
            hangye = HANGYE_DICT[form.cleaned_data['hangye']]
            if hangye == '未知':
                hangye = None
            QUYU_DICT = dict((('UN', '未知'), ('SD', '山东'), ('GD', '广东'), ('GX', '广西'), ('JX', '江西'), ('HB', '湖北'),
                            ('HN', '湖南'), ('FJ', '福建')))
            quyu = QUYU_DICT[form.cleaned_data['quyu']]
            if quyu == '未知':
                quyu = None
            QIYELEIXING_DICT = dict((('UN', '未知'), ('NM', '农民专业合作社'), ('HH', '合伙企业'), ('YX', '有限责任公司'),
                                   ('GF', '股份有限公司'), ('JT', '集体所有制企业')))
            qiyeleixing = QIYELEIXING_DICT[form.cleaned_data['qiyeleixing']]
            if qiyeleixing == '未知':
                qiyeleixing = None
            KONGZHIREN_CHOICES = dict((('UN', '未知'), ('QY', '企业法人'), ('ZR', '自然人')))
            kongzhiren_leixing = KONGZHIREN_CHOICES[form.cleaned_data['kongzhiren_leixing']]
            if kongzhiren_leixing == '未知':
                kongzhiren_leixing = None
            kongzhiren_chigubili = form.cleaned_data['kongzhiren_chigubili']
            base_test_sum = pd.DataFrame({'ID': [company_id], '注册时间': [zhuce_time], '注册资本': [zhuce_ziben],
                                          '行业': [hangye], '区域': [quyu], '企业类型': [qiyeleixing],
                                          '控制人类型': [kongzhiren_leixing], '控制人持股比例': [kongzhiren_chigubili]})
            base_test_sum.to_csv('classifier/upload/base_test_sum.csv', encoding='gbk', index=False)

            BINARY_DICT = dict((('UN', '未知'), ('Y', '1'), ('N', '0')))
            zhuanli = BINARY_DICT[form.cleaned_data['zhuanli']]
            if zhuanli == '未知':
                zhuanli = None
            shangbiao = BINARY_DICT[form.cleaned_data['shangbiao']]
            if shangbiao == '未知':
                shangbiao = None
            zhuzuoquan = BINARY_DICT[form.cleaned_data['zhuzuoquan']]
            if zhuzuoquan == '未知':
                zhuzuoquan = None
            knowledge_test_sum = pd.DataFrame({'ID': [company_id], '专利': zhuanli, '商标': shangbiao, '著作权': zhuzuoquan})
            knowledge_test_sum.to_csv('classifier/upload/knowledge_test_sum.csv', encoding='gbk', index=False)

            zhaiquan_chengben1 = form.cleaned_data['zhaiquan_chengben1']
            zhaiquan_edu1 = form.cleaned_data['zhaiquan_edu1']
            zhaiquan_chengben2 = form.cleaned_data['zhaiquan_chengben2']
            zhaiquan_edu2 = form.cleaned_data['zhaiquan_edu2']
            zhaiquan_chengben3 = form.cleaned_data['zhaiquan_chengben3']
            zhaiquan_edu3 = form.cleaned_data['zhaiquan_edu3']
            guquan_chengben1 = form.cleaned_data['guquan_chengben1']
            guquan_edu1 = form.cleaned_data['guquan_edu1']
            guquan_chengben2 = form.cleaned_data['guquan_chengben2']
            guquan_edu2 = form.cleaned_data['guquan_edu2']
            guquan_chengben3 = form.cleaned_data['guquan_chengben3']
            guquan_edu3 = form.cleaned_data['guquan_edu3']
            neibu_chengben1 = form.cleaned_data['neibu_chengben1']
            neibu_edu1 = form.cleaned_data['neibu_edu1']
            neibu_chengben2 = form.cleaned_data['neibu_chengben2']
            neibu_edu2 = form.cleaned_data['neibu_edu2']
            neibu_chengben3 = form.cleaned_data['neibu_chengben3']
            neibu_edu3 = form.cleaned_data['neibu_edu3']
            xiangmu_chengben1 = form.cleaned_data['xiangmu_chengben1']
            xiangmu_edu1 = form.cleaned_data['xiangmu_edu1']
            xiangmu_chengben2 = form.cleaned_data['xiangmu_chengben2']
            xiangmu_edu2 = form.cleaned_data['xiangmu_edu2']
            xiangmu_chengben3 = form.cleaned_data['xiangmu_chengben3']
            xiangmu_edu3 = form.cleaned_data['xiangmu_edu3']
            money_report_test_sum = pd.DataFrame({'ID': [company_id, company_id, company_id], 'year': [2015, 2016, 2017],
                                                  '债权融资额度': [zhaiquan_edu1, zhaiquan_edu2, zhaiquan_edu3],
                                                  '债权融资成本': [zhaiquan_chengben1, zhaiquan_chengben2, zhaiquan_chengben3],
                                                  '股权融资额度': [guquan_edu1, guquan_edu2, guquan_edu3],
                                                  '股权融资成本': [guquan_chengben1, guquan_chengben2, guquan_chengben3],
                                                  '内部融资和贸易融资额度': [neibu_edu1, neibu_edu2, neibu_edu3],
                                                  '内部融资和贸易融资成本': [neibu_chengben1, neibu_chengben2, neibu_chengben3],
                                                  '项目融资和政策融资额度': [xiangmu_edu1, xiangmu_edu2, xiangmu_edu3],
                                                  '项目融资和政策融资成本': [xiangmu_chengben1, xiangmu_chengben2, xiangmu_chengben3]})
            money_report_test_sum.to_csv('classifier/upload/money_report_test_sum.csv', encoding='gbk', index=False)

            congyerenshu1 = form.cleaned_data['congyerenshu1']
            congyerenshu2 = form.cleaned_data['congyerenshu2']
            congyerenshu3 = form.cleaned_data['congyerenshu3']
            zichanzonge1 = form.cleaned_data['zichanzonge1']
            zichanzonge2 = form.cleaned_data['zichanzonge2']
            zichanzonge3 = form.cleaned_data['zichanzonge3']
            fuzhaizonge1 = form.cleaned_data['fuzhaizonge1']
            fuzhaizonge2 = form.cleaned_data['fuzhaizonge2']
            fuzhaizonge3 = form.cleaned_data['fuzhaizonge3']
            yingshou1 = form.cleaned_data['yingshou1']
            yingshou2 = form.cleaned_data['yingshou2']
            yingshou3 = form.cleaned_data['yingshou3']
            zhuyingshou1 = form.cleaned_data['zhuyingshou1']
            zhuyingshou2 = form.cleaned_data['zhuyingshou2']
            zhuyingshou3 = form.cleaned_data['zhuyingshou3']
            lirun1 = form.cleaned_data['lirun1']
            lirun2 = form.cleaned_data['lirun2']
            lirun3 = form.cleaned_data['lirun3']
            jinglirun1 = form.cleaned_data['jinglirun1']
            jinglirun2 = form.cleaned_data['jinglirun2']
            jinglirun3 = form.cleaned_data['jinglirun3']
            nashui1 = form.cleaned_data['nashui1']
            nashui2 = form.cleaned_data['nashui2']
            nashui3 = form.cleaned_data['nashui3']
            suoyouzhe1 = form.cleaned_data['suoyouzhe1']
            suoyouzhe2 = form.cleaned_data['suoyouzhe2']
            suoyouzhe3 = form.cleaned_data['suoyouzhe3']
            year_report_test_sum = pd.DataFrame({'ID': [company_id, company_id, company_id], 'year': [2015, 2016, 2017],
                                                 '从业人数': [congyerenshu1, congyerenshu2, congyerenshu3],
                                                 '资产总额': [zichanzonge1, zichanzonge2, zichanzonge3],
                                                 '负债总额': [fuzhaizonge1, fuzhaizonge2, fuzhaizonge3],
                                                 '营业总收入': [yingshou1, yingshou2, yingshou3],
                                                 '主营业务收入': [zhuyingshou1, zhuyingshou2, zhuyingshou3],
                                                 '利润总额': [lirun1, lirun2, lirun3],
                                                 '净利润': [jinglirun1, jinglirun2, jinglirun3],
                                                 '纳税总额': [nashui1, nashui2, nashui3],
                                                 '所有者权益合计': [suoyouzhe1, suoyouzhe2, suoyouzhe3]})
            year_report_test_sum.to_csv('classifier/upload/year_report_test_sum.csv', encoding='gbk', index=False)

            return HttpResponseRedirect(reverse('single-result'))
    else:
        form = SingleDataInputForm()
    return render(request, 'single_input.html', {'form': form})

def single_result_visualize_base(request):
    base_test_sum = pd.read_csv('classifier/upload/base_test_sum.csv', encoding='gbk')
    knowledge_test_sum = pd.read_csv('classifier/upload/knowledge_test_sum.csv', encoding='gbk')
    money_report_test_sum = pd.read_csv('classifier/upload/money_report_test_sum.csv', encoding='gbk')
    year_report_test_sum = pd.read_csv('classifier/upload/year_report_test_sum.csv', encoding='gbk')
    clf = CompanyClassifier(base_test_sum, knowledge_test_sum, money_report_test_sum, year_report_test_sum)
    result = clf.predict()
    company_id = base_test_sum.iloc[0]['ID']
    pred = result.iloc[0]['flag']
    zhuce_time = base_test_sum.iloc[0]['注册时间']
    if pd.isnull(zhuce_time):
        zhuce_time = '未知'
    zhuce_ziben = base_test_sum.iloc[0]['注册资本']
    if pd.isnull(zhuce_ziben):
        zhuce_ziben = '未知'
    hangye = base_test_sum.iloc[0]['行业']
    if pd.isnull(hangye):
        hangye = '未知'
    quyu = base_test_sum.iloc[0]['区域']
    if pd.isnull(quyu):
        quyu = '未知'
    qiyeleixing = base_test_sum.iloc[0]['企业类型']
    if pd.isnull(qiyeleixing):
        qiyeleixing = '未知'
    kongzhiren_leixing = base_test_sum.iloc[0]['控制人类型']
    if pd.isnull(kongzhiren_leixing):
        kongzhiren_leixing = '未知'
    kongzhiren_chigubili = base_test_sum.iloc[0]['控制人持股比例']
    if pd.isnull(kongzhiren_chigubili):
        kongzhiren_chigubili = 0

    zhuanli = knowledge_test_sum.iloc[0]['专利']
    if pd.isnull(zhuanli):
        zhuanli = '未知'
    shangbiao = knowledge_test_sum.iloc[0]['商标']
    if pd.isnull(shangbiao):
        shangbiao = '未知'
    zhuzuoquan = knowledge_test_sum.iloc[0]['著作权']
    if pd.isnull(zhuzuoquan):
        zhuzuoquan = '未知'

    c_kongzhiren = (
        Liquid(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add("未知", [kongzhiren_chigubili], label_opts=opts.LabelOpts(font_size=40, position="inside"))
    )

    def jingyingfengxian(x):
        xmean = (x.iloc[0] + x.iloc[1] + x.iloc[2]) / 3
        return (abs(x.iloc[0] - xmean) + abs(x.iloc[1] - xmean) + abs(x.iloc[2] - xmean)) / 3 / (xmean + 1)

    year_report_groupby_sum2 = pd.DataFrame(
        year_report_test_sum['净利润'].groupby(year_report_test_sum['ID']).apply(jingyingfengxian).reset_index())
    year_report_groupby_sum2.columns = ['ID', '经营风险']

    def jingyingganggan(x):
        return ((x['净利润'].iloc[1] - x['净利润'].iloc[0]) / (x['营业总收入'].iloc[1] - x['营业总收入'].iloc[0] + 1) +
                (x['净利润'].iloc[2] - x['净利润'].iloc[1]) / (x['营业总收入'].iloc[2] - x['营业总收入'].iloc[1] + 1)) / 2

    year_report_groupby_sum3 = pd.DataFrame(year_report_test_sum.groupby('ID').apply(jingyingganggan).reset_index())
    year_report_groupby_sum3.columns = ['ID', '经营杠杆']

    zhengfuyilai = money_report_test_sum['项目融资和政策融资额度'] / (year_report_test_sum['净利润'] + 1)
    zichanfuzhai = year_report_test_sum['负债总额'] / (year_report_test_sum['资产总额'] + 1)
    zichanzhouzhuan = year_report_test_sum['营业总收入'] / (year_report_test_sum['资产总额'] + 1)

    v1 = [[float(year_report_groupby_sum2.iloc[0]['经营风险']),
           float(year_report_groupby_sum3.iloc[0]['经营杠杆']), zhengfuyilai.mean(), zichanfuzhai.mean(),
           zichanzhouzhuan.mean()]]

    r_jingying = (
        Radar(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="经营风险", max_=5, min_=-5),
                opts.RadarIndicatorItem(name="经营杠杆", max_=5, min_=-5),
                opts.RadarIndicatorItem(name="政府依赖", max_=5, min_=-5),
                opts.RadarIndicatorItem(name="资产负债率", max_=5, min_=-5),
                opts.RadarIndicatorItem(name="资产周转率", max_=5, min_=-5),
            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        )
        .add(
            series_name="企业经营状况",
            data=v1,
            linestyle_opts=opts.LineStyleOpts(color="#CD0000"),
        )
    )

    return render(request, 'single_result_visualize_base.html', {'company_id': company_id,
                                                                 'pred': pred,
                                                                 'zhuce_time': zhuce_time,
                                                                 'zhuce_ziben': zhuce_ziben,
                                                                 'hangye': hangye,
                                                                 'quyu': quyu,
                                                                 'qiyeleixing': qiyeleixing,
                                                                 'kongzhiren_leixing': kongzhiren_leixing,
                                                                 'zhuanli': zhuanli,
                                                                 'shangbiao': shangbiao,
                                                                 'zhuzuoquan': zhuzuoquan,
                                                                 'c_kongzhiren': c_kongzhiren.render_embed(),
                                                                 'r_jingying': r_jingying.render_embed()})


def single_result_visualize_money(request):
    money_report_test_sum = pd.read_csv('classifier/upload/money_report_test_sum.csv', encoding='gbk')
    bar_chengben = (
        Bar()
            .add_xaxis(list(money_report_test_sum['year']))
            .add_yaxis("债权融资成本", list(money_report_test_sum['债权融资成本']))
            .add_yaxis("股权融资成本", list(money_report_test_sum['股权融资成本']))
            .add_yaxis("内部融资和贸易融资成本", list(money_report_test_sum['内部融资和贸易融资成本']))
            .add_yaxis("项目融资和政策融资成本", list(money_report_test_sum['项目融资和政策融资成本']))
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年融资成本变化"))
    )

    bar_edu = (
        Bar()
            .add_xaxis(list(money_report_test_sum['year']))
            .add_yaxis("债权融资额度", list(money_report_test_sum['债权融资额度']))
            .add_yaxis("股权融资额度", list(money_report_test_sum['股权融资额度']))
            .add_yaxis("内部融资和贸易融资额度", list(money_report_test_sum['内部融资和贸易融资额度']))
            .add_yaxis("项目融资和政策融资额度", list(money_report_test_sum['项目融资和政策融资额度']))
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年融资额度变化"))
    )

    chengben = ['债权融资成本', '股权融资成本', '内部融资和贸易融资成本', '项目融资和政策融资成本']
    chengben_v1 = [money_report_test_sum.iloc[0][x] for x in chengben]
    chengben_v2 = [money_report_test_sum.iloc[1][x] for x in chengben]
    chengben_v3 = [money_report_test_sum.iloc[2][x] for x in chengben]
    c_chengben = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(chengben, chengben_v1)],
            radius=["20%", "30%"],
            center=["25%", "50%"],
            rosetype="area",
            # label_opts=opts.LabelOpts(is_show=False),
        )
            .add(
            "",
            [list(z) for z in zip(chengben, chengben_v2)],
            radius=["20%", "30%"],
            center=["50%", "50%"],
            rosetype="area",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add(
            "",
            [list(z) for z in zip(chengben, chengben_v3)],
            radius=["20%", "30%"],
            center=["75%", "50%"],
            rosetype="area",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年融资成本占比"))
    )

    edu = ['债权融资额度', '股权融资额度', '内部融资和贸易融资额度', '项目融资和政策融资额度']
    edu_v1 = [money_report_test_sum.iloc[0][x] for x in edu]
    edu_v2 = [money_report_test_sum.iloc[1][x] for x in edu]
    edu_v3 = [money_report_test_sum.iloc[2][x] for x in edu]
    c_edu = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(edu, edu_v1)],
            radius=["20%", "30%"],
            center=["25%", "50%"],
            rosetype="area",
            # label_opts=opts.LabelOpts(is_show=False),
        )
            .add(
            "",
            [list(z) for z in zip(edu, edu_v2)],
            radius=["20%", "30%"],
            center=["50%", "50%"],
            rosetype="area",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add(
            "",
            [list(z) for z in zip(edu, edu_v3)],
            radius=["20%", "30%"],
            center=["75%", "50%"],
            rosetype="area",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年融资额度占比"))
    )

    eduoverchengben = ['融资额度', '融资成本']
    eduoverchengben1 = [money_report_test_sum.iloc[0]['债权融资额度'] + money_report_test_sum.iloc[0]['股权融资额度'] +
                         money_report_test_sum.iloc[0]['内部融资和贸易融资额度'] + money_report_test_sum.iloc[0]['内部融资和贸易融资额度'],
                         money_report_test_sum.iloc[0]['债权融资成本'] + money_report_test_sum.iloc[0]['股权融资成本'] +
                         money_report_test_sum.iloc[0]['内部融资和贸易融资成本'] + money_report_test_sum.iloc[0]['内部融资和贸易融资成本']]

    eduoverchengben2 = [money_report_test_sum.iloc[1]['债权融资额度'] + money_report_test_sum.iloc[1]['股权融资额度'] +
                        money_report_test_sum.iloc[1]['内部融资和贸易融资额度'] + money_report_test_sum.iloc[1]['内部融资和贸易融资额度'],
                        money_report_test_sum.iloc[1]['债权融资成本'] + money_report_test_sum.iloc[1]['股权融资成本'] +
                        money_report_test_sum.iloc[1]['内部融资和贸易融资成本'] + money_report_test_sum.iloc[1]['内部融资和贸易融资成本']]

    eduoverchengben3 = [money_report_test_sum.iloc[1]['债权融资额度'] + money_report_test_sum.iloc[1]['股权融资额度'] +
                        money_report_test_sum.iloc[1]['内部融资和贸易融资额度'] + money_report_test_sum.iloc[1]['内部融资和贸易融资额度'],
                        money_report_test_sum.iloc[1]['债权融资成本'] + money_report_test_sum.iloc[1]['股权融资成本'] +
                        money_report_test_sum.iloc[1]['内部融资和贸易融资成本'] + money_report_test_sum.iloc[1]['内部融资和贸易融资成本']]

    c_eduoverchengben = (
        Pie()
            .add("", [list(z) for z in zip(eduoverchengben, eduoverchengben1)], radius='30%', center=["20%", "50%"])
            .add("", [list(z) for z in zip(eduoverchengben, eduoverchengben2)], radius='30%', center=["50%", "50%"])
            .add("", [list(z) for z in zip(eduoverchengben, eduoverchengben3)], radius='30%', center=["80%", "50%"])
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年融资额度/融资成本"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: \n{c}"))
    )

    rongziedu = [money_report_test_sum.iloc[i]['债权融资额度'] + money_report_test_sum.iloc[i]['股权融资额度'] +
                 money_report_test_sum.iloc[i]['内部融资和贸易融资额度'] + money_report_test_sum.iloc[i]['内部融资和贸易融资额度'] for i in range(3)]
    rongzichengben = [money_report_test_sum.iloc[i]['债权融资成本'] + money_report_test_sum.iloc[i]['股权融资成本'] +
                      money_report_test_sum.iloc[i]['内部融资和贸易融资成本'] + money_report_test_sum.iloc[i]['内部融资和贸易融资成本'] for i in range(3)]
    zonghe_zijinchengben = [(money_report_test_sum.iloc[i]['债权融资成本'] * money_report_test_sum.iloc[i]['债权融资额度'] +
                             money_report_test_sum.iloc[i]['股权融资成本'] * money_report_test_sum.iloc[i]['股权融资额度'] +
                             money_report_test_sum.iloc[i]['内部融资和贸易融资成本'] * money_report_test_sum.iloc[i][
                                 '内部融资和贸易融资额度'] +
                             money_report_test_sum.iloc[i]['项目融资和政策融资成本'] * money_report_test_sum.iloc[i][
                                 '项目融资和政策融资额度']) / (rongziedu[i] + 1) for i in range(3)]

    c_overview = (
        Line()
            .add_xaxis([str(x) for x in list(money_report_test_sum['year'])])
            .add_yaxis("融资额度", rongziedu)
            .add_yaxis("融资成本", rongzichengben)
            .add_yaxis("综合资金成本", zonghe_zijinchengben)
            .set_global_opts(title_opts=opts.TitleOpts(title="融资数据概览"))
    )

    return render(request, 'single_result_visualize_money.html', {'bar_chengben': bar_chengben.render_embed(),
                                                                  'bar_edu': bar_edu.render_embed(),
                                                                  'c_chengben': c_chengben.render_embed(),
                                                                  'c_edu': c_edu.render_embed(),
                                                                  'c_eduoverchengben': c_eduoverchengben.render_embed(),
                                                                  'c_overview': c_overview.render_embed()})

def single_result_visualize_year(request):
    year_report_test_sum = pd.read_csv('../webclassifier/classifier/upload/year_report_test_sum.csv', encoding='gbk')
    bar_zichan = (
        Bar()
            .add_xaxis(list(year_report_test_sum['year']))
            .add_yaxis("资产总额", list(year_report_test_sum['资产总额']))
            .add_yaxis("负债总额", list(year_report_test_sum['负债总额']))
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年资产与负债总额"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        )
    )

    l_yingshou = (
        Line()
            .add_xaxis([str(x) for x in list(year_report_test_sum['year'])])
            .add_yaxis("营业总收入", list(year_report_test_sum['营业总收入']),
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .add_yaxis("主营业务收入", list(year_report_test_sum['主营业务收入']),
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年营收"))
    )

    item = ['营业总收入', '主营业务收入']
    yingshou1 = [float(year_report_test_sum.iloc[0]['营业总收入']), float(year_report_test_sum.iloc[0]['主营业务收入'])]
    yingshou2 = [float(year_report_test_sum.iloc[1]['营业总收入']), float(year_report_test_sum.iloc[1]['主营业务收入'])]
    yingshou3 = [float(year_report_test_sum.iloc[2]['营业总收入']), float(year_report_test_sum.iloc[2]['主营业务收入'])]

    p_yingshou = (
        Pie()
            .add("", [list(z) for z in zip(item, yingshou1)], radius='30%', center=["20%", "50%"])
            .add("", [list(z) for z in zip(item, yingshou2)], radius='30%', center=["50%", "50%"])
            .add("", [list(z) for z in zip(item, yingshou3)], radius='30%', center=["80%", "50%"])
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年营收/主营收"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: \n{c}"))
    )

    bar_lirun = (
        Bar()
            .add_xaxis(list(year_report_test_sum['year']))
            .add_yaxis("利润总额", list(year_report_test_sum['利润总额']))
            .add_yaxis("净利润", list(year_report_test_sum['净利润']))
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年利润"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        )
    )

    l_nashui = (
        Line()
            .add_xaxis([str(x) for x in list(year_report_test_sum['year'])])
            .add_yaxis("纳税总额", list(year_report_test_sum['纳税总额']),
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),)
            .set_global_opts(title_opts=opts.TitleOpts(title="近三年纳税"))
    )
    return render(request, 'single_result_visualize_year.html', {'bar_zichan': bar_zichan.render_embed(),
                                                                 'l_yingshou': l_yingshou.render_embed(),
                                                                 'p_yingshou': p_yingshou.render_embed(),
                                                                 'bar_lirun': bar_lirun.render_embed(),
                                                                 'l_nashui': l_nashui.render_embed()
                                                                 })