from django.conf.urls import url
from .views import (
                about, contact,
                draft_page, index_page,
                post_create, post_update,
                post_delete, post_detail,
                staff_logout,
                )

app_name = "posts"

urlpatterns = [
    url(r'^$', index_page, name = "home"),
    url(r'^about/$', about, name = "about"),
    url(r'^create/$', post_create, name = "create"),
    url(r'^contact/$', contact, name = "contact"),
    url(r'^drafts/$', draft_page, name = "drafts"),
    url(r'^detail/(?P<slug>[\w-]+)/delete/$', post_delete, name = "delete"),
    url(r'^detail/(?P<slug>[\w-]+)/$', post_detail, name = "detail"),
    url(r'^detail/(?P<slug>[\w-]+)/edit/$', post_update, name = "update"),
    url(r'^logout/$', staff_logout, name = "logout"),
]
