import pandas as pd
from itertools import combinations
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Professor, Session, Formula
from .serializers import ProfessorSerializer, SessionSerializer
from .utils import calculate_max_hours


class UploadExcelView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                Professor.objects.create(
                    name=row["Nom Et Prénom Enseignant"],
                    department=row["Département"],
                    grade=row["Grade"],
                    courses=row["Cours"],
                    td=row["TD"],
                    tp=row["TP"],
                    coef=row["coef"],
                    max_surveillance_hours=calculate_max_hours(row),
                    available=True,
                )
            return Response({"message": "Excel file uploaded successfully!"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UpdateAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professor_id = request.data.get("id")
        available = request.data.get("available")

        try:
            professor = Professor.objects.get(id=professor_id)
            professor.available = available
            professor.save()
            return Response({"message": "Availability updated successfully!"}, status=200)
        except Professor.DoesNotExist:
            return Response({"error": "Professor not found"}, status=404)


class AssignSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professors = Professor.objects.filter(available=True).exclude(grade="Chef de Département")
        sessions = Session.objects.all()

        for session in sessions:
            for prof1, prof2 in combinations(professors, 2):
                if (prof1.max_surveillance_hours > 0 and prof2.max_surveillance_hours > 0):
                    session.professor_1 = prof1
                    session.professor_2 = prof2
                    session.save()

                    prof1.max_surveillance_hours -= 1
                    prof2.max_surveillance_hours -= 1
                    prof1.save()
                    prof2.save()
                    break

        return Response({"message": "Sessions assigned successfully!"}, status=200)


class GeneratePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="surveillance_schedule.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica", 12)

        y = 750
        sessions = Session.objects.all()
        for session in sessions:
            p.drawString(50, y, f"Session: {session.session_id}, Date: {session.date}, Time: {session.time}")
            p.drawString(50, y - 20, f"Professors: {session.professor_1}, {session.professor_2}")
            y -= 40
            if y < 50:
                p.showPage()
                y = 750

        p.save()
        return response