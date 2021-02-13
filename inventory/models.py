from django.db import models
from django.utils.text import slugify
import random, string
from django.utils import timezone
from django.urls import reverse
from django.core.validators import ValidationError
from django.utils.text import gettext_lazy as _
from PIL import Image as image
from io import StringIO, BytesIO
from django.core.files.base import ContentFile
import os.path

# Create your models here.
from PIL import Image


def MakeThumb(instance, thubm_size=((400, 400))):
    img = image.open(instance)
    img.thumbnail(thubm_size, image.ANTIALIAS)

    thumb_name, thumb_extension = os.path.splitext(instance.name)
    thumb_extension = thumb_extension.lower()

    thumb_filename = thumb_name + thumb_extension

    if thumb_extension in [".jpg", ".jpeg"]:
        FTYPE = "JPEG"
    elif thumb_extension == ".gif":
        FTYPE = "GIF"
    elif thumb_extension == ".png":
        FTYPE = "PNG"
    else:
        return False  # Unrecognized file type

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    img.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    data = {
        "name": thumb_filename,
        "content": ContentFile(temp_thumb.read()),
        "save": False,
    }
    temp_thumb.close()

    return data

    return True


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

    @property
    def has_banner_ad(self):
        if self.banner_ad:
            return True
        return False

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
    __original_image_name = None

    def __init__(self, *args, **kwargs):
        super(BannerAd, self).__init__(*args, **kwargs)
        self.__original_image_name = self.image.name

    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.CharField(max_length=200, editable=False)
    product = models.OneToOneField(
        Product, models.CASCADE, null=True, blank=True, related_name="banner_ad"
    )
    active = models.BooleanField(default=True, blank=False, null=False)
    show_prices = models.BooleanField(default=True, blank=False, null=False)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="banners", blank=False, null=True)
    thumbnail = models.ImageField(
        upload_to="banners/thumbnails/", blank=False, null=True
    )
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.make_slug(self.title)

        if not self.order:
            last_banner = BannerAd.objects.order_by("-order", "title").first()
            if last_banner and last_banner.order:
                self.order = last_banner.order + 1

        image = self.image
        if self.pk:
            self.make_thumbnail(self.pk, self.image)
        else:
            self.thumbnail.save(**MakeThumb(self.image))
        super().save(*args, **kwargs)

    @classmethod
    def make_thumbnail(cls, pk, image):
        instance = cls.objects.get(pk=pk)
        if instance.image != image:
            instance.thumbnail.save(**MakeThumb(instance.image))
        return None

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
        ordering = ["order", "title"]
