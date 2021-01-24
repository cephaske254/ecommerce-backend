from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListCreate.as_view(), name="products_list_create"),
    path("products/<slug>/", views.ProductDetail.as_view(), name="products_detail"),
    path(
        "categories/", views.CategoryListCreate.as_view(), name="categories_list_create"
    ),
    path(
        "categories/<slug>/", views.CategoryDetail.as_view(), name="categories_detail"
    ),
]