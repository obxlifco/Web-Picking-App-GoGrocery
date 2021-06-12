from rest_framework import pagination
from rest_framework.response import Response
import math
from webservices.models import EngageboostGlobalSettings
from webservices.serializers import GlobalsettingsSerializer

class CustomPagination(pagination.PageNumberPagination):
	
	settings = EngageboostGlobalSettings.objects.filter(isdeleted='n',isblocked='n',website_id=1).first()
	if settings:
		page_size = settings.itemlisting_backend
	else:
		page_size = 15
		
	def paginate_queryset(self, queryset, request, view=None):
		"""
		Paginate a queryset if required, either returning a
		page object, or `None` if pagination is not configured for this view.
		"""
		page_size = self.get_page_size(request)
		if not page_size:
			return None

		paginator = self.django_paginator_class(queryset, page_size)
		page_number = request.query_params.get(self.page_query_param, 1)
		if page_number in self.last_page_strings:
			page_number = paginator.num_pages

		try:
			self.page = paginator.page(page_number)
		except InvalidPage as exc:
			msg = self.invalid_page_message.format(
				page_number=page_number, message=six.text_type(exc)
			)
			raise NotFound(msg)

		if paginator.num_pages > 1 and self.template is not None:
			# The browsable API should display pagination controls.
			self.display_page_controls = True

		self.request = request
		return list(self.page)

	def get_page_size(self, request):
		settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
		size=settings.itemlisting_backend

		return size	

	def get_paginated_response(self, data):

		settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
		size=settings.itemlisting_backend

		page_size = size
		
		return Response({
			'links': {
			   'next': self.get_next_link(),
			   'previous': self.get_previous_link()
			},
			'count': self.page.paginator.count,
			'per_page_count': math.ceil(self.page.paginator.count/page_size),
			'page_size':page_size,
			'results': data
		})

	def get_paginated_response_elastic(self, data):

		settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
		size=settings.itemlisting_backend

		page_size = size
		
		return Response({
			'links': {
			   'next': self.get_next_link(),
			   'previous': self.get_previous_link()
			},
			'count': self.page.paginator.count,
			'per_page_count': math.ceil(self.page.paginator.count/page_size),
			'page_size':page_size,
			'results': data
		})	
