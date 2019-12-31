from flask import Blueprint

font_ocr = Blueprint('font_ocr', __name__)

from . import views
