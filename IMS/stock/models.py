from django.db import models
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=100,blank=True)
    description = models.TextField(max_length=200, blank=True)
    price = models.IntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
   

    def save(self, *args, **kwargs):
        if not self.slug:  # only generate slug if not set
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class Size_Variation(models.Model):
    size = models.CharField(max_length=225,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    price_per_unit = models.IntegerField(null=False)
    stock = models.IntegerField()
    
    def __str__(self):
        return f"{self.product.product_name},{self.size}"
    
class Length_Variation(models.Model):
    length_in_inch = models.IntegerField(null=True, blank=True)
    size = models.ForeignKey(Size_Variation,on_delete=models.CASCADE)
    total_price = models.IntegerField(null=False,blank=True)

    def save(self, *args, **kwargs):
        # Calculate total_price automatically
        if self.length_in_inch and self.size.price_per_unit:
            self.total_price = self.size.price_per_unit * self.length_in_inch
        else:
            self.total_price = self.size.price_per_unit  # fallback if either field is None
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.size}"