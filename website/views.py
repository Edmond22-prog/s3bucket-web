import os

import boto3
from django.shortcuts import render
from django.views import View

from .core.business.use_cases.github.repository_scanner import RepositoryScanner
from .core.business.use_cases.aws.aws_access_acl import AwsAccessAcl
from .core.business.use_cases.aws.scrapping_aws import ScrappingAws


# class HomeView(View):
#     template_name = "website/index.html"
#     # settings = AwsSettings()
#
#     def get(self, request, *args, **kwargs):
#         context = {"navbar": "home"}
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         value = request.POST["bucket_name"]
#
#         result = ScrappingAws(value).run()
#         if result is None:
#             context = {"message": "Invalid bucket name or url."}
#             return render(request, self.template_name, context)
#
#         # # Settings ACL Properties to the Bucket
#         # client = boto3.client("s3")
#         # AwsAccessAcl(result, client, self.settings).get_bucket_acl()
#
#         context = {"result": result, "navbar": "scan"}
#         return render(request, "website/scan_result.html", context)


def home(request):
    template_name = "website/index.html"
    return render(request, template_name, {"navbar": "home"})


class RepositoryView(View):
    template_get = "website/repository_scan.html"
    template_post = "website/scan_result.html"

    def get(self, request, *args, **kwargs):
        context = {"navbar": "repository"}
        return render(request, self.template_get, context)

    def post(self, request, *args, **kwargs):
        context = {"navbar": "scan"}
        repository = request.POST["repository_name"]
        result = RepositoryScanner(repository).run()
        if result is None:
            context = {"message": "Repository not found."}
            return render(request, self.template_get, context)

        context["repository"] = result
        context["vulnerabilities_count"] = len(result.vulnerabilities)
        return render(request, self.template_post, context)


def scan(request):
    template_name = "website/scan_result.html"
    context = {"navbar": "scan"}
    if request.method == "POST":
        value = request.POST["object"]
        context["value"] = value
        result = ScrappingAws(value).run()
        if result is None:
            context = {"message": "Invalid bucket name/url or bucket doesn't exist."}
            return render(request, "website/index.html", context)

        if result.access_browser == "Public":
            # Settings ACL Properties to the Public Bucket
            client = boto3.client("s3")
            AwsAccessAcl(result, client).get_bucket_acl()

        context["result"] = result
        return render(request, template_name, context)


def scan_file(request):
    template_name = "website/scan_result.html"
    context = {"navbar": "scan"}
    if request.method == "POST":
        file = request.FILES["object_file"]
        file_name = str(file)

        # Local file creation
        location = os.path.join(os.getcwd(), "website/file")
        os.chdir(location)
        open(file_name, "w").close()

        # Open the local file and write all data who
        # are contained in the uploaded file
        with open(file_name, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Verify if the file is empty
        if os.stat(file_name).st_size == 0:
            context = {"message_for_file": "The file is empty."}
            os.remove(file_name)
            os.chdir(os.path.join(os.getcwd(), ".."))
            return render(request, "website/index.html", context)

        buckets = []
        not_exists = []
        with open(file_name, "r") as f:
            for bucket in f.readlines():
                bucket = bucket.rstrip("\n")
                result = ScrappingAws(bucket).run()
                if result is None:
                    not_exists.append(bucket)

                else:
                    if result.access_browser == "Public":
                        # Settings ACL Properties to the Public Bucket
                        client = boto3.client("s3")
                        AwsAccessAcl(result, client).get_bucket_acl()
                    buckets.append(result)

        # Delete the local file
        if os.path.exists(file_name):
            os.remove(file_name)
            os.chdir(os.path.join(os.getcwd(), ".."))

        context["buckets"] = buckets
        context["file_name"] = file_name
        if not_exists:
            context["not_exists"] = not_exists

        return render(request, template_name, context)
