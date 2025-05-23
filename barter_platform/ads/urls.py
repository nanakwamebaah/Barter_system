from django.urls import path
from . import views

urlpatterns = [
    path('ads/', views.ad_list, name='ad_list'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposals/create/', views.create_exchange_proposal, name='create_proposal'),
    path('proposals/<int:proposal_id>/',views.proposal_detail,name='proposal_detail'),
    path('proposals/<int:proposal_id>/update/', views.update_exchange_proposal, name='update_proposal'),
    path('signup/', views.signup_view, name='signup'),
]
