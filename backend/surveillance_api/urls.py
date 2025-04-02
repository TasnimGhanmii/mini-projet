from django.urls import path
from .views import UploadExcelView, UpdateAvailabilityView, AssignSessionsView, GeneratePDFView

urlpatterns = [
    path("upload-excel/", UploadExcelView.as_view(), name="upload_excel"),
    path("update-availability/", UpdateAvailabilityView.as_view(), name="update_availability"),
    path("assign-sessions/", AssignSessionsView.as_view(), name="assign_sessions"),
    path("generate-pdf/", GeneratePDFView.as_view(), name="generate_pdf"),
]