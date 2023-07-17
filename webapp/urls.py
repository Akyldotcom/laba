from django.urls import path
from django.views.generic import RedirectView

from webapp import views
from webapp.views import \
    ProductListView, ProductCreateView, ProductDetailView, ProductDeleteView, category_create_view, ProductUpdateView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="index")),
    path('products/', ProductListView.as_view(), name="index"),
    path('product/create', ProductCreateView.as_view(), name="create_product"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name="update_product"),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name="delete_product"),
    path('categories/', category_create_view, name="categories_create_view"),
    path('product/<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/create_order/', views.create_order, name='create_order'),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
]
