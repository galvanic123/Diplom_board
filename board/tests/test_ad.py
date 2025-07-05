import pytest
from django.urls import reverse
from rest_framework import status

from board.models import Advertisement
from users.tests.conftest import admin_fixture, api_client, user_fixture, user_is_owner_fixture


@pytest.mark.django_db
def test_advertisement_create(api_client, user_fixture, category_fixture):
    """Тестирование создания нового объявления"""
    url = reverse("board:advertisement-list")
    data = {
        "title": "title new",
        "description": "description new",
        "price": 100,
        "category": category_fixture.id  # Добавляем обязательное поле
    }

    # Неавторизованный запрос
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Авторизованный запрос
    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == data["title"]
    assert Advertisement.objects.count() == 1
    assert Advertisement.objects.first().owner == user_fixture


@pytest.mark.django_db
def test_advertisement_list(advertisement_fixture, api_client, user_fixture):
    """Тестирование просмотра списка объявлений"""
    url = reverse("board:advertisement-list")

    # Создаем второе объявление для проверки порядка
    from board.models import Advertisement
    Advertisement.objects.create(
        title="Newer Ad",
        description="New description",
        price=200,
        owner=user_fixture,
        category=advertisement_fixture.category
    )

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Проверяем порядок (новые первыми)
    results = response.json()["results"]
    assert len(results) == 2
    assert results[0]["title"] == "Newer Ad"
    assert results[1]["title"] == "test title"

@pytest.mark.django_db
def test_advertisement_retrieve(
    api_client, user_is_owner_fixture, user_fixture, advertisement_fixture, admin_fixture
):
    """Тестирование просмотра одного объявления"""

    url = reverse(
        "board:advertisement-detail", kwargs={"pk": advertisement_fixture.pk}
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user=user_is_owner_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "test title"

    api_client.force_authenticate(user=admin_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "test title"


@pytest.mark.django_db
def test_advertisement_update(
    api_client, user_is_owner_fixture, user_fixture, advertisement_fixture
):
    """Тестирование изменения информация в одном объявлении"""

    url = reverse(
        "board:advertisement-detail", kwargs={"pk": advertisement_fixture.pk}
    )
    data = {
        "title": "test_title_updated",
        "price": 200,
    }
    data_1 = {
        "title": "test_title_updated",
        "price": 300,
    }
    response = api_client.put(url, data)
    response_1 = api_client.patch(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_1.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.put(url, data)
    response_1 = api_client.patch(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response_1.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.put(url, data)
    response_1 = api_client.patch(url, data_1)

    assert response.status_code == status.HTTP_200_OK
    assert response_1.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "test_title_updated"


@pytest.mark.django_db
def test_advertisement_delete(
    api_client, user_is_owner_fixture, user_fixture, advertisement_fixture
):
    """Тестирование удаления объявления"""

    url = reverse(
        "board:advertisement-detail", kwargs={"pk": advertisement_fixture.pk}
    )
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Advertisement.objects.count() == 0
