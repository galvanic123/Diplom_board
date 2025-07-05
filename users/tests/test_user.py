import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


# url = reverse("users:register")
# data = {
#     "email": "testnew@test.ru",
#     "password": "Qwerty123",
#     "first_name": "Test",
#     "last_name": "Test",
# }
# response = client.post(url, data)
#
# assert response.status_code == status.HTTP_201_CREATED
# assert User.objects.count() == 1
# user = User.objects.first()
# assert user.email == data["email"]
# assert user.is_active is False
# assert user.check_password(data["password"])
# assert user.token is not None
#
# assert len(mail.outbox) == 1
# assert mail.outbox[0].subject == "Активация учетной записи"
# assert "Для активации учетной записи пройдите по ссылке" in mail.outbox[0].body
# assert user.email in mail.outbox[0].to


@pytest.mark.django_db
def test_user_email_confirm(user_fixture, client):
    """
    Тестирование подтверждения электронной почты
    """

    url = reverse("users:email_confirm", kwargs={"token": user_fixture.token})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Ваша учетная запись подтверждена!"


@pytest.mark.django_db
def test_user_reset_password(user_fixture, api_client):
    """
    Тестирование сброса пароля
    """

    url = reverse("users:reset_password")
    data = {"email": user_fixture.email}
    api_client.force_authenticate(user_fixture)
    response = api_client.post(url, data)
    response_1 = api_client.post(url, data={})

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["message"]
        == "Ссылка для сброса пароля отправлена на ваш email."
    )
    assert response_1.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_reset_password_confirm(user_fixture, api_client):
    """
    Тестирование подтверждения сброса пароля
    """

    user_fixture.token = "valid_token"
    user_fixture.save()

    url = reverse(
        "users:reset_password_confirm",
        kwargs={"uid": user_fixture.id, "token": user_fixture.token},
    )

    data = {
        "password": "NewPassword123",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Пароль успешно изменен."

    user_fixture.refresh_from_db()
    assert user_fixture.check_password("NewPassword123")
    assert user_fixture.token is not None

    response_1 = api_client.post(url, data={})
    assert response_1.status_code == status.HTTP_400_BAD_REQUEST
    assert response_1.json()["error"] == "Требуется ввести пароль."

    user_fixture.token = "invalid_token"
    user_fixture.save()
    response_2 = api_client.post(url, data)
    assert response_2.status_code == status.HTTP_400_BAD_REQUEST
    assert response_2.json()["error"] == "Ссылка для сброса пароля недействительна."


@pytest.mark.django_db
def test_user_create(client):
    """
    Тестирование создания нового пользователя
    """
    url = reverse("users:register")

    # Полные корректные данные со всеми обязательными полями
    data = {
        "email": "testnew@test.ru",
        "password": "Qwerty123!",  # Спецсимвол для валидации
        "password_confirm": "Qwerty123!",  # Если требуется подтверждение
        "first_name": "Test",
        "last_name": "Test",
        "phone": "+79991112233",  # Если поле обязательно
    }

    response = client.post(url, data)

    # Выведем ответ сервера для отладки
    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    user = User.objects.first()
    assert user.email == data["email"]
    assert not user.is_active  # Пользователь неактивен до подтверждения
    assert user.check_password(data["password"])


@pytest.mark.django_db
def test_user_retrieve(api_client, user_fixture, user_is_owner_fixture):
    """Тестирование просмотра одного пользователя"""
    from board.models import Advertisement, Comment

    # Создаем тестовые данные
    ad = Advertisement.objects.create(
        owner=user_is_owner_fixture, title="Test Ad", price=100.00
    )
    Comment.objects.create(
        advertisement=ad, owner=user_fixture, text="Test comment", rating=4
    )

    url = reverse("users:user-profile-detail", kwargs={"pk": user_is_owner_fixture.pk})

    api_client.force_authenticate(user_fixture)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "comments" in response.json()
    assert len(response.json()["comments"]) == 1


@pytest.mark.django_db
def test_user_delete(api_client, user_fixture, user_is_owner_fixture):
    """
    Тестирование удаления пользователя
    """

    url = reverse("users:user-profile-detail", kwargs={"pk": user_is_owner_fixture.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user_is_owner_fixture)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 1
