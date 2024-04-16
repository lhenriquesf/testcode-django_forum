URL: https://testcode-forum-51a7911138d7.herokuapp.com/

*Admin criado:*
    login: admin@testcode.com
    senha: User@123

*Usuários:*
    login: user1@testcode.com e user2@testcode.com
    senha: User@123


*Caso for baixar o código fonte:*
    Ativar venv:
        pipenv shell


    Para instalar as dependências:
        pipenv install

    python manage.py runserver #Criar o DB
    python manage.py makemigrations 
	python manage.py migrate #Atualizar o DB
	python manage.py runserver # Para rodar novamente


    Criação de usuário administrador (somente via comando no terminal):
        python manage.py createsuperuser

        Email: exemplo@exemplo.com
        Nome: Nome do Admin
        Sobrenome: Sobrenome do Admin
        Gênero: M ou F
        Data de nascimento: YYYY-MM-DD
        Password: ****


Uma tabela para a **Categoria** foi criada. Como não havia especificações sobre a criação de categorias, optei por mantê-las gerenciáveis através do painel de administração do Django. Dessa forma, ao criar um novo tópico, os usuários podem selecionar uma das categorias já existentes

Criada tela para **alteração de senha**


-- Teste de código.
Criar site fórum com autenticação de login.
Usar python/django versão acima de 3.1 para criar o site.

Página
- Páginas de Login *OK*
- Páginas de Visualização de tópicos *OK*
- Páginas de Cadastrar post e comentários *OK*
- Páginas de Cadastrar usuários. *OK*
- Páginas de Editar o cadastro( informações de usuários ) *OK*

Regras

- Visualizar os tópicos sem login. *OK*
- Fazer o Login ou login na hora de postar tópicos e comentários. *OK*
- No tópicos. Campos: Assunto, autor(login), categoria, data de postagem, imagem(não obrigatório), mensagens e comentários. *OK*
- No comentário, mostrar o autor. *OK*
- Ter o administrador para monitorar os post. *OK*
- No cadastro. Campos: Nome, Sobrenome, sexo, data de nascimento, e-mail(único), Data de criação e Data de alteração. *OK*
- Autenticação deve ser de uma tabela de usuário que não seja do admin django. *OK*
