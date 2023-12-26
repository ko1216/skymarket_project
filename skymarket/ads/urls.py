from django.urls import path

from ads.apps import SalesConfig

from ads.views import (AdListAPIView, AdCreateAPIView,
                       AdMyListAPIView, AdRetrieveAPIView,
                       AdPatchAPIView, AdDestroyAPIView,
                       CommentListAPIView, CommentCreateAPIView,
                       CommentRetrieveAPIView, CommentPatchAPIView,
                       CommentDestroyAPIView
                       )

app_name = SalesConfig.name

urlpatterns = [
    path('ads/', AdListAPIView.as_view(), name='ads_list'),
    path('ads/create/', AdCreateAPIView.as_view(), name='ads_create'),
    path('ads/me/', AdMyListAPIView.as_view(), name='ads_my_list'),
    path('ads/<int:pk>/', AdRetrieveAPIView.as_view(), name='ad_retrieve'),
    path('ads/update/<int:pk>/', AdPatchAPIView.as_view(), name='ad_patch'),
    path('ads/delete/<int:pk>/', AdDestroyAPIView.as_view(), name='ad_delete'),

    path('ads/<int:ad_pk>/comments/', CommentListAPIView.as_view(), name='comments'),
    path('ads/<int:ad_pk>/comments/create/', CommentCreateAPIView.as_view(), name='comments_create'),
    path('ads/<int:ad_pk>/comments/<int:com_pk>/', CommentRetrieveAPIView.as_view(), name='comments_retrieve'),
    path('ads/<int:ad_pk>/comments/update/<int:com_pk>/', CommentPatchAPIView.as_view(), name='comments_patch'),
    path('ads/<int:ad_pk>/comments/delete/<int:com_pk>/', CommentDestroyAPIView.as_view(), name='comments_delete'),
]
