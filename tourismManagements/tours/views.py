from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views import View
from rest_framework import viewsets, permissions, generics, parsers, status
from rest_framework.parsers import MultiPartParser
from . import serializers, perms
from .models import Tour, TourDetail, User, Category, Comment, Like
from .serializers import TourSerializer, TourDeitailSerializer, UserSerializer, TourDetailLikedSerializer


class UserViewSet (viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(detail=False, methods=['get'], url_name='current_user')
    def current_user(self, request):
        request.user
        return Response(serializers.UserSerializer(request.user).data)


class TourViewset(viewsets.ModelViewSet):
    queryset = Tour.objects.filter(active=True)
    serializer_class = TourSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]
    permission_classes = [permissions.IsAuthenticated]
    # List (Get) ->xem ds tour
    # ..(Post) -> them tour
    # detail -> xem chi tiet tour
    # ..(Put) --> cap nhat
    # ..(delete) -->Xoa khoa hoc


class TourDetailViewset(viewsets.ModelViewSet):
    queryset = TourDetail.objects.filter(active=True)
    serializer_class = TourDetailLikedSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment', 'like']: #like or comment cần đăng nhập
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk): # có pk nếu detail là true
        c = Comment.objects.create(user=request.user, tour_name=self.get_object(), content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, tour_name=self.get_object())
        if not created:
            like.active = not like.active
            like.save()
        return Response(serializers.TourDetailLikedSerializer(self.get_object(), context={'request': request}).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.OwnerAuthenticated]


def index(request):
    return HttpResponse("Tours app")
