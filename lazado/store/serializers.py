from rest_framework import serializers
from decimal import Decimal
from lazado.store.models import Address, Items, LookupItemType, Order, Review, Customer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

#LookupItem serializer
class LookupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupItemType
        fields = ['id','title']

#Item serializer
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id','item_name','item_price','price_with_tax','item_type','item_type_name']


    
    item_type = serializers.PrimaryKeyRelatedField(queryset= LookupItemType.objects.all())
    item_type_name = serializers.StringRelatedField(source='item_type')
    # item_type = LookupItemSerializer()
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, item:Items):
        return item.item_price * Decimal(1.1)


#Review serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description','item']

#Order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','item','customer','payment']

        # item = serializers.PrimaryKeyRelatedField(queryset= Items.objects.all())
        # customer = serializers.PrimaryKeyRelatedField(queryset= Customer.objects.all())

#UserCreate serializer
# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ['id','username','password','email','first_name','last_name']

#Address serializer
class AddressSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Address
        fields =['id','postcode','city','state','address']



#Customer serializer
class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        
        model = Customer
        fields = ['age','user_id']

   
    
   

#Customer serializer
# class CustomerSerializer(serializers.ModelSerializer):

#     user_id = serializers.IntegerField(read_only=True)
#     class Meta:
        
#         model = Customer
#         fields = ['age','address','user_id']

#     address = AddressSerializer()
#     print(user_id,'useriddd')
#     def create(self, validated_data):
#         print(self.customer,'selfff')
        
#         addvalue = validated_data['address']
#         address = Address(
#             postcode= addvalue['postcode'],
#             city= addvalue['city'],
#             state= addvalue['state'],
#             address= addvalue['address']
#         )
#         address.save()
#         users = User.objects.get(pk=self.user_id)
#         addid = Address.objects.latest('id')
#         customer = Customer(
#             age = validated_data['age'],
#             address = addid,
#             user = users
#         )
#         customer.save()
#         return customer
    
#     def update(self, instance, validated_data):
        
#         addvalue = validated_data['address']
#         address = Address(
#             postcode= addvalue['postcode'],
#             city= addvalue['city'],
#             state= addvalue['state'],
#             address= addvalue['address']
#         )
#         address.save()
#         users = User.objects.get(pk=self.user_id)
#         addid = Address.objects.latest('id')
#         customer = Customer(
#             age = validated_data['age'],
#             address = addid,
#             user = users
#         )
#         customer.save()
#         return instance      
        
        