from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^warara/', include('warara.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
    (r'^main/$', 'warara.views.main'),
    (r'^list/([^/]+)/$', 'warara.views.list'),
    (r'^modify/([^/]+)/(\d)+/$', 'warara.views.modify'),
)