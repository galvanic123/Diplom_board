from pathlib import Path

from rest_framework.exceptions import ValidationError

from board.models import Advertisement


class ForbiddenWordValidator:
    """Валидатор для проверки текста на запрещенные слова"""

    __slots__ = ("advertisement_title", "advertisement_description", "comment_text")

    def __init__(
        self,
        advertisement_title=None,
        advertisement_description=None,
        comment_text=None,
    ):
        self.advertisement_title = advertisement_title
        self.advertisement_description = advertisement_description
        self.comment_text = comment_text

    def __call__(self, value):

        advertisement_title_field = value.get(self.advertisement_title)
        advertisement_description_field = value.get(self.advertisement_description)
        comment_text_field = value.get(self.comment_text)

        with open(
            Path(__file__).parent.joinpath("forbidden_words.txt"), "r", encoding="utf-8"
        ) as file:
            forbidden_words = file.read().splitlines()

        for word in forbidden_words:
            try:
                if (
                    word in advertisement_title_field.lower()
                    or word in advertisement_description_field.lower()
                ):
                    raise ValidationError("Имеется запрещенное слово в тексте")
            except TypeError:
                pass
            except AttributeError:
                pass
            try:
                if word in comment_text_field.lower():
                    raise ValidationError("Имеется запрещенное слово в тексте")
            except TypeError:
                pass
            except AttributeError:
                pass


class RepeatAdvertisementValidator(ForbiddenWordValidator):
    """Валидатор для проверки повторения объявления"""

    __slots__ = ("title", "description", "price")

    def __init__(self, title, description, price):
        super().__init__(
            advertisement_title=title, advertisement_description=description
        )
        self.price = price

    def __call__(self, value):
        title_field = value.get(self.advertisement_title)
        description_field = value.get(self.advertisement_description)
        price_field = value.get(self.price)

        if Advertisement.objects.filter(
            title=title_field, description=description_field, price=price_field
        ).exists():
            raise ValidationError("Такое объявление уже существует")


def price_zero_validator(value):
    """Валидатор для проверки цены объявления равной нулю"""

    if not value:
        raise ValidationError("Цена объявления не может быть пустая")
