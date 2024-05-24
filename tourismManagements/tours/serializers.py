from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Tour, TourDetail, Tag, User, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': 'true'} #chi hien khi tao
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class TourSerializer(ModelSerializer):
    class Meta:
        model = Tour
        fields = ["id", "tour_name", "image", "created_date", "category"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TourDeitailSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = TourDetail
        fields = ["id", "tour_name", "content", "created_date", "tour", "tags"]


class TourDetailLikedSerializer(TourDeitailSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, tour_name):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return tour_name.like_set.filter(active=True).exists()

    class Meta:
        model = TourDeitailSerializer.Meta.model
        fields = TourDeitailSerializer.Meta.fields + ['liked']


class CommentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user']