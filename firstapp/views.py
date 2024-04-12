from django.shortcuts import render,HttpResponse

from django.views.generic import TemplateView,FormView,CreateView

from django.core.exceptions import ValidationError


from django.urls import reverse_lazy, reverse
# def index(request):
#     return render(request,'firstapp/index.html')
    
from . forms import ContactUsForm,RegistrationForm
class Index(TemplateView):
    template_name='firstapp/index.html'
    def get_context_data(self,**kwargs):
        age = 10
        arr = ['adksk', 'gasdgas', 'agdsgads']
        context = {'age': age, 'array': arr}
        return context

def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST['phone']
        if len(phone)<10 or len(phone)>10:
            raise ValidationError("Phone number length is not right")
        query = request.POST['query']
        print(name + " " + email + " " + phone + " " +query)
    return render(request, 'firstapp/contactus.html')

def contactus2(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():      #clean_data
            if len(form.cleaned_data.get('query'))>10:
                form.add_error('query', 'Query length is not right')
                return render(request, 'firstapp/contactus2.html', {'form':form})
            form.save()
            return HttpResponse("Thank YOu")
        else:
            if len(form.cleaned_data.get('query'))>10:
                #form.add_error('query', 'Query length is not right')
                form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
            return render(request, 'firstapp/contactus2.html', {'form':form})
    return render(request, 'firstapp/contactus2.html', {'form':ContactUsForm})

class ContanctUs(FormView):
    form_class = ContactUsForm
    template_name = 'firstapp/contactus2.html'
    # success_url = '/home/'
    success_url = reverse_lazy('index')


    def form_valid(self,form):
        if len(form.cleaned_data.get('query'))>10:
                form.add_error('query', 'Query length is not right')
                return render(request, 'firstapp/contactus2.html', {'form':form})
        form.save()
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            #form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
        response = super().form_invalid(form)
        return response
        


class RegisterView(CreateView):
    template_name = 'firstapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

