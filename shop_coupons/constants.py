from django.db.models import TextChoices


class DiscountType(TextChoices):
    PERCENT = "percent"
    ABSOLUTE = "absolute"
