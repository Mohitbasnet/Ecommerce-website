from django.shortcuts import render,HttpResponse

from django.views.generic import TemplateView



# def index(request):
#     return render(request,'firstapp/index.html')
    

class Index(TemplateView):
    template_name='firstapp/index.html'
    def get_context_data(self,**kwargs):
        age = 10
        arr = ['adksk', 'gasdgas', 'agdsgads']
        context = {'age': age, 'array': arr}
        return context