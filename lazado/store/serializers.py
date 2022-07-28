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
        fields = ['item','customer','payment']

        item = serializers.PrimaryKeyRelatedField(queryset= Items.objects.all())
        customer = serializers.PrimaryKeyRelatedField(queryset= Customer.objects.all())

#UserCreate serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','password','email','first_name','last_name']

#Address serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields =['id','postcode','city','state','address']



#Customer serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['age','address']

    address = AddressSerializer()

    def create(self, validated_data):
        print(User,'sini')
        addvalue = validated_data['address']
        address = Address(
            postcode= addvalue['postcode'],
            city= addvalue['city'],
            state= addvalue['state'],
            address= addvalue['address']
        )
        address.save()
        addid = Address.objects.latest('id')
        customer = Customer(
            age = validated_data['age'],
            address = addid,
            user = User.id
        )
        customer.save()
        pass