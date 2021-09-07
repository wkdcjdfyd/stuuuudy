from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News
from .serializers import NewsSerializer, InputSerializer
from .parser import scraper


class NewsDetail(APIView):
    def get(self, request):
        serializer_input = InputSerializer(data=request.query_params)
        if not serializer_input.is_valid(raise_exception=True):
            return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer_input.validated_data.get('query', None)
        comment_num = serializer_input.validated_data.get('comment_num', None)
        angry = serializer_input.validated_data.get('angry', None)
        warm = serializer_input.validated_data.get('warm', None)
        like = serializer_input.validated_data.get('like', None)
        want = serializer_input.validated_data.get('want', None)
        sad = serializer_input.validated_data.get('sad', None)

        data = News.objects.all();

        if query:
            data = data.filter(keyword__contains=query)
        if comment_num:
            data = data.filter(comment_num__gte=comment_num)
        if angry:
            data = data.filter(angry__gte=angry)
        if warm:
            data = data.filter(warm__gte=warm)
        if like:
            data = data.filter(like__gte=like)
        if want:
            data = data.filter(want__gte=want)
        if sad:
            data = data.filter(sad__gte=sad)

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
