"""autotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static

# language related stuff
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import javascript_catalog
js_info_dict = {
    'domain': 'djangojs',
    'packages': ('myproject',),
}


# custom stuff
from autotest.views import index, about, contact, profile, test_admin, test_user, success

urlpatterns = [
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),

    # index
    url(r'^$', index, name='index'),
    url(r'^about$', about, name='about'),
    url(r'^contact$', contact, name='contact'),
    url(r'^profile$', profile, name='profile'),
    url(r'^test_user$', test_user, name='test_user'),
    url(r'^test_admin$', test_admin, name='test_admin'),
    url(r'^success$', success, name='success'),

    # translations
    url(r'^jsi18n/$', javascript_catalog, js_info_dict,
        name='javascript-catalog'),

    # Avoid the signout verifying page
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),
    # allauth
    url(r'^accounts/', include('allauth.urls')),

)

#django-debug-toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
