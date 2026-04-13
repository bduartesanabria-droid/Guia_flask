from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.perfil import Perfil
from app.models.users import User
from app import db

bp = Blueprint('perfil', __name__, url_prefix='/perfil')

@bp.route('/')
@login_required
def index():
    # Mostrar perfiles de todos los usuarios o solo del usuario actual
    perfiles = Perfil.query.all()
    return render_template('perfil/index.html', perfiles=perfiles)

@bp.route('/mi-perfil')
@login_required
def mi_perfil():
    # Mostrar el perfil del usuario actual
    perfil = Perfil.query.filter_by(user_id=current_user.idUser).first()
    if not perfil:
        # Si no tiene perfil, redirigir a crear uno
        return redirect(url_for('perfil.add'))
    return render_template('perfil/detail.html', perfil=perfil)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # Verificar si el usuario ya tiene un perfil
    existing_perfil = Perfil.query.filter_by(user_id=current_user.idUser).first()
    if existing_perfil:
        flash('Ya tienes un perfil creado. Puedes editarlo.', 'warning')
        return redirect(url_for('perfil.edit', id=existing_perfil.idPerfil))

    if request.method == 'POST':
        bio = request.form.get('bio', '')

        new_perfil = Perfil(
            bio=bio,
            user_id=current_user.idUser
        )
        db.session.add(new_perfil)
        db.session.commit()

        flash('Perfil creado exitosamente.', 'success')
        return redirect(url_for('perfil.mi_perfil'))

    return render_template('perfil/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    perfil = Perfil.query.get_or_404(id)

    # Verificar que el perfil pertenece al usuario actual
    if perfil.user_id != current_user.idUser:
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('perfil.index'))

    if request.method == 'POST':
        perfil.bio = request.form.get('bio', '')
        db.session.commit()

        flash('Perfil actualizado exitosamente.', 'success')
        return redirect(url_for('perfil.mi_perfil'))

    return render_template('perfil/edit.html', perfil=perfil)

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    perfil = Perfil.query.get_or_404(id)
    return render_template('perfil/detail.html', perfil=perfil)