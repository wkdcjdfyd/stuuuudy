from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News
from .serializers import NewsSerializer


class NewsListAPI(APIView):
    def get(self, request):
        queryset = News.objects.all()
        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)
