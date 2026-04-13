from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models.publicacion import Publicacion
from app.models.etiqueta import Etiqueta
from app import db

bp = Blueprint('publicacion', __name__, url_prefix='/post')
@bp.route('/etiqueta/<string:nombre>')
def por_etiqueta(nombre):
    etiqueta = Etiqueta.query.filter_by(nombre=nombre).first_or_404()

    publicaciones = etiqueta.publicaciones

    return render_template(
        'posts/por_etiqueta.html',
        etiqueta=etiqueta,
        publicaciones=publicaciones
    )
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']

        # 🔥 usar usuario logueado
        user_id = current_user.idUser

        nueva = Publicacion(
            titulo=titulo,
            contenido=contenido,
            user_id=user_id
        )

        # 🔥 etiquetas desde texto (ej: python, flask)
        etiquetas_texto = request.form['etiquetas']
        lista = etiquetas_texto.split(',')

        for nombre in lista:
            nombre = nombre.strip()

            if nombre:  # evita vacíos
                etiqueta = Etiqueta.query.filter_by(nombre=nombre).first()

                if not etiqueta:
                    etiqueta = Etiqueta(
                        nombre=nombre,
                        slug=nombre.lower()
                    )
                    db.session.add(etiqueta)

                nueva.etiquetas.append(etiqueta)

        db.session.add(nueva)
        db.session.commit()

        return redirect(url_for('perfil.index'))  # puedes cambiar esto si quieres

    return render_template('posts/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Publicacion.query.get_or_404(id)
    if post.user_id != current_user.idUser:
        return redirect(url_for('perfil.index'))

    if request.method == 'POST':
        post.titulo = request.form['titulo']
        post.contenido = request.form['contenido']
        db.session.commit()
        return redirect(url_for('perfil.mi_perfil'))

    return render_template('posts/edit.html', post=post)

@bp.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post = Publicacion.query.get_or_404(id)
    if post.user_id == current_user.idUser:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('perfil.mi_perfil'))