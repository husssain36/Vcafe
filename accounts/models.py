from django.db import models
from django.contrib.auth.models import User

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=40, null=True)
#     name = models.CharField(max_length=70, null=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
     
#     def __str__(self):
#         return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    count = models.DecimalField(decimal_places=0, max_digits=5, null=True)
    def __str__(self):
        return self.name

class VcanteenMenu(models.Model):
    item = models.CharField(max_length=100)
    category = models.ForeignKey(Category, max_length=100,on_delete= models.SET_NULL, null=True)
    price = models.IntegerField()
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.item

# class VloungeMenu(models.Model):
#     item = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, max_length=100,on_delete= models.SET_NULL, null=True)
#     price = models.IntegerField()
#     image = models.ImageField()
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     def __str__(self):
#         return self.item
        
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    successful = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    vcanteen = models.ForeignKey(VcanteenMenu, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id)
        
    @property
    def get_total(self):
        total = self.vcanteen.price * self.quantity
        return total


