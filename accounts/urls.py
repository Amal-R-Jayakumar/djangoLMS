from django.urls import path, reverse_lazy
from .views import user_profile, home, send_email, signup, view_user_profile,login_view, performance_analysis, enquiry
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'accounts'
urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    # path('register/', signup, name='register'),

    # This is to edit user profile
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/view/', view_user_profile,name='view_profile'),
    path('profile/update/', user_profile, name='profile'),
    # Change user password
    path('profile/change-password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html',success_url=reverse_lazy('accounts:password_change_done')), name='change_password'),
    # Password reset views
    
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="accounts/password-reset.html",success_url = reverse_lazy('accounts:password_reset_done'),email_template_name = 'accounts/password_reset_email.html'), name='reset_password'),# success_url=reverse_lazy('accounts:password_reset_confirm')
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",success_url = reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),

    path('profile/performance/', performance_analysis,name="performance_analysis"),
    path('enquiry/',enquiry,name="enquiry"),
    # tests
    path('email/',send_email),

]
# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
