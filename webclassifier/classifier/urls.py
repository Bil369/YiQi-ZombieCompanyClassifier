from django.urls import path
from classifier import views

urlpatterns = [
    path('', views.index, name='index'),
    path('multiple/upload/', views.multiple_upload, name='multiple-upload'),
    path('multiple/result/', views.multiple_result, name='multiple-result'),
    path('multiple/download/', views.multiple_download, name='multiple-download'),
    path('single/upload/', views.single_upload, name='single-upload'),
    path('single/result/', views.single_result, name='single-result'),
    path('single/input/', views.single_input, name='single-input'),
    path('single/result/visualize/base/', views.single_result_visualize_base, name='single-result-visualize-base'),
    path('single/result/visualize/money/', views.single_result_visualize_money, name='single-result-visualize-money'),
    path('single/result/visualize/year/', views.single_result_visualize_year, name='single-result-visualize-year'),
]