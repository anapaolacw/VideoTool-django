import os
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import Context, Template
from apps.models import *
from apps.forms import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from lxml import etree
# Create your views here.

def home(request):
    videos = Video.objects.all()
    return render_to_response('base.html',{'videos': videos})

def quienes(request):
    return render(request, "quienes.html")

def iniciar(request):
	return render(request, "inicio.html")

def registrar(request):
	return render(request, "registro.html")

def contactar(request):
    return render(request, "contacto.html")

def vistaUsuario(request):
    videos = Video.objects.all()
    return render_to_response('vistaUsuario.html',{'videos': videos})

@csrf_exempt
def masVistos(request):
    videos = Video.objects.order_by("numeroVisto")
    orden = "Los más vistos"
    return render_to_response('base.html',{'videos': videos, 'orden':orden})

@csrf_exempt
def masBuscados(request):
    videos = Video.objects.order_by("numeroBuscado")
    orden = "Los más buscados"
    return render_to_response('base.html',{'videos': videos, 'orden':orden})

@csrf_exempt
def masRecientes(request):
    videos = Video.objects.order_by("fecha")
    orden = "Los más recientes"
    return render_to_response('base.html',{'videos': videos, 'orden':orden})

@csrf_exempt
def ordenarVistos(request):
    videos = Video.objects.order_by("numeroVisto")
    return render_to_response('vistaUsuario.html',{'videos': videos})

@csrf_exempt
def ordenarBuscados(request):
    videos = Video.objects.order_by("numeroBuscado")
    return render_to_response('vistaUsuario.html',{'videos': videos})

@csrf_exempt
def ordenarRecientes(request):
    videos = Video.objects.order_by("fecha")
    return render_to_response('vistaUsuario.html',{'videos': videos})

@csrf_exempt
def buscar(request):
    print("Buscando")
    p = request.GET.get('buscador', '')
    busqueda = Video.objects.filter(titulo__icontains=p)|Video.objects.filter(resumen__icontains=p)
    if busqueda :
        for b in busqueda:
            b.numeroBuscado = b.numeroBuscado+1
            b.save()
    return render_to_response('resultadoBusqueda.html',{'busqueda': busqueda})

def verVideo(request, id_video):
    try:
        video = Video.objects.get(id = id_video)
        video.numeroVisto = video.numeroVisto + 1
        print("Video visto")
        video.save()
        print("Se guardo")
        return render(request, 'verVideo.html', {'video':video})
    except:
        return render (request, 'verVideo.html')

def verVideoMio(request, id_video):
    try:
        video = Video.objects.get(id = id_video)
        video.numeroVisto = video.numeroVisto + 1
        print("Video visto")
        video.save()
        print("Se guardo")
        return render(request, 'verVideoMio.html', {'video':video})
    except:
        return render (request, 'verVideoMio.html')
@csrf_exempt
def busqueda(request):
    print("Buscando")
    p = request.GET.get('buscador', '')
    busqueda = Video.objects.filter(titulo__icontains=p)|Video.objects.filter(resumen__icontains=p)
    if busqueda :
        for b in busqueda:
            b.numeroBuscado = b.numeroBuscado+1
            b.save()
    return render_to_response('busqueda.html',{'busqueda': busqueda})
    
def videosSubidos(request):
    videos = Video.objects.filter(autor_id = request.session['id'])
    return render_to_response('videosSubidos.html',{'videos': videos})


def verPerfil(request):
    user = request.session['username']
    perfil = Usuario.objects.get(username = user)
    print(perfil)
    return render_to_response('perfil.html',{'perfil': perfil})

@csrf_exempt
def subir(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            titulo =request.POST.get('titulo', '')
            resumen = request.POST.get('resumen', '')
            archivo = request.FILES.get('archivo', '')
            autor = Usuario.objects.get(id = request.session['id'])
            video = Video(titulo = titulo, resumen = resumen, archivo=archivo, autor=autor)
            video.save()
            try:
                mensaje = 'Video subido'
                status= 'exito'
                form = VideoForm()
                return render(request, 'videosSubidos.html')
            except:
                print("Error al guardar")
                mensaje = 'Error al subir el video'
                status= 'error'
                return render(request, 'formVideo.html', {'form': form, 'mensaje':mensaje, 'status': status})
        else:
            print("Form invalido")
            form = VideoForm(request.POST, request.FILES)
            mensaje = 'Campos invalidos'
            return render(request, 'formVideo.html', {'form': form, 'mensaje':mensaje})
    else:
        form = VideoForm()
        print("ID usuario", request.session['id'])
        return render(request, 'formVideo.html', {'form': form})

@csrf_exempt
def accionIniciar(request):
    if request.method == 'GET':
        if request.session.get('logueado',None): 
            print("Ya estaba logueado", request.session['tipo'])
            return redirect("/vistaUsuario/")
        return render_to_response('inicio.html') #se redirigue al inicio de sesion
        print("No esta logueado")
        
    elif request.method == 'POST':
        user = request.POST.get('username','') #Podría hacerse con ['usuario'] pero si no encuentra la llave generaría un error
        password = request.POST.get('contrasena','')
        print(user,password)
        if not user or not password:
            error = 'Usuario o contraseña vacios'
            return render_to_response('inicio.html',{'error':error}) 
        try:
            usuario = Usuario.objects.get(username = user, contrasena = password) 
            request.session['logueado'] = True
            request.session['username'] = user
            request.session['id'] = usuario.id
            print("ID", request.session['id'])
            usuario = Usuario.objects.get(username=user)
            return redirect("/vistaUsuario/")
        except: 
            error = 'Usuario o contraseña inválidos'
            return render_to_response('inicio.html',{'error':error})

@csrf_exempt
def accionRegistrar(request):
    nombre = request.POST.get('nombre', '')
    username = request.POST.get('username','')
    contrasena = request.POST.get('password','')
    correo = request.POST.get('correo','')
    print(username, contrasena)
    if not nombre or not username or not correo or not contrasena:
        print("Campos vacios")
        context = {"error" : "No puede haber campos vacios"}
        return render_to_response("registro.html", context)
    try:
        usuario = Usuario(nombre = nombre, username = username, contrasena=contrasena, correo=correo)
        usuario.save()
        return redirect('/iniciar/')

    except:
        context = {"error" : "Usuario ya registrado"}
        return render_to_response("registro.html", context)

def importar(request):
    try:
        xml = os.path.join(settings.MEDIA_ROOT, 'xml/usuarios.xml')
        tree = etree.parse(xml)
        root = tree.getroot()
        elementosAgregados = 0
        for hijo in root:
            nombre = hijo[0].text 
            username = hijo[1].text
            contrasena = hijo[2].text
            correo = hijo[3].text

            usuario = Usuario(nombre = nombre, username = username, contrasena=contrasena, correo=correo)
            usuario.save()
            elementosAgregados = elementosAgregados + 1
            print("Usuario ", elementosAgregados, "registrado")
        print("Fin archivo xml")
        return render_to_response('importar.html',{'elementosAgregados': elementosAgregados})
    except:
        context = {"error" : "Archivo invalido"}
        return render_to_response('importar.html',context)

@csrf_exempt
def cerrar(request):
    request.session['logueado'] = False
    return redirect("/home")
    


