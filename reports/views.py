from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from movies.models import Movie

from .models import MovieReport
from .serializers import MovieReportSerializer


class ReportMovieView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id, *args, **kwargs):
        """
        Allows a user to report a movie.
        """
        movie = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieReportSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(movie=movie, reported_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminManageReportsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Allows admin to view all movie reports.
        """
        reports = MovieReport.objects.all()
        serializer = MovieReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, report_id, *args, **kwargs):
        """
        Allows admin to approve or reject a report.
        """
        report = get_object_or_404(MovieReport, pk=report_id)
        status_action = request.data.get("status")

        if status_action not in ["approved", "rejected"]:
            return Response(
                {"error": "Invalid status. Must be 'approved' or 'rejected'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report.status = status_action
        report.save()

        return Response(
            {"message": f"Report has been {status_action}."}, status=status.HTTP_200_OK
        )
