from cgitb import lookup
from email.mime import base
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

app_name = "store"

#router 
router = routers.DefaultRouter()
router.register('allitems',views.ItemViewSet)
router.register('items',views.ItemFilterViewSet, basename='items')
router.register('reviews',views.ReviewViewSet)
router.register('order',views.OrderViewSet)
router.register('customer',views.CustomerViewSet)

#router for items
items_router = routers.NestedDefaultRouter(router, 'items', lookup='item')
items_router.register('reviews',views.ReviewViewSet,basename='items-review')


urlpatterns = router.urls + items_router.urls

# urlpatterns = [
#     path("itemmainpage/", views.item_mainpage , name="itemmainpage"),
#     path("itemmainpageall/", views.get_all_item , name="itemmainpageall"),
#     #basic serialization/deseriliaztion
#     path("itemlist/", views.list_item ),
#     path("itemlist/<int:id>/", views.item_details ),
#     path("itemlistdes/", views.list_item_des ),
#     path("itemlistupdate/<int:id>/", views.item_details_update ),
#     #class-based view url
#     path("itemlistCB/<int:id>/", views.ItemDetails.as_view()),
#     #generic-based view url
#     path("itemlistGV/", views.ItemDetailsViewGV.as_view()),
#     path("itemlistGV/<int:pk>", views.ItemDetailsGV.as_view()),
# ]
