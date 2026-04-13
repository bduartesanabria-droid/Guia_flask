from app import db

class Perfil(db.Model):
    __tablename__ = 'perfiles'
    idPerfil = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idUser'), nullable=False)
    user = db.relationship('User', back_populates='perfil')

    def __repr__(self):
        return f'<Perfil {self.idPerfil}>'
