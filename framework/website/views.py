import logging

import boto3
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from core.business.entities import AwsBucketEntity
from core.business.use_cases.aws_access_acl import AwsAccessAcl
from core.business.use_cases.aws_bucket_manag import AwsBucketManagement
from core.business.use_cases.aws_settings import AwsSettings
from core.business.use_cases.scrapping_aws import ScrappingAws
from infrastructure.repository.aws_bucket_repos import AwsBucketRepository
from website.models import AwsBucket


class HomeView(View):
    template_name = "website/index.html"
    settings = AwsSettings()

    def get(self, request, *args, **kwargs):
        context = {"navbar": "home"}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bucket_name = request.POST["bucket_name"]

        result = ScrappingAws(bucket_name).run()
        if result is None:
            return redirect("home")

        # Settings ACL Properties to the Bucket
        client = boto3.client("s3")
        AwsAccessAcl(result, client, self.settings).get_bucket_acl()

        context = {"result": result, "navbar": "scan"}
        return render(request, "website/scan_result.html", context)


class ScanResultView(View):
    template_name = "website/scan_result.html"
    aws_bucket_repos = AwsBucketRepository(AwsBucket)

    def post(self, request, *args, **kwargs):
        bucket = AwsBucketEntity.factory(
            name=request.POST["bucket_name"],
            access_browser=request.POST["bucket_access_browser"],
            location=request.POST["bucket_location"],
            url=request.POST["bucket_url"],
            properties=request.POST["bucket_properties"],
            uuid=request.POST["bucket_id"],
        )

        aws_bucket_manage = AwsBucketManagement(self.aws_bucket_repos)
        try:
            # Try to get the bucket if exist
            bucket = aws_bucket_manage.find_bucket_by_name(bucket.name())
            # Update the bucket information
            aws_bucket_manage.update_bucket(bucket)

        except TypeError:
            # Create the bucket in the database
            aws_bucket_manage.create_bucket(bucket)

        return redirect("saved_buckets")


class SavedBucketsView(TemplateView):
    template_name = "website/saved_buckets.html"
    aws_bucket_repos = AwsBucketRepository(AwsBucket)

    def get(self, request, *args, **kwargs):
        aws_bucket_manage = AwsBucketManagement(self.aws_bucket_repos)
        buckets = aws_bucket_manage.list_buckets()
        context = {"navbar": "saved_buckets", "buckets": buckets}
        return render(request, self.template_name, context)
