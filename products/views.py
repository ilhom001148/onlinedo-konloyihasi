from django.shortcuts import render
from django.views import View

from products.models import Category, Product, ProductImages


class HomeView(View):
    def get(self,request):
        categories=Category.objects.all()
        products=Product.objects.all()
        return render(request, 'index.html', {
            'categories': categories,
            'products': products
        })



class ProductsView(View):
    def get(self,request):
        products=Product.objects.all()
        return render(request, 'products.html', {
            'products': products,
        })


class ProductDetailView(View):
    def get(self,request,id):
        product=Product.objects.get(id=id)
        images=product.images.all()
        return render(request, 'product_detail.html', {
            'product': product,
            'images': images,

        })


















