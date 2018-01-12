from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Problem
from accounts.models import SubmittedHistory
from datetime import datetime 

#@login_required(login_url="/accounts/login/")
def index(request):
    return render(request, "problems/index.html",
                  {'user' : request.user, "problems": Problem.objects.all()}
              )

@login_required(login_url="/accounts/login/")
def detail(request, problemTitle):
    problem = get_object_or_404(Problem, title=problemTitle)
    showModalFlag = 0
    if ("showModalFlag" in request.COOKIES) and (request.COOKIES["showModalFlag"] == "correct"):
        showModalFlag = 1
    if ("showModalFlag" in request.COOKIES) and (request.COOKIES["showModalFlag"] == "fail"):
        showModalFlag = 2
    response = render(request, "problems/detail.html",
                      {'user': request.user,
                       "problem": problem,
                       "showModalFlag": showModalFlag}
                  )
    response.delete_cookie('showModalFlag')
    return response


@login_required(login_url="/accounts/login/")
def unlockHint(request, problemTitle):
    problem = get_object_or_404(Problem, title=problemTitle)
    if problem not in request.user.hintedProblems.all():
        request.user.addHintedProblems(problem)
    return HttpResponseRedirect(reverse('problems:detail',
                                        kwargs={'problemTitle':problemTitle}))

@login_required(login_url="/accounts/login/")
def submit(request, problemTitle):
    problem = get_object_or_404(Problem, title=problemTitle)
    response = HttpResponseRedirect(reverse('problems:detail',
                                            kwargs={'problemTitle':problemTitle}))
    if problem not in request.user.solvedProblems.all():
        withHint = True
        if problem not in request.user.hintedProblems.all():
            withHint = False
        if problem.flag == request.POST['flag']:
            request.user.addSolvedProblems(problem)
            request.user.lastSubmitDatetime = datetime.now()
            if not withHint:
                request.user.addNoHintedSolvedProblems(problem)
            request.user.score = request.user.score + problem.score
            request.user.save()

            if problem not in request.user.affiliate.solvedProblems.all():
                request.user.affiliate.score = request.user.affiliate.score + problem.score
                request.user.affiliate.solvedProblems.add(problem)
                request.user.affiliate.save()
            response.set_cookie("showModalFlag", "correct")
            isCorrect = True
        else:
            response.set_cookie("showModalFlag", "fail")
            isCorrect = False
        history = SubmittedHistory(user = request.user, withHint = withHint, isCorrect = isCorrect, problem=problem)
        history.save()
    return response

