from django.urls import path

from .views import HomeView, ScanResultView, SavedBucketsView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("bucket_saved/", ScanResultView.as_view(), name="saving_bucket"),
    path("saved_buckets/", SavedBucketsView.as_view(), name="saved_buckets"),
]
