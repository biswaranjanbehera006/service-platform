from django.shortcuts import render
from .models import Service, Category

def home(request):
    services = Service.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        services = services.filter(name__icontains=query)

    if category_id:
        services = services.filter(category_id=category_id)

    return render(request, 'services/home.html', {
        'services': services,
        'categories': categories
    })