from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Items(models.Model):   

    item_name= models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=6,decimal_places=2)
    item_type = models.ForeignKey('LookupItemType', on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.item_name

    class Meta:
        ordering = ['item_name']  

class LookupItemType(models.Model):
    title = models.CharField(max_length=255)
    

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Review(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Address(models.Model):

    STATE_LIST = [

    ('NS','NEGERI SEMBILAN'),
    ('MLK','MELAKA'),
    ('KEL','KELANTAN'),
    ('KED','KEDAH'),
    ('PER','PERLIS'),
    ('SEL','SELANGOR'),

    ]

    postcode = models.CharField(max_length=5)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255,choices=STATE_LIST)
    address = models.TextField()

    def __str__(self) -> str:
        return self.address

class Customer(models.Model):
    age = models.PositiveIntegerField(max_length=3)
    address = models.ForeignKey('Address',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Order(models.Model):
    PAYMENT_STATUS = [

        ('P','Pending'),
        ('D','Paid'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey('Items',on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    payment = models.CharField(max_length=1,choices=PAYMENT_STATUS,default='P')

    def __str__(self) -> str:
        return self.item.item_name



