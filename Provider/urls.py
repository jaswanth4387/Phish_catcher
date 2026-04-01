from django.urls import path
from . import views  # your file name is view.py

app_name = 'provider'

urlpatterns = [
    path('serviceproviderlogin/', views.serviceproviderlogin, name='serviceproviderlogin'),
    path('train_model/', views.train_model, name='train_model'),
    path('users/', views.View_Remote_Users, name='View_Remote_Users'),
    path('predictions/', views.View_Prediction_Of_Web_Spoofing_Attack_Status,
         name='View_Prediction_Of_Web_Spoofing_Attack_Status'),
    path('ratio/', views.View_Web_Spoofing_Attack_Status_Ratio,
         name='View_Web_Spoofing_Attack_Status_Ratio'),

    path('charts/<str:chart_type>/', views.charts, name='charts'),
    path('charts1/<str:chart_type>/', views.charts1, name='charts1'),
    path('likeschart/<str:like_chart>/', views.likeschart, name='likeschart'),

    path('download/', views.Download_Trained_DataSets, name='Download_Trained_DataSets'),
]