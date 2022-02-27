from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.shortcuts import render, get_list_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateUserForm, LoginForm, EditUserForm


# register/login user funcs
def register_user(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password2'])
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()

            new_user.groups.add(Group.objects.get(name="Default_User"))

            loginUser = authenticate(request, username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password2'])

            if loginUser:
                login(request, loginUser)
                return HttpResponseRedirect(reverse('home_page'))
            return HttpResponseRedirect(reverse("login_user"))
    else:
        form = CreateUserForm()
    return render(request, "register.html", locals())


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            request.session["user_id"] = request.user.id
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("home_page"))
    else:
        form = LoginForm()
    return render(request, 'login.html', locals())


def logout_user(request):
    del request.session['user_id']
    logout(request)
    return HttpResponseRedirect(reverse("login_user"))


# render index.html
def render_all_users(request):
    users = User.objects.filter()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("register"))

    return render(request, 'index.html', locals())


# Managing user objects
def delete_user_view(request, id):
    if request.user.is_superuser or request.user.is_staff:
        if not User.objects.get(id=1) == User.objects.get(id=id):
            user = User.objects.filter(id=id)
            user.delete()

    return HttpResponseRedirect(reverse("home_page"))


def edit_user_view(request, id):
    form = EditUserForm()
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            edited_user = form.save(commit=False)
            edited_user.email = form.cleaned_data['email']
            edited_user.first_name = form.cleaned_data['first_name']
            edited_user.last_name = form.cleaned_data['last_name']
            edited_user.save()
            return HttpResponseRedirect(reverse('home_page'))
    return render(request, 'edit.html', locals())
