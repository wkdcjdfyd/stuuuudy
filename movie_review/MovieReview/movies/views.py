from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.shortcuts import get_list_or_404
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer


class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    def get(self, request):
        title = request.GET.get('title', None)
        movie = Movie.object.filter(title=title)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewList(APIView):
    def get(self, request, movie_id):
        reviews = get_list_or_404(Review, movie_id=movie_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ReviewCreate(APIView):
#     def post(self, request, movie_id):
#         movie = get_object_or_404(Movie, pk=movie_id)
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(movie=movie)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
