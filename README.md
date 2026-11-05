# Portal Inmobiliario Coquimbo
## Evaluación Sumativa #3 - Programación Back End (TI3041)

**Institución:** INACAP - Sede La Serena  
**Docente:** Alex Díaz Araos  
**Estudiante:** Javier Vicencio Zamora  
**Semestre:** Primavera 2026  
**Repositorio:** [https://github.com/javiervicencio09/Proyecto-Backend.git](https://github.com/javiervicencio09/Proyecto-Backend.git)

---

## 1. Descripción del Proyecto

Aplicación web desarrollada sobre **Django Framework** para la gestión inmobiliaria y atención comercial en la Región de Coquimbo. La plataforma opera de forma autónoma sin depender de Django Admin, utilizando **Django Templates** y **Bootstrap 5** para todas sus interfaces y operaciones.

### Funcionalidades Esenciales:
- **Autenticación y Seguridad:** Inicio y cierre de sesión, protección de vistas mediante decoradores y recuperación de contraseña mediante código de 5 dígitos (OTP) por correo electrónico.
- **Mantenedores CRUD:** Gestión completa de **Propiedades** y **Zonas Inmobiliarias** con búsqueda por texto y filtros dinámicos.
- **Transacción Operacional:** Módulo de **Reserva de Visitas**, relacionando en un solo acto la Propiedad, el Cliente prospecto y el Usuario que atiende, con validación de horarios y ciclo de estados.
- **Despliegue Cloud:** Operativo en **AWS EC2** con base de datos relacional y variables de entorno (`.env`).

---

## 2. Roles del Sistema y Diferenciación

El sistema cuenta con tres niveles de acceso definidos mediante grupos de Django y decoradores de permisos:

- **Administrador:** Acceso total al sistema. Es el único perfil facultado para la **Gestión de Usuarios** (crear, editar, activar y asignar roles) y el mantenedor de **Zonas Inmobiliarias**.
- **Supervisor:** Perfil de gestión y supervisión operativa. Está facultado para **administrar el catálogo de propiedades** (crear, editar y eliminar propiedades) y controlar el flujo de las citas agendadas (confirmar, realizar o cancelar visitas). No tiene acceso a la gestión de usuarios ni a la eliminación de zonas.
- **Operador (Administrativo):** Perfil de primera línea orientado a la atención al cliente. Su función primordial es la **captación y registro de nuevas reservas de visitas** y la consulta del catálogo de propiedades y zonas para brindar información. A diferencia del Supervisor, tiene **estrictamente restringida la edición o eliminación de propiedades y zonas**, protegiendo la integridad del catálogo maestro.

---

## 3. Instalación y Puesta en Marcha

```bash
# 1. Clonar el proyecto y entrar a la carpeta
git clone https://github.com/javiervicencio09/Proyecto-Backend.git
cd Proyecto-Backend

# 2. Crear y activar entorno virtual
python -m venv entorno
# En Windows:
.\entorno\Scripts\activate
# En Linux (EC2):
source entorno/bin/activate

# 3. Instalar librerías requeridas
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear roles y usuarios de demostración
python manage.py crear_roles
python manage.py crear_usuarios_demo

# 6. Ejecutar pruebas unitarias (26 tests)
python manage.py test

# 7. Iniciar el servidor local
python manage.py runserver
```

---

## 4. Usuarios de Prueba

| Usuario | Contraseña | Perfil | Alcance |
| :--- | :--- | :--- | :--- |
| `admin_demo` | `admin123` | **Administrador** | Control total, usuarios y zonas. |
| `supervisor_demo` | `super123` | **Supervisor** | Control del inventario de propiedades y visitas. |
| `operativo_demo` | `oper123` | **Operador (Administrativo)** | Registro de visitas y consultas de catálogo. |

---

## 5. Justificación y Evidencia del Uso de Inteligencia Artificial (IA)

En concordancia con los objetivos de la asignatura, se emplearon herramientas de Inteligencia Artificial como copiloto de desarrollo y soporte en la toma de decisiones técnicas, arquitectura de software y depuración de infraestructura en la nube.

### Justificación del Uso de la IA
El apoyo de la IA permitió acelerar el ciclo de desarrollo en tres ámbitos críticos:
1. **Desacoplamiento arquitectónico:** Diseñar un sistema de control de acceso por roles (RBAC) robusto sin depender del panel administrativo nativo de Django.
2. **Lógica transaccional compleja:** Estructurar validaciones cruzadas entre modelos para evitar conflictos operacionales en la reserva de citas.
3. **Resolución de problemas de despliegue:** Diagnosticar fallas a nivel de socket de red y compatibilidad entre versiones de librerías en entornos Linux/AWS EC2.

### Bitácora de Prompts y Aplicación Práctica

#### Prompt 1: Planificación y Línea de Trabajo a Seguir
- **Prompt:**
  > *"¿Qué me recomiendas revisar en el proyecto? Dame un orden de trabajo a seguir para cumplir con los requisitos de la evaluación."*
- **Respuesta de la IA:** Analizó la pauta de la evaluación y organizó una hoja de ruta por etapas: 1) Sistema de autenticación y roles con dashboards propios sin Django Admin, 2) Mantenedores CRUD con búsquedas y filtros, 3) Transacción operacional de reservas y visitas, y 4) Recuperación de contraseñas y verificación en AWS EC2.
- **Aplicación Práctica:** Sirvió como guía para estructurar el desarrollo paso a paso, priorizar funcionalidades y realizar commits incrementales limpios en GitHub.

