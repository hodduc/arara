from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'warara.sysop.views.index'),
    (r'^add_board/$', 'warara.sysop.views.add_board'),
    (r'^modify_boards/$', 'warara.sysop.views.modify_boards'),
    (r'^edit_board/$', 'warara.sysop.views.edit_board'),
    (r'^confirm_user/$', 'warara.sysop.views.confirm_user'),
    (r'^refresh_weather/$', 'warara.sysop.views.refresh_weather'),
    (r'^add_banner/$', 'warara.sysop.views.add_banner'),
    (r'^select_banner/$', 'warara.sysop.views.select_banner'),
    (r'^remove_banner/$', 'warara.sysop.views.remove_banner'),
)
