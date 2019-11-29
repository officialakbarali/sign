from django.shortcuts import render, render_to_response
from django.core.files.storage import FileSystemStorage
#from myproject.myapp.verify import m
from .predict import predict
from .models import Customer
# Create your views here.
def index(request):
  #  Customer.objects.all().delete()
    return render_to_response('index.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage(location='myapp/upload')
        fileName = fs.save(uploaded_file.name, uploaded_file)
        custName = request.POST['cName']
        newCust = Customer(name=custName, path=fileName)
        newCust.save()
        context['title'] = "Successfully Added " + newCust.name + ", His/Her Id :" + str(newCust.id)
        return render(request, 'page.html', context)
    else:
        context['title'] = "Enter Name"
        context['btn'] = "Upload"
        return render(request, 'upload.html', context)


def verify(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage(location='myapp/verify')
        fileName = fs.save(uploaded_file.name, uploaded_file)
        custId = request.POST['cName']
        customer =Customer.objects.filter(id=custId)
        savedFileName = customer[0].path
        customerName = customer[0].name
        pred = predict.load("/home/user/Documents/project/myproject/myapp/upload/" +savedFileName,"/home/user/Documents/project/myproject/myapp/verify/" +fileName)
        if(pred==True):
            context['title'] = "Genuine Signature :" + customerName
        else:
            context['title'] = "Forged Signature :" + customerName
        fs.delete(fileName)
        return render(request, 'page.html', context)

    fromS = request.GET.get('s', '')
    if fromS == '':
        fromQ = request.GET.get('q', '')
        context['query'] = fromQ
        if (fromQ == ''):
            context['myList'] =Customer.objects.all()
            return render(request, 'verify.html', context)
        else:
            context['myList'] =Customer.objects.filter(name__contains=fromQ)
            return render(request, 'verify.html', context)
