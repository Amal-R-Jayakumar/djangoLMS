from django.urls import path
from .views import answer_a_question, ask_a_question, q_and_a
from django.conf import settings
from django.conf.urls.static import static

app_name='ask_an_expert'
urlpatterns=[
    path('q-and-a/',q_and_a,name="q_and_a"),
    path('q-and-a/ask-question/',ask_a_question,name="ask_question"),
    path('q-and-a/<int:id>/answer/',answer_a_question,name="answer"),
]

urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
