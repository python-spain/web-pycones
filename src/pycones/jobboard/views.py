from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from pycones.jobboard.models import JobOffer


class JobBoardView(View):
    template_name = "jobboard/list.html"

    def get(self, request):
        data = {
            "job_offers": JobOffer.objects.all()
        }
        return render(request, self.template_name, data)


class JobOfferView(View):
    template_name = "jobboard/details.html"

    def get(self, request, pk):
        job_offer = get_object_or_404(JobOffer, pk=pk)
        data = {
            "job_offer": job_offer,
        }
        return render(request, self.template_name, data)
