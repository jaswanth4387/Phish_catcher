from django.contrib import admin
from django.urls import path, re_path, include
from User import views as remoteuser
from Provider import views as serviceprovider
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Provider/', include('Provider.urls')),

    path('', remoteuser.index, name="index"),
    path('login/', remoteuser.login, name="login"),
    path('Register1/', remoteuser.Register1, name="Register1"),
    path('Predict_Web_Spoofing_Attack_Type/', remoteuser.Predict_Web_Spoofing_Attack_Type, name="Predict_Web_Spoofing_Attack_Type"),
    path('ViewYourProfile/', remoteuser.ViewYourProfile, name="ViewYourProfile"),

    path('serviceproviderlogin/', serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
    path('View_Remote_Users/', serviceprovider.View_Remote_Users, name="View_Remote_Users"),

    re_path(r'^charts/(?P<chart_type>\w+)/$', serviceprovider.charts, name="charts"),
    re_path(r'^charts1/(?P<chart_type>\w+)/$', serviceprovider.charts1, name="charts1"),
    re_path(r'^likeschart/(?P<like_chart>\w+)/$', serviceprovider.likeschart, name="likeschart"),

    path('View_Web_Spoofing_Attack_Status_Ratio/', serviceprovider.View_Web_Spoofing_Attack_Status_Ratio, name="View_Web_Spoofing_Attack_Status_Ratio"),
    path('train_model/', serviceprovider.train_model, name="train_model"),
    path('View_Prediction_Of_Web_Spoofing_Attack_Status/', serviceprovider.View_Prediction_Of_Web_Spoofing_Attack_Status, name="View_Prediction_Of_Web_Spoofing_Attack_Status"),
    path('Download_Trained_DataSets/', serviceprovider.Download_Trained_DataSets, name="Download_Trained_DataSets"),
]

# Serve media files (ONLY in development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)