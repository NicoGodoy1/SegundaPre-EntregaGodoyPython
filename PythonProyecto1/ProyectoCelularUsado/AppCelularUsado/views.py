from django.shortcuts import render
from django.http import HttpResponse
from AppCelularUsado.models import *
from AppCelularUsado.forms import *
from django.views.generic import ListView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from AppCelularUsado.forms import UserRegisterForm, UserEditForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


# Create your views here.
# def celular(self):

#     celular= Celular(nombre="motoPRUEBA", precio=111111, vendido= False)
#     celular.save()

#     documentodeTexto = f'-----Celular: {celular.nombre} Precio: {celular.precio} Vendido: {celular.vendido}'
    
#     return HttpResponse(documentodeTexto)

# @login_required
# def agregarAvatar(request):
#     avatares = Avatar.objects.filter(user=request.user.id)
#     if request.method == 'POST':
#         miFormulario = AvatarFormulario(request.POST, request.FILES )
#         if miFormulario.is_valid():
#             u = User.objects.get(username=request.user)
#             avatar = Avatar(user=u, imagen=miFormulario.cleaned_data['imagen'])
#             avatar.save()

#             return render(request, 'inicio.html')
#     else:
#         miFormulario = AvatarFormulario()
#     return render(request, 'agregarAvatar.html', {'miFormulario': miFormulario,'url': avatares[0].imagen.url})


@login_required
def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, 'inicio.html', {'url': avatares[0].imagen.url})


# def inicio(request):
#     return render(request, 'inicio.html')

def celular(request):
    return render(request, 'celular.html')

def usuario(request):
    return render(request, 'usuarios.html')

def comentarios(request):
    return render(request, 'comentarios.html')

@login_required
def agregarProducto(request):

    avatares = Avatar.objects.filter(user=request.user.id)
    # fotos = Producto.objects.filter(Producto.imagen)
    
    if request.method == 'POST':
        miFormulario = ProductoFormulario(request.POST, request.FILES)
        print(miFormulario)
        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data
            celular = Producto(nombre=informacion['nombre'], precio=informacion['precio'], imagen=miFormulario.cleaned_data['imagen'] )
            celular.save()
        
            return render(request, 'inicio.html')
    else:
        miFormulario = ProductoFormulario()

    return render(request, 'agregarProducto.html', {'miFormulario': miFormulario,'url': avatares[0].imagen.url})

@login_required
def agregarAvatar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == 'POST':
        miFormulario = AvatarFormulario(request.POST, request.FILES )
        if miFormulario.is_valid():
            u = User.objects.get(username=request.user)
            avatar = Avatar(user=u, imagen=miFormulario.cleaned_data['imagen'])
            avatar.save()

            return render(request, 'inicio.html')
    else:
        miFormulario = AvatarFormulario()
    return render(request, 'agregarAvatar.html', {'miFormulario': miFormulario,'url': avatares[0].imagen.url})

def crearUsuario(request):

    if request.method == 'POST':

        miFormulario = UsuarioFormulario(request.POST)
    
        print(miFormulario)

        if miFormulario.is_valid:
    
            informacion = miFormulario.cleaned_data
    
            usuario = Usuario(nombre=informacion['nombre'], apellido=informacion['apellido'],edad=informacion['edad'],email=informacion['email'])
    
            usuario.save()
        
            return render(request, 'usuarioCreadoExito.html')
    else:
        miFormulario = UsuarioFormulario()

    return render(request, 'agregarUsuario.html', {'miFormulario': miFormulario})

def usuarioCreadoExito(request):
    return render(request, 'usuarioCreadoExito.html')

def buscarCelular(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, 'buscarCelular.html', {'url': avatares[0].imagen.url})

def buscar(request):
    # respuesta = f"Estoy buscando el celular por nombre: {request.GET['nombre'] }"
    avatares = Avatar.objects.filter(user=request.user.id)

    if request.GET["nombre"]:

        # respuesta = f"Estoy buscando el celular por nombre: {request.GET['nombre'] }"
        nombre = request.GET['nombre']
        productos = Producto.objects.filter(nombre__icontains= nombre)

        return render(request, 'resultadosPorBusqueda.html', { "productos": productos, "nombre": nombre, 'url': avatares[0].imagen.url})
    else:
        respuesta = 'No enviaste bien los datos'

    return HttpResponse(respuesta, {'url': avatares[0].imagen.url})

