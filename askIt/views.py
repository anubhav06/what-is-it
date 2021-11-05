import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Answers, User, Questions

# Create your views here.


def index(request):
    
    if request.method == "POST":

        if request.user is None:
            return HttpResponse('User not logged in !')
        
        if request.POST.get("content"):
            content = request.POST["content"]
            if content.isspace() or content == "":
                return HttpResponse('You cannot ask an empty question !')

            questions = Questions(content= request.POST["content"], randomPoster = "Anonymous")
            questions.save()
        
        else:
            answerContent = request.POST["answerContent"]
            if answerContent.isspace() or answerContent == "":
                return HttpResponse('Your answer cannot be empty!')

            questionId = request.POST["question-id"]
            questions = Questions.objects.get(id = questionId)

            answers = Answers(question= questions ,content=answerContent, randomPoster = "Anonymous")
            answers.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        questions = Questions.objects.all()
        answers = Answers.objects.all()

        return render(request, "askIt/index.html", {
            "questions" : questions,
            "answers" : answers,
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "askIt/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "askIt/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "askIt/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "askIt/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "askIt/register.html")
