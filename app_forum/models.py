from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,verbose_name='Nome')
    last_name = models.CharField(max_length=30,verbose_name='Sobrenome')
    gender = models.CharField(max_length=10, verbose_name='Gênero' ,choices=[('M', 'Masculino'), ('F', 'Feminino')], default=('N','Não informado'))
    date_of_birth = models.DateField(default='2000-01-01',verbose_name='Data de nascimento')
    date_created = models.DateTimeField(auto_now_add=True,verbose_name='Criado')
    date_updated = models.DateTimeField(auto_now=True,verbose_name='Atualizado')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','gender','date_of_birth']

    def __str__(self):
        return self.email
    


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255,verbose_name='Título')

    def __str__(self) -> str:
        return self.title



class Topic(models.Model):
    subject = models.CharField(max_length=255,verbose_name='Assunto')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name='Autor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='Categoria')
    post_date = models.DateTimeField(default=timezone.now,verbose_name='Data de publicação')
    content = models.TextField(verbose_name='Conteúdo')

    def __str__(self):
        return self.subject
    
    def get_summary(self, length=200):
        if len(self.content) > length:
            return self.content[:length] + "..."
        return self.content



class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments',verbose_name='Tópico')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name='Autor')
    content = models.TextField(verbose_name='Conteúdo')
    comment_date = models.DateTimeField(default=timezone.now,verbose_name='Data do comentário')

    def __str__(self):
        return f'{self.author}: {self.content[:20]}...'
