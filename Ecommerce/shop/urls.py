from django.urls import path
from shop.views import *

# Create your views here.

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("cadastro/", register, name="register"),
    path("itens/cadastrar/", create, name="criar_item"),
    path("itens/editar/<int:id>", edit, name="editar_item"),
    path("itens/atualizar/<int:id>", update, name="atualizar_item"),
    path("itens/visualizar/<int:id>", read, name="visualizar_item"),
    path("itens/lista/", all, name="lista_item"),
    path("itens/deletar/<int:id>", delete, name="deletar_item"),
    path("logout/", logout , name="logout"), 
    path("carrinho/", carrinho, name="carrinho"),

]
