from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .forms import MenuForm
from .models import Menu, Item
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, \
    update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    PasswordChangeForm
from django.contrib.auth.decorators import login_required


def menu_list(request):
    all_menus = Menu.objects.filter(expiration_date__lte=timezone.now())\
        .order_by('expiration_date').prefetch_related('items')
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': all_menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.created_date = timezone.now()
            menu = form.save()
            print(form.cleaned_data)
            messages.success(request, "New menu created!")
            return HttpResponseRedirect(reverse('menu_detail',
                                                kwargs={'pk': menu.pk}))
    else:
        form = MenuForm()
    return render(request, 'menu/change_menu.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(data=request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu updated!")
            return HttpResponseRedirect(reverse('menu_detail',
                                                kwargs={'pk': pk}))
    return render(request, 'menu/change_menu.html', {'form': form})


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('menu_list')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'menu/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You can create and edit menus. "
            )
            return HttpResponseRedirect(reverse('menu_list'))
        else:
            print(form.errors)
    return render(request, 'menu/sign_up.html', {'form': form})


@login_required(login_url='/sign_in/')
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out.")
    return HttpResponseRedirect(reverse('menu_list'))


@login_required(login_url='/sign_in/')
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,
                             'Password changed successfully')
            return HttpResponseRedirect(reverse('menu_list'))
        else:
            messages.error(request,
                           'Password not changed')
    return render(request, 'menu/change_password.html', {'form': form})
