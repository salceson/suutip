from django.views.generic import ListView
from rest_framework import viewsets, serializers

from dashboard.models import Flow


class Overview(ListView):
    queryset = Flow.objects.all()
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super(Overview, self).get_context_data(**kwargs)

        for k, v in Flow.PROTOCOLS:
            context[v.lower()] = Flow.objects.filter(protocol=k)

        for k, v in Flow.RISKS:
            context[v] = Flow.objects.filter(risk=k)

        return context


class FlowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flow


class FlowViewSet(viewsets.ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()

    def get_queryset(self):
        start_with_id = self.request.query_params.get('start', None)

        if start_with_id is not None and start_with_id != "":
            self.queryset = self.queryset.filter(id__gte=start_with_id)
        return self.queryset


class FlowListView(ListView):
    model = Flow
    template_name = 'dashboard/flow_list.html'


class Charts(ListView):
    queryset = Flow.objects.all()
    template_name='dashboard/charts.html'
