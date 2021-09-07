from django.contrib import admin
from django.urls import path
from news.views import NewsDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', NewsDetail.as_view()),
]
