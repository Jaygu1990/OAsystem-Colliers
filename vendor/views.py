from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from vendor.models import vendorRequest,AXvendor
from vendor.forms import vendorRequestForm,vendorReviewForm,uploadAXvendors
from django.core.files.storage import FileSystemStorage
from vendor.import_excel import process_excel_file
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

def preparer_required(group_name="vendor preparer"):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapped_view
    return decorator

def reviewer_required(group_name="vendor reviewer"):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapped_view
    return decorator




# Create your views here.
def AXvenderSearch(request):
    AXvendors = AXvendor.objects.order_by("vendor_name")
    diction = {'AXvendors': AXvendors}
    return render(request, 'vendor/vendorSearch.html',context= diction)

def pending(request):
    vendor_requests = vendorRequest.objects.order_by("date")
    diction = {'vendor_requests': vendor_requests}
    return render(request, 'vendor/pendingList.html',context= diction)

def reviewing(request):
    review = vendorRequest.objects.order_by("date")
    diction = {'vendor_reviews': review}
    return render(request, 'vendor/reviewingList.html',context= diction)

def createRequest(request):
    form = vendorRequestForm()
    if request.method =="POST":
        form = vendorRequestForm(request.POST,request.FILES)

        if form.is_valid():
            form.instance.status = 'pending for setup'
            form.save(commit=True)
            return pending(request)
        else:
            print("Your form has errors:", form.errors)
    return render(request,'vendor/requestePage.html',{'createForm':form})

@preparer_required('vendor preparer')
def setRequest(request,deal_number,vendor_name):
    vendor_request = get_object_or_404(vendorRequest, deal_number=deal_number,vendor_name=vendor_name)
    if request.method == 'POST':
        form = vendorReviewForm(request.POST, request.FILES,instance=vendor_request)
        if form.is_valid():
            form.instance.status = 'pending for review'
            form.save()
            return pending(request)
    else:
            form = vendorReviewForm(instance=vendor_request)
    return render(request, 'vendor/setupPage.html', {'setupForm': form})
@preparer_required('reviewer preparer')
def reviewRequest(request,deal_number,vendor_name):
    vendor_request = get_object_or_404(vendorRequest, deal_number=deal_number,vendor_name=vendor_name)
    if request.method == 'POST':
        form = vendorReviewForm(request.POST,instance=vendor_request)
        if form.is_valid():
            action = request.POST.get('action')
            if action == 'approve':
                form.instance.status = 'finished'
            elif action == 'reject':
                form.instance.status = 'pending for setup'
            form.save()
            return reviewing(request)
    else:
            form = vendorReviewForm(instance=vendor_request)
    return render(request, 'vendor/reviewPage.html', {'reviewForm': form})

@preparer_required('reviewer preparer')
def upload_excel(request):
    if request.method == 'POST':
        form = uploadAXvendors(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            fs = FileSystemStorage()

            # Ensure unique filenames
            filename = fs.get_available_name(excel_file.name)
            file_path = fs.save(filename, excel_file)

            success, message = process_excel_file(file_path)

            if success:
                return pending(request)
            else:
                return pending(request)

    else:
        form = uploadAXvendors()

    return render(request, 'vendor/uploadAXvendor.html', {'AXform': form})


@preparer_required('reviewer preparer')
def licensemanagement(request):
    vendor_requests = vendorRequest.objects.order_by("expiration_date")
    diction = {'vendor_license': vendor_requests}
    return render(request, 'vendor/LicenseManagement.html',context= diction)