def mostrarCelulares(request):
    productos = Producto.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    contexto = {"productos": productos,'url': avatares[0].imagen.url }

    return render(request, 'mostrarCelulares.html', contexto )


@login_required
def editarProducto(request, producto_nombre):
    producto = Producto.objects.get(nombre=producto_nombre)
    # if producto.user != request.user:
    #     return HttpResponseForbidden()
    if request.method == 'POST':
        miFormulario = ProductoFormulario(request.POST)
        print(miFormulario)

        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data

            producto.nombre = informacion['nombre']
            producto.precio = informacion['precio']

            producto.save()

            return render(request, "inicio.html")
    else:
        miFormulario = ProductoFormulario(initial={'nombre': producto.nombre, 'precio': producto.precio})

        return render(request, "editarProducto.html", {"miFormulario": miFormulario, 'producto_nombre': producto_nombre})

@login_required
def eliminarProducto(request, producto_nombre):
    producto = Producto.objects.get(nombre= producto_nombre)
    producto.delete()

    productos = Producto.objects.all()

    contexto = {"productos": productos}
    return render(request, "mostrarCelulares.html", contexto)

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)
            if user is not None:
                login(request, user)
                return render(request, "inicio.html", {"mensaje": f"Bienvenido {usuario}"})
            else: 
                return render(request, "inicio.html", {"mensajeNegativo": "Error, datos incorrectos."})
            
        else:
            return render(request, "inicio.html", {"mensajeNegativo": "Error, formulario erroneo."})
    form = AuthenticationForm()
    # avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "login.html", {"form": form})

def register(request):

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)

        form  = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return render(request, 'inicio.html', {'mensaje': 'Usuario Creado :)' })
    else: 
        # form =  UserCreationForm()
        form =  UserRegisterForm()

    return render(request, 'registro.html', {'form': form})


def carrito(request):
    return render(request, 'carrito.html')

def acercaDeMi(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, 'acercaDeMi.html', {'url': avatares[0].imagen.url})



def editarPerfil(request):
    usuario = request.user
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST)
        print(miFormulario)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            print(miFormulario)
            usuario.email = informacion['email']
            usuario.first_name = informacion['first_name']
            usuario.last_name = informacion['last_name']
            if informacion['password1'] == informacion['password2']:
                usuario.password = make_password(informacion['password1'])
                usuario.save()
            else:
                return render(request, 'inicio.html', {'mensaje': 'Contraseña incorrecta.'})    
            
            return render(request, 'inicio.html')
    else:
        miFormulario = UserEditForm(initial={'email': usuario.email})
    
    return render (request, 'editarPerfil.html', {'miFormulario': miFormulario, 'usuario': usuario, 'url': avatares[0].imagen.url})

class ProductoList(ListView):
    model = Producto
    template_name = "producto_list.html"

class ProductoDetalle(DetailView):
    model = Producto
    template_name = "producto_detalle.html"

class ProductoCreacion(CreateView):
    model = Producto
    template_name = "productos_form.html"
    success_url = reverse_lazy("List")
    fields = ['nombre', 'precio', "imagen"]

class ProductoUpdate(UpdateView):
    model = Producto
    success_url = "producto/list"
    template_name = "productos_form.html"
    fields = ['nombre', 'precio']

class ProductoDelete(DeleteView):
    model = Producto
    template_name = "producto_confirm_delete.html"
    success_url = "producto/list"


# @login_required
# def agregarAvatar(request):
#     if request.method == 'POST':
#         miFormulario = AvatarFormulario(request.POST, request.FILES )
#         if miFormulario.is_valid():
#             u = User.objects.get(username=request.user)
#             avatar = Avatar(user=u, imagen=miFormulario.cleaned_data['imagen'])
#             avatar.save()

#             return render(request, 'inicio.html')
#     else:
#         miFormulario = AvatarFormulario()
#     return render(request, 'agregarAvatar.html', {'miFormulario': miFormulario})


# @login_required
# def inicio(request):
#     avatares = Avatar.objects.filter(user=request.user.id)
#     return render(request, 'inicio.html', {'url': avatares[0].imagen.url})

# def resultadosPorBusqueda(request):
#     return render(request, 'resultadosPorBusqueda.html')
