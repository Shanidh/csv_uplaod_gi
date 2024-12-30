from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
import csv
from io import StringIO

from csv_upload_app.serializers import UserSerializer

# Create your views here.
class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "CSV file is required."}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']
        
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must be a CSV."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = StringIO(decoded_file)
            reader = csv.DictReader(csv_data)
        except Exception as e:
            return Response({"error": f"Invalid CSV format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        saved_count = 0
        rejected_count = 0
        validation_errors = []

        for row in reader:
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved_count += 1
                except Exception as e:
                    validation_errors.append({"email": row.get("email", "Unknown"), "error": "Duplicate email."})
                    rejected_count += 1
            else:
                rejected_count += 1
                validation_errors.append({"row": row, "errors": serializer.errors})

        return Response({
            "total_saved": saved_count,
            "total_rejected": rejected_count,
            "validation_errors": validation_errors
        })
