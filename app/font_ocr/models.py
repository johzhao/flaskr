from .. import db


class FontRecord(db.Model):
    __tablename__ = 'font_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(8), nullable=False)
    text = db.Column(db.String(1), nullable=False, index=True, default='')
