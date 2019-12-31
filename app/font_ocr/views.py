import os

from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from . import font_ocr
from .forms import FontOcrForm
from .models import FontRecord
from .. import db


@font_ocr.route('/scan')
def scan():
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

    return redirect(url_for('font_ocr.next_'))


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
        return render_template('./root.html')
