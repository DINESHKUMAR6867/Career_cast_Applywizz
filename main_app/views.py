from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from .models import CustomUser, CareerCast
import json
import random

import os
from datetime import datetime, timedelta
import uuid
import msal
import requests
from .utils import generate_teleprompter_text

# Initialize Gemini (if used in your project)

def generate_otp():
    """Generates a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    """Send OTP email via Microsoft Graph API (Application-level permissions)"""
    access_token = get_outlook_access_token()

    # Prepare email data
    email_data = {
        "message": {
            "subject": "Your CareerCast OTP Verification Code",
            "body": {
                "contentType": "Text",
                "content": f"Hello, \n\nYour OTP verification code for CareerCast is: {otp}\n\nThis code will expire in 10 minutes.\n\nIf you didn't request this code, please ignore this email.\n\nBest regards,\nCareerCast Team"
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": email
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    # Send email using Microsoft Graph API (Application permissions)
    graph_url = f"https://graph.microsoft.com/v1.0/users/{settings.OUTLOOK_SENDER_EMAIL}/sendMail"
    response = requests.post(
        graph_url,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=email_data
    )

    if response.status_code == 202:
        return True
    else:
        print(f"Error sending OTP email: {response.text}")
        return False

def get_outlook_access_token():
    """Fetches access token using OAuth2 for Microsoft Graph API."""
    authority = f"https://login.microsoftonline.com/{settings.OUTLOOK_TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        settings.OUTLOOK_CLIENT_ID,
        authority=authority,
        client_credential=settings.OUTLOOK_CLIENT_SECRET
    )

    # Get token
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Error obtaining access token.")

def landing_page(request):
    """Landing page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'main_app/landing.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CareerCast
from .utils import extract_text_from_resume, generate_teleprompter_text

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import CareerCast
from .utils import extract_text_from_resume, generate_teleprompter_text
from django.shortcuts import get_object_or_404

@csrf_exempt
@login_required
def rewrite_teleprompter(request, cast_id):
    """Regenerate the teleprompter text for an existing CareerCast"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    career_cast = get_object_or_404(CareerCast, id=cast_id, user=request.user)

    try:
        # Re-extract and regenerate
        resume_content = extract_text_from_resume(career_cast.resume_file)
        new_text = generate_teleprompter_text(
            career_cast.job_title,
            career_cast.job_description,
            resume_content
        )

        career_cast.teleprompter_text = new_text
        career_cast.save()

        return JsonResponse({'success': True, 'teleprompter_text': new_text})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

def auth_page(request):
    """Authentication page for OTP login and signup"""
    if request.user.is_authenticated:
        return redirect('dashboard')  # If already authenticated, redirect to dashboard
        
    if request.method == 'POST':
        if 'signup' in request.POST:
            # Handle signup logic
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Validate passwords
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('auth')

            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use.')
                return redirect('auth')

            # Create user
            user = CustomUser.objects.create_user(
                username=email.split('@')[0],  # Can generate username based on email
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # Send OTP and proceed as before (if needed)
            otp_code = generate_otp()
            user.otp = otp_code
            user.otp_created_at = timezone.now()
            user.save()
            send_otp_email(email, otp_code)

            request.session['email_for_verification'] = email
            messages.success(request, f'OTP sent to {email}')
            return redirect('verify_otp')

        if 'login' in request.POST:
            # Handle login logic (email + password)
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Authenticate using email and password (now handled by custom backend)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                # Directly redirect to dashboard after login
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')

    return render(request, 'main_app/auth.html')


from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta

from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser

def verify_otp(request):
    """Verify OTP entered by the user during signup"""
    if request.user.is_authenticated:
        return redirect('dashboard')  # If already authenticated, redirect to dashboard

    email = request.session.get('email_for_verification')
    if not email:
        return redirect('auth')  # Redirect back if no email in session

    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        if otp_entered:
            try:
                user = CustomUser.objects.get(email=email)
                
                # Check OTP validity (10 min expiry)
                if (user.otp == otp_entered and 
                    user.otp_created_at and 
                    timezone.now() <= user.otp_created_at + timedelta(minutes=10)):
                    
                    user.otp = None
                    user.otp_created_at = None
                    user.is_verified = True
                    user.save()
                    
                    # Log user in
                    login(request, user, backend='main_app.backends.EmailBackend')
                    messages.success(request, 'Successfully verified! Welcome to CareerCast.')

                    # ✅ Redirect properly
                    next_url = request.GET.get('next')
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return redirect('dashboard')

                else:
                    messages.error(request, 'Invalid or expired OTP. Please try again.')

            except CustomUser.DoesNotExist:
                messages.error(request, 'User not found. Please register again.')
                return redirect('auth')
        else:
            messages.error(request, 'Please enter the OTP.')

    return render(request, 'main_app/verify_otp.html', {'email': email})



def login_page(request):
    """Login page where users can log in after OTP verification"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'main_app/login.html')


