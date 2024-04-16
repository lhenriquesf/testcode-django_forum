from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .models import CustomUser, Topic, Comment
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    TopicForm,
    CommentForm,
    EditProfileForm
)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('topics_list')

    def form_valid(self, form):
        # Autentica o usuário com as credenciais fornecidas
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
   
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Email ou senha inválidos.")
            return self.form_invalid(form)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')



class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



class TopicsListView(ListView):
    model = Topic
    template_name = 'topics_list.html'
    context_object_name = 'topics'



class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['category'] = self.object.category
        return context

# View para excluir um tópico (somente usuários com permissão de staff)
@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_topic_view(request, pk):
    if request.method == 'POST':
        topic = get_object_or_404(Topic, pk=pk)
        topic.delete()
        return redirect('topics_list')
    else:
        return redirect('topic_detail', pk=pk)

# View para excluir um comentário (somente usuários com permissão de staff)
@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_comment_view(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return redirect('topic_detail', pk=comment.topic.id)
    else:
        return redirect('topic_detail', pk=comment.topic.id)



@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        form.save()
        return redirect('topic_detail', pk=self.kwargs['pk'])



@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('topics_list')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context




@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateTopicView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'create_topic.html'
    success_url = reverse_lazy('topics_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('topics_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Atualiza a sessão para manter o usuário logado
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = self.get_form()
        return context
