from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'surveillance_api'  # This is important for namespacing!

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload-excel/', views.UploadExcelView.as_view(), name='upload_excel'),
    path('api/update-availability/', views.UpdateAvailabilityView.as_view(), name='update_availability'),
    path('api/assign-sessions/', views.AssignSessionsView.as_view(), name='assign_sessions'),
    path('api/generate-pdf/', views.GeneratePDFView.as_view(), name='generate_pdf'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
