from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class InputSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255, required=False)
    comment_num = serializers.IntegerField(required=False)
    angry = serializers.IntegerField(required=False)
    warm = serializers.IntegerField(required=False)
    like = serializers.IntegerField(required=False)
    want = serializers.IntegerField(required=False)
    sad = serializers.IntegerField(required=False)

