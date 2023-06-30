from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound

from webapp.models import Product, Category


def product_list_view(request):
    products = Product.objects.order_by("-updated_at")
    context = {"products": products}
    return render(request, "index.html", context)


def product_create_view(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "create_product.html", {"categories": categories})
    else:
        product = Product.objects.create(
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            cost=request.POST.get("cost"),
            image=request.POST.get("image")
        )
        return redirect("product_view", pk=product.pk)


def product_view(request, *args, pk, **kwargs):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return HttpResponseNotFound()
    return render(request, "product.html", {"product": product})


# def product_view(request, *args, pk, **kwargs):
#     product = get_object_or_404(Product, id=pk)
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
