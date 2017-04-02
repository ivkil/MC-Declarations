import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from councils_members.models import Council


def index(request):
    return render(request, 'councils_members/index.html')


def about(request):
    return render(request, 'councils_members/about.html')


def detail(request, council_id):
    council = get_object_or_404(Council, pk=council_id)
    active_mcs = council.person_set.filter(active_member_council=True)
    return render(request, 'councils_members/detail.html', {'council': council, 'active_mcs': active_mcs})


def get_councils_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        councils = Council.objects.filter(title__icontains=q)[:10]
        results = []
        for council in councils:
            council_json = {'data': council.id, 'value': council.title}
            results.append(council_json)
        data = json.dumps(results)
    else:
        data = {'error': 'Error occurs'}
    return HttpResponse(data, 'application/json')
