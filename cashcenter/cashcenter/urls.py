from django.contrib import admin
from django.urls import path
from directories.views import get_subcategories
from records.views import index, add_record, edit_record, delete_record, manage_directories, add_status, delete_status, add_type, delete_type, add_category, delete_category, add_subcategory, delete_subcategory


urlpatterns = [
    path('', index, name='index'),
    path('add/', add_record, name='add_record'),
    path('edit/<int:record_id>/', edit_record, name='edit_record'),
    path('delete/<int:record_id>/', delete_record, name='delete_record'),
    path('directories/', manage_directories, name='manage_directories'),
    path('directories/add_status/', add_status, name='add_status'),
    path('directories/delete_status/<int:status_id>/', delete_status, name='delete_status'),
    path('directories/add_type/', add_type, name='add_type'),
    path('directories/delete_type/<int:type_id>/', delete_type, name='delete_type'),
    path('directories/add_category/', add_category, name='add_category'),
    path('directories/delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('directories/add_subcategory/', add_subcategory, name='add_subcategory'),
    path('directories/delete_subcategory/<int:subcategory_id>/', delete_subcategory, name='delete_subcategory'),
    path('admin/get_subcategories/', get_subcategories, name='get_subcategories'),  # Новый маршрут
    path('admin/', admin.site.urls),  # Админка идёт после
]