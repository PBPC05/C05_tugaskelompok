from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from apps.authentication.models import UserProfile, BanHistory
from django.http import Http404
from apps.forums.models import Forums, ForumsReplies
from apps.prediction.models import PredictionVote
from apps.news.models import Comment


def register_user(request):
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

    threads_count = Forums.objects.filter(user=request.user).count()
    recent_forums = Forums.objects.filter(user=request.user).order_by('-created_at')[:5]
    votes_counts = PredictionVote.objects.filter(user=request.user).count()
    comments_count = Comment.objects.filter(user=request.user).count() + ForumsReplies.objects.filter(user=request.user).count()

    context = {
        'profile': profile,
        'threads_count': threads_count,  
        'votes_count': votes_counts,    
        'comments_count': comments_count, 
        'recent_threads': recent_forums,
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
    user = get_object_or_404(User, username=username)
    
    if not user.is_active and not request.user.is_superuser:
        raise Http404("This profile is not available.")
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None

    threads_count = Forums.objects.filter(user=user).count()
    votes_counts = PredictionVote.objects.filter(user=request.user).count()
    comments_count = Comment.objects.filter(user=request.user).count() + ForumsReplies.objects.filter(user=request.user).count()

    context = {
        'profile_user': user,
        'profile': profile,
        'threads_count': threads_count, 
        'votes_count': votes_counts,
        'comments_count': comments_count,
        'is_owner': request.user == user,  
    }
    return render(request, 'view_profile.html', context)

# =========================================== flutter integration ===========================================
from django.contrib.auth import authenticate, login as auth_login, logout, authenticate
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

@csrf_exempt
def flutter_login(request):
    """Flutter login endpoint"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login successful!"
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Your account has been banned. Please contact admin."
                }, status=401)
        else:
            return JsonResponse({
                "status": False,
                "message": "Invalid username or password."
            }, status=401)
    
    return JsonResponse({
        "status": False,
        "message": "Invalid request method."
    }, status=400)


@csrf_exempt
def flutter_register(request):
    """Flutter register endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')

            # Validate input
            if not username or not password1 or not password2:
                return JsonResponse({
                    "status": "error",
                    "message": "All fields are required."
                }, status=400)

            # Check if passwords match
            if password1 != password2:
                return JsonResponse({
                    "status": "error",
                    "message": "Passwords do not match."
                }, status=400)
            
            # Check password length
            if len(password1) < 8:
                return JsonResponse({
                    "status": "error",
                    "message": "Password must be at least 8 characters long."
                }, status=400)
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Username already exists."
                }, status=400)
            
            # Create the new user
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            
            return JsonResponse({
                "username": user.username,
                "status": "success",
                "message": "User created successfully!"
            }, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON data."
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)

@csrf_exempt
@login_required
def flutter_logout(request):
    """Flutter logout endpoint"""
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": f"Logout failed: {str(e)}"
        }, status=401)

@csrf_exempt
def flutter_profile(request):
    """Get user profile for Flutter"""
    if request.method == 'GET':
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': False,
                'message': 'User not authenticated. Please login first.'
            }, status=401)
        
        try:
            user = request.user
            profile = user.profile if hasattr(user, 'profile') else None
            
            # Get user statistics
            from apps.forums.models import Forums, ForumsReplies
            from apps.prediction.models import PredictionVote
            from apps.news.models import Comment
            
            threads_count = Forums.objects.filter(user=user).count()
            votes_count = PredictionVote.objects.filter(user=user).count()
            comments_count = (
                Comment.objects.filter(user=user).count() + 
                ForumsReplies.objects.filter(user=user).count()
            )
            
            # Prepare profile data
            profile_data = None
            if profile:
                profile_data = {
                    'id': profile.id,
                    'phone_number': profile.phone_number or '',
                    'address': profile.address or '',
                    'bio': profile.bio or '',
                    'nationality': str(profile.nationality.code) if profile.nationality else '',
                    'created_at': profile.created_at.isoformat(),
                    'updated_at': profile.updated_at.isoformat(),
                }
            
            return JsonResponse({
                'status': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email or '',
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser,
                    'date_joined': user.date_joined.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'profile': profile_data,
                },
                'stats': {
                    'threads_count': threads_count,
                    'votes_count': votes_count,
                    'comments_count': comments_count,
                }
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f'Error fetching profile: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': False,
        'message': 'Invalid request method.'
    }, status=400)

@csrf_exempt
def flutter_edit_profile(request):
    """Edit profile endpoint for Flutter (safe for JSON)"""
    if request.method != 'POST':
        return JsonResponse({
            'status': False,
            'message': 'Invalid request method.'
        }, status=400)

    # Check authentication (cookie session)
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': False,
            'message': 'User not authenticated. Please login first.'
        }, status=401)

    try:
        data = json.loads(request.body)
        user = request.user

        # Update email
        email = data.get('email')
        if email is not None:
            user.email = email
            user.save()

        # Get or create profile
        profile = user.profile if hasattr(user, 'profile') else UserProfile.objects.create(user=user)

        # Update profile fields
        profile.phone_number = data.get('phone_number', profile.phone_number)
        profile.address = data.get('address', profile.address)
        profile.bio = data.get('bio', profile.bio)

        # Nationality handling
        nationality_code = data.get('nationality')
        if nationality_code:
            profile.nationality = nationality_code
        else:
            profile.nationality = None

        profile.save()

        return JsonResponse({
            'status': True,
            'message': 'Profile updated successfully!'
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': False,
            'message': 'Invalid JSON data.'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': f'Error updating profile: {str(e)}'
        }, status=500)


@csrf_exempt
def flutter_get_countries(request):
    """Get list of all countries for Flutter"""
    if request.method == 'GET':
        try:
            from django_countries import countries
            
            # Convert countries to list of dictionaries
            countries_list = [
                {
                    'code': code,
                    'name': name
                }
                for code, name in countries
            ]
            
            return JsonResponse({
                'status': True,
                'countries': countries_list
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f'Error fetching countries: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': False,
        'message': 'Invalid request method.'
    }, status=400)