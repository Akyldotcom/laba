from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy, reverse
from django.utils.html import urlencode
from django.views import View

from webapp.models import Product, Category, CartItem, Ordering

from django.views.generic import FormView, ListView, DeleteView, UpdateView, TemplateView
from webapp.forms import SearchForm, ProductForm


class ProductListView(ListView):
    model = Product
    template_name = "index.html"
    context_object_name = "products"
    ordering = [Lower('name')]
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["form"] = self.form
        if self.search_value:
            context["query"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data["search"]
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.search_value)
        if self.search_value:
            queryset = queryset.filter(Q(name__icontains=self.search_value) |
                                       Q(description__icontains=self.search_value) |
                                       Q(cost__icontains=self.search_value))
        return queryset


# def product_list_view(request):
#     products = Product.objects.order_by("-updated_at")
#     context = {"products": products}
#     return render(request, "index.html", context)
class ProductCreateView(FormView):
    form_class = ProductForm
    template_name = "create_product.html"

    def form_valid(self, form):
        product = form.save()
        return redirect("product_view", pk=product.pk)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "update_product.html"
    success_url = reverse_lazy("index")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "delete_product.html"
    success_url = reverse_lazy("index")


# def product_create_view(request):
#     if request.method == "GET":
#         categories = Category.objects.all()
#         return render(request, "create_product.html", {"categories": categories})
#     else:
#         product = Product.objects.create(
#             description=request.POST.get("description"),
#             category=request.POST.get("category"),
#             cost=request.POST.get("cost"),
#             image=request.POST.get("image")
#         )
#         return redirect("product_view", pk=product.pk)
class ProductDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = get_object_or_404(Product, id=kwargs['pk'])
        return context

    def get_template_names(self):
        return "product.html"


# def product_view(request, *args, pk, **kwargs):
#     try:
#         product = Product.objects.get(id=pk)
#     except Product.DoesNotExist:
#         return HttpResponseNotFound()
#     return render(request, "product.html", {"product": product})


def category_create_view(request):
    if request.method == "GET":
        return render(request, "category_create_view.html")
    else:
        Category.objects.create(
            name=request.POST.get("Name"),
            description=request.POST.get("description")
        )
        return HttpResponseRedirect("/")


def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    cart_item = CartItem.objects.filter(product=product, order=None).first()
    order = Ordering.objects.last()  # Get the last order, assuming you have one created, for setting the order field

    if not order:
        order = Ordering.objects.create(name='', phone='', address='')

    if not cart_item and product.stock > 0:
        CartItem.objects.create(product=product, order=order)
    elif cart_item and cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('index')


def cart(request):
    cart_items = CartItem.objects.all()
    cart_total = 0
    for cart_item in cart_items:
        cart_item.total_amount = cart_item.product.cost * cart_item.quantity
        cart_total += cart_item.total_amount

    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


def remove_from_cart(request, pk):
    CartItem.objects.filter(pk=pk).delete()
    return redirect('cart')


def create_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        order = Ordering.objects.create(name=name, phone=phone, address=address)
        cart_items = CartItem.objects.all()
        for cart_item in cart_items:
            order.products.add(cart_item.product, through_defaults={'quantity': cart_item.quantity})

        cart_items.delete()
        return redirect(
            'order_confirmation')
    else:
        return redirect('cart')
