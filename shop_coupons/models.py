from django.db import models
from django.db.models import Q, F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from shop_discounts.constants import DiscountType


class Offer(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    is_active = models.BooleanField(_("Is active"), default=True)
    valid_from = models.DateTimeField(_("Valid from"), default=timezone.now)
    valid_until = models.DateTimeField(_("Valid until"), blank=True, null=True)

    discount_type = models.CharField(choices=DiscountType.choices, max_length=16)
    value = models.FloatField(help_text=_("Percent/Absolute discount value."))

    def __str__(self):
        return self.name


class CouponManager(models.Manager):
    def active(self):
        """
        Coupon is considered active when:
        1. offer is active
        2. offer is valid by date
        3. max_usage is less than or equal to used_count
        """
        at_datetime = timezone.now()
        qs = self.filter(
            Q(offer__is_active=True)
            & Q(offer__valid_from__lte=at_datetime)
            & (Q(offer__valid_until__isnull=True) | Q(offer__valid_until__gt=at_datetime))
            & Q(max_usage__gte=F("used_count"))
        )
        return qs


class Coupon(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    code = models.CharField(
        _("Code"),
        max_length=30,
        blank=True,
        null=False,
        unique=True,
        help_text=_("Is discount valid only with included code"),
    )
    max_usage = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0, editable=False)

    objects = CouponManager()

    def apply_discount(self, amount):
        if self.offer.discount_type == DiscountType.PERCENT:
            discount = (amount * self.offer.value)/100
        else:
            discount = self.offer.value

        return discount

    def update_usage(self, inc=1, force_save=False):
        self.used_count = F('used_count') + inc
        if force_save:
            self.save(update_fields=['used_count'])


