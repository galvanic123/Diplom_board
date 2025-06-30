import pytest

from board.models import Advertisement, Comment


@pytest.fixture
def advertisement_fixture(user_is_owner_fixture):
    """
    фикстура модели Announcement
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
