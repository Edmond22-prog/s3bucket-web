from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from core.business.use_cases.scrapping_aws import ScrappingAws


class HomeView(View):
    template_name = "website/index.html"

    def get(self, request, *args, **kwargs):
        context = {"navbar": "home"}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bucket_name = request.POST["bucket"]
        result = ScrappingAws(bucket_name).run()
        if result is None:
            return redirect("home")
        context = {"result": result, "navbar": "scan"}
        return render(request, "website/scan_result.html", context)


class ScanResultView(TemplateView):
    template_name = "website/scan_result.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
