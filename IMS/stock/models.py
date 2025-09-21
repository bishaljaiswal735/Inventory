from django.db import models
from django.utils.text import slugify

# Create your models here.

class Size_Variation(models.Model):
    size = models.CharField(max_length=225)
    
    def __str__(self):
        return self.size
    
class Length_Variation(models.Model):
    length_in_inch = models.CharField(max_length = 20)

    def __str__(self):
        return self.length_in_inch
    
class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(max_length=100,blank=True)
    description = models.TextField(max_length=200, blank=True)
    size = models.ForeignKey(Size_Variation,on_delete=models.CASCADE, null=True, blank=True)
    length = models.ForeignKey(Length_Variation,on_delete=models.CASCADE, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:  # only generate slug if not set
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


