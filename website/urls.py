from django.urls import path

from .views import home, scan, scan_file, RepositoryView

urlpatterns = [
    path("", home, name="home"),
    path("scanning_name_or_url/", scan, name="scan"),
    path("scanning_file/", scan_file, name="scan_file"),
    path("scanning_repository/", RepositoryView.as_view(), name="repository"),
    # path("bucket_saved/", ScanResultView.as_view(), name="saving_bucket"),
    # path("saved_buckets/", SavedBucketsView.as_view(), name="saved_buckets"),
    # path("saving_buckets/", save_buckets, name="saving_buckets"),
]
