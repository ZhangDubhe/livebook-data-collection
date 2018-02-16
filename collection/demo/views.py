from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your views here.
from io import BytesIO
from reportlab.pdfgen import canvas
import json
import random

from .models import Disease, Symptom, DiseaseLink, UMLS_tgt, UMLS_st, User,UserLog
from .Authentication import Authentication as auth




def index(request):
    user_name = _("user")
    content = "Are you ready?"
    para = "Please read this carefully."
    return render(request, 'home/index.html', {
        'content': content,
        'title': 'Home',
        'username': user_name,
        'para': para
    })


def get_random(model, number):
    last = model.objects.count() - 1


def user_auth(uuid):
    try:
        user_is_related = User.objects.get(pk=uuid).is_related
    except User.DoesNotExist:
        return False
    if user_is_related:
        return True
    else:
        return False



def quiz(request, uuid):
    # check uuid
    try:
        user = User.objects.get(pk=uuid)
        if user.is_doctor:
            pass
        else:
            return render(request, 'quiz/index.html', {
                'content': "Your have no such permission",
                'title': 'Auth Error',
                'username': user.user_name
            })
    except User.DoesNotExist:
        return render(request, 'quiz/index.html', {
            'content': "No this user",
            'title': 'Auth Error',
            'username': "no auth"
        })

    try:
        diseases = Disease.objects.filter(concept_type='Otitis').order_by('?')
        length = diseases.count()

    except:
        diseases = ["Otitis"]
        length = 1

    para = "You might want to search the term below?"
    user_name = _(user.user_name)
    try:

        symptoms = Symptom.objects.order_by('?')[0:5]
    #TODO:     to query which have link with the disease
    except Symptom.DoesNotExist:
        raise Http404("Symptoms do not exist")

    try:
        tgt = UMLS_tgt.objects.order_by('-add_at')[0]
        if not is_tgt_valid(tgt):
            tgt = create_new_tgt()

    except:
        tgt = create_new_tgt()

    return render(request, 'quiz/index.html', {
        'title': 'Home',
        'username': user_name,
        'para': para,
        'disease': diseases[0],
        'diseases_num': length,
        'type': "symptom",
        'symptoms': symptoms,
        'tgt': tgt
    })


def polls(request):
    return render(request, 'polls/index.html', {
        'content': 'This is poll page ',
        'title': 'Poll'
    })


def update_disease(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cui = request.POST.get('cui')
        try:
            Disease.objects.create(name=name, content_unique_id=cui)
            result = "UPDATE Disease success"
            status = 20
        except:
            result = "UPDATE Disease error"
            status = 500
        return HttpResponse(json.dumps({
            "result": result,
            "status": status
        }))


def update_symptom(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cui = request.POST.get('cui')
        try:
            Symptom.objects.create(name=name, content_unique_id=cui)
            result = "UPDATE Symptom success"
            status = 20
        except:
            result = "UPDATE Symptom error"
            status = 500
        return HttpResponse(json.dumps({
            "result": result,
            "status": status
        }))


def update_disease_link(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cui = request.POST.get('cui')
        try:
            DiseaseLink.objects.create(name=name, content_unique_id=cui)
            result = "UPDATE Symptom success"
            status = 20
        except:
            result = "UPDATE Symptom error"
            status = 500
        return HttpResponse(json.dumps({
            "result": result,
            "status": status
        }))


def umls_auth(request):
    if request.method == "POST":
        name = request.POST.get('name')
        status = 0
        if name:
            try:
                tgt_res = UMLS_tgt.objects.order_by('-add_at')[0]
            except:
                tgt_res = None
            if tgt_res != None:
                if is_tgt_valid(tgt_res):
                    pass
                else:
                    tgt_res = create_new_tgt()
            else:
                tgt_res = create_new_tgt()
            st = create_new_st(tgt_res)
            if st:
                result = str(st)
                status = 200
        else:
            result = "Please INPUT something"
            print(result)
        return HttpResponse(json.dumps({
            "status": status,
            "result": result,
            "tgt": str(tgt_res)
        }))


def is_tgt_valid(tgt):
    now_time = timezone.now().timestamp()
    add_time = tgt.add_at.timestamp()
    during = now_time - add_time
    # valid 8 hours
    if during >= 28800:
        return False
    else:
        return True


def create_new_st(tgt):
    connect = auth()
    st = None
    try:
        st = connect.getst(tgt)
    except:
        return False
    if st:
        try:
            UMLS_st.objects.create(ticket=st)
            return st
        except:
            return False


def create_new_tgt():
    connect = auth()
    tgt = None
    try:
        tgt = connect.gettgt()
    except:
        return False
    if tgt:
        try:
            UMLS_tgt.objects.create(ticket=tgt)
            return tgt
        except:
            return False


def document(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="test.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
