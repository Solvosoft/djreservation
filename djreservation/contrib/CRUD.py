# encoding: utf-8

'''
Free as freedom will be 26/8/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.http.response import HttpResponseRedirect


class ObjectView(object):
    model = None
    template_name_base = ""
    namespace = ""
    fields = '__all__'

    def get_base_name(self):
        ns = self.template_name_base
        if not self.template_name_base:
            ns = self.model.__class__.__name__
        return ns

    def get_create_view_class(self):
        return CreateView

    def get_create_view(self):
        CreateViewClass = self.get_create_view_class()

        class OCreateView(CreateViewClass):
            name_urls = self.get_name_urls()

            def get_context_data(self, **kwargs):
                context = super(OCreateView, self).get_context_data(**kwargs)
                context['name_urls'] = self.name_urls
                return context
        return OCreateView

    def get_edit_view_class(self):
        return UpdateView

    def get_edit_view(self):
        EditViewClass = self.get_edit_view_class()

        class OEditView(EditViewClass):
            name_urls = self.get_name_urls()

            def get_context_data(self, **kwargs):
                context = super(OEditView, self).get_context_data(**kwargs)
                context['name_urls'] = self.name_urls
                return context
        return OEditView

    def __init__(self):
        tnb = self.get_base_name()
        OCreateView = self.get_create_view()
        self.create = login_required(OCreateView.as_view(
            model=self.model,
            fields=self.fields,
            success_url=reverse_lazy(self.namespace + ':objectview_list'),
            template_name=tnb + "_form.html"
        ))

        OUpdateView = self.get_edit_view()
        self.edit = login_required(OUpdateView.as_view(
            model=self.model,
            fields=self.fields,
            success_url=reverse_lazy(self.namespace + ':objectview_list'),
            template_name=tnb + "_form.html"
        ))

        self.delete = login_required(DeleteView.as_view(
            model=self.model,
            success_url=reverse_lazy(self.namespace + ':objectview_list'),
            template_name=tnb + "_delete.html"
        ))

        OListView = self.get_list_view()
        self.list = login_required(OListView.as_view(
            model=self.model,
            paginate_by=10,
            template_name=tnb + "_list.html"
        ))

    def get_list_view_class(self):
        return ListView

    def get_list_view(self):
        OListViewClass = self.get_list_view_class()

        class OListView(OListViewClass):
            name_urls = self.get_name_urls()

            def get_context_data(self, **kwargs):

                context = super(OListView, self).get_context_data(**kwargs)
                context['name_urls'] = self.name_urls
                return context
        return OListView

    def get_name_urls(self):
        return {
            'add': self.namespace + ":objectview_create",
            'edit': self.namespace + ":objectview_update",
            'delete': self.namespace + ":objectview_delete",
            'list': self.namespace + ":objectview_list"
        }

    def get_urls(self):
        return [
            url(r"^list$", self.list, name="objectview_list"),
            url(r"^create$", self.create, name="objectview_create"),
            url(r"^edit/(?P<pk>\d+)$", self.edit, name="objectview_update"),
            url(r"^delete/(?P<pk>\d+)$", self.delete,
                name="objectview_delete"),
        ]


class UserObjectView(ObjectView):

    def get_create_view_class(self):
        class UCreateView(CreateView):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
        return UCreateView

    def get_edit_view_class(self):
        class UUpdateView(UpdateView):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
        return UUpdateView

    def get_list_view_class(self):
        class UListView(ListView):

            def get_queryset(self):
                queryset = super(UListView, self).get_queryset()
                queryset = queryset.filter(user=self.request.user)
                return queryset
        return UListView
