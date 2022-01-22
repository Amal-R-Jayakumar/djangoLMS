from django import forms
from django.core.checks.messages import Error
from django.http import response
from ask_an_expert.forms import AskQuestionForm, NewResponseForm
from django.shortcuts import render
from .models import Question, Response
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


@login_required
def q_and_a(request):
    if request.user.user_type == 1:
        questions = Question.objects.filter(author=request.user).order_by('-asked_at')
    else:
        questions = Question.objects.all().order_by('-asked_at')
    context = {
        'title': 'IT Kerala | Q and A',
        'questions': questions,
    }
    return render(request, 'ask_an_expert/q_and_a.html', context)

@login_required
def ask_a_question(request):
    form = AskQuestionForm()
    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            user = request.user
            category = form.cleaned_data.get('category')
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            if Question.objects.filter(title=title).filter(category=category).filter(author=user):
                form.add_error(
                    error='This question was already asked by you.', field='title')
            else:
                Question.objects.create(
                    author=user, title=title, category=category, body=body)
                return redirect('ask_an_expert:q_and_a')
        # print(f'\n{user}\n{category}\n{title}\n{body}\n')
    context = {'title': 'IT Kerala | Ask our Experts', 'form': form}
    return render(request, 'ask_an_expert/ask.html', context)

@login_required
def answer_a_question(request, id):
    form = NewResponseForm()
    question = get_object_or_404(Question, id=id)
    responses =  Response.objects.filter(question=question).order_by('asked_at')
    context = {'title': 'IT Kerala | Ask our Experts', 'form': form, 'question': question,'responses':responses}
    if request.method == 'POST':
        form = NewResponseForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            parent = None
            user = request.user
            question = question
            Response.objects.create(user=user,question=question,parent=parent,body=body)
            return redirect('ask_an_expert:answer',id)
    return render(request, 'ask_an_expert/answer.html', context)
