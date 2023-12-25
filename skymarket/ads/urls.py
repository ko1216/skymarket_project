from django.urls import path

from ads.apps import SalesConfig

from ads.views import (AdListAPIView, AdCreateAPIView,
                       AdMyListAPIView, AdRetrieveAPIView,
                       AdPatchAPIView, AdDestroyAPIView,
                       )

app_name = SalesConfig.name

urlpatterns = [
    path('ads/', AdListAPIView.as_view(), name='ads_list'),
    path('ads/create/', AdCreateAPIView.as_view(), name='ads_create'),
    path('ads/me/', AdMyListAPIView.as_view(), name='ads_my_list'),
    path('ads/<int:pk>/', AdRetrieveAPIView.as_view(), name='ad_retrieve'),
    path('ads/update/<int:pk>/', AdPatchAPIView.as_view(), name='ad_patch'),
    path('ads/delete/<int:pk>/', AdDestroyAPIView.as_view(), name='ad_delete')

]
