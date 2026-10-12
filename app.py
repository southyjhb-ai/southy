from flask import Flask, render_template, request
from models import db, Job

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        try:
            job = Job(
                name=request.form.get('name'),
                phone=request.form.get('phone'),
                title=request.form.get('title'),
                description=request.form.get('description'),
                location=request.form.get('location'),
                budget=request.form.get('budget')
            )

            db.session.add(job)
            db.session.commit()

            # ✅ SHOW SUCCESS PAGE
            return render_template('success.html', name=job.name)

        except Exception as e:
            return f"Error: {e}"

    return render_template('create_job.html')


@app.route('/dashboard')
def dashboard():
    jobs = Job.query.all()
    return render_template('dashboard.html', jobs=jobs)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=True)