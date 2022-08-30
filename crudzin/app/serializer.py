from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError
from model import Book

ma = Marshmallow()


def configure(app):
    ma.init_app(app)
    

class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book

    livro = fields.Str(required=True)
    escritor = fields.Str(required=True)
