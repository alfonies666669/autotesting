from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpRequest, Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from testing.forms import TestUserForm, TestAdminForm
from django.contrib import messages
from testing.models import TestAdmin, TestUser

def get_username_str(request):
    current_user = request.user
    created_by_usr = current_user.username
    return str(created_by_usr)

def index(request):
    context = {
    'title':'Home',
    'year':datetime.now().year
    }
    assert isinstance(request, HttpRequest)
    return render(request, "index.html", context)

def about(request):
    context = {
    'title':'About',
    'year':datetime.now().year
    }
    assert isinstance(request, HttpRequest)
    return render(request, "about.html", context)

def contact(request):
    context = {
    'title':'Contact',
    'year':datetime.now().year
    }
    assert isinstance(request, HttpRequest)
    return render(request, "contact.html", context)

@login_required(login_url='/accounts/login/')
def profile(request):
    context = {
    'title':'Profile',
    'year':datetime.now().year
    }
    assert isinstance(request, HttpRequest)
    return render(request, "profile.html", context)

@login_required(login_url='/accounts/login/')
def test_user(request):
    try:
        TestAdmin_LatObj = TestAdmin.objects.latest('created_at')
    except TestAdmin.DoesNotExist:
        raise Http404('No Question papers found.')

    if TestAdmin_LatObj.allow_access:
        if request.method == 'POST':
            form = TestUserForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                form.save()
                return HttpResponseRedirect('/success/')
        else:
            form = TestUserForm()
        num_of_ques_int = int(TestAdmin_LatObj.num_of_ques)
        question_paper_link = str(TestAdmin_LatObj.question_paper)
        context = {
        'question_paper_link' : question_paper_link,
        'range': range(1, num_of_ques_int+1),
        'form': form,
        'title':'Upload Answers',
        'year': datetime.now().year
        }
        assert isinstance(request, HttpRequest)
        return render(request, "test_user.html", context)
    else:
        raise Http404('No test in progress.')

@login_required(login_url='/accounts/login/')
def test_admin(request):
    current_user = request.user
    created_by_usr = current_user.username

    if 'admin' in created_by_usr:
        if request.method == 'POST':
            form = TestAdminForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                # instance = form.save(commit=False)
                form.created_by = request.user
                form.save()
                return HttpResponseRedirect('/success/')
        else:
            form = TestAdminForm()
        context = {
        'created_by_usr' : created_by_usr,
        'form': form,
        'title':'Create Test',
        'year': datetime.now().year
        }
        #assert isinstance(request, HttpRequest)
        return render(request, "test_admin.html", context)
    else:
        raise Http404('Hard luck mate, you ain\'t got no access in here.')


@login_required(login_url='/accounts/login/')
def success(request):
    context = {
    'title':'Success',
    'year':datetime.now().year
    }
    assert isinstance(request, HttpRequest)
    return render(request, "success.html", context)
