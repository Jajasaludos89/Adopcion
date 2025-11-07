from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/register/', views.registro, name='registro'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='adopciones/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.persona_list, name='persona_list'),
    path('personas/', views.persona_list, name='persona_list'),
    path('personas/nueva/', views.persona_create, name='persona_create'),
    path('personas/editar/<int:id>/', views.persona_update, name='persona_update'),
    path('personas/eliminar/<int:id>/', views.persona_delete, name='persona_delete'),

    path('mascotas/', views.mascota_list, name='mascota_list'),
    path('mascotas/nueva/', views.mascota_create, name='mascota_create'),
    path('mascotas/editar/<int:id>/', views.mascota_update, name='mascota_update'),
    path('mascotas/eliminar/<int:id>/', views.mascota_delete, name='mascota_delete'),

    path('adopciones/', views.adopcion_list, name='adopcion_list'),
    path('adopciones/nueva/', views.adopcion_create, name='adopcion_create'),
    path('adopciones/eliminar/<int:id>/', views.adopcion_delete, name='adopcion_delete'),

    path('reportes/', views.reportes, name='reportes'),

    # --- Organizaciones (nuevas) ---
    path('organizaciones/', views.listarOrganizacion, name='listarOrganizacion'),
    path('organizaciones/nueva/', views.nuevaOrganizacion, name='nuevaOrganizacion'),
    path('organizaciones/guardar/', views.guardarOrganizacion, name='guardarOrganizacion'),
    path('organizaciones/editar/<int:id>/', views.editarOrganizacion, name='editarOrganizacion'),
    path('organizaciones/procesarEdicion/', views.procesarEdicionOrganizacion, name='procesarEdicionOrganizacion'),
    path('organizaciones/eliminar/<int:id>/', views.eliminarOrganizacion, name='eliminarOrganizacion'),
]
