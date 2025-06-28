from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('category/<slug:category_slug>/', views.AdListView.as_view(), name='ad_list_by_category'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/new/', views.AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad_edit'),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('ad/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('my-ads/', views.UserAdsListView.as_view(), name='user_ads'),
]