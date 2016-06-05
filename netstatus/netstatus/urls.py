from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from dashboard.views import Overview, FlowViewSet, FlowListView

router = routers.DefaultRouter()
router.register(r'flows', FlowViewSet)

urlpatterns = [
    url(r'^$', Overview.as_view(), name='overview'),
    url(r'^flows/$', FlowListView.as_view(), name='flow_list'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
