from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from yaml import serialize
from lazado.store.models import Items
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Items, Review, Order, Customer, Address
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,UpdateModelMixin
from .serializers import AddressSerializer, CustomerSerializer, ItemSerializer, OrderSerializer, ReviewSerializer
from rest_framework.views import APIView

# Create your views here.


def item_mainpage(request):
    return render(request, "item/item_mainpage.html")

def get_all_item(request):
    query_set = Items.objects.all()

    for items in query_set:
        print(items)
    return render(request, "item/item_mainpage.html")

#creating api using drf
#view all record 
@api_view()
def list_item(request):
    queryset = Items.objects.all()
    serializer = ItemSerializer(queryset,many=True)
    return Response(serializer.data)

#view record per id
@api_view()
def item_details(request, id):

    item = get_object_or_404(Items,pk=id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

#deserilaztion
 #create record
@api_view(['GET','POST'])
def list_item_des(request):
    if request.method == 'GET':
        queryset = Items.objects.all()
        serializer = ItemSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#update/delete record 
@api_view(['GET','PUT','PATCH','DELETE'])
def item_details_update(request, id):
    item = get_object_or_404(Items,pk=id)
    if request.method == 'GET':      
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Class-based view

class ItemDetails(APIView):
    def get(self,request,id):
        item = get_object_or_404(Items,pk=id) 
        queryset = Items.objects.all()
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    def post(self,request,id):
        item = get_object_or_404(Items,pk=id) 
        serializer = ItemSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def put(self,request,id):
        item = get_object_or_404(Items,pk=id) 
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#generic-view
    #create/list gv
class ItemDetailsViewGV(ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemSerializer

    #list/delete/update gv
class ItemDetailsGV(RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemSerializer
    def delete(self,request,pk):
        item = get_object_or_404(Items,pk=pk) 
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#item viewset
class ItemViewSet(ModelViewSet):
    
    queryset = Items.objects.all()
    serializer_class = ItemSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#item viewset with filter
class ItemFilterViewSet(ModelViewSet):
    
    queryset = Items.objects.all()
    def get_queryset(self):
        queryset = Items.objects.all()
        item_type_id = self.request.query_params.get('item_type_id')
        if item_type_id is not None:
          queryset =  queryset.filter(item_type_id=item_type_id)
          return queryset

    serializer_class = ItemSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#order viewset
class OrderViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        print(request.user.id , '---')
        print(request , '---')

        customer = Customer.objects.get(user_id=request.user.id)
        order = Order.objects.filter(customer = customer)

        if request.method == 'GET':
            serializer = OrderSerializer(order,many=True)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = OrderSerializer(order,data=request.data,many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#review viewset
class ReviewViewSet(ModelViewSet):
        queryset = Review.objects.all()
        serializer_class = ReviewSerializer

#customer viewset
class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        print(request.user , '---')
        (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

#adress viewset
class AdressViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = Address.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        
        (customer, created) = Address.objects.get_or_create(user_id = request.user.id)

        if request.method == 'GET':
            serializer = AddressSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AddressSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)






  

 

