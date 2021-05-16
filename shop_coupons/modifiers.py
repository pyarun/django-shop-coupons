from shop.modifiers.base import BaseCartModifier
from shop.serializers.cart import ExtraCartRow
from shop_discounts.models import Coupon


class DiscountCartModifier(BaseCartModifier):
    identifier = "discount"

    def add_extra_cart_row(self, cart, request):
        if "discount" in cart.extra:
            code = cart.extra["discount"]["code"]
            coupon = Coupon.objects.get(code=code)
            discount = coupon.apply_discount(cart.subtotal)
            row = ExtraCartRow({"label": "Discount Coupon", "amount": discount})
            cart.extra_rows[self.identifier] = row
            cart.extra["discount"].update({"amount": str(discount)})
            cart.total = max(cart.total - discount, 0)
        return cart
