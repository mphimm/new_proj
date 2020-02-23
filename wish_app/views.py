import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job


# Create your views here.

def index(request):
    return render (request, "index.html")

def dashboard(request):
    context = {
            "all_jobs" : Job.objects.all(),
            # "user" : User.objects.get(request.user_id),
            "user" : User.objects.all(),

    }
    return render (request, "dashboard.html", context)


def proc_reg(request):
    errors = User.objects.new_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    
    else:
        newFirstName = request.POST["first_name"]
        newLastName = request.POST["last_name"]
        newEmail = request.POST["email"]
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print("pw has been hashed "*10)
        new_user = User.objects.create(first_name=newFirstName, last_name=newLastName, email=newEmail, password=pw_hash)
        request.session["user_id"] = new_user.id
        print("user has been submitted "*10)
        return redirect("/dashboard")

def login(request):
    if request.method != "POST":
        return redirect("/")
    valid = User.objects.login_validator(request.POST)
    if len (valid["errors"]) > 0:
        for key, value in valid ["errors"].items():
            messages.error(request,value)
        return redirect("/")
    else:
        request.session["user_id"] = valid["user"].id
        return redirect ("/dashboard")

def logout(request):
    request.session.clear()
    return redirect ("/")

def new(request):
        return render(request, "new.html")

def proc_job(request):
    errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect ("/new")
    
    else:
        print("NEW JOB HAS BEEN SUBMITTED "*10)
        temp_user = User.objects.get(id=request.session["user_id"])
        Job.objects.create(title=request.POST["title"], desc=request.POST["desc"], location=request.POST["location"], user=temp_user)
        return redirect("/dashboard")

def view(request, id):
    context = {
        "job" : Job.objects.get(id=id),
        "user" : User.objects.get(id=id),
        
        
    }
    return render(request, "view.html", context)

def edit_proc(request):
    errors = Job.objects.edit_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/edit")

    job = Job.objects.get(id=request.POST["job_id"])
    job.title = request.POST["title"]
    job.desc = request.POST["desc"]
    job.location = request.POST["location"]
    print ("job.title", job.title)
    print("job.desc",job.desc)
    job.save()
    return redirect("/dashboard")

def edit(request,id):
    context ={
        "job" : User.objects.get(id=id),
    }
    return render (request, "edit.html", context)

def remove(request,id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect("/dashboard")
 