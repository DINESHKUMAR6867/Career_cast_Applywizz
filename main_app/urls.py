from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('auth/', views.auth_page, name='auth'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('verify-otp/dashboard/', views.dashboard, name='dashboard'),
    path('/auth/?next=/dashboard/', views.dashboard, name='dashboard'),
    path('create-cast/step1/', views.create_cast_step1, name='create_cast_step1'),
    path('create-cast/step2/', views.create_cast_step2, name='create_cast_step2'),
    path('create-cast/step3/', views.create_cast_step3, name='create_cast_step3'),
    path('record/', views.record_view, name='record'),
    path('video/upload/', views.video_upload, name='video_upload'),
    
    # Use UUID patterns for all cast_id URLs
    path('final-result/<int:cast_id>/', views.final_result, name='final_result'),  # For integer cast_id
    path('download-resume/<uuid:cast_id>/', views.download_resume, name='download_resume'),
    path('view-video/<uuid:cast_id>/', views.view_video, name='view_video'),
    path('career-cast/<int:cast_id>/rewrite-teleprompter/', views.rewrite_teleprompter, name='rewrite_teleprompter'),
    
    # path('rewrite-teleprompter/', views.rewrite_teleprompter, name='rewrite_teleprompter'),
    path('logout/', views.logout_view, name='logout'),
 path('download_enhanced_resume/<int:cast_id>/', views.download_enhanced_resume, name='download_enhanced_resume'),
 ]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from django.urls import path
# from . import views

# urlpatterns = [
#     # Dashboard page
#     path('dashboard/', views.dashboard, name='dashboard'),
    
#     # Authentication and signup
#     path('auth/', views.auth_page, name='auth'),
#     path('verify-otp/', views.verify_otp, name='verify_otp'),

#     # Career Cast creation steps
#     path('create-cast/step1/', views.create_cast_step1, name='create_cast_step1'),
#     path('create-cast/step2/', views.create_cast_step2, name='create_cast_step2'),
#     path('create-cast/step3/', views.create_cast_step3, name='create_cast_step3'),

#     # Video recording page
#     path('record/', views.record_view, name='record'),

#     # Video upload page
#     path('video/upload/', views.video_upload, name='video_upload'),

#     # Final Result page (where user views resume and video)
#     path('final-result/<int:cast_id>/', views.final_result, name='final_result'),

#     # Download the enhanced resume (with play video button on the first page)
#     path('download_enhanced_resume/<int:cast_id>/', views.download_enhanced_resume, name='download_enhanced_resume'),

#     # Logout
#     path('logout/', views.logout_view, name='logout'),

#     # Resend OTP for email verification
#     # path('resend-otp/', views.resend_otp, name='resend_otp'),

#     # Download Resume for User
#     path('download-resume/<uuid:cast_id>/', views.download_resume, name='download_resume'),

#     # Rewrite the teleprompter script
#     path('rewrite-teleprompter/', views.rewrite_teleprompter, name='rewrite_teleprompter'),
# ]
