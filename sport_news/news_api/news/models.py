from django.db import models


class News(models.Model):
    # 기사제목
    title = models.CharField(max_length=120)

    # 기사 url
    url = models.TextField()

    # 언론사
    press = models.CharField(max_length=20)

    # 카테고리
    category = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
