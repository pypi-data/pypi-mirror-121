from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from bridger.settings import bridger_settings


class FrontendView(TemplateView):
    template_name = bridger_settings.FRONTEND_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = bridger_settings.FRONTEND_CONTEXT
        if version := self.request.GET.get("frontend_version", None):
            context["JS_URL"] = f'{settings.CDN_BASE_ENDPOINT_URL}/js/main-{version.replace(".", "-")}.js'
            context["CSS_URL"] = f'{settings.CDN_BASE_ENDPOINT_URL}/css/main-{version.replace(".", "-")}.js'
        context["BRIDGER_CONTEXT"] = context
        return context

    @classmethod
    def bundled_view(cls, url_path):
        return path(route=url_path, view=cls.as_view(), name="frontend")
