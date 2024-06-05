from django.shortcuts import redirect, render, get_object_or_404
from shop.models import  *
from shop.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    if request.method == "GET":
        return render(request, 'site/cadastro.html')
    else: 
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()
        
        if user:
            messages.error(request, "Usuari já existe")
            return render(request, "site/cadastro.html")
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect(login)


def login(request):
    if request.method == "GET":
        return render(request, "site/login.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(username=username, password=senha)
        
        if user:

            login_django(request, user)
            messages.success(request, 'Usuário logado com sucesso!')
            return redirect(index)
        
        else:
            messages.error(request, "Nome ou senha invalidos")
            return redirect(register)
        
def logout(request):
    auth.logout(request)
    messages.success(request, 'Usuário Deslogado!')
    return redirect(login)



def index(request):
    produtos = Product.objects.all()
    return render(request, 'site/index.html', {"itens": produtos})

@login_required
def create(request):
    form = ProductForm
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'item cadastrada com sucesso!')
            return redirect('index')
        
    return render(request, "site/cadastro_item.html", {"forms":form})

# def create_cart(request):
#     id_user = request.user.id
#     cart, created = Cart.objects.get_or_create(user_id=id_user, is_active=True, defaults={'created_at': datetime.now()})
#     if not created:
#         cart.created_at = datetime.now()
#         cart.save()
#     return cart
    
# @login_required
# def addcarrinho(request, id):
#     cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
#     product = get_object_or_404(Product, id=id)
    
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     messages.success(request, f'{product.name} adicionado ao carrinho!')
#     return redirect('carrinho')

# @login_required
# def carrinho(request):
#     cart = Cart.objects.filter(user=request.user, is_active=True).first()
#     items = CartItem.objects.filter(cart=cart) if cart else []
#     return render(request, "site/carrinho.html", {"items": items})

@login_required
def edit(request, id):
    item = Product.objects.get(pk=id)
    form = ProductForm(instance=item)
    return render(request, "site/update.html",{"form":form, "item":item})

@login_required
def update(request, id):
    try:
        if request.method == "POST":
            item = Product.objects.get(pk=id)
            form = ProductForm(request.POST, request.FILES, instance=item)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'item foi alterada com sucesso!')
                return redirect('index')
    except Exception as e:
        messages.error(request, e)
        return redirect('index')

@login_required
def read(request, id):
    item = Product.objects.get(pk=id)
    return render(request, "site/read.html", {"item": item})


@login_required
def all(request):
    return render(request, "site/lista.html", {"itens": Product.objects.all()})



@login_required
def delete(request, id):
    item = Product.objects.get(pk=id)
    item.delete()
    messages.success(request, 'item foi deletada com sucesso!')
    return redirect('index')

