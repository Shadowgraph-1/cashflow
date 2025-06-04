from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Record
from directories.models import Status, Type, Category, Subcategory
from datetime import datetime



@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def index(request):
    records = Record.objects.all()
    statuses = Status.objects.all()
    types = Type.objects.all()

    # Фильтры
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')

    if date_from:
        records = records.filter(date__gte=date_from)
    if date_to:
        records = records.filter(date__lte=date_to)
    if status_id:
        records = records.filter(status_id=status_id)
    if type_id:
        records = records.filter(type_id=type_id)

    return render(request, 'records/index.html', {
        'records': records,
        'statuses': statuses,
        'types': types,
    })

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def add_record(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        status_id = request.POST.get('status')
        type_id = request.POST.get('type')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        # Валидация
        if not (date and status_id and type_id and category_id and amount):
            return render(request, 'records/add_record.html', {
                'error': 'Все обязательные поля должны быть заполнены!',
                'statuses': Status.objects.all(),
                'types': Type.objects.all(),
                'categories': Category.objects.all(),
                'today': datetime.now().strftime('%Y-%m-%d'),
            })

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Сумма должна быть больше 0!")
        except ValueError as e:
            return render(request, 'records/add_record.html', {
                'error': str(e),
                'statuses': Status.objects.all(),
                'types': Type.objects.all(),
                'categories': Category.objects.all(),
                'today': datetime.now().strftime('%Y-%m-%d'),
            })

        # Проверка зависимостей
        category = get_object_or_404(Category, id=category_id)
        if category.type_id != int(type_id):
            return render(request, 'records/add_record.html', {
                'error': 'Категория не соответствует типу!',
                'statuses': Status.objects.all(),
                'types': Type.objects.all(),
                'categories': Category.objects.all(),
                'today': datetime.now().strftime('%Y-%m-%d'),
            })

        if subcategory_id:
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            if subcategory.category_id != int(category_id):
                return render(request, 'records/add_record.html', {
                    'error': 'Подкатегория не соответствует категории!',
                    'statuses': Status.objects.all(),
                    'types': Type.objects.all(),
                    'categories': Category.objects.all(),
                    'today': datetime.now().strftime('%Y-%m-%d'),
                })
        else:
            subcategory = None

        # Создание записи
        Record.objects.create(
            date=date,
            status_id=status_id,
            type_id=type_id,
            category_id=category_id,
            subcategory=subcategory,
            amount=amount,
            comment=comment
        )
        return redirect('index')

    return render(request, 'records/add_record.html', {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'today': datetime.now().strftime('%Y-%m-%d'),
    })

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def edit_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        status_id = request.POST.get('status')
        type_id = request.POST.get('type')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        # Валидация
        if not (date and status_id and type_id and category_id and amount):
            return render(request, 'records/edit_record.html', {
                'error': 'Все обязательные поля должны быть заполнены!',
                'record': record,
                'statuses': Status.objects.all(),
                'types': Type.objects.all(),
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.filter(category_id=category_id),
            })

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Сумма должна быть больше 0!")
        except ValueError as e:
            return render(request, 'records/edit_record.html', {
                'error': str(e),
                'record': record,
                'statuses': Status.objects.all(),
                'types': Type.objects.all(),
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.filter(category_id=category_id),
            })

        # Проверка зависимостей
        category = get_object_or_404(Category, id=category_id)
        if category.type_id != int(type_id):
            return render(request, 'records/edit_record.html', {
                'error': 'Категория не соответствует типу!',
                'record': record,
                'statuses': Status.objects.all(),
                'types': Type.objects.all(),
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.filter(category_id=category_id),
            })

        if subcategory_id:
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            if subcategory.category_id != int(category_id):
                return render(request, 'records/edit_record.html', {
                    'error': 'Подкатегория не соответствует категории!',
                    'record': record,
                    'statuses': Status.objects.all(),
                    'types': Type.objects.all(),
                    'categories': Category.objects.all(),
                    'subcategories': Subcategory.objects.filter(category_id=category_id),
                })
        else:
            subcategory = None

        # Обновление записи
        record.date = date
        record.status_id = status_id
        record.type_id = type_id
        record.category_id = category_id
        record.subcategory = subcategory
        record.amount = amount
        record.comment = comment
        record.save()
        return redirect('index')

    return render(request, 'records/edit_record.html', {
        'record': record,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.filter(category_id=record.category.id),
    })

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def delete_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    record.delete()
    return redirect('index')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def manage_directories(request):
    return render(request, 'records/manage_directories.html', {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    })

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def add_status(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Status.objects.create(name=name)
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def delete_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    status.delete()
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def add_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Type.objects.create(name=name)
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def delete_type(request, type_id):
    type_obj = get_object_or_404(Type, id=type_id)
    type_obj.delete()
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type_id = request.POST.get('type')
        if name and type_id:
            Category.objects.create(name=name, type_id=type_id)
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def add_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            Subcategory.objects.create(name=name, category_id=category_id)
    return redirect('manage_directories')

@login_required(login_url='/admin/login/?next=/add/?refresh=1')
def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    subcategory.delete()
    return redirect('manage_directories')