@login_required
def dashboard(request):
    """User dashboard view"""
    try:
        # Ensure that you're querying with the user instance
        career_casts = CareerCast.objects.filter(user=request.user).order_by('-created_at')

        profile_initials = request.user.get_profile_initials()

        return render(request, 'main_app/dashboard.html', {
            'career_casts': career_casts,
            'profile_initials': profile_initials
        })
    except Exception as e:
        print(f"Error fetching career casts: {e}")
        return redirect('landing')  # Fallback if there's an error
  # Fallback if there's an error




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CareerCast
from django.utils import timezone

def create_cast_step1(request):
    """Step 1: Create career cast - job details"""
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        
        if job_title and job_description:
            # Create CareerCast with teleprompter_text field
            career_cast = CareerCast.objects.create(
                user=request.user,
                job_title=job_title,
                job_description=job_description,
                teleprompter_text=""  # Set initial empty value or leave it blank
            )
            request.session['current_cast_id'] = str(career_cast.id)
            return redirect('create_cast_step2')
        else:
            messages.error(request, 'Please fill in all fields')
    
    return render(request, 'main_app/step1_job.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CareerCast

# @login_required
# def create_cast_step2(request):
#     career_cast_id = request.session.get('current_cast_id')
#     if not career_cast_id:
#         return redirect('create_cast_step1')
    
#     career_cast = get_object_or_404(CareerCast, id=career_cast_id, user=request.user)
    
#     if request.method == 'POST':
#         resume_file = request.FILES.get('resume_file')
#         if resume_file:
#             allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
#             file_extension = os.path.splitext(resume_file.name)[1].lower()
            
#             if file_extension not in allowed_extensions:
#                 messages.error(request, 'Please upload a PDF, DOC, DOCX, or TXT file.')
#                 return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})
            
#             if resume_file.size > 5 * 1024 * 1024:
#                 messages.error(request, 'File size too large. Please upload a file smaller than 5MB.')
#                 return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})
            
#             # ✅ Just save the file — don't generate text here
#             career_cast.resume_file = resume_file
#             career_cast.teleprompter_text = ""  # clear any stale text
#             career_cast.save()

#             return redirect('create_cast_step3')
#         else:
#             messages.error(request, 'Please upload a resume file')
    
#     return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})

import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from supabase import create_client

from .models import CareerCast

# ✅ Initialize Supabase client using your environment vars
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@login_required
def create_cast_step2(request):
    career_cast_id = request.session.get('current_cast_id')
    if not career_cast_id:
        return redirect('create_cast_step1')

    career_cast = get_object_or_404(CareerCast, id=career_cast_id, user=request.user)

    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')
        if not resume_file:
            messages.error(request, 'Please upload a resume file')
            return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})

        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        file_extension = os.path.splitext(resume_file.name)[1].lower()

        if file_extension not in allowed_extensions:
            messages.error(request, 'Please upload a PDF, DOC, DOCX, or TXT file.')
            return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})

        if resume_file.size > 5 * 1024 * 1024:
            messages.error(request, 'File size too large. Please upload a file smaller than 5MB.')
            return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})

        # ✅ Read file bytes for upload
        file_bytes = resume_file.read()
        file_path = f"{request.user.id}/{resume_file.name}"

        try:
            # Upload file to your Supabase Storage bucket (e.g., 'career_cast_media')
            supabase.storage.from_("career_cast_media").upload(file_path, file_bytes)

            # Get public URL for storage reference
            public_url = supabase.storage.from_("career_cast_media").get_public_url(file_path)

            # Save the Supabase file URL in your database
            career_cast.resume_file = public_url
            career_cast.teleprompter_text = ""
            career_cast.save()

            return redirect('create_cast_step3')

        except Exception as e:
            messages.error(request, f"Upload failed: {e}")

    return render(request, 'main_app/step2_resume.html', {'career_cast': career_cast})






