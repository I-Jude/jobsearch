from django.shortcuts import render
from .forms import RegisterForm , LoginForm , UserProfileEditForm ,OpportunityForm
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required , user_passes_test
from .models import Opportunity , AppliedJob ,user_table
from django.contrib import messages
from django import template
from django.db.models import Q


def logout_view(request):
    logout(request)
    return redirect('login_1')

def register_view(request):
    return render(request, 'register.html')

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_1')
            
    else:
        form = RegisterForm()
    print(form)
    return render(request, 'register.html', {'form': form})

def login_1(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            print("Login successful")
            if user.is_superuser:
                return redirect('manage_users')  
            else:
                return redirect('opportunity_list')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def user_profile_edit(request):
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileEditForm(instance=request.user)
    
    return render(request, 'user_profile_edit.html', {'form': form}) 

@login_required
def user_profile(request):
    user=request.user
    return render(request, 'user_profile.html', {'user': user})




def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def manage_opportunities(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_opportunities')
    else:
        form = OpportunityForm()

    # Get search and filter parameters from the GET request
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')

    # Start with all opportunities
    opportunities = Opportunity.objects.all()

    # Apply search filter
    if search_query:
        opportunities = opportunities.filter(
        Q(domain__icontains=search_query) | Q(title__icontains=search_query)
    )

    # Apply type filter
    if type_filter:
        opportunities = opportunities.filter(type=type_filter)

    return render(request, 'manage_opportunities.html', {
        'form': form,
        'opportunities': opportunities
    })

@superuser_required(login_url='login')
def edit_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, request.FILES, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect('manage_opportunities')
    else:
        form = OpportunityForm(instance=opportunity)
    
    return render(request, 'edit_opportunity.html', {'form': form})

@superuser_required(login_url='login')
def delete_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        opportunity.delete()
        return redirect('manage_opportunities')
    return render(request, 'confirm_delete.html', {'opportunity': opportunity})

def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def manage_users(request):
    users = user_table.objects.exclude(is_superuser=True)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id:
            try:
                user_to_update = user_table.objects.get(id=user_id)

                if action == 'deactivate':
                    user_to_update.is_active = False
                    user_to_update.save()
                    messages.success(request, 'User marked as inactive successfully.')
                elif action == 'activate':
                    user_to_update.is_active = True
                    user_to_update.save()
                    messages.success(request, 'User activated successfully.')

            except user_table.DoesNotExist:
                messages.error(request, 'User does not exist.')

        return redirect('manage_users')

    return render(request, 'manage_users.html', {'users': users})

def opportunity_list(request):
    jobs = Opportunity.objects.filter(type='job')
    internships = Opportunity.objects.filter(type='internship')
    return render(request, 'opportunity_list.html', {'jobs': jobs, 'internships': internships})


@login_required
def apply_opportunity(request):
    if request.method == 'POST':
        opportunity_id = request.POST.get('opportunity_id')
        opportunity = get_object_or_404(Opportunity, id=opportunity_id)
        if not AppliedJob.objects.filter(user=request.user, opportunity=opportunity).exists():
            AppliedJob.objects.create(user=request.user, opportunity=opportunity)
    return redirect('opportunity_list')


@login_required
def user_applications(request):
    user = request.user
    applied_jobs = AppliedJob.objects.filter(user=user)
    return render(request, 'user_applications.html', {'applied_jobs': applied_jobs})