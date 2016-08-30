"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

# from students.views.testview import StudentList
# from students.views.contact_admin_class import ContactAdmin

# Domashka 343
# from students.views.contact import KontaktView

# Domashka 352
# from students.views.kontakt_admin_class import KontaktAdmin

# str361
from students.views.students import StudentUpdateView,StudentDeleteView ,StudentAddView

# Domashka 365 GroupDeleteView
from students.views.groups import GroupAddView, GroupEditView, GroupDeleteView, groups_list

from students.views.journal import JournalView

from students.views.exams import ExamAddView,ExamEditView,ExamDeleteView, exams_list

from students.views.logentries import log_list

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.decorators import permission_required

js_info_dict = {
    'packages':('students'),
}

urlpatterns = patterns('',

    # Javascript translation
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog',js_info_dict),

    # i18n
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Students urls
        # url(r'^students/add/$', 'students.views.students_edit',
    url(r'^$', 'students.views.students.students_list', name='home'),

    # url(r'^students/add/$', 'students.views.students.students_add',
    #      name='students_add'),

# domashka 361
    url(r'^students/add/$', StudentAddView.as_view(),
         name='students_add'),

    # url(r'^students/(?P<sid>\d+)/edit/$',
    #      'students.views.students.students_edit',
    #      name='students_edit'),
    url(r'^students/(?P<pk>\d+)/edit/$',
         StudentUpdateView.as_view(),
         name='students_edit'),

# Domashka 357
#     url(r'^students/(?P<pk>\d+)/edit1/$',
#          'students.views.student_edit.student_edit' ,
#          name='students_edit1'),

    # url(r'^students/(?P<sid>\d+)/delete/$',
    #      'students.views.students.students_delete',
    #      name='students_delete'),
    url(r'^students/(?P<pk>\d+)/delete/$',
         StudentDeleteView.as_view(),
         name='students_delete'),

# Domashka del students by hands
    # url(r'^students/(?P<pk>\d+)/delete/$',
     #     'students.views.students.students_delete_my',
     #     name='students_delete'),

    # Groups Listing urls
    # url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/$', login_required(groups_list), name='groups'),

    url(r'^groups/add/$', login_required(GroupAddView.as_view()),
         name='groups_add'),
    # url(r'^groups/add/$', 'students.views.groups.groups_add',
 #         name='groups_add'),

    url(r'^groups/(?P<pk>\d+)/edit/$',login_required(GroupEditView.as_view()),
        name='groups_edit'),
    # url(r'^groups/(?P<pk>\d+)/edit/$','students.views.groups.groups_edit',
    #   name='groups_edit'),

    url(r'^groups/(?P<pk>\d+)/delete/$',
         login_required(GroupDeleteView.as_view()),
         name='groups_delete'),
    # url(r'^groups/(?P<pk>\d+)/delete/$',
 #         'students.views.groups.groups_delete_my',
 #         name='groups_delete'),

    # Journal urls
    # url(r'^journal/$', 'students.views.journal.journal_list', name='journal'),
    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),


    # Exams Listing urls
    url(r'^exams/$', login_required(exams_list), name='exams'),
    # url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),

    # url(r'^exams/add/$', 'students.views.exams.exams_add',
    #      name='exams_add'),
    url(r'^exams/add/$', login_required(ExamAddView.as_view()),
         name='exams_add'),

    # url(r'^exams/(?P<eid>\d+)/edit/$','students.views.exams.exams_edit',
    #     name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/edit/$', login_required(ExamEditView.as_view()),
            name='exams_edit'),

    # url(r'^exams/(?P<eid>\d+)/delete/$',
 #         'students.views.exams.exams_delete',
 #         name='exams_delete'),
    url(r'^exams/(?P<pk>\d+)/delete/$', login_required(ExamDeleteView.as_view()),
         name='exams_delete'),


    # Contact Admin Form
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin',
            name='contact_admin'),
    # url(r'^contact-admin/$', KontaktAdmin.as_view(),
    #         name='contact_admin'),

    # test form
    # url(r'^student-list/$', StudentList.as_view()),

# Domashka 343
#     url(r'^contact/', include('contact_form.urls')),
    # url(r'^contact/',KontaktView.as_view(),name='kontakt'),
    # url(r'contact/', KontaktAdmin.as_view(), name='contact_form'),

# Domashka 352
#     url(r'^kontakt/$', KontaktAdmin.as_view(),
#         name='kontakt'),

 # Domashka 526
    url(r'^log/$', permission_required('auth.add_user')(log_list) ,
        name='log'),

    # User Related urls
    # url(r'^users/profile/$', login_required(TemplateView.as_view(
    #     template_name='registration/profile.html')), name='profile'),

    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
        name='auth_logout'),

    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
        name='registration_complete'),
    #
    url(r'^users/profile/$', login_required(TemplateView.as_view(
               template_name='registration/profile.html')), name='profile'),

    url(r'^accounts/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),


    url(r'^users/', include('registration.backends.simple.urls',
        namespace='users')),
    # url(r'^accounts/', include('registration.backends.default.urls',
    #     namespace='users')),

    url('^social/', include('social.apps.django_app.urls', namespace='social')),
# social.apps.django_app.urls
#                        from social.apps.django_app.urls import extra
#                        social.apps.django_app.views
#                        from social.apps.django_app.views import auth
    #Default admin url
    url(r'^admin/', include(admin.site.urls)),

)

from .settings import MEDIA_ROOT, DEBUG

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$','django.views.static.serve',{
            'document_root':MEDIA_ROOT }))

# urlpatterns = ['',




