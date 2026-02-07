from django.conf import settings
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='category_images/',null=True,blank=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    title=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    percent=models.IntegerField(null=True,blank=True)
    main_image=models.ImageField(upload_to='product_images/',null=True,blank=True)
    desc=models.TextField(null=True,blank=True)
    stock=models.IntegerField()


    def save(self,*args,**kwargs):
        if self.percent:
            self.discount_price=self.price-((self.price/100)*self.percent)
        super(Product,self).save(*args,**kwargs)


    def __str__(self):
        return self.title


class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='product_images/',null=True,blank=True)


    def __str__(self):
        return self.product.title




class WishList(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='wishlist')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlists')


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} savati"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        price_to_use = self.product.discount_price if self.product.discount_price else self.product.price
        return self.quantity * price_to_use
