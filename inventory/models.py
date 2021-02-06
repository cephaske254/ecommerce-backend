from django.db import models
from django.utils.text import slugify
import random, string
from django.utils import timezone
from django.urls import reverse
from django.core.validators import ValidationError
from django.utils.text import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    """
    name, @products
    """

    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def product_count(self):
        return self.products.count()

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["pk", "name"]

    def __str__(self):
        return self.name

    @classmethod
    def make_slug(cls, name):
        slug = slugify(name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug

    @property
    def products(self):
        return Product.objects.filter(categories=self.pk).all()

    def save(self, *args, **kwargs):
        self.name = self.name.title() if self.name else self.name
        self.slug = self.make_slug(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)
    icon = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title() if self.name else self.name
        super().save(*args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey(
        "inventory.Product", models.CASCADE, null=True, related_name="images"
    )
    image = models.ImageField(upload_to="products", blank=False, null=True)


class Product(models.Model):
    """
    name, category, description, @images, @image_count, available, brand, price, date
    """

    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(unique=True, editable=False, null=False, blank=True)
    categories = models.ManyToManyField(Category)
    description = models.TextField(blank=False, null=False)
    brand = models.ForeignKey(Brand, models.CASCADE, blank=True, null=True)
    market_price = models.FloatField(
        max_length=200, default=12, blank=False, null=False
    )
    discount_price = models.FloatField(
        max_length=200, default=None, blank=True, null=True
    )
    colors = models.TextField(default="[]", blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.pk)

    @property
    def price(self):
        if self.discount_price and float(self.discount_price) > 0:
            return self.discount_price
        else:
            return self.market_price

    @property
    def image(self):
        obj = self.images.first()
        if obj and obj.image:
            return obj.image.url
        return None

    @property
    def image_count(self):
        return self.images.all().count()

    @property
    def url(self):
        return reverse("products_detail", kwargs={"slug": self.slug})

    @classmethod
    def make_slug(cls, name):
        slug = slugify(name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        if not self.slug:
            self.slug = self.make_slug(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-pk", "name"]


class deal(models.Model):
    product = models.OneToOneField(Product, models.CASCADE, verbose_name="deal")
    start = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class BannerAd(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.CharField(max_length=200, editable=False)
    product = models.ForeignKey(
        Product, models.CASCADE, null=True, blank=True, related_name="banner_ad"
    )
    active = models.BooleanField(default=True, blank=False, null=False)
    show_prices = models.BooleanField(default=True, blank=False, null=False)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="banners", blank=False, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.make_slug(self.title)
        super().save(*args, **kwargs)

    @classmethod
    def make_slug(cls, name):
        slug = slugify(name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug

    @property
    def link(self):
        if self.product:
            return self.product.url
        elif self.url:
            return self.url
        return None

    class Meta:
        ordering = ["-pk", "date", "title"]