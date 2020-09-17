from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import os
from flask_login import login_required, current_user
from website import app, db
from secrets import token_urlsafe
from .utils import make_meme as util_make
from .forms import Template
from website.models import MemeStats, User, MemeTemplate
from datetime import datetime
from werkzeug.utils import secure_filename

memes = Blueprint('memes', __name__)


@memes.route('/templates', methods=['GET', 'POST'])
@login_required
def memes_templates():
    form = Template()
    templates = MemeTemplate.query.all()
    if form.validate_on_submit():
        file = form.image.data
        file_name = secure_filename(file.filename)
        new_name = token_urlsafe(10) + '.' + file_name.split('.')[-1]
        template_name = form.name.data
        template = MemeTemplate(name=template_name, file_name=new_name, uploaded_by=current_user.id)
        db.session.add(template)
        db.session.commit()
        path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        file.save(path)
        flash('New Template has been added!', 'success')
        return redirect(url_for('memes.memes_templates'))

    return render_template('memestemps.html', templates=templates, form=form, User=User)


@memes.route('/creatememe', methods=['POST'])
def make_meme():
    req_data = request.get_json()
    top_text = req_data['top']
    bottom_text = req_data['bottom']
    image_path = req_data['image']
    image_path = image_path.split('/')[-1].replace('%20', ' ')

    MemeTemplate.query.filter_by(file_name=image_path).first().usage += 1

    image_path = os.path.join(app.root_path, 'static', 'templates', image_path)
    b64_image = util_make(top_text, bottom_text, image_path)
    date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    today = MemeStats.query.filter_by(date=int(date.timestamp())).first()
    if today:
        today.total += 1
    else:
        today = MemeStats(date=int(date.timestamp()), total=0)
        today.total += 1
        db.session.add(today)
    db.session.commit()
    return jsonify({'result': b64_image.decode(), 'status': 201})


@memes.route('/stats')
def get_stats():
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    today_timestamp = int(today.timestamp())
    all_records = MemeStats.query.all()
    total = 0
    if all_records:
        for record in all_records:
            total += record.total
        data = {'total': total}
        today_record = MemeStats.query.filter_by(date=today_timestamp).first()
        data['today'] = today_record.total
        path = os.path.join(app.root_path, 'static', 'templates')
        data['templates'] = len(MemeTemplate.query.all())
        data['users'] = len(User.query.all())
    else:
        data = {'total': 0, 'today': 0, 'templates': 0, 'users': 0}
    return jsonify(data)
