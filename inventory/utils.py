import base64, json
from django.core.files.base import ContentFile
from . import models


def buildImage(data, name):
    format, imgstr = data.split(";base64,")
    ext = format.split("/")[-1]
    return ContentFile(base64.b64decode(imgstr), name=str(name).strip() + "." + ext)


def saveProductImages(request, product):
    images = request.data.get("images")
    name = request.data.get("name")
    if images:
        if isinstance(images, list):
            for image in images:
                data = image.get("current", image.get("original", None))
                models.Image.objects.create(
                    product=product, image=buildImage(data, name)
                )
        elif isinstance(images, dict):
            data = images.get("current", images.get("original", None))

            if not (data):
                return

            models.Image.objects.create(
                product=product,
                image=buildImage(data, name),
            )


def removeProductImages(request):
    removedImages = request.data.get("removedImages", [])
    images = models.Image.objects.filter(id__in=removedImages).all().delete()


def setProductCategories(request, product):
    categories = [(ctg.lower()) for ctg in request.data.get("categories")]
    existing = [(ctg.name.lower()) for ctg in product.categories.all()]

    new = [(ctg) for ctg in categories if ctg not in existing]
    removed = [(ctg) for ctg in existing if ctg not in categories]

    addCategories(product, new)
    removeCategories(product, removed)


def addCategories(product, categories):
    if categories:
        for _category in categories:
            try:
                category = models.Category.objects.get(pk=_category)
            except:
                category = models.Category.objects.filter(
                    name__iexact=_category
                ).first()
                category = (
                    models.Category.objects.create(name=_category)
                    if not category
                    else category
                )
            product.categories.add(category)


def removeCategories(product, categories):
    if categories:
        for _category in categories:
            category = models.Category.objects.filter(name__iexact=_category).first()
            if not category:
                return
            product.categories.remove(category)


def addProductBrand(brand_data):
    if brand_data:
        try:
            brand = models.Brand.objects.get(pk=brand_data)
        except:
            brand = models.Brand.objects.filter(name__iexact=brand_data).first()
            brand = models.Brand.objects.create(name=brand_data) if not brand else brand
        return brand
    return None


def saveBannerAdsImage(request, banner):
    image = request.data.get("image")
    name = request.data.get("name")

    banner.image = buildImage(image, name)
    banner.save()