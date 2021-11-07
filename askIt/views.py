import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

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
            if content.upper().strip() == "EASTER EGG":
                return HttpResponseRedirect(reverse("secretSpy"))


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
        questions = Questions.objects.filter(askedFor = None).order_by('-id')
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


def user(request, name):

    if request.method == "POST":
        userQuestion = request.POST["userQuestion"]
        if userQuestion.isspace() or userQuestion == "":
            return HttpResponse('Your question cannot be empty !')

        askedFor = User.objects.get(username = name)

        questions = Questions(content= request.POST["userQuestion"], randomPoster = "Anonymous", askedFor = askedFor)
        questions.save()

        return HttpResponseRedirect(reverse('user', args=(name,)))

    else:

        try:
            user = User.objects.get(username = name)
        except ObjectDoesNotExist:
            user = None
            return HttpResponse('No user exists with that name!')

        answers = Answers.objects.all()
        questions = Questions.objects.filter(askedFor = user, id__in = answers.values_list('question', flat=True)).all()

        return render(request, "askIt/user.html", {
            "questions" : questions,
            "user" : user,
            "answers" : answers,
        })

@login_required(login_url="/login")  
def access(request, name):

    if request.method == "POST":
        answerContent = request.POST["answerContent"]
        if answerContent.isspace() or answerContent == "":
            return HttpResponse('Your answer cannot be empty!')

        questionId = request.POST["question-id"]
        questions = Questions.objects.get(id = questionId)

        answers = Answers(question= questions ,content=answerContent, answerPoster = request.user)
        answers.save()
        Questions.objects.filter(id = questionId).update(answered = True)
        return HttpResponseRedirect(reverse('access', args=(name,)))

    else:

        try:
            user = User.objects.get(username = name)
        except ObjectDoesNotExist:
            user = None
            return HttpResponse('No user exists with that name!')

        if request.user != user:
            print(request.user)
            print(user)
            return HttpResponse("You need to be logged in as that user to access!")

        questions = Questions.objects.filter(askedFor = user, answered = False).order_by('-id')
        answers = Answers.objects.all()

        return render(request, "askIt/access.html", {
            "questions" : questions,
            "user" : user,
            "answers" : answers,
        })

@login_required(login_url="/login")  
def secretSpy(request):
    return render(request, "askIt/secretSpy.html")

@login_required(login_url="/login")  
def secretSpyOne(request):
    return render(request, "askIt/secretSpyOne.html")

@login_required(login_url="/login")  
def secretSpyTwo(request):
    return render(request, "askIt/secretSpyTwo.html")

@login_required(login_url="/login")      
def secretSpyThree(request):
    return render(request, "askIt/secretSpyThree.html")

@login_required(login_url="/login")  
def secretSpyThreeAlt(request):
    return HttpResponseRedirect(reverse('secretSpyThree'))

@login_required(login_url="/login")  
def secretSpyFour(request):
    return render(request, "askIt/secretSpyFour.html")

@login_required(login_url="/login")  
def secretSpyFinal(request):
    return render(request, "askIt/secretSpyFinal.html")