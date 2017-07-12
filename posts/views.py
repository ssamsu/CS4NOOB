from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import Post_form, Feedback_form
from .models import Post, Category

HOME_PAGE = "/"

# For handling ABOUT Page
def about(request):
    return render(request, "about.html")

# For handling CONTACT Page
def contact(request):
    form = Feedback_form(request.POST or None)
    if request.method == "POST":
        if(form.is_valid()):
            form.save()
            # Once form data is recieved and stored, a mail is send to ADMIN
            email = EmailMessage(subject='CS4NOOB Notification', body='You got a new notification in CS4NOOB. Check it out!', to=[settings.TO_MAIL_ID])
            email.send()
            message = "Message recieved. We will get back to you ASAP! :)"
        else:
            message = "Sorry something went wrong! :("
        context = {'message': message}
        return render(request, 'contact.html', context)
    else:
        context = {'form' : form}
        return render(request, 'contact.html', context)

# For handling DRAFT Page
def draft_page(request):
    # Only ADMIN or authenitcated staff should access this page
    if request.user.is_authenticated():
        # Get the draft posts and sort it by creation date (reverse order)
        object_list = Post.objects.filter(draft=True).order_by("-created")
        page_request_var, queryset = search(request, object_list)
        context = {
            "title" : "Drafts",
            "object_list" : queryset,
            "page_request_var": page_request_var
        }
        return render(request, "index.html", context)
    else:
        # If the user is not authenitcated, return 404 page
        raise Http404

# For handling INDEX/HOME Page
def index_page(request):
    # Get the published posts and sort it by creation date
    object_list = Post.objects.filter(draft=False).order_by("-created")
    # If the search string is EMPTY, return to HOME page
    if ('q' in request.GET) and (request.GET.get('q') == ''):
        return HttpResponseRedirect(HOME_PAGE)
    page_request_var, queryset = search(request, object_list)
    context = {
        "object_list" : queryset,
        "page_request_var": page_request_var
    }
    return render(request, "index.html", context)

# For handling Pagination in DRAFT and INDEX page
def pagination(request, object_list):
    paginator = Paginator(object_list, 10) # 10 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    return page_request_var, queryset

def post_create(request):
    # For handling CREATE Page
    # Only ADMIN or authenitcated staff should access this page
    if request.user.is_authenticated():
        form = Post_form(request.POST or None, request.FILES or None) # request.FILES is added for handling image data
        if request.method == "POST":
            if form.is_valid():
                form.save()
                # If there are multiple users, uncomment the below lines and delete the above one
                # instance = form.save(commit=False)
                # instance.user = request.user
                # instance.save()
                messages.success(request, 'Created Successfully.')
                return HttpResponseRedirect(HOME_PAGE)
            elif form.errors:
                messages.success(request, 'Not Successful.')
        else:
            context = {"form" : form}
            return render(request, "create.html", context)
    else:
        # If the user is not authenitcated, return 404 page
        raise Http404

# For handling Page DELETION
def post_delete(request, slug=None):
    # Only ADMIN or authenitcated staff should access this page
    if request.user.is_authenticated():
        object_detail = get_object_or_404(Post, slug=slug)
        object_detail.delete()
        messages.success(request, 'Deleted Successfully.')
        return HttpResponseRedirect(HOME_PAGE)
    else:
        # If the user is not authenitcated, return 404 page
        raise Http404

# For handling DETAIL Page
def post_detail(request, slug=None):
    object_detail = get_object_or_404(Post, slug=slug)
    # Only ADMIN or authenitcated staff should access this page
    if object_detail.draft and not(request.user.is_authenticated()):
        raise Http404
    context = {"detail" : object_detail}
    return render(request, "detail.html", context)

# For handling Page UPDATE
def post_update(request, slug=None):
    # Only ADMIN or authenitcated staff should access this page
    if request.user.is_authenticated():
        object_detail = get_object_or_404(Post, slug=slug)
        form = Post_form(request.POST or None, request.FILES or None, instance=object_detail)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated Successfully.')
                return HttpResponseRedirect(HOME_PAGE)
            elif form.errors:
                messages.success(request, 'Not Successful.')
        else:
            context = {"form" : form}
            return render(request, "create.html", context)
    else:
        # If the user is not authenitcated, return 404 page
        raise Http404

# For searching the content
def search(request, object_list):
    query = request.GET.get('tag') if 'tag' in request.GET else request.GET.get('q')
    if query and request.GET.get('tag'):
        post_qs = Category.objects.filter(
            Q(title__iexact=query)
            )
        object_list = object_list.filter(
            Q(category=post_qs)
            ).distinct()
    elif query:
            object_list = object_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    return pagination(request, object_list)

# For handling ADMIN/STAFF Page
def staff_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully.')
    return HttpResponseRedirect(HOME_PAGE)
