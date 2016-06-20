from django.views.generic import ListView
from rest_framework import viewsets, serializers

from dashboard.models import Flow


class Overview(ListView):
    queryset = Flow.objects.all()
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super(Overview, self).get_context_data(**kwargs)

        context['tcp'] = Flow.objects.filter(protocol=6)
        context['udp'] = Flow.objects.filter(protocol=17)

        context['low'] = Flow.objects.filter(risk=0)
        context['neutral'] = Flow.objects.filter(risk=1)
        context['moderate'] = Flow.objects.filter(risk=2)
        context['high'] = Flow.objects.filter(risk=3)

        return context


class FlowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flow


class FlowViewSet(viewsets.ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all().order_by('date')

    def get_queryset(self):
        date_since = self.request.query_params.get('since', None)

        if date_since is not None and date_since != "":
            self.queryset = self.queryset.filter(date__gt=date_since)
        return self.queryset


class FlowListView(ListView):
    model = Flow
    template_name = 'dashboard/flow_list.html'
