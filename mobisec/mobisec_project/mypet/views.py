# Create your views here.
import requests
from django.shortcuts import render,redirect
from .models import MyPet


def mypet(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        # Fetch random cat image from the API
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        # Extract image URL from the response
        cat_image_url = data[0]['url']

        # Save cat name and image URL to the database
        cat_name = request.POST['name']
        cat = MyPet(name=cat_name, image_url=cat_image_url)
        cat.save()

    all_data = MyPet.objects.all()
    context = {'all_data': all_data}
    return render(request, 'mypet.html', context)

