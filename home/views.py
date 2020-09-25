from django.shortcuts import render
from django.views import View

# Create your views here.
class PrincipalView(View):
	template_name = 'principal.html'
	context = {'title': 'Principal'}

	def get(self, request):
		return render(request, self.template_name, self.context)
