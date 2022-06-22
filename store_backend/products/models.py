from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string

from .utils import arabic_slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=False, null=False)
    slug = models.SlugField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'categories'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if not self.slug:
                self.slug = arabic_slugify(self.name)
            super(Category, self).save()
        except IntegrityError:
            self.slug = arabic_slugify("{}-{}".format(get_random_string(length=7), self.name))
            super(Category, self).save()

    def __str__(self):
        return self.name




class Product(models.Model):

    categories = models.ManyToManyField(
        'Category',
        related_name='products'
    )
    name = models.CharField(max_length=300, blank=False, null=False)
    slug = models.SlugField(editable=False)
    image = models.URLField(max_length=5550, null=True, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty_available = models.PositiveIntegerField(null=False, blank=False, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'products'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.qty_available < 1:
            self.is_available = False
        else:
            self.is_available = True
        try:
            if not self.slug:
                self.slug = arabic_slugify(self.name)
            super(Product, self).save()
        except IntegrityError:
            self.slug = arabic_slugify("{}-{}".format(get_random_string(length=7), self.name))
            super(Product, self).save()

    def __str__(self):
        return '{}'.format(self.name)
