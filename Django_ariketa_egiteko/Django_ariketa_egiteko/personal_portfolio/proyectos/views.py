from django.shortcuts import render, redirect
from proyectos.models import Proyecto
from proyectos.models import Pregunta
from proyectos.forms import PostForm
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def proyecto_index(request):
    proyectos = Proyecto.objects.all()

    context = {
        'proyectos': proyectos
    }
    return render(request, 'proyecto_index.html', context)

def proyecto_detail(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    context = {
        'proyecto': proyecto
    }
    return render(request, 'proyecto_detail.html', context)

def obtener_preguntas(request):
    if request.method == 'GET' and 'proyecto_id' in request.GET:
        proyecto_id = request.GET['proyecto_id']
        try:
            proyecto = Proyecto.objects.get(pk=proyecto_id)
            preguntas = Pregunta.objects.filter(proyecto=proyecto)
            # Aquí puedes personalizar cómo deseas devolver las preguntas,
            # por ejemplo, podrías devolver una lista de texto de preguntas.
            preguntas_texto = [pregunta.pregunta_texto for pregunta in preguntas]
            return JsonResponse({'galderak': preguntas_texto})
        except Proyecto.DoesNotExist:
            return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def pregunta_guardar(request, pk):
    form = PostForm(request.POST)
    if form.is_valid():
        pregunta = form.save(commit=False)
        proyecto = Proyecto.objects.get(pk=pk)
        pregunta.proyecto = proyecto
        pregunta.save()

    return redirect('proyecto_index')

def post_teknologia(request):
    post_id = request.POST.get('id')
    post_tekno = request.POST.get('tecnologia')
    print(post_id)
    print(post_tekno)
    with connection.cursor() as cursor:
        sql = "UPDATE proyectos_proyecto set tecnologia = %s where id = %s"
        cursor.execute(sql, [post_tekno, post_id])
    return JsonResponse({"id": post_id, "tecnologia": post_tekno}, status=200)