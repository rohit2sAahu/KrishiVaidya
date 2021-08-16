from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),

    path('analysis/', views.analysis, name="analysis"),
    path('admin/', admin.site.urls),
    path('register/',views.sign, name="sign"),
    path('login/',views.login_up, name="login_up"),
    path('logout/',views.logout_up, name="logout_up"),

    
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="home/password_reset.html"),name="reset_password"),

    
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="home/password_reset_sent.html"),name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="home/password_reset_form.html"),name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="home/password_reset_done.html"),name="password_reset_complete"),

    path('diseases/early_blight', views.early_blight, name='early_blight'),
    path('diseases/late_bligth', views.late_bligth, name='late_bligth'),
    path('diseases/Septorial_Disease', views.Septorial_Disease, name='Septorial_Disease'),
    path('diseases/yellow_curl', views.yellow_curl, name='yellow_curl'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)