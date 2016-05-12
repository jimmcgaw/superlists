from django.shortcuts import render

from .models import Item

# Create your views here.
def home_page(request):
  if request.method == 'POST':
    new_item_text = request.POST.get('item_text', '')
    if len(new_item_text) > 0:
      new_item = Item(text=new_item_text)
      new_item.save()
  items = Item.objects.all().order_by('id')
  return render(request, 'index.html', locals())
