import pytest

from django.urls import reverse
from rest_framework import status
from board.models import Comment
from users.tests.conftest import api_client, user_fixture, user_is_owner_fixture


@pytest.mark.django_db
def test_comment_create(api_client, user_fixture, advertisement_fixture):
    url = reverse("board:comment_create")

    assert advertisement_fixture.pk is not None

    data = {
        "text": "new text",
        "advertisement": advertisement_fixture.pk,  # Must be valid PK
        "rating": 5,
    }

    # Неавторизованный запрос
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Авторизованный запрос
    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data, format='json')

    if response.status_code != 201:
        print("Error response:", response.json())

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_comment_list(api_client, comment_fixture, user_is_owner_fixture, user_fixture):
    """
    Тест получения списка отзывов
    """
    url = reverse("board:comment_list")
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

    url = reverse("board:comment_update", kwargs={"pk": comment_fixture.pk})

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
def test_comment_delete(api_client, comment_fixture, user_is_owner_fixture, user_fixture):
    """Тест удаления комментария"""
    # Проверяем, что комментарий существует перед удалением
    assert Comment.objects.filter(pk=comment_fixture.pk).exists()

    url = reverse("board:comment_delete", kwargs={"pk": comment_fixture.pk})

    # 1. Неавторизованный запрос (должен возвращать 401)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
        f"Ожидался 401 Unauthorized, получен {response.status_code}. "
        f"Ответ: {response.json()}"
    )

    # 2. Запрос от другого пользователя (должен возвращать 403)
    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # 3. Запрос от владельца (должен возвращать 204)
    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(pk=comment_fixture.pk).exists()
