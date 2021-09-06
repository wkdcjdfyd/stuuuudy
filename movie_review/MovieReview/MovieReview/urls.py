from django.contrib import admin
from django.urls import path
from users.views import UserList, UserDetail
from movies.views import MovieList, MovieDetail, ReviewList, ReviewDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserList.as_view()),
    path('users/<int:user_id>/', UserDetail.as_view()),
    path('movies/', MovieList.as_view()),
    # path('movies/<int:movie_id>/', MovieDetail.as_view()),
    path('movies/', MovieDetail.as_view()),
    path('reviews/<int:review_id>/', ReviewDetail.as_view()),
    path('movies/<int:movie_id>/reviews/', ReviewList.as_view())
]
