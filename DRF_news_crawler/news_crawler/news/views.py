from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News
from .serializers import NewsSerializer
from .parser import scraper


class NewsDetail(APIView):
    def get(self, request):
        query = request.GET.get("query", None)
        data = News.objects.filter(keyword=query)
        serializer = NewsSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        query = request.GET.get("query", None)
        data = scraper(query)
        for item in data:
            serializer = NewsSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
