from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import CalorieLog
from .forms import CalorieForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


@login_required(login_url='login')

def tracker_dashboard(request, update_id=None):
    # Fetch data for display (Same as your Admin list)
    today_logs = CalorieLog.objects.filter(user=request.user, date=date.today()).order_by('-id')
    all_history = CalorieLog.objects.filter(user=request.user).order_by('-date', '-id')

    # Handle the "ADD" and "UPDATE" Actions
    instance = get_object_or_404(CalorieLog, id=update_id, user=request.user) if update_id else None
    
    if request.method == 'POST':
        form = CalorieForm(request.POST, instance=instance)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.user = request.user # This links the food to your account
            new_log.save()             # This sends it to the Admin table
            return redirect('dashboard')
    else:
        form = CalorieForm(instance=instance)

    return render(request, 'health/home.html', {
        'logs': today_logs,
        'history': all_history,
        'form': form,
        'editing': instance
    })

@login_required
def delete_log(request, pk):
    get_object_or_404(CalorieLog, pk=pk, user=request.user).delete()
    return redirect('dashboard')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'health/signup.html', {'form': form})

