from django.db import models


class Movie(models.Model):
    title = models.CharField('영화제목', max_length=30)
    genre = models.CharField('장르', max_length=20)
    year = models.IntegerField('개봉년도')
    created_at = models.DateTimeField('등록일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.IntegerField("점수")
    content = models.TextField("내용")
    created_at = models.DateTimeField('등록일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.movie, self.score)
