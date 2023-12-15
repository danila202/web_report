import random

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .forms import FencingForm
from .models import Fence, Marking, Protocol
from report.services.fill_first_page import FistPage
from report.services.fill_tables import Table

import os
from docx2pdf import convert
import datetime


def home(request):
    if request.method == 'POST':

        form = FencingForm(data=request.POST)
        if form.is_valid():

            if Fence.objects.filter(marking=request.POST.get('marking')).exists():
                Marking.objects.create(marking=request.POST.get('marking'))
                FistPage.execute()
                Table.execute()
                docx_path = 'static/empty_report1.docx'
                convert(docx_path,f'media/pdf/protocol{Marking.objects.last().id}.pdf')
                full_path = os.path.join(settings.BASE_DIR, f'media/pdf/protocol{Marking.objects.last().id}.pdf')

                with open(full_path, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline; filename="protol.pdf"; target="_blank" '

                    new_protocol = Protocol.objects.create(
                        id = str(random.randint(1,10000)),
                        data=datetime.date.today(),
                        performer='Самигуллин Л.Ф',
                        kind='виртуальный',
                        name_file='empty_report1.pdf',
                        fence_id = Fence.objects.get(marking=Marking.objects.last().marking).id
                    )

                    new_protocol.save()
                    os.remove('static/empty_report1.docx')
                    Marking.objects.last().delete()

                    return response

            else:
                return HttpResponse('Такого ограждения нет')

    else:
        form = FencingForm()

    return render(request, 'html/home.html', {'form': form})


def search_fence(request):
    fence = request.GET.get('fence')
    payload = []
    if fence:
        fence_marking = Fence.objects.filter(marking__contains=fence)

        for fence_marking_obj in fence_marking:
            payload.append(fence_marking_obj.marking)

    return JsonResponse({'status': 200, 'data': payload})












