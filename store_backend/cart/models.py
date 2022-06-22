from django.db import models
from django.conf import settings


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = 'carts'

    def __str__(self):
        return '{}\'s cart'.format(self.user.username)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        db_table = 'cart_items'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.quantity
