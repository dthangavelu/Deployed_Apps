from django.conf.urls import url
from .views import *

urlpatterns = [	
	url(r'^$', index),	
	url(r'^login/$', login),
	url(r'^register/$', register_user),
	url(r'^logout/$', logout),
	url(r'^poke_dashboard$', poke_dashboard),
	url(r'^pokes/(?P<id>\d+)/$', pokes),
	# url(r'^users/$', index),
	# url(r'^users/new$', display_new_user_page),	
	# url(r'^users/create$', create_new_user_db),	
	# url(r'^users/(?P<id>\d+)/$', display_user_by_id),	
	# url(r'^users/(?P<id>\d+)/destroy$', delete_user_by_id),	
	# url(r'^users/(?P<id>\d+)/edit$', display_edit_user_by_id_page),	
]



