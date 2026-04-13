from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.users import User

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']

        # 🔍 Buscar usuario por nombre
        user = User.query.filter_by(nameUser=nameUser).first()

        # 🔐 Validar contraseña correctamente
        if user and user.check_password(passwordUser):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('perfil.mi_perfil'))

        flash('Usuario o contraseña incorrectos', 'danger')

    # Si ya está logueado, redirigir
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    return render_template("login.html")


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/pruebajs')
def pruebajs():
    import json
    example_data = {
        'title': 'Bienvenido a Flet',
        'message': 'Este es un mensaje desde Flask.'
    }
    return json.dumps(example_data)