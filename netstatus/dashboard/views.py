from django.views.generic import ListView
from rest_framework import viewsets, serializers

from dashboard.models import Flow


class Overview(ListView):
    pass


class FlowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flow


class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer


# class FlowListView(ListView):
#     pass
