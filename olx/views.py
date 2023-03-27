from django.shortcuts import render,redirect,HttpResponse
from olx.forms import RegistrationForm,LoginForm,UserCreationForm
from django.views.generic import View,FormView,CreateView,TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from olx.forms import ProductForm
from olx.models import Products


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class IndexView(ListView):
    template_name="index.html"
    context_object_name="products"
    model=Products



class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})


class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")
    def form_valid(self, form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)


class UserProfileView(CreateView):
    template_name="user-profile.html"
    form_class=UserCreationForm
    success_url=reverse_lazy("signin")
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"profile has been created")
        return super().form_valid(form)

@login_required(login_url='login')
def Edit_profile(request):
    name=request.user
    form = UserCreationForm(instance=name)
    if request.method == 'POST':
        form=UserCreationForm(request.POST,request.FILES,instance=name)
        if form.is_valid():
            form.save()
            username= request.user.username
            messages.info(request,f'{username}, your profile has been updated')
            return redirect('user-profile.html')

    context={'form':form}


    return render(request,'index.html',context)




class ProductCreateView(CreateView):
    template_name="product-add.html"
    form_class=ProductForm
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Product has been added")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"couldn't add product")
        return super().form_invalid(form)
        

    


class ProductDetailView(DetailView):
    template_name="product-detail.html"
    context_object_name="product"
    pk_url_kwarg="id"
    model=Products


def logout_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logged out")
    return redirect("signin")




 





    




    


