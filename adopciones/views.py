from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistroForm, PersonaForm, MascotaForm, AdopcionForm
from .models import Persona, Mascota, Adopcion, Organizacion
from django.db.models import Count
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import os



def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f"Usuario {username} registrado correctamente.")
            return redirect('persona_list')
    else:
        form = RegistroForm()
    return render(request, 'adopciones/registro.html', {'form': form})


@login_required
def persona_list(request):
    personas = Persona.objects.all()
    return render(request, 'adopciones/persona_list.html', {'personas': personas})

@login_required
def persona_create(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Persona registrada correctamente.")
            return redirect('persona_list')
    else:
        form = PersonaForm()
    return render(request, 'adopciones/persona_form.html', {'form': form})

@login_required
def persona_update(request, id):
    persona = get_object_or_404(Persona, id=id)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, "Persona actualizada correctamente.")
            return redirect('persona_list')
    else:
        form = PersonaForm(instance=persona)
    return render(request, 'adopciones/persona_form.html', {'form': form})

@login_required
def persona_delete(request, id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    messages.success(request, "Persona eliminada correctamente.")
    return redirect('persona_list')



@login_required
def mascota_list(request):
    mascotas = Mascota.objects.all()
    return render(request, 'adopciones/mascota_list.html', {'mascotas': mascotas})

@login_required
def mascota_create(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota registrada correctamente.")
            return redirect('mascota_list')
    else:
        form = MascotaForm()
    return render(request, 'adopciones/mascota_form.html', {'form': form})

@login_required
def mascota_update(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
           
            if 'foto' in request.FILES and mascota.foto:
                if os.path.isfile(mascota.foto.path):
                    os.remove(mascota.foto.path)
            form.save()
            messages.success(request, "Mascota actualizada correctamente.")
            return redirect('mascota_list')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'adopciones/mascota_form.html', {'form': form})

@login_required
def mascota_delete(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if mascota.foto and os.path.isfile(mascota.foto.path):
        os.remove(mascota.foto.path)
    mascota.delete()
    messages.success(request, "Mascota eliminada correctamente.")
    return redirect('mascota_list')


@login_required
def adopcion_list(request):
    adopciones = Adopcion.objects.select_related('persona', 'mascota').all()
    return render(request, 'adopciones/adopcion_list.html', {'adopciones': adopciones})

@login_required
def adopcion_create(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST)
        if form.is_valid():
            adopcion = form.save()
            adopcion.mascota.adoptada = True
            adopcion.mascota.save()
            messages.success(request, "Adopción registrada correctamente.")
            return redirect('adopcion_list')
    else:
        form = AdopcionForm()
    return render(request, 'adopciones/adopcion_form.html', {'form': form})

@login_required
def adopcion_delete(request, id):
    adopcion = get_object_or_404(Adopcion, id=id)

    adopcion.mascota.adoptada = False
    adopcion.mascota.save()
    adopcion.delete()
    messages.success(request, "Adopción eliminada correctamente.")
    return redirect('adopcion_list')



@login_required
def reportes(request):
    total_adopciones = Adopcion.objects.count()

    especies = (
        Mascota.objects
        .values_list('especie')
        .annotate(total=Count('adopcion'))
        .order_by('-total')
    )

    labels = [e[0] for e in especies]
    data = [e[1] for e in especies]

    if 'excel' in request.GET:
        df = pd.DataFrame(list(especies), columns=['Especie', 'Total'])
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reporte_adopciones.xlsx"'
        df.to_excel(response, index=False)
        return response

    if 'pdf' in request.GET:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        try:
            logo_path = os.path.join(settings.BASE_DIR, 'adopciones', 'static', 'img', 'logo.png')

            if os.path.exists(logo_path):
                elements.append(Image(logo_path, width=60, height=60))

        except:
            pass

        elements.append(Paragraph("<b>Reporte de Adopciones</b>", styles["Title"]))
        elements.append(Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), styles["Normal"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>Total Adopciones:</b> {total_adopciones}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        data_table = [["Especie", "Total"]] + [[e[0], e[1]] for e in especies]
        table = Table(data_table, colWidths=[250, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007bff")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        elements.append(table)

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_adopciones.pdf"'
        response.write(pdf)
        return response

    return render(request, 'adopciones/reportes.html', {
        'total_adopciones': total_adopciones,
        'especies': especies,
        'labels': labels,
        'data': data
    })

# Lista de Organizaciones

def listarOrganizacion(request):
    organizaciones = Organizacion.objects.all()
    return render(request, "adopciones/organizacion/listarorganiza.html", {
        'organizaciones': organizaciones
    })

def nuevaOrganizacion(request):
    return render(request, "adopciones/organizacion/nuevoorganiza.html")

def guardarOrganizacion(request):
    nombre = request.POST["nombre"]
    ruc = request.POST["ruc"]
    direccion = request.POST["direccion"]
    telefono = request.POST.get("telefono", "")
    correo = request.POST.get("correo", "")
    representante = request.POST.get("representante", "")

    Organizacion.objects.create(
        nombre=nombre,
        ruc=ruc,
        direccion=direccion,
        telefono=telefono,
        correo=correo,
        representante=representante
    )

    messages.success(request, "La organización ha sido GUARDADA correctamente")
    return redirect('/listarOrganizacion')

def eliminarOrganizacion(request, id):
    organizacion = Organizacion.objects.get(id=id)
    organizacion.delete()
    messages.success(request, "La organización ha sido ELIMINADA correctamente")
    return redirect('/listarOrganizacion')

def editarOrganizacion(request, id):
    organizacion = Organizacion.objects.get(id=id)
    return render(request, "adopciones/organizacion/editarorganiza.html", {
        'organizacion': organizacion
    })

def procesarEdicionOrganizacion(request):
    id = request.POST["id"]
    nombre = request.POST["nombre"]
    ruc = request.POST["ruc"]
    direccion = request.POST["direccion"]
    telefono = request.POST.get("telefono", "")
    correo = request.POST.get("correo", "")
    representante = request.POST.get("representante", "")

    organizacion = Organizacion.objects.get(id=id)
    organizacion.nombre = nombre
    organizacion.ruc = ruc
    organizacion.direccion = direccion
    organizacion.telefono = telefono
    organizacion.correo = correo
    organizacion.representante = representante

    organizacion.save()
    messages.success(request, "La organización ha sido ACTUALIZADA exitosamente")
    return redirect('/listarOrganizacion')
