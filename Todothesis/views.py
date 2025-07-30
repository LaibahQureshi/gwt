from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import ProgressUpdate, GoalSetting, SubCategory
from .forms import RegisterForm, ProgressUpdateForm, FeedbackForm, SubCategoryForm


def create_subcategory(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            subcat = form.save(commit=False)
            subcat.user = request.user
            subcat.save()
            return redirect('dashboard')
    else:
        form = SubCategoryForm()
    return render(request, 'Todothesis/create_subcategory.html', {'form': form})


@login_required
def delete_update(request, update_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    update = get_object_or_404(ProgressUpdate, id=update_id, user=request.user)
    update.delete()
    return redirect('dashboard')


@staff_member_required
def all_progress_view(request):
    all_updates = ProgressUpdate.objects.select_related('user', 'category').order_by('-timestamp')
    
    if request.method == 'POST':
        update_id = request.POST.get('update_id')
        feedback_text = request.POST.get('feedback')
        try:
            update = ProgressUpdate.objects.get(id=update_id)
            update.feedback = feedback_text
            update.save()
        except ProgressUpdate.DoesNotExist:
            pass
        return redirect('all_progress')

    return render(request, 'Todothesis/all_progress.html', {'updates': all_updates})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'Todothesis/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'Todothesis/login.html', {'error': 'Invalid credentials'})
    return render(request, 'Todothesis/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())

    # Get progress updates from the current week
    weekly_updates = ProgressUpdate.objects.filter(user=user, timestamp__gte=week_start)

    # Handle goal setting via POST
    current_goal = GoalSetting.objects.filter(user=user).first()
    if request.method == 'POST':
        goal_val = int(request.POST.get('goal', 0))
        if current_goal:
            current_goal.value = goal_val
            current_goal.save()
        else:
            GoalSetting.objects.create(user=user, value=goal_val)
        return redirect('dashboard')

    # Prepare calendar data: count progress entries per date in the week
    calendar_data = {}
    for update in weekly_updates:
        date_str = update.timestamp.date().isoformat()
        calendar_data[date_str] = calendar_data.get(date_str, 0) + 1

    # Get all updates by user ordered by timestamp descending
    updates = ProgressUpdate.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'Todothesis/dashboard.html', {
        'calendar_data': calendar_data,
        'updates': updates,
        'weekly_updates_count': weekly_updates.count(),
        'current_goal': current_goal.value if current_goal else 0,
    })


def submit_view(request):
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.save()
            return redirect('dashboard')
    else:
        form = ProgressUpdateForm()
    return render(request, 'Todothesis/submit.html', {'form': form})
@login_required
def set_goal(request):
    if request.method == 'POST':
        goal_val = int(request.POST.get('goal', 0))
        current_goal = GoalSetting.objects.filter(user=request.user).first()
        if current_goal:
            current_goal.value = goal_val
            current_goal.save()
        else:
            GoalSetting.objects.create(user=request.user, value=goal_val)
    return redirect('dashboard')
