from django.db import models

class Brand(models.Model):
    brand_id = models.BigAutoField(primary_key=True)
    name = models.CharField("Brand name", max_length=50)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Product(models.Model):
    the_name = models.CharField("Product Name", max_length=100, default="no-name", help_text="This is the help text")
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    url = models.SlugField()

    class Meta:
        ordering = ["age"]
    
    def __str__(self):
        return f"Product name: {self.the_name}"

class Stock(models.Model):
    units = models.BigIntegerField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.product)