from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CareerCast
from .utils import extract_text_from_resume, generate_teleprompter_text

@login_required
def create_cast_step3(request):
    career_cast_id = request.session.get('current_cast_id')
    if not career_cast_id:
        return redirect('create_cast_step1')

    career_cast = get_object_or_404(CareerCast, id=career_cast_id, user=request.user)

    if not career_cast.resume_file:
        messages.error(request, 'Please upload your resume first.')
        return redirect('create_cast_step2')

    try:
        if not career_cast.teleprompter_text or career_cast.teleprompter_text.strip() == "":
            resume_content = extract_text_from_resume(career_cast.resume_file)

            print("\n--- DEBUG ---")
            print("JOB TITLE:", career_cast.job_title)
            print("JOB DESCRIPTION:", career_cast.job_description[:200])
            print("RESUME CONTENT (first 500):", resume_content[:500])
            print("--------------\n")

            teleprompter_text = generate_teleprompter_text(
                career_cast.job_title,
                career_cast.job_description,
                resume_content
            )
            career_cast.teleprompter_text = teleprompter_text
            career_cast.save()
        else:
            teleprompter_text = career_cast.teleprompter_text

        return render(request, 'main_app/step3_record.html', {
            'career_cast': career_cast,
            'tele': teleprompter_text
        })

    except Exception as e:
        messages.error(request, f"Error generating teleprompter text: {e}")
        return redirect('create_cast_step2')




@login_required
def record_view(request):
    """Recording studio page"""
    career_cast_id = request.session.get('current_cast_id')
    if not career_cast_id:
        return redirect('create_cast_step1')
    
    career_cast = get_object_or_404(CareerCast, id=career_cast_id, user=request.user)
    
    context = {
        'tele': career_cast.teleprompter_text or "Hello! I'm excited to introduce myself for this position.",
        'career_cast': career_cast
    }
    return render(request, 'main_app/record.html', context)

# @login_required
# def video_upload(request):
#     """Handle video upload after recording"""
#     if request.method == 'POST' and request.FILES.get('video'):
#         try:
#             career_cast_id = request.session.get('current_cast_id')
#             if not career_cast_id:
#                 return JsonResponse({'status': 'error', 'message': 'No CareerCast found'}, status=400)
            
#             career_cast = get_object_or_404(CareerCast, id=career_cast_id, user=request.user)
#             video_file = request.FILES['video']
            
#             # Check file type
#             allowed_extensions = ['.webm', '.mp4', '.mov', '.avi']
#             file_extension = os.path.splitext(video_file.name)[1].lower()
            
#             if file_extension not in allowed_extensions:
#                 return JsonResponse({'status': 'error', 'message': 'Invalid video format. Please use WebM, MP4, MOV, or AVI.'}, status=400)
            
#             # Check file size (50MB limit)
#             if video_file.size > 50 * 1024 * 1024:
#                 return JsonResponse({'status': 'error', 'message': 'File size too large. Please upload a video smaller than 50MB.'}, status=400)
            
#             # Save the video file (using the model's upload_to path)
#             career_cast.video_file = video_file
#             career_cast.save()
            
