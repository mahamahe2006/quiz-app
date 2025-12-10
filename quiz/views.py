from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Category, Question, Choice, Result
import random

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()      # create user
            login(request, user)    # auto login after signup
            return redirect('dashboard')  # go directly to dashboard
    else:
        form = UserCreationForm()

    return render(request, 'quiz/signup.html', {'form': form})


@login_required
def dashboard(request):
    categories = Category.objects.all()
    results = Result.objects.filter(user=request.user).order_by('-taken_at')[:5]
    return render(request, 'quiz/dashboard.html', {'categories': categories, 'results': results})

@login_required
def start_quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return redirect('quiz_view', category_id=category.id)

@login_required
def quiz_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions_qs = list(category.questions.all())
    total = min(10, len(questions_qs))
    selected = random.sample(questions_qs, total) if total > 0 else []

    if request.method == 'POST':
        score = 0
        for q in selected:
            choice_id = request.POST.get(str(q.id))
            if choice_id:
                choice = Choice.objects.filter(id=choice_id).first()
                if choice and choice.is_correct:
                    score += 1

        result = Result.objects.create(
            user=request.user,
            category=category,
            score=score,
            total=total
        )
        return redirect('result_view', result_id=result.id)

    return render(request, 'quiz/quiz.html', {
        'category': category,
        'questions': selected,
        'total': total
    })

@login_required
def result_view(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    return render(request, 'quiz/result.html', {'result': result})
