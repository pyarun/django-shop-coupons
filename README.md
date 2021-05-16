# Django Shop Coupons

This project is inspired by [django-shop-discounts](https://github.com/bmihelac/django-shop-discounts).
It was good but not updated to use latest django-shop design.

Django-Shop-Coupons is still work in progress and do not support full features of django-shop-discounts. 

### Features

- Create Offers and set attributes like date range, number of users.
- Create multiple coupons for each Offer.


### Installation
 This assumes you have already installed django-shop
 
- `pip install git+https://github.com/pyarun/django-shop-coupons.git`
- Add `shop_coupons` in `INSTALLED_APPS`.

##### Configuration
- Add `shop_coupons.modifiers.DiscountCartModifier` to `SHOP_CART_MODIFIERS`.
- Add `shop_coupons.forms.DiscountForm` to `SHOP_DIALOG_FORMS`.
