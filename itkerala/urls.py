from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('courses.urls')),
    path('', include('student_report.urls')),
    path('', include('ask_an_expert.urls')),
    path('', include('college_or_atc.urls')),
    path('', include('payments.urls')),
    
    # path('', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'accounts.views.error_404'
handler500 = 'accounts.views.error_500'
handler403 = 'accounts.views.error_403'
# handler400 = 'accounts.views.error_400'
