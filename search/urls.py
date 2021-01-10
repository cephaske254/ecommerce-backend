from django.urls import path
from . import views

urlpatterns = [
    path(
        "products/",
        views.searchProducts.as_view(),
    ),
    path(
        "categories/",
        views.searchCategories.as_view(),
    ),
]
