from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, CustomPasswordChangeForm
from django.contrib import messages
from shop.models import Order, Product
from homepage.models import Category, Artwork
from homepage.models import Artwork
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

# Create your views here.

User = get_user_model()
# for login
# cleaned code from the previous 
@login_required
def home(request):
    return render(request, "homepage/gallery.html", {})

def landing(request):
    return render(request, "landing.html", {})

def aboutUs(request):
    return render(request, "about.html", {})

@login_required
def profile_settings(request):
    return render(request, "profile-settings.html", {})

@login_required
def userProfile(request):
    if request.user.is_staff:
        return render(request, "admin-profile.html", {})
    else:
        products = Product.objects.filter(user=request.user)
        artworks = Artwork.objects.filter(user=request.user)
        return render(request, "home.html", {'products': products, 'artworks': artworks})

@login_required
def viewHoneycomb(request):
    return render(request, 'honeycomb/honey-comb-main.html', {})

@login_required
def viewOrderTrack(request):
    user = request.user
    pk = request.user.id
    order = Order.objects.get(id = pk)

    context = {
        'order': order,
        'order_items': order.orderitem_set.all(),
        'total_price': order.get_cart_total,
        'total_items': order.get_cart_items(),
    }

    return render(request, 'honeycomb/order-track.html', context)

@login_required
def deactivate_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        from django.contrib.auth import logout
        logout(request)
        return redirect('/')
    return render(request, 'profile-settings.html')

# for authorization
def authView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                # username already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken. Please choose another one.')
                else:
                    # create user if username is not taken
                    user = User.objects.create_user(
                        username = username,
                        email = email,
                        first_name = firstname,
                        last_name = lastname,
                        password = password # will not be hashed
                    )
                    user.save()

                # if registration is a success.
                # redirects to login page
                messages.success(request, 'Profile registered successfully! You can now log in')
                return redirect("login")
            else:
                messages.error(request, 'Passwords do not match!')
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('landing')
        else:
            print(form.errors)  # Debugging the form errors
            messages.error(request, "Password Too Common")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("User is not admin")
    else:
        users = User.object.all()
        categories = Category.objects.all()
        artworks = Artwork.objects.all()
        orders = Order.objects.all()

        # Pass data to template
        context = {
            'users': users,
            'categories': categories,
            'artworks': artworks,
            'orders':orders,
        }

        return render(request, 'honeycomb/admin-profile.html')