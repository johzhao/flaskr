import json
import os
from io import BytesIO

from flask import redirect, send_file
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

        record = FontRecord()
        record.code, _ = os.path.splitext(item)
        records.append(record)

    FontRecord.query.delete()
    db.session.add_all(records)
    db.session.commit()


def _export_json() -> dict:
    result = {}
    for row in db.session.query(FontRecord.code, FontRecord.text).filter(FontRecord.text != '').all():
        result[row[0]] = row[1]
    return result


@font_ocr.route('/summary', methods=['GET', 'POST'])
def summary():
    form = SummaryForm()
    if form.validate_on_submit():
        if form.scan.data:
            _scan()
            return redirect(url_for('font_ocr.summary'))

        if form.continue_.data:
            return redirect(url_for('font_ocr.next_'))

        if form.export.data:
            content = _export_json()
            json_str = json.dumps(content, ensure_ascii=False, sort_keys=True)
            file = BytesIO(json_str.encode('utf-8'))
            return send_file(file, mimetype='application/json', as_attachment=True, attachment_filename='output.json')

    done = db.session.query(func.count(FontRecord.id)).filter(FontRecord.text != '').scalar()
    total = db.session.query(func.count(FontRecord.id)).scalar()
    return render_template('./font_ocr/summary.html', form=form, done=done, total=total)


@font_ocr.route('/next', methods=['GET', 'POST'])
def next_():
    form = FontOcrForm()
    if form.validate_on_submit():
        session['font_id'] = form.id.data
        session['font_text'] = form.text.data
        return redirect(url_for('font_ocr.next_'))

    if 'font_id' in session:
        record = db.session.query(FontRecord).filter(FontRecord.id == session['font_id']).one()
        record.text = session['font_text']
        db.session.commit()
        session.pop('font_id')
        session.pop('font_text')

    record = db.session.query(FontRecord).filter(FontRecord.text == '').first()
    if record is not None:
        form.id.data = record.id
        form.text.data = record.text
        return render_template('./font_ocr/next.html', form=form,
                               image_file=url_for('static', filename=os.path.join('font_ocr', f'{record.code}.png')))
    else:
        return redirect(url_for('font_ocr.summary'))
