from flask import Flask, render_template, request, redirect, url_for
from models import db, Project, File
import os

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/upload', methods=['GET', 'POST'])
def upload_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        project = Project(title=title, description=description)
        db.session.add(project)
        db.session.commit()

        files = request.files.getlist('files')
        for file in files:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            new_file = File(project_id=project.id, filename=file.filename, file_path=file_path)
            db.session.add(new_file)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('upload_project.html')

if __name__ == '__main__':
    app.run(debug=True)
