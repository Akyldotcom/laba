from django.urls import path
from django.views.generic import RedirectView

from webapp.views import \
    ProductListView, ProductCreateView, ProductDetailView, ProductDeleteView, category_create_view, ProductUpdateView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="index")),
    path('products/', ProductListView.as_view(), name="index"),
    path('product/create', ProductCreateView.as_view(), name="create_product"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name="delete_product"),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name="delete_product"),
    path('categories/', category_create_view, name="categories_create_view"),
]
