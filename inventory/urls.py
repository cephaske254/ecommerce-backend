from django.urls import path
from . import views

urlpatterns = [
    path("visitorIn/", views.visitorIn.as_view()),
    path("products/", views.ProductListCreate.as_view(), name="products_list_create"),
    path("products/top/", views.TopProducts.as_view(), name="top_products"),
    path("products/<slug>/", views.ProductDetail.as_view(), name="products_detail"),
    path(
        "categories/", views.CategoryListCreate.as_view(), name="categories_list_create"
    ),
    path(
        "categories/<slug>/", views.CategoryDetail.as_view(), name="categories_detail"
    ),
    path("banners/", views.BannerAdListCreate.as_view(), name="banner_ads_list_create"),
    path(
        "banners/reorder/",
        views.BannerAdsReOrder.as_view(),
        name="banner_ads_reorder",
    ),
    path(
        "banners/<slug>/",
        views.BannerAdsDetail.as_view(),
        name="banner_ads_list_create",
    ),
]