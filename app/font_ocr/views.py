import os

from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from sqlalchemy import func

from . import font_ocr
from .forms import FontOcrForm
from .forms import SummaryForm
from .models import FontRecord
from .. import db


@font_ocr.route('/')
def root():
    return redirect(url_for('font_ocr.summary'))


def _scan():
    records = []
    path = './app/static/font_ocr'
    for item in os.listdir(path):
        if not item.endswith('.png'):
            continue

        name, _ = os.path.splitext(item)
        record = FontRecord()
        record.code = name
        records.append(record)

    FontRecord.query.delete()
    db.session.add_all(records)
    db.session.commit()


@font_ocr.route('/summary', methods=['GET', 'POST'])
def summary():
    form = SummaryForm()
    if form.validate_on_submit():
        if form.scan.data:
            _scan()
            return redirect(url_for('font_ocr.next_'))

        if form.continue_.data:
            return redirect(url_for('font_ocr.next_'))

    done = db.session.query(func.count(FontRecord.id)).filter(FontRecord.text != '').scalar()
    total = db.session.query(func.count(FontRecord.id)).scalar()
    return render_template('./font_ocr/summary.html', form=form, done=done, total=total)


@font_ocr.route('/next', methods=['GET', 'POST'])
def next_():
    form = FontOcrForm()
    if form.validate_on_submit():
        session['font_code'] = form.code.data
        session['font_text'] = form.text.data
        return redirect(url_for('font_ocr.next_'))

    if 'font_code' in session:
        record = db.session.query(FontRecord).filter(FontRecord.code == session['font_code']).one()
        record.text = session['font_text']
        db.session.commit()

    record = db.session.query(FontRecord).filter(FontRecord.text == '').first()
    if record is not None:
        form.code.data = record.code
        form.text.data = record.text
        return render_template('./font_ocr/next.html', form=form,
                               image_file=url_for('static', filename=os.path.join('font_ocr', f'{record.code}.png')))
    else:
        return redirect(url_for('font_ocr.summary'))
