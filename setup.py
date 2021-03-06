from setuptools import setup, find_packages


VERSION = __import__("shop_coupons").__version__

setup(
    name="django-shop-coupons",
    description="configurable and extendible discount app for Django-shop",
    version=VERSION,
    author="Bojan Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://github.com/bmihelac/django-shop-discounts",
    license='BSD License',
    install_requires=[
        # 'django-shop',
        ],
    packages=find_packages(exclude=["example", "example.*"]),
)