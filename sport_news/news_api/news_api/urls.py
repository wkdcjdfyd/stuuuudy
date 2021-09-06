from django.contrib import admin
from django.urls import path
from news.views import NewsListAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', NewsListAPI.as_view())
]
