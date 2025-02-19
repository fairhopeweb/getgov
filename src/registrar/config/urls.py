"""URL Configuration

For more information see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from registrar.views import health, index, profile, whoami
from registrar.forms import ApplicationWizard, WIZARD_CONDITIONS
from api.views import available

APPLICATION_URL_NAME = "application_step"
application_wizard = ApplicationWizard.as_view(
    url_name=APPLICATION_URL_NAME,
    done_step_name="finished",
    condition_dict=WIZARD_CONDITIONS,
)

urlpatterns = [
    path("", index.index, name="home"),
    path("whoami/", whoami.whoami, name="whoami"),
    path("admin/", admin.site.urls),
    path("application/<id>/edit/", application_wizard, name="edit-application"),
    path("health/", health.health),
    path("edit_profile/", profile.edit_profile, name="edit-profile"),
    path("openid/", include("djangooidc.urls")),
    path("register/", application_wizard, name="application"),
    path("register/<step>/", application_wizard, name=APPLICATION_URL_NAME),
    path("api/v1/available/<domain>", available, name="available"),
]

if not settings.DEBUG:
    urlpatterns += [
        # redirect to login.gov
        path(
            "admin/login/", RedirectView.as_view(pattern_name="login", permanent=False)
        ),
        # redirect to login.gov
        path(
            "admin/logout/",
            RedirectView.as_view(pattern_name="logout", permanent=False),
        ),
    ]

# we normally would guard these with `if settings.DEBUG` but tests run with
# DEBUG = False even when these apps have been loaded because settings.DEBUG
# was actually True. Instead, let's add these URLs any time we are able to
# import the debug toolbar package.
try:
    import debug_toolbar  # type: ignore

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
except ImportError:
    pass
