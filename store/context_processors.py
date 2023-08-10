from category.models import Category

def category_links(request):
    categories=Category.objects.all().order_by('-category_name')
    return dict(categories=categories)