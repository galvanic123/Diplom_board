from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь с таким email не найден.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Генерируем токен и uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Формируем ссылку для сброса пароля
        reset_url = reverse(
            'password_reset_confirm',
            kwargs={'uidb64': uid, 'token': token}
        )

        # Полный URL (включая домен)
        full_reset_url = f"{settings.FRONTEND_URL}{reset_url}"

        # Отправляем письмо
        subject = 'Сброс пароля'
        message = f'Для сброса пароля перейдите по ссылке: {full_reset_url}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        return Response({'detail': 'Письмо с инструкциями по сбросу пароля отправлено на ваш email.'})


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Валидация и смена пароля
        new_password = serializer.validated_data['new_password']

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Пароль успешно изменен.'})

        return Response(
            {'detail': 'Неверная ссылка для сброса пароля.'},
            status=status.HTTP_400_BAD_REQUEST
        )
