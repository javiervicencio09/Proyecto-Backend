def user_role_context(request):
    if not request.user.is_authenticated:
        return {
            'user_role': None,
            'es_admin': False,
            'es_supervisor': False,
            'es_administrativo': False,
        }

    user = request.user
    user_groups = set(user.groups.values_list('name', flat=True))

    is_admin = user.is_superuser or ('Administrador' in user_groups)
    is_supervisor = ('Supervisor' in user_groups)
    is_administrativo = ('Administrativo' in user_groups)

    if is_admin:
        role_name = 'Administrador'
    elif is_supervisor:
        role_name = 'Supervisor'
    elif is_administrativo:
        role_name = 'Administrativo'
    else:
        role_name = 'Sin Rol'

    return {
        'user_role': role_name,
        'es_admin': is_admin,
        'es_supervisor': is_supervisor or is_admin,
        'es_administrativo': is_administrativo or is_supervisor or is_admin,
    }

