from app import db

# 🔗 tabla intermedia (muchos a muchos)
publicacion_etiqueta = db.Table(
    'publicacion_etiqueta',
    db.Column('publicacion_id', db.Integer, db.ForeignKey('publicaciones.id')),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiquetas.id'))
)

class Publicacion(db.Model):
    __tablename__ = 'publicaciones'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.idUser'), nullable=False)

    # relación con usuario
    user = db.relationship('User', back_populates='publicaciones')

    # relación con etiquetas
    etiquetas = db.relationship(
        'Etiqueta',
        secondary=publicacion_etiqueta,
        back_populates='publicaciones'
    )      