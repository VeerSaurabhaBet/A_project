from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('employee/<int:employee_id>/assets/', views.view_assets, name='view_assets'),
    path('employee/<int:employee_id>/asset/add/', views.add_asset, name='add_asset'),
    path('asset/edit/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('asset/delete/<int:asset_id>/', views.delete_asset, name='delete_asset'),
]