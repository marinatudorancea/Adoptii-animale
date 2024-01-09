from flask import Flask, request, redirect, url_for, render_template
from database import db
from werkzeug.utils import secure_filename
import os

from models import Animal


app = Flask(__name__)
#configurare baza de date
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Path pentru db
db.init_app(app)

#configurare upload de fisiere
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    animals = Animal.query.all()
    return render_template('index.html', animals=animals)

@app.route('/adauga', methods=['GET', 'POST'])
def create_animal():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        age = request.form['age']
        description = request.form['description']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)           
        else:
            filename = 'default.jpg'
        
        #adaugare Animal in baza de date
        new_animal = Animal(name=name, species=species, age=age, description=description, image_file=filename)
        db.session.add(new_animal)
        db.session.commit()
        return redirect(url_for('home'))
   
    return render_template('create.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)
    