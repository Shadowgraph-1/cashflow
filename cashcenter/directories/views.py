from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Subcategory

@staff_member_required
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)