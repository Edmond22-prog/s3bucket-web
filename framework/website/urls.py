from django.urls import path, include

from .views import HomeView, ScanResultView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("scan-result/", ScanResultView.as_view(), name="scanned"),
]
