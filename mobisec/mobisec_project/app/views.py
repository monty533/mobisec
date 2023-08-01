from django.shortcuts import render,redirect,get_object_or_404
from .models import Friends
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import SignUpForm
from django.views import View
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
import re,json
# Create your views here.
def home(request):
    return render (request,'home.html')

def add_index(request): 
    if not request.user.is_authenticated:
            return redirect("/")
    return render(request,'add_index.html')  

@csrf_exempt
def add_friend(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        name = request.POST.get('name')
        hobby =request.POST.get('hobby')
        dob =request.POST.get('dob')
        photo = request.FILES.get('photo')
        gender =request.POST.get('gender')
        data=Friends.objects.create(
        name=name,dob=dob,photo=photo,gender=gender,hobby=hobby
        )
        data.save()
        messages.warning(request,'User has been added successfully.')
        return redirect('/')
    if request.method == 'GET':
        return JsonResponse({'status_code':'400','msg':f'{request.method} method is not allowed','title':'Bad request'})

def list_friend(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    data = Friends.objects.all()
    # print(data[0])
    # print(data.query)
    return render(request,'list.html',context={"data":data})

@csrf_exempt
def search_user(request):
    name = request.GET.get('name')
    if not request.user.is_authenticated or name == None:
        return redirect("/")
    data = Friends.objects.filter(name__icontains=name)[:10]
    user_list = serializers.serialize('python', data)
    return JsonResponse(user_list, safe=False) 

@login_required
def update_user(request):
    data = Friends.objects.all()
    return render(request,'update_search.html',context={"data":data})

@csrf_exempt
def update(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'GET':
        id = request.GET.get('friend_id')
        if id is None:
            return redirect('/')
        data = Friends.objects.get(id=id)
        return render(request,'update.html',context={"data":data})

    if request.method == 'POST':
        id = request.POST.get('id')
        data = Friends.objects.get(id=id)
        data.name = request.POST.get('name')
        data.hobby = request.POST.get('hobby')
        data.dob = request.POST.get('dob')
        data.photo = request.FILES.get('upload_photo')
        data.gender = request.POST.get('gender')
    
        data.save()
        messages.warning(request,'Updated Succesfully')
        return redirect('/')

@csrf_exempt
# @login_required
def delete_user(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        id = request.POST.get('id')
        user = Friends.objects.get(id=id)
        user.delete()
        return render(request,'list.html') 

    else:
        return JsonResponse({'status_code':'400','msg':f'{request.method} method is not allowed','title':'Bad request'})


@csrf_exempt
# @login_required
def total_sum(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        numbers = data['input']
        total_sum = 0
        for i in numbers:
            for k, v in i.items():
                total_sum += v
        return JsonResponse({'sum': total_sum})
    else:
        return JsonResponse({'status_code':'400','msg':f'{request.method} method is not allowed','title':'Bad request'})

@login_required
def calculator(request):
    return render(request, 'calculator.html')


class LoginUser(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request,'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password =  request.POST.get('password')
        if (not email) or (not password):
            return render(request,'login.html',{'error':'Both the fields are required'})
        if email:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email):
                pass
            else:
                return render(request, 'login.html', {'error': 'Invalid email address'})
        user = authenticate(username=email.strip(), password=password)
        if user is None:
            return render(request, 'login.html', {'error': 'Your Email or Password is incorrect'})
        if not user.is_active:
            return render(request, 'login.html', {'error': 'Your account has disabled'})
        messages.success(request,'You are successfully logged in.')
        login(request, user)
        return redirect("/")
    
class RegisterUser(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        form = SignUpForm()
        return render(request,'register.html',{'form': form})

    def post(self,request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'You are successfully Registered.')
            return redirect('/login/')
        return render(request,'register.html',{'form': form})

@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login/')