from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from apps.authentication.models import UserProfile, BanHistory
from django.http import Http404

def register(request):
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to home if already logged in
        
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile automatically created by signal
            messages.success(request, 'Your account has been successfully created! Please login.')
            return redirect('authentication:login')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')  
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            
            # Check if user is banned
            if not user.is_active:
                messages.error(request, 'Your account has been banned. Please contact admin.')
                return render(request, 'login.html', {'form': form})
            
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next parameter or default page
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)
    
    context = {'form': form}
    return render(request, 'login.html', context)


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('authentication:login')

@login_required
def user_dashboard(request):
    profile = None
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    context = {
        'profile': profile,
        'threads_count': 0,  # TODO: Replace with actual count
        'votes_count': 0,    # TODO: Replace with actual count
        'comments_count': 0, # TODO: Replace with actual count
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def edit_profile(request):
    """Edit user's own profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        # Update user info
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # Update profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.bio = request.POST.get('bio', '')

         # Handle nationality - now expects country code or empty string
        nationality_code = request.POST.get('nationality', '')
        if nationality_code:  # Only set if a country was selected
            profile.nationality = nationality_code
        else:
            profile.nationality = None  # Set to None/blank if not selected
        profile.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('authentication:user_dashboard')
    
    return render(request, 'edit_profile.html', {'profile': profile})

# Admin Views
@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def manage_users(request):
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'banned_users': users.filter(is_active=False).count(),
    }
    return render(request, 'manage_users.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update user info
        user_to_edit.username = request.POST.get('username', user_to_edit.username)
        user_to_edit.email = request.POST.get('email', user_to_edit.email)
        user_to_edit.is_active = 'is_active' in request.POST
        user_to_edit.save()
        
        # Update profile if exists
        if hasattr(user_to_edit, 'profile'):
            user_to_edit.profile.phone_number = request.POST.get('phone_number', '')
            user_to_edit.profile.address = request.POST.get('address', '')
            user_to_edit.profile.bio = request.POST.get('bio', '')

            # Handle nationality properly
            nationality_code = request.POST.get('nationality', '')
            if nationality_code:
                user_to_edit.profile.nationality = nationality_code
            else:
                user_to_edit.profile.nationality = None
                
            user_to_edit.profile.save()
        
        messages.success(request, f'User {user_to_edit.username} updated successfully!')
        return redirect('authentication:manage_users')
    
    return render(request, 'edit_user.html', {'user': user_to_edit})


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Prevent admin from deleting themselves
    if user_to_delete == request.user:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('authentication:manage_users')
    
    # Prevent deleting other superusers
    if user_to_delete.is_superuser:
        messages.error(request, 'You cannot delete another admin account!')
        return redirect('authentication:manage_users')
    
    username = user_to_delete.username
    user_to_delete.delete()
    messages.success(request, f'User "{username}" has been permanently deleted.')
    return redirect('authentication:manage_users')


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def ban_user(request, user_id):
    user_to_ban = get_object_or_404(User, id=user_id)
    
    # Prevent admin from banning themselves
    if user_to_ban == request.user:
        messages.error(request, 'You cannot ban your own account!')
        return redirect('authentication:manage_users')
    
    # Prevent banning other superusers
    if user_to_ban.is_superuser:
        messages.error(request, 'You cannot ban another admin account!')
        return redirect('authentication:manage_users')
    
    # Toggle ban status
    if user_to_ban.is_active:
        user_to_ban.is_active = False
        # Create ban history record
        BanHistory.objects.create(
            user=user_to_ban,
            banned_by=request.user,
            reason="Banned by admin via dashboard"
        )
        messages.warning(request, f'User "{user_to_ban.username}" has been banned.')
    else:
        user_to_ban.is_active = True
        # Deactivate previous ban records
        BanHistory.objects.filter(user=user_to_ban, is_active=True).update(is_active=False)
        messages.success(request, f'User "{user_to_ban.username}" has been unbanned.')
    
    user_to_ban.save()
    return redirect('authentication:manage_users')

def view_profile(request, username):
    """View another user's public profile."""
    user = get_object_or_404(User, username=username)
    
    if not user.is_active and not request.user.is_superuser:
        raise Http404("This profile is not available.")
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        'profile_user': user,
        'profile': profile,
        'threads_count': 0, 
        'votes_count': 0,
        'comments_count': 0,
        'is_owner': request.user == user,  
    }
    return render(request, 'view_profile.html', context)