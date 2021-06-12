# #import geocoder
# class CommonFunctionality:
# 	def __init__(self):
# 		pass

# 	@staticmethod
# 	def get_lat_lng_by_ip(ipaddress):
# 		"""
# 			Get latitude and longitude by ip address
# 		"""
# 		# print("**************** ipaddress from method **************")
# 		# print(ipaddress)
# 		g = geocoder.ip('182.71.170.222')
# 		print(g)
# 		return g.latlng
	
# 	@staticmethod
# 	def get_client_ip(request):
# 		"""
# 		  Getting client ip address by request
# 		  access static
# 		"""
# 		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# 		if x_forwarded_for:
# 			ip = x_forwarded_for.split(',')[0]
# 		else:
# 			ip = request.META.get('REMOTE_ADDR')
# 		return ip

