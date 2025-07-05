import pytest

from django.urls import reverse
from rest_framework import status
from board.models import Comment
from users.tests.conftest import api_client, user_fixture, user_is_owner_fixture


@pytest.mark.django_db
def test_comment_create(api_client, user_fixture, advertisement_fixture):
    """
    Тест создания нового отзыва
    """

    url = reverse("advertisement:comment_create")
    data = {"text": "new text", "advertisement": advertisement_fixture.pk, "rating": 5}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == data["text"]
    assert Comment.objects.count() == 1
    assert Comment.objects.first().owner == user_fixture


@pytest.mark.django_db
def test_comment_list(api_client, comment_fixture, user_is_owner_fixture, user_fixture):
    """
    Тест получения списка отзывов
    """
    url = reverse("advertisement:comment_list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["results"][0]["text"] == "test text"

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["results"][0]["text"] == "test text"


@pytest.mark.django_db
def test_comment_update(
    api_client,
    comment_fixture,
    user_is_owner_fixture,
    user_fixture,
    advertisement_fixture,
):
    """
    Тест изменения отзыва
    """

    url = reverse("advertisement:comment_update", kwargs={"pk": comment_fixture.pk})

    data = {
        "text": "test text updated",
        "rating": 4,
        "advertisement": advertisement_fixture.pk,
    }

    data_1 = {
        "text": "test text updated",
    }

    # Проверка без аутентификации
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Проверка с аутентификацией, но без прав владельца
    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)
    print(response.data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Проверка с аутентификацией и правами владельца
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.put(url, data)
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "test text updated"
    assert response.json()["rating"] == 4

    # Проверка PATCH-запроса
    response_patch = api_client.patch(url, data_1)
    assert response_patch.status_code == status.HTTP_200_OK
    assert response_patch.json()["text"] == "test text updated"


@pytest.mark.django_db
def test_comment_delete(
    api_client, comment_fixture, user_is_owner_fixture, user_fixture
):
    """
    Тест удаления отзыва
    """

    url = reverse("board:comment-detail", kwargs={"pk": comment_fixture.pk})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0