#             return JsonResponse({
#                 'status': 'success', 
#                 'message': 'Video uploaded successfully',
#                 'cast_id': career_cast.id
#             })
            
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
#     return JsonResponse({'status': 'error', 'message': 'No video file received'}, status=400)


# @login_required
# def video_upload(request):
#     """Handle video upload after recording"""
#     if request.method == "POST" and request.FILES.get("video"):
#         try:
#             # accept from POST or session
#             career_cast_id = (
#                 request.POST.get("career_cast_id")
#                 or request.session.get("current_cast_id")
#             )
#             if not career_cast_id:
#                 return JsonResponse(
#                     {"status": "error", "message": "No CareerCast found"}, status=400
#                 )

#             career_cast = get_object_or_404(
#                 CareerCast, id=career_cast_id, user=request.user
#             )
#             video_file = request.FILES["video"]

#             # Check file type
#             allowed_extensions = [".webm", ".mp4", ".mov", ".avi"]
#             file_extension = os.path.splitext(video_file.name)[1].lower()
#             if file_extension not in allowed_extensions:
#                 return JsonResponse(
#                     {
#                         "status": "error",
#                         "message": "Invalid video format. Please use WebM, MP4, MOV, or AVI.",
#                     },
#                     status=400,
#                 )

#             # Check file size (50 MB limit)
#             if video_file.size > 50 * 1024 * 1024:
#                 return JsonResponse(
#                     {
#                         "status": "error",
#                         "message": "File size too large. Please upload a video smaller than 50 MB.",
#                     },
#                     status=400,
#                 )

#             # Save the uploaded file
#             career_cast.video_file = video_file
#             career_cast.save()

#             return JsonResponse(
#                 {
#                     "status": "success",
#                     "message": "Video uploaded successfully",
#                     "cast_id": career_cast.id,
#                 }
#             )

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=500)

#     return JsonResponse(
#         {"status": "error", "message": "No video file received"}, status=400
#     )

import os
import re
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from supabase import create_client
from django.conf import settings

# Make sure you have these in your settings.py (or .env)
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

@login_required
def video_upload(request):
    """Upload video to Supabase Storage (works on Vercel)"""
    if request.method == "POST" and request.FILES.get("video"):
        try:
            # Get CareerCast record
            career_cast_id = (
                request.POST.get("career_cast_id")
                or request.session.get("current_cast_id")
            )
            if not career_cast_id:
                return JsonResponse(
                    {"status": "error", "message": "No CareerCast found"}, status=400
                )

            career_cast = get_object_or_404(
                CareerCast, id=career_cast_id, user=request.user
            )
            video_file = request.FILES["video"]

            # ✅ Check file type
            allowed_extensions = [".webm", ".mp4", ".mov", ".avi"]
            file_extension = os.path.splitext(video_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid video format. Please use WebM, MP4, MOV, or AVI.",
                    },
                    status=400,
                )

            # ✅ Check file size (50 MB limit)
            if video_file.size > 50 * 1024 * 1024:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "File size too large. Please upload a video smaller than 50 MB.",
                    },
                    status=400,
                )

            # ✅ Sanitize filename and build path
            safe_name = re.sub(r"[^\w\-.]", "_", video_file.name)
            file_path = f"{career_cast.id}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_name}"

            # ✅ Upload directly to Supabase Storage
            file_bytes = video_file.read()
            response = supabase.storage.from_("career_cast_media").upload(file_path, file_bytes)

            # If upload fails
            if not response or getattr(response, "status_code", None) not in (200, 201, None):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Upload failed: {getattr(response, 'error', 'Unknown error')}",
                    },
                    status=500,
                )

            # ✅ Get public URL
            public_url = supabase.storage.from_("career_cast_media").get_public_url(file_path)

            # ✅ Save URL in database
            career_cast.video_file = public_url
            career_cast.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Video uploaded successfully.",
                    "video_url": public_url,
                }
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "No video file received."}, status=400
    )



from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse

