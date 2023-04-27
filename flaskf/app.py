from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from io import BytesIO
import base64
from base64 import b64encode

app = Flask(__name__)


app.jinja_env.filters['b64encode'] = b64encode
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edu_data.db'
db = SQLAlchemy(app)

class StudyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_hours = db.Column(db.Integer)
    score = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    study_hours = int(request.form['study_hours'])
    score = int(request.form['score'])

    data = StudyData(study_hours=study_hours, score=score)
    db.session.add(data)
    db.session.commit()

    all_data = StudyData.query.all()
    hours = []
    scores = []
    for data in all_data:
        hours.append(data.study_hours)
        scores.append(data.score)

    corr_coef = round(np.corrcoef(hours, scores)[0, 1], 2)

    plt.scatter(hours, scores)
    plt.title(f"Correlation Coefficient: {corr_coef}")
    plt.xlabel("Study Hours")
    plt.ylabel("Score")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('results.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