#### Prompt 2: Creación de Roles y Dashboards Diferenciados
- **Prompt:**
  > *"¿Cómo puedo crear los tres roles de usuario (Admin, Supervisor y Administrativo) y hacer que cada uno vea un dashboard diferente?"*
- **Respuesta de la IA:** Explicó cómo utilizar los grupos de Django (`auth.Group`), crear decoradores simples para restringir el acceso a las vistas y redirigir automáticamente a cada usuario a su panel correspondiente según su rol.
- **Aplicación Práctica:** Creación de los grupos de permisos, el comando de inicialización `crear_roles` y los tres dashboards en Django Templates.

#### Prompt 3: Flujo de Recuperación de Contraseña por Código OTP
- **Prompt:**
  > *"Al abrir el enlace de recuperación en el celular no abre localhost. ¿Se puede cambiar para que en vez de un link largo llegue un código de 5 dígitos al correo y pueda ingresarlo en la pantalla?"*
- **Respuesta de la IA:** Propuso un mecanismo de verificación de 2 pasos mediante sesión cifrada: generación de un código numérico aleatorio de 5 dígitos con expiración de 15 minutos y formulario de validación para cambio de clave con `user.set_password()`.
- **Aplicación Práctica:** Implementación en `usuarios/views.py` (`solicitar_recuperacion_view` y `verificar_codigo_view`), resolviendo el flujo para dispositivos móviles y de escritorio.

#### Prompt 4: Diagnóstico y Solución del Error `[Errno 111] Connection refused` en AWS EC2
- **Prompt:**
  > *"En EC2 me sale el error: 'No se pudo enviar el correo: [Errno 111] Connection refused'. ¿Por qué ocurre este error?"*
- **Respuesta de la IA:** Diagnosticó que el entorno EC2 ejecuta Python 3.9 con Django 4.x (el cual no reconoce la directiva `MAILERS` de Django 6 y recurría a `localhost:25`). Además, identificó variables pegadas en el `.env` y el bloqueo del puerto 587 por parte de AWS, recomendando estandarizar la configuración con `EMAIL_BACKEND` y puerto 465 (SSL).
- **Aplicación Práctica:** Corrección de `config/settings.py` a parámetros universales y limpieza del archivo `.env`, logrando el despacho exitoso e inmediato de correos reales en producción.
