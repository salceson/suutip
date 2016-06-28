from django.views.generic import ListView, TemplateView
from rest_framework import viewsets, serializers

from dashboard.models import Flow, Protocols, Risks


class Overview(ListView):
    queryset = Flow.objects.all()
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super(Overview, self).get_context_data(**kwargs)

        for proto in Protocols:
            context[proto.name.lower()] = Flow.objects.filter(protocol=proto.value)

        for risk in Risks:
            context[risk.name.lower()] = Flow.objects.filter(risk=risk.value)

        return context


class FlowSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(FlowSerializer, self).__init__(*args, **kwargs)
        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            wanted = set(fields)
            existing = set(self.fields.keys())
            for field in existing - wanted:
                self.fields.pop(field)

    class Meta:
        model = Flow
        fields = ['url'] + [f.name for f in Flow._meta.get_fields()]


class FlowViewSet(viewsets.ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()

    def get_queryset(self):
        start_with_id = self.request.GET.get('start', None)

        if start_with_id is not None and start_with_id != "":
            self.queryset = self.queryset.filter(id__gte=start_with_id)
        return self.queryset


class FlowListView(TemplateView):
    template_name = 'dashboard/flow_list.html'

    def get_context_data(self, **kwargs):
        context = super(FlowListView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        context['search'] = '' if not search else search
        return context


class Charts(ListView):
    queryset = Flow.objects.all()
    template_name = 'dashboard/charts.html'
