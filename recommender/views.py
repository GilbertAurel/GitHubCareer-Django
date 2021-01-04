import math

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .fetchAPI import get_pandas_json, get_json
from .recommenderAPI import recommendation


def home_view(request):
    return render(request, 'home.html', {})


def get_value_view(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))

    # See whether the input is from post or get
    if request.method == "POST":
        input_param = request.POST.get('position')
        input_type = request.POST.get('types')
    else:
        input_param = request.GET.get('position')
        input_type = request.GET.get('type')

    # Check if the user provide any input
    if input_param:
        recommended_title = recommendation(get_pandas_json(), input_param)
        jobs = get_job_dict(recommended_title, input_type)
    else:
        jobs = get_all_jobs(input_type)

    # Check if there is any recommended job founded
    if jobs == 'null':
        return render(request, 'notFound.html', {'input_param': input_param})
    else:
        paginator = Paginator(jobs, per_page)
        page_object = paginator.page(page)
        max_page = paginator.count / per_page

        # Set up max page value, if 0 then it is one page only output
        if max_page == 0:
            max_page = 1
        else:
            max_page = math.ceil(max_page)

        data = {
            'jobs': page_object,
            'page': page,
            'max': max_page,
            'pages': paginator.page_range,
            'search': input_param,
            'type': input_type,
        }

        return render(request, 'result.html', context=data)


# GET JOBS BY INPUT
def get_job_dict(recommended_title, input_type):
    job_json = get_json()
    job_list = []

    # Check if there is an output, if not return null
    if recommended_title:
        # Check the type (other, full time, part time)
        if input_type == 'Other':
            for title in recommended_title:
                for job in job_json:
                    if job.get('title') == title.get('title'):
                        job_list.append(job)
        else:
            for title in recommended_title:
                for job in job_json:
                    if job.get('title') == title.get('title') and job.get('type') == input_type:
                        job_list.append(job)
    else:
        return 'null'

    return job_list


# GET ALL JOBS
def get_all_jobs(input_type):
    job_json = get_json()
    job_list = []

    if input_type == 'Other':
        for job in job_json:
            job_list.append(job)
    else:
        for job in job_json:
            if job.get('type') == input_type:
                job_list.append(job)

    return job_list


# GET ALL JOBS VIEW
def get_all_job_view(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))

    jobs = get_all_jobs("Other")

    if jobs == 'null':
        return HttpResponse("not found")
    else:
        paginator = Paginator(jobs, per_page)
        page_object = paginator.page(page)
        max_page = paginator.count / per_page

        if max_page == 0:
            max_page = 1
        else:
            max_page = math.ceil(max_page)

        data = {
            'jobs': page_object,
            'page': page,
            'max': max_page,
            'pages': paginator.page_range,
        }

        return render(request, 'allJobs.html', context=data)
