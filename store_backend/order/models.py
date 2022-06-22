from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings


# Create your models here.
class Order(models.Model):
    STATUSES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )

    PAYMENT = (
        ('Paypal', 'Paypal'),
        ('Card', 'Card'),
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    payment_method = models.CharField(max_length=15, null=False, blank=False, choices=PAYMENT)
    status = models.CharField(choices=STATUSES, default='Accepted', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'all_orders'

    def __str__(self):
        return 'Order N°= {}'.format(self.id)

    def get_items_cost(self):
        return float(sum(item.get_quantity_price() for item in self.items.all()))

    def get_total_items_count(self):
        return int(sum(item.quantity for item in self.items.all()))



class OrderItem(models.Model):
    order = models.ForeignKey(
        to='order.Order',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='items'
    )
    product = models.ForeignKey(
        to='products.product',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)], default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False , default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        db_table = 'order_items'

    def __str__(self):
        return "Item no {} of order {} ".format(self.id, self.order.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_quantity_price(self):
        return self.price * self.quantity

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.product.qty_available < self.quantity:
            return ValidationError('The quantity of the product available is insufficient for this order')
        else:
            self.price = self.product.price
            super(OrderItem, self).save()
