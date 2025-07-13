import pytest

from board.models import Advertisement, Comment, Category
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def category_fixture():
    from board.models import Category
    return Category.objects.create(name="Test Category")


@pytest.fixture
def advertisement_fixture(user_is_owner_fixture):
    """
    фикстура модели Advertisement
    """
    advertisement = Advertisement.objects.create(
        title="test title", price=100, owner=user_is_owner_fixture
    )
    return advertisement


@pytest.fixture
def comment_fixture(user_is_owner_fixture, advertisement_fixture):
    """
    фикстура модели Comment
    """

    return Comment.objects.create(
        text="test text",
        owner=user_is_owner_fixture,
        advertisement=advertisement_fixture,
        rating=5,
    )
