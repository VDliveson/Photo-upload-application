from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ImageUploadForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UploadedImage


# Create your views here.

def views_signup(request):
    if(request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')
        else:
            print("Form is not valid. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
                    messages.add_message(request, messages.ERROR,error)
            

    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def views_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.add_message(request, messages.SUCCESS,'User logged in successfully')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/app/login')
def views_logout(request):
    logout(request)
    messages.add_message(request, messages.WARNING,'User logged out successfully')
    return redirect('login')

@login_required(login_url='/app/login')
def home(request):
    uploaded_images = UploadedImage.objects.filter(user=request.user)
    image_paths = [uploaded_image.image.path for uploaded_image in uploaded_images]
    print(image_paths)
    return render(request, 'home.html', {'uploaded_images': uploaded_images})


@login_required(login_url='/app/login')
def views_upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.add_message(request, messages.SUCCESS,'Image uploaded successfully')
            return redirect('home')  # Redirect to home page after successful upload
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

