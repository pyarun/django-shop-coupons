from django.forms import fields, ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from shop.forms.base import DialogForm
from shop_discounts.models import Coupon


class DiscountForm(DialogForm):
    scope_prefix = "discount"
    code = fields.CharField(max_length=30, label=_("Discount Code"))

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        self._coupon = None  # coupon object

    def clean_code(self):
        value = self.cleaned_data["code"]
        try:
            self._coupon = Coupon.objects.active().get(code=value)
        except Coupon.DoesNotExist:
            raise ValidationError(_("Discount code is invalid or expired"))
        return value

    @classmethod
    def form_factory(cls, request, data, cart: "Cart"):
        discount_form = cls(data=data, cart=cart)
        if discount_form.is_valid():
            data = discount_form.cleaned_data
            data["timestamp"] = str(timezone.now())
            cart.extra_rows[cls.scope_prefix] = data
            cart.extra.update({cls.scope_prefix: data})
        else:
            # if coupon is invalid remove any previously added coupon from cart
            if cls.scope_prefix in cart.extra:
                cart.extra.pop(cls.scope_prefix, None)
                cart.save(update_fields=["extra"])
        return discount_form
