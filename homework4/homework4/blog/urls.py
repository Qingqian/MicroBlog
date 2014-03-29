from django.conf.urls import patterns, url
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
			url(r'^$', 'blog.views.main',name='home'),
			url(r'^managePost','blog.views.manage', name='manage'),
			url(r'^blogger-list','blog.views.blogger_list', name='list'),
			url(r'^blogger-page/(?P<username>[a-zA-Z0-9_@\+\-\.]+)','blog.views.blogger_page', name='page'),
			url(r'^follow/(?P<username>[a-zA-Z0-9_@\+\-\.]+)','blog.views.follow', name='follow'),
			url(r'^addPost','blog.views.add_post', name='add'),
			url(r'^deletePost/(?P<id>\d+)$', 'blog.views.delete_post', name = 'delete'),
			url(r'^photo/(?P<id>\d+)$', 'blog.views.get_photo', name='photo'),
			url(r'^login$', 'django.contrib.auth.views.login' , {'template_name':'blog/login.html'}, name='login'),
			url(r'^logout$','django.contrib.auth.views.logout_then_login', name='logout'),
			url(r'^register$','blog.views.register',name='register'),
            url(r'^confirm/(?P<username>[a-zA-Z0-9_@\+\-\.]+)/(?P<token>[a-z0-9\-]+)$','blog.views.register_confirm', name='confirm'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
