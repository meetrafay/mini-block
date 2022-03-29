from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UsernameField
from django.http import request
from django.shortcuts import redirect, render , HttpResponseRedirect
from .forms import SignUpForm , loginForm ,Postform
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
#homepage
def home(request):
    
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})


#aboutpage
def about(request):
    
    return render(request, 'blog/about.html')

#contactpage
def contact(request):
    
    return render(request, 'blog/contact.html')

#dasboardpage
def dashboard(request):
    if request.user.is_authenticated:
     posts = Post.objects.all()
     user = request.user
     full_name = user.get_full_name()
     gps = user.groups.all()
     return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name , 'groups':gps} )
    else:
        return HttpResponseRedirect('/login/')
#logoutpage
def logout_user(request):
    logout(request)
    return redirect('/')

#loginpage
def login_user(request):
    
    if not request.user.is_authenticated:
     if request.method == "POST":
        
        form = loginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,'you are login successfully')
                return HttpResponseRedirect('/dashboard')
        
     else:
            
         form = loginForm()
     return render(request, 'blog/login.html',{'form':form})
    else:
        
        return HttpResponseRedirect("/dashboard")
#signinpage
def signin_user(request):
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'you are now author')
            user = form.save()
            group = Group.objects.get(name = 'Author')
            user.group.add(group)
        form = SignUpForm()
    else:
     form = SignUpForm()
    return render(request, 'blog/sigup.html', {'form':form} )



def add_post(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
         form = Postform(request.POST)
         if form.is_valid():
             title = form.cleaned_data['title']
             desc = form.cleaned_data['desc']
             pst = Post(title=title,desc=desc)
             pst.save()
             form = Postform()
        else:
            form = Postform()
        return render(request, 'blog/addpost.html',{'form':form})
    
    else:
    
     return HttpResponseRedirect('/login/')
        
        

def edit_post(request,id):
    
    if request.user.is_authenticated:
        
        if request.method  == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST , instance=pi)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
            
        
        return render(request, 'blog/edit.html',{'form':form})
    
    else:
    
     return HttpResponseRedirect('/login/')




def delete_post(request,id):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    
    else:
    
     return HttpResponseRedirect('/login/')
                