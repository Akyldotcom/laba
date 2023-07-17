from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.utils.html import urlencode
from webapp.models import Product, Category

from django.views.generic import FormView, ListView, DeleteView, UpdateView, TemplateView
from webapp.forms import SearchForm, ProductForm


class ProductListView(ListView):
    model = Product
    template_name = "index.html"
    context_object_name = "products"
    ordering = ("-updated_at",)
    paginate_by = 7

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
                                       Q(description__icontains=self.search_value))
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
    success_url = reverse_lazy("your-success-url")


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
