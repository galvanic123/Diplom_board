from rest_framework import serializers

from board.models import Comment
from board.pagination import ADSPagination
from board.serializers import AdvertisementSerializer, CommentSerializer

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля"""

    class Meta:
        model = User
        fields = "__all__"


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор для владельца профиля"""

    advertisements = AdvertisementSerializer(many=True, read_only=True)
    author_comments = CommentSerializer(many=True, read_only=True)
    received_comments = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "image",
            "advertisements",
            "author_comments",
            "received_comments",
            "average_rating",
        )

    def get_received_comments(self, obj):
        """Получаем оставленные отзывы"""
        advertisements = obj.advertisements.all()
        comments = Comment.objects.filter(advertisement__in=advertisements)

        paginator = ADSPagination()
        paginated_comments = paginator.paginate_queryset(
            comments, self.context["request"]
        )

        return CommentSerializer(paginated_comments, many=True).data

    def get_average_rating(self, obj):
        """Получаем общий рейтинг"""
        advertisements = obj.advertisements.all()
        comments = Comment.objects.filter(advertisement__in=advertisements)

        if comments.exists():
            total_rating = sum(comment.rating for comment in comments)
            average_rating = total_rating / comments.count()
            return round(average_rating, 2)
        return 0


class ProfileOwnerAdSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей, не являющихся владельцами профиля"""

    advertisements = AdvertisementSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    overall_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "phone",
            "image",
            "advertisements",
            "comments",
            "overall_rating",
        )

    def get_comments(self, obj):
        """Получаем оставленные отзывы"""
        advertisements = obj.advertisements.all()
        comments = Comment.objects.filter(advertisement__in=advertisements)

        paginator = ADSPagination()
        paginated_comments = paginator.paginate_queryset(
            comments, self.context["request"]
        )
        return CommentSerializer(paginated_comments, many=True).data

    def get_overall_rating(self, obj):
        """Получаем общий рейтинг"""
        advertisements = obj.advertisements.all()
        comments = Comment.objects.filter(advertisement__in=advertisements)

        if comments.exists():
            total_rating = sum(comment.rating for comment in comments)
            average_rating = total_rating / comments.count()
            return round(average_rating, 2)
        return 0
