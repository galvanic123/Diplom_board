from django.utils import timezone
from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status
from board.models import Advertisement, Category
from users.tests.conftest import api_client, user_fixture


@pytest.mark.django_db
def test_advertisement_create(api_client, user_fixture):
    category = Category.objects.create(name="Electronics", slug="electronics")

    url = reverse("board:advertisement-list")
    data = {
        "title": "New iPhone",
        "description": "Brand new iPhone 15",
        "price": "999",
        "category": category.id,
    }

    # Unauthenticated request (should return 401)
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Authenticated request (should return 201)
    api_client.force_authenticate(user=user_fixture)
    response = api_client.post(url, data, format="json")
    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert Advertisement.objects.count() == 1
    ad = Advertisement.objects.first()
    assert ad.title == "New iPhone"
    assert ad.owner == user_fixture
    assert ad.category == category

@pytest.mark.django_db
def test_advertisement_list(api_client, user_fixture):
    """Тестирование получения списка объявлений"""
    # Создаем тестовые объявления
    category = Category.objects.create(name="Electronics", slug="electronics")
    ad1 = Advertisement.objects.create(
        title="Laptop",
        description="Gaming laptop",
        price=1500,
        category=category,
        owner=user_fixture
    )
    ad2 = Advertisement.objects.create(
        title="Phone",
        description="Smartphone",
        price=800,
        category=category,
        owner=user_fixture
    )

    url = reverse("board:advertisement-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 2
    assert response.json()["results"][0]["title"] == "Laptop"
    assert response.json()["results"][1]["title"] == "Phone"


@pytest.mark.django_db
def test_advertisement_retrieve(api_client, user_fixture):
    """Тестирование получения одного объявления"""
    category = Category.objects.create(name="Cars", slug="cars")
    ad = Advertisement.objects.create(
        title="Tesla Model S",
        description="Electric car",
        price=75000,
        category=category,
        owner=user_fixture
    )

    url = reverse("board:advertisement-detail", kwargs={"pk": ad.pk})

    api_client.force_authenticate(user=user_fixture)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Tesla Model S"
    assert response.json()["price"] == "75000.00"

@pytest.mark.django_db
def test_advertisement_update(api_client, user_fixture):
    """Тестирование обновления объявления"""
    category = Category.objects.create(name="Books", slug="books")
    ad = Advertisement.objects.create(
        title="Old Book",
        description="Some old book",
        price=10,
        category=category,
        owner=user_fixture
    )

    url = reverse("board:advertisement-detail", kwargs={"pk": ad.pk})
    update_data = {
        "title": "Updated Book Title",
        "price": "15"
    }

    # Неавторизованный запрос
    response = api_client.patch(url, update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Авторизованный запрос
    api_client.force_authenticate(user=user_fixture)
    response = api_client.patch(url, update_data, format='json')
    if response.status_code != 200:
        print("Response errors:", response.json())

    assert response.status_code == status.HTTP_200_OK
    ad.refresh_from_db()
    assert ad.title == "Updated Book Title"
    assert ad.price == 15


@pytest.mark.django_db
def test_advertisement_delete(api_client, user_fixture):
    """Тестирование удаления объявления"""
    category = Category.objects.create(name="Furniture", slug="furniture")
    ad = Advertisement.objects.create(
        title="Wooden Table",
        description="Nice wooden table",
        price=200,
        category=category,
        owner=user_fixture
    )

    url = reverse("board:advertisement-detail", kwargs={"pk": ad.pk})

    # Неавторизованный запрос
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Авторизованный запрос
    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Advertisement.objects.count() == 0
