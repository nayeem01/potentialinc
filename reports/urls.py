from django.urls import path
from .views import ReportMovieView, AdminManageReportsView

urlpatterns = [
    path(
        "movies/<int:movie_id>/report/", ReportMovieView.as_view(), name="report-movie"
    ),
    path("admin/reports/", AdminManageReportsView.as_view(), name="view-reports"),
    path(
        "admin/reports/<int:report_id>/manage/",
        AdminManageReportsView.as_view(),
        name="manage-report",
    ),
]
