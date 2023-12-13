from django.shortcuts import render, HttpResponse
from .forms import FencingForm
from .models import Fence, Marking
from report.services.fill_first_page import FistPage
from report.services.fill_tables import Table

import pypandoc

from docx2pdf import convert
from pdf2image import convert_from_path

def home(request):
    if request.method == 'POST':

        form = FencingForm(data=request.POST)
        if form.is_valid():
            if Fence.objects.filter(marking=request.POST.get('marking')).exists():
                Marking.objects.create(marking=request.POST.get('marking'))
                FistPage.execute()
                Table.execute()
                docx_path = 'static/empty_report1.docx'
                convert(docx_path,'static/empty_report1.pdf')

                return render(request, 'html/docx.html')

            else:
                return HttpResponse('Такого ограждения нет')

    else:
        form = FencingForm()

    return render(request, 'html/home.html', {'form': form})