@xframe_options_exempt
@login_required
def final_result(request, cast_id):
    """Display the final result with resume and video"""
    career_cast = get_object_or_404(CareerCast, id=cast_id, user=request.user)
    print(f"Resume File URL: {career_cast.resume_file.url}")  # Debugging line
    return render(request, 'main_app/final_result.html', {'career_cast': career_cast})

# from django.http import FileResponse
# from django.shortcuts import get_object_or_404
# from django.conf import settings
# from .models import CareerCast
# import os

# @login_required
# def final_result(request, cast_id):
#     """Display the final result with resume and video"""
#     career_cast = get_object_or_404(CareerCast, id=cast_id, user=request.user)
    
#     # Serve the resume file directly using FileResponse
#     if career_cast.resume_file:
#         resume_file_path = career_cast.resume_file.path  # Get the actual file path
#         if os.path.exists(resume_file_path):
#             return FileResponse(open(resume_file_path, 'rb'), content_type='application/pdf')
#         else:
#             messages.error(request, 'Resume file not found.')
    
#     return render(request, 'main_app/final_result.html', {'career_cast': career_cast})




@login_required
def download_resume(request, cast_id):
    """Download the resume file"""
    career_cast = get_object_or_404(CareerCast, id=cast_id, user=request.user)
    if career_cast.resume_file:
        response = HttpResponse(career_cast.resume_file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{career_cast.resume_file.name}"'
        return response
    else:
        messages.error(request, 'No resume file found')
        return redirect('final_result', cast_id=cast_id)

@login_required
def view_video(request, cast_id):
    """View the uploaded video"""
    career_cast = get_object_or_404(CareerCast, id=cast_id, user=request.user)
    if career_cast.video_file:
        response = HttpResponse(career_cast.video_file, content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{career_cast.video_file.name}"'
        return response
    else:
        messages.error(request, 'No video file found')
        return redirect('final_result', cast_id=cast_id)

def logout_view(request):
    """Logout the user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.conf import settings
import os
import tempfile
from io import BytesIO
import traceback
import shutil

def download_enhanced_resume(request, cast_id):
    """
    Download resume with clickable Play Video button
    """
    print(f"=== DOWNLOAD REQUEST STARTED ===")
    print(f"Cast ID: {cast_id}")
    print(f"User: {request.user}")
    
    try:
        career_cast = get_object_or_404(CareerCast, id=cast_id, user=request.user)
        print(f"CareerCast found: {career_cast.id}")
        
        if not career_cast.resume_file:
            print("ERROR: No resume file attached")
            messages.error(request, 'No resume file found.')
            return redirect('final_result', cast_id=cast_id)
        
        # Get file info
        resume_path = career_cast.resume_file.path
        file_extension = os.path.splitext(resume_path)[1].lower()
        original_filename = career_cast.resume_file.name
        
        print(f"Resume path: {resume_path}")
        print(f"File exists: {os.path.exists(resume_path)}")
        print(f"File extension: {file_extension}")
        print(f"Original filename: {original_filename}")
        
        # Check if file exists
        if not os.path.exists(resume_path):
            print(f"ERROR: File does not exist at path: {resume_path}")
            messages.error(request, 'Resume file not found on server.')
            return redirect('final_result', cast_id=cast_id)
        
        # Generate URL for button
        final_result_url = request.build_absolute_uri(f'/final-result/{cast_id}/')
        print(f"Final result URL: {final_result_url}")
        
        # Process based on file type - CALL THE ACTUAL FUNCTIONS
        if file_extension == '.pdf':
            print("Processing as PDF file with button")
            modified_file_path = add_play_video_button_to_pdf_with_image(resume_path, original_filename, final_result_url)
            content_type = 'application/pdf'
            download_filename = f"enhanced_{original_filename}"
            
        elif file_extension in ['.docx', '.doc']:
            print("Processing as DOCX file with button")
            modified_file_path = add_play_video_button_to_docx_with_image(resume_path, original_filename, final_result_url)
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            download_filename = f"enhanced_{original_filename}"
            
        else:
            print(f"Unsupported file type, returning original: {file_extension}")
            # Return original file for unsupported types
            return FileResponse(
                open(resume_path, 'rb'),
                as_attachment=True,
                filename=original_filename
            )
        
        # Check if modified file was created
        if not os.path.exists(modified_file_path):
            print(f"ERROR: Modified file not created at: {modified_file_path}")
            messages.error(request, 'Failed to create enhanced resume.')
            return redirect('final_result', cast_id=cast_id)
        
        print(f"SUCCESS: Enhanced resume created at: {modified_file_path}")
        print(f"File size: {os.path.getsize(modified_file_path)} bytes")
        
        # Return the modified file
        response = FileResponse(
            open(modified_file_path, 'rb'),
            as_attachment=True,
            filename=download_filename
        )
        response['Content-Type'] = content_type
        
        print("=== DOWNLOAD RESPONSE SENT ===")
        return response
            
    except Exception as e:
        print(f"=== CRITICAL ERROR ===")
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        messages.error(request, f'Download failed: {str(e)}')
        return redirect('final_result', cast_id=cast_id)

def add_play_video_button_to_pdf_with_image(original_pdf_path, original_filename, final_result_url):
    """
    Add Play Video button using static image at top-right corner
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from PyPDF2.generic import DictionaryObject, ArrayObject, FloatObject, NameObject, TextStringObject
        
        print("Starting PDF processing with static image button...")
        
        # Create a temporary file for the modified PDF
        temp_dir = tempfile.gettempdir()
        safe_filename = f"enhanced_{os.path.basename(original_pdf_path)}"
        modified_pdf_path = os.path.join(temp_dir, safe_filename)
        
        # Ensure original file exists
        if not os.path.exists(original_pdf_path):
            raise Exception(f"Original PDF file not found: {original_pdf_path}")
        
        # CORRECTED: Your image path
        button_image_path = os.path.join(settings.BASE_DIR, 'career_cast', 'main_app', 'static', 'main_app', 'images', 'play_video_button.png')
        
        print(f"Looking for button image at: {button_image_path}")
        
        # Check if button image exists
        if not os.path.exists(button_image_path):
            print("Button image not found at primary path, trying alternatives...")
            # Try alternative paths
            alternative_paths = [
                os.path.join(settings.BASE_DIR, 'static', 'main_app', 'images', 'play_video_button.png'),
                os.path.join(settings.BASE_DIR, 'main_app', 'static', 'main_app', 'images', 'play_video_button.png'),
                os.path.join(settings.BASE_DIR, 'static', 'images', 'play_video_button.png'),
                os.path.join(settings.BASE_DIR, 'main_app', 'static', 'images', 'play_video_button.png'),
            ]
            
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    button_image_path = alt_path
                    print(f"Found button image at: {button_image_path}")
                    break
            else:
                # If no image found, create a simple button programmatically
                print("No button image found, creating programmatic button...")
                return add_play_video_button_programmatic(original_pdf_path, original_filename, final_result_url)
        
        print(f"Button image found at: {button_image_path}")
        
        # Read original PDF
        print("Reading original PDF...")
        original_pdf = PdfReader(original_pdf_path)
        if len(original_pdf.pages) == 0:
            raise Exception("PDF file has no pages")
        
        first_page = original_pdf.pages[0]
        media_box = first_page.mediabox
        
        # Get page dimensions
        page_width = float(media_box.width)
        page_height = float(media_box.height)
        
        print(f"Page dimensions: {page_width}x{page_height}")
        
        # Button dimensions (from your image)
        button_width = 85   # Exact width from image
        button_height = 30  # Exact height from image
        margin_right = 20   # 30px from right edge
        margin_top = 15     # 30px from top edge
        
        # Calculate button position (top-right corner)
        x_pos = page_width - button_width - margin_right
        y_pos = page_height - button_height - margin_top
        
        print(f"Button position: ({x_pos}, {y_pos})")
        
        # Create overlay with image button
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # Add the button image
        try:
            img = ImageReader(button_image_path)
            c.drawImage(img, x_pos, y_pos, width=button_width, height=button_height, mask='auto')
            print("Button image added successfully")
        except Exception as img_error:
            print(f"Image error: {img_error}. Creating fallback button...")
            # Fallback to programmatic button
            return add_play_video_button_programmatic(original_pdf_path, original_filename, final_result_url)
        
        c.save()
        
        # Merge with original PDF
        print("Merging button with original PDF...")
        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        output = PdfWriter()
        
        # Process first page with overlay
        first_page.merge_page(overlay_pdf.pages[0])
        
        # Add clickable annotation
        try:
            llx = FloatObject(x_pos)
            lly = FloatObject(y_pos)
            urx = FloatObject(x_pos + button_width)
            ury = FloatObject(y_pos + button_height)
            
            annotation = DictionaryObject({
                NameObject("/Type"): NameObject("/Annot"),
                NameObject("/Subtype"): NameObject("/Link"),
                NameObject("/Rect"): ArrayObject([llx, lly, urx, ury]),
                NameObject("/Border"): ArrayObject([FloatObject(0), FloatObject(0), FloatObject(0)]),
                NameObject("/A"): DictionaryObject({
                    NameObject("/S"): NameObject("/URI"),
                    NameObject("/URI"): TextStringObject(final_result_url)
                }),
                NameObject("/F"): FloatObject(4),
            })
            
            if "/Annots" in first_page:
                first_page[NameObject("/Annots")].append(annotation)
            else:
                first_page[NameObject("/Annots")] = ArrayObject([annotation])
                
            print("Added clickable annotation to PDF")
                
        except Exception as annotation_error:
            print(f"PDF Annotation error: {annotation_error}")
        
        output.add_page(first_page)
        
        # Add remaining pages without modification
        for page_num in range(1, len(original_pdf.pages)):
            output.add_page(original_pdf.pages[page_num])
        
        # Save modified PDF
        print(f"Saving enhanced PDF to: {modified_pdf_path}")
        with open(modified_pdf_path, "wb") as output_file:
            output.write(output_file)
        
        print("PDF enhancement with image button completed successfully")
        return modified_pdf_path
        
    except ImportError as e:
        raise Exception(f"Required packages not installed: {e}. Install with: pip install PyPDF2 reportlab")
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def add_play_video_button_programmatic(original_pdf_path, original_filename, final_result_url):
    """
    Create button programmatically if image is not found
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import HexColor
        from PyPDF2.generic import DictionaryObject, ArrayObject, FloatObject, NameObject, TextStringObject
        
        print("Creating programmatic button...")
        
        # Create a temporary file for the modified PDF
        temp_dir = tempfile.gettempdir()
        safe_filename = f"enhanced_{os.path.basename(original_pdf_path)}"
        modified_pdf_path = os.path.join(temp_dir, safe_filename)
        
        # Read original PDF
        original_pdf = PdfReader(original_pdf_path)
        first_page = original_pdf.pages[0]
        media_box = first_page.mediabox
        
        # Get page dimensions
        page_width = float(media_box.width)
        page_height = float(media_box.height)
        
        # Button dimensions
        button_width = 85
        button_height = 25
        margin_right = 30
        margin_top = 30
        
        # Calculate button position
        x_pos = page_width - button_width - margin_right
        y_pos = page_height - button_height - margin_top
        
        # Create overlay
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # Create exact button matching your image
        # Main background (light blue)
        c.setFillColor(HexColor("#4DABF5"))
        c.rect(x_pos, y_pos, button_width, button_height, fill=True, stroke=False)
        
        # Darker bottom for gradient effect
        c.setFillColor(HexColor("#1971C2"))
        c.rect(x_pos, y_pos, button_width, button_height * 0.4, fill=True, stroke=False)
        
        # Border
        c.setStrokeColor(HexColor("#1864AB"))
        c.setLineWidth(0.8)
        c.rect(x_pos, y_pos, button_width, button_height, fill=False, stroke=True)
        
        # Play icon (white triangle)
        c.setFillColor(HexColor("#FFFFFF"))
        play_x = x_pos + 8
        play_y = y_pos + button_height / 2
        
        # Draw play triangle
        p = c.beginPath()
        p.moveTo(play_x, play_y - 4)
        p.lineTo(play_x, play_y + 4)
        p.lineTo(play_x + 6, play_y)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        
        # Text
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 7)
        text_x = x_pos + 20
        text_y = y_pos + (button_height - 7) / 2 + 4
        c.drawString(text_x, text_y, "Play Video")
        
        c.save()
        
        # Merge with original PDF
        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        output = PdfWriter()
        
        first_page.merge_page(overlay_pdf.pages[0])
        
        # Add clickable annotation
        llx = FloatObject(x_pos)
        lly = FloatObject(y_pos)
        urx = FloatObject(x_pos + button_width)
        ury = FloatObject(y_pos + button_height)
        
        annotation = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Link"),
            NameObject("/Rect"): ArrayObject([llx, lly, urx, ury]),
            NameObject("/Border"): ArrayObject([FloatObject(0), FloatObject(0), FloatObject(0)]),
            NameObject("/A"): DictionaryObject({
                NameObject("/S"): NameObject("/URI"),
                NameObject("/URI"): TextStringObject(final_result_url)
            }),
            NameObject("/F"): FloatObject(4),
        })
        
        if "/Annots" in first_page:
            first_page[NameObject("/Annots")].append(annotation)
        else:
            first_page[NameObject("/Annots")] = ArrayObject([annotation])
        
        output.add_page(first_page)
        
        for page_num in range(1, len(original_pdf.pages)):
            output.add_page(original_pdf.pages[page_num])
        
        with open(modified_pdf_path, "wb") as output_file:
            output.write(output_file)
        
        print("Programmatic button created successfully")
        return modified_pdf_path
        
    except Exception as e:
        raise Exception(f"Error creating programmatic button: {str(e)}")

def add_play_video_button_to_docx_with_image(original_docx_path, original_filename, final_result_url):
    """
    Add Play Video button to DOCX using image (simplified - will use text for DOCX)
    """
    try:
        from docx import Document
        from docx.shared import Pt, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        print("Starting DOCX processing...")
        
        # Create a temporary file for the modified DOCX
        temp_dir = tempfile.gettempdir()
        safe_filename = f"enhanced_{os.path.basename(original_docx_path)}"
        modified_docx_path = os.path.join(temp_dir, safe_filename)
        
        # Load the original document
        doc = Document(original_docx_path)
        
        # Create a table for precise positioning
        table = doc.add_table(rows=1, cols=1)
        table.autofit = False
        table.columns[0].width = Inches(6.5)  # Control width
        
        # Get the cell and set alignment to right
        cell = table.cell(0, 0)
        
        # Create paragraph in the cell
        button_paragraph = cell.paragraphs[0]
        button_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # Add the button text (for DOCX, we use text since adding images is complex)
        run = button_paragraph.add_run("▶ Play Video")
        run.font.bold = True
        run.font.size = Pt(8)
        run.font.color.rgb = None  # Default color
        
        # Add some styling to make it look like a button
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
        
        # Add background color
        rPr = run._r.get_or_add_rPr()
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), "4DABF5")  # Light blue
        rPr.append(shading)
        
        # Move table to top of document
        doc._body._element.insert(0, table._tbl)
        
        # Add spacing
        button_paragraph.paragraph_format.space_after = Pt(10)
        
        # Save modified document
        doc.save(modified_docx_path)
        
        print("DOCX enhancement completed successfully")
        return modified_docx_path
        
    except ImportError as e:
        raise Exception(f"Required packages not installed: {e}. Install with: pip install python-docx")
    except Exception as e:
        raise Exception(f"Error processing DOCX: {str(e)}")