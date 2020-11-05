from django.db import models
from django.utils.text import slugify
import string, random, datetime


class Product(models.Model):
    id = models.CharField(
        primary_key=True,
        unique=True,
        null=False,
        editable=False,
        max_length=255,
        db_index=True,
    )
    name = models.CharField(max_length=100, blank=False)
    slug = models.CharField(
        max_length=200, editable=False, null=False, blank=True, db_index=True
    )
    description = models.TextField(blank=False, null=True)
    other_info = models.TextField(blank=True, null=True)
    price = models.FloatField(default=None, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    last_edited = models.DateTimeField(auto_now=True, null=True, editable=False)

    @property
    def images_count(self):
        return self.images.count()

    @property
    def images(self):
        return self.product_images.all()

    @classmethod
    def generate_unique_id(cls):
        product_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        while product_id and cls.objects.filter(pk=product_id).exists():
            product_id = "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            )
        return product_id

    @classmethod
    def generate_unique_slug(cls, name):
        slug = slugify(name)
        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                "%s-%s"
                % (
                    name,
                    int(
                        datetime.datetime.strftime(datetime.datetime.now(), "%X")
                        .replace(":", "")
                        .replace(" ", "")
                    ),
                ),
                allow_unicode=False,
            )
        return slug

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.generate_unique_id()
            self.slug = self.generate_unique_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.slug)


def product_image_to_folder(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.product.name, ext)
    return "products/images/%s"% (filename)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, related_name="product_images"
    )
    image = models.ImageField(upload_to=product_image_to_folder)
    date_added = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    @classmethod
    def generate_index(cls, product_id):
        product_count = Product.objects.filter(id=product_id).count()
        if product_count == 0:
            return product_count
        return product_count + 1

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def itemIndex(cls, product_id, item_id=0):
        product_images = ProductImage.objects.filter(product=product_id).all()
        ids = [(item.pk) for item in product_images]
        try:
            return (ids).index(item_id)
        except:
            return 0

    def __str__(self):
        # return "%s (#%s)" % (self.product.slug, self.itemIndex(self.product, self.pk))
        return "%s" % (self.product.slug)

    class Meta:
        ordering = ("-product", "-id")


def banner_image_to_folder(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.product.name, ext)
    return "products/images/banners/%s"% (filename)


class BannerImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, related_name="banner_images"
    )
    image = models.ImageField(upload_to=banner_image_to_folder)
    date_added = models.DateTimeField(auto_now_add=True, null=True, editable=False)
