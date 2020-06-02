from django.test import TestCase
import os

# Create your tests here.

class IndexViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get('/classifier/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

class MultipleUploadViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/multiple/upload/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/multiple/upload/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'multiple_upload.html')

    def test_view_can_upload_files(self):
        base_test_sum = open('../testdata/single/base_test_sum.csv', 'rb+')
        knowledge_test_sum = open('../testdata/single/knowledge_test_sum.csv', 'rb+')
        money_report_test_sum = open('../testdata/single/money_report_test_sum.csv', 'rb+')
        year_report_test_sum = open('../testdata/single/year_report_test_sum.csv', 'rb+')
        resp = self.client.post('/classifier/multiple/upload/', data={
            'base_test_sum': base_test_sum,
            'knowledge_test_sum': knowledge_test_sum,
            'money_report_test_sum': money_report_test_sum,
            'year_report_test_sum': year_report_test_sum
        })
        self.assertEqual(resp.status_code, 302)
        base_test_sum.close()
        knowledge_test_sum.close()
        money_report_test_sum.close()
        year_report_test_sum.close()
        self.assertTrue(os.path.exists('classifier/upload/base_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/knowledge_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/money_report_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/year_report_test_sum.csv'))

class MultipleResultViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/multiple/result/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/multiple/result/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'multiple_result.html')

    def test_view_can_produce_result(self):
        resp = self.client.get('/classifier/multiple/result/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(os.path.exists('classifier/result/result.csv'))

class MultipleDownloadViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/multiple/download/')
        self.assertEqual(resp.status_code, 200)

class SingleUploadViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/single/upload/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/single/upload/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'single_upload.html')

    def test_view_can_upload_files(self):
        base_test_sum = open('../testdata/single/base_test_sum.csv', 'rb+')
        knowledge_test_sum = open('../testdata/single/knowledge_test_sum.csv', 'rb+')
        money_report_test_sum = open('../testdata/single/money_report_test_sum.csv', 'rb+')
        year_report_test_sum = open('../testdata/single/year_report_test_sum.csv', 'rb+')
        resp = self.client.post('/classifier/single/upload/', data={
            'base_test_sum': base_test_sum,
            'knowledge_test_sum': knowledge_test_sum,
            'money_report_test_sum': money_report_test_sum,
            'year_report_test_sum': year_report_test_sum
        })
        self.assertEqual(resp.status_code, 302)
        base_test_sum.close()
        knowledge_test_sum.close()
        money_report_test_sum.close()
        year_report_test_sum.close()
        self.assertTrue(os.path.exists('classifier/upload/base_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/knowledge_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/money_report_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/year_report_test_sum.csv'))


class SingleInputViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/single/input/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/single/input/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'single_input.html')

    def test_view_can_upload_files(self):
        resp = self.client.post('/classifier/single/input/', data={
            'company_id': ['28'],
            'zhuce_time': [''],
            'zhuce_ziben': [''],
            'hangye': ['UN'],
            'quyu': ['UN'],
            'qiyeleixing': ['UN'],
            'kongzhiren_leixing': ['UN'],
            'kongzhiren_chigubili': [''],
            'zhuanli': ['UN'],
            'shangbiao': ['UN'],
            'zhuzuoquan': ['UN'],
            'zhaiquan_chengben1': [''],
            'zhaiquan_chengben2': [''],
            'zhaiquan_chengben3': [''],
            'zhaiquan_edu1': [''],
            'zhaiquan_edu2': [''],
            'zhaiquan_edu3': [''],
            'guquan_chengben1': [''],
            'guquan_chengben2': [''],
            'guquan_chengben3': [''],
            'guquan_edu1': ['', ''],
            'guquan_edu2': [''],
            'neibu_chengben1': [''],
            'neibu_chengben2': [''],
            'neibu_chengben3': [''],
            'neibu_edu1': [''],
            'neibu_edu2': [''],
            'neibu_edu3': [''],
            'xiangmu_chengben1': [''],
            'xiangmu_chengben2': [''],
            'xiangmu_chengben3': [''],
            'xiangmu_edu1': [''],
            'xiangmu_edu2': [''],
            'xiangmu_edu3': [''],
            'congyerenshu1': [''],
            'congyerenshu2': [''],
            'congyerenshu3': [''],
            'zichanzonge1': [''],
            'zichanzonge2': [''],
            'zichanzonge3': [''],
            'fuzhaizonge1': [''],
            'fuzhaizonge2': [''],
            'fuzhaizonge3': [''],
            'yingshou1': [''],
            'yingshou2': [''],
            'yingshou3': [''],
            'zhuyingshou1': [''],
            'zhuyingshou2': [''],
            'zhuyingshou3': [''],
            'lirun1': [''],
            'lirun2': [''],
            'lirun3': [''],
            'jinglirun1': [''],
            'jinglirun2': [''],
            'jinglirun3': [''],
            'nashui1': [''],
            'nashui2': [''],
            'nashui3': [''],
            'suoyouzhe1': [''],
            'suoyouzhe2': [''],
            'suoyouzhe3': ['']
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(os.path.exists('classifier/upload/base_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/knowledge_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/money_report_test_sum.csv'))
        self.assertTrue(os.path.exists('classifier/upload/year_report_test_sum.csv'))


class SingleResultViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/single/result/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/single/result/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'single_result.html')

    def test_view_can_produce_result(self):
        resp = self.client.get('/classifier/single/result/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(os.path.exists('classifier/result/result.csv'))

class SingleResultVisualizeBaseViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/single/result/visualize/base/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/single/result/visualize/base/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'single_result_visualize_base.html')

class SingleResultVisualizeMoneyViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/single/result/visualize/money/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/single/result/visualize/money/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'single_result_visualize_money.html')

class SingleResultVisualizeYearViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/classifier/single/result/visualize/year/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/classifier/single/result/visualize/year/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'single_result_visualize_year.html')
