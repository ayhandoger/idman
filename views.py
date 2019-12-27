from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Innovator, Idea

class IndexView(generic.ListView):
	template_name = 'idman/index.html'
	context_object_name = 'latest_idea_list'

	def get_queryset(self):
		"""	Return the last five published idea (not including those set to be
		published in the future).
		"""
		return Idea.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]
			
class DetailView(generic.DetailView):
	model = Idea
	template_name = 'idman/detail.html'
	
	def get_queryset(self):
		"""
		Excludes any ideas that aren't published yet.
		"""
		return Idea.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Idea
	template_name = 'idman/results.html'

def vote(request, idea_id):
	p = get_object_or_404(Idea, pk=idea_id)
	try:
		selected_innovator = p.innovator_set.get(pk=request.POST['innovator'])
	except (KeyError, Innovator.DoesNotExist):
		# Redisplay the idea voting form.
		return render(request, 'idman/detail.html', {
			'idea': p,
			'error_message': "You didn't select an innovator.",
		})
	else:
		selected_innovator.votes += 1
		selected_innovator.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('idman:results', args=(p.id,)))