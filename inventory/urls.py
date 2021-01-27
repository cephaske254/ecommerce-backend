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
    path("banner_ads/", views.BannerAdListCreate.as_view(), name="banner_ads_list_create"),
    path("banner_ads/<slug>/", views.BannerAdsDetail.as_view(), name="banner_ads_list_create"),
]