from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from unicodedata import category
from products.models import Category, Product, ProductImages
from .models import WishList
from .models import CartItem



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
        related_products=Product.objects.filter(category=product.category).exclude(id=product.id)[:3]

        return render(request, 'product_detail.html', {
            'product': product,
            'images': images,
            'related_products': related_products,

        })




@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishList.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()
        messages.info(request, f"{product.title} saralanganlardan olib tashlandi.")
    else:
        messages.success(request, f"{product.title} saralanganlarga qo'shildi.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))




@login_required
def wishlist_view(request):
    wishlist_items = WishList.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})




def cart_detail(request):

    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        items = []

    context = {
        'items': items,
    }
    return render(request, 'cart_detail.html', context)













