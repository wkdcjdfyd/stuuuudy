from django.db import models


class News(models.Model):
    keyword = models.CharField("검색어", null=True, max_length=50)
    title = models.CharField("제목", max_length=120)
    body = models.TextField("본문")
    press = models.CharField("언론사", max_length=20)
    journalist = models.CharField("기자", max_length=20)
    comment_num = models.IntegerField("댓글 수")
    angry = models.IntegerField("화나요")
    warm = models.IntegerField("훈훈해요")
    like = models.IntegerField("좋아요")
    want = models.IntegerField("후속기사 원해요")
    sad = models.IntegerField("슬퍼요")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
