from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5432/books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key = True)
    email       = db.Column(db.String(80))
    password    = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email      = email
        self.password   = password


class Editorial(db.Model):
    __tablename__ = "editorial"
    id_editorial        = db.Column(db.Integer, primary_key = True)
    nombre_editorial    = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial

class Genero(db.Model):
    __tablename__ = "genero"
    id_genero       = db.Column(db.Integer, primary_key = True)
    nombre_genero   = db.Column(db.String(80))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

class Autor(db.Model):
    __tablename__ = "autor"
    id_autor            = db.Column(db.Integer, primary_key = True)
    nombre_autor        = db.Column(db.String(150))
    fecha_nacimiento    = db.Column(db.Date)
    nacionalidad        = db.Column(db.String(80))

    def __init__(self, nombre_autor, fecha_nacimiento, nacionalidad):
        self.nombre_autor       = nombre_autor
        self.fecha_nacimiento   = fecha_nacimiento
        self.nacionalidad       = nacionalidad

class Libro(db.Model):
    __tablename__ = "libro"
    id_libro            = db.Column(db.Integer, primary_key = True)
    titulo_libro        = db.Column(db.String(255))
    fecha_publicacion   = db.Column(db.Date)
    numero_paginas      = db.Column(db.Integer)
    formato             = db.Column(db.String(30))
    id_editorial        = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))    #llave foranea
    id_genero           = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))    #llave foranea
    id_autor            = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))    #llave foranea

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, id_editorial, id_genero, id_autor):
        self.titulo_libro       = titulo_libro
        self.fecha_publicacion  = fecha_publicacion
        self.numero_paginas     = numero_paginas
        self.formato            = formato
        self.id_editorial       = id_editorial
        self.id_genero          = id_genero
        self.id_autor           = id_autor



class Favoritos(db.Model):
    __tablename__ = "favoritos"
    id_favorito = db.Column(db.Integer, primary_key = True)
    fecha       = db.Column(db.Date)
    id_usuario  = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    id_libro    = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))

    def __init__(self, fecha, id_usuario, id_libro):
        self.fecha       = fecha
        self.id_usuario  = id_usuario
        self.id_libro    = id_libro

class EditorialSchema(ma.Schema):
    class Meta:
        fields = ("id_editorial","nombre_editorial")

class GeneroSchema(ma.Schema):
    class Meta:
        fields = ("id_genero","nombre_genero")    

class AutorSchema(ma.Schema):
    class Meta:
        fields = ("id_autor","nombre_autor", "fecha_nacimiento", "nacionalidad")

class LibroSchema(ma.Schema):
    class Meta:
        fields = ("id_libro","titulo_libro", "fecha_publicacion", "numero_paginas", "formato", "id_editorial", "id_genero", "id_autor") 

class FavoritosSchema(ma.Schema):
    class Meta: 
        fields = ("id_favorito","fecha", "id_usuario", "id_libro")

#####################################################################################


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    email = request_data["email"]
    password = request_data["password"]
    user_query = Usuarios.query.filter_by(email=email).first()
    #bcrypt.check_password_hash(user_query.password, password)
    if password == user_query.password:
        return "Login success"
    else:
        return "Login unsuccess"
    

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/createUser", methods=["POST"])
def createUser():
    request_data = request.get_json()
    email = request_data["email"]
    password = request_data["password"]
    #password_encrypted = bcrypt.generate_password_hash(password).decode("utf-8")
    #print("password_encrypted")
    #new_user = Usuarios(email=email, password=password_encrypted)
    new_user = Usuarios(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return "User created"


## C R E A T E ##
@app.route("/createEditorial", methods=["POST"])
def createEditorial():
    request_data = request.get_json()
    editorial = request_data["editorial"]
    new_editorial = Editorial(nombre_editorial=editorial)
    db.session.add(new_editorial)
    db.session.commit()
    return "Editorial created"

@app.route("/createGender", methods=["POST"])
def createGender():
    request_data = request.get_json()
    genero = request_data["gender"]
    new_genero = Genero(nombre_genero=genero)
    db.session.add(new_genero)
    db.session.commit()
    return "Genero created"

@app.route("/createAuthor", methods=["POST"])
def createAuthor():
    request_data = request.get_json()
    autor = request_data["author"]
    fecha_nacimiento = request_data["date"]
    nacionalidad = request_data["nationality"]
    new_author = Autor(nombre_autor=autor, fecha_nacimiento=fecha_nacimiento,nacionalidad=nacionalidad)
    db.session.add(new_author)
    db.session.commit()
    return "Authors created"  

@app.route("/createBook", methods=["POST"])
def createBook():
    request_data = request.get_json()
    titulo_libro = request_data["book"]
    fecha_publicacion = request_data["date"]
    formato = request_data["format"]
    numero_paginas = request_data["number"]
    id_editorial = request_data["editorials"]
    id_genero = request_data["genders"]
    id_autor = request_data["authors"]
    new_book = Libro(titulo_libro=titulo_libro, fecha_publicacion=fecha_publicacion, formato=formato, numero_paginas=numero_paginas, id_editorial=id_editorial, id_genero=id_genero, id_autor=id_autor)
    db.session.add(new_book)
    db.session.commit()
    return "Book created" 


@app.route("/createFavorite", methods=["POST"])
def createFavorite():
    request_data = request.get_json()
    fecha = request_data["date"]
    id_usuario = request_data["id_usuario"]
    id_libro = request_data["books"]
    new_favorite = Favoritos(fecha=fecha, id_usuario=id_usuario, id_libro=id_libro)
    db.session.add(new_favorite)
    db.session.commit()
    return "Favorite added" 


## R E A D ##
@app.route("/getEditorials")
def getEditorials():
    editorial_schema = EditorialSchema()
    editorial_schema = EditorialSchema(many=True)
    all_editorials = Editorial.query.all()
    editorials = editorial_schema.dump(all_editorials)
    print(editorials)
    return jsonify(editorials)

@app.route("/getGenders")
def getGenders():
    gender_schema = GeneroSchema()
    gender_schema = GeneroSchema(many=True)
    all_genders = Genero.query.all()
    genders = gender_schema.dump(all_genders)
    print(genders)
    return jsonify(genders)

@app.route("/getAuthors")
def getAuthors():
    author_schema = AutorSchema()
    author_schema = AutorSchema(many=True)
    all_authors = Autor.query.all()
    authors = author_schema.dump(all_authors)
    print(authors)
    return jsonify(authors)

@app.route("/getBooks")
def getBooks():
    book_schema = LibroSchema()
    book_schema = LibroSchema(many=True)
    all_books = Libro.query.all()
    books = book_schema.dump(all_books)
    print(books)
    return jsonify(books)

class FavoritosSchemaJoin(ma.Schema):
    class Meta: 
        fields = ("id_favorito","fecha", "email", "titulo_libro")

@app.route("/getFavorites")
def getFavorites():
    favorites_schema = FavoritosSchemaJoin()
    favorites_schema = FavoritosSchemaJoin(many=True)
    all_favorites = Favoritos.query.join(Libro, Favoritos.id_libro == Libro.id_libro).join(Usuarios, Favoritos.id_usuario == Usuarios.id).add_columns(Favoritos.id_favorito, Favoritos.fecha, Usuarios.email, Libro.titulo_libro)
    favorites = favorites_schema.dump(all_favorites)
    return jsonify(favorites)

class LibroSchemaJoin(ma.Schema):
    class Meta:
        fields = ("id_libro","titulo_libro", "fecha_publicacion", "numero_paginas", "formato", "nombre_editorial", "nombre_genero", "nombre_autor") 

@app.route("/getBooksJoin")
def getBooksJoin():
    book_schema = LibroSchemaJoin()
    book_schema = LibroSchemaJoin(many=True)
    all_books = Libro.query.join(Editorial, Libro.id_editorial == Editorial.id_editorial).join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).add_columns(Libro.id_libro, Libro.titulo_libro, Libro.fecha_publicacion, Libro.numero_paginas, Libro.formato, Editorial.nombre_editorial, Genero.nombre_genero, Autor.nombre_autor)
    books = book_schema.dump(all_books)
    print("##################################################")
    print(books)
    return jsonify(books)
    

## U P D A T E ##
@app.route("/updateBook", methods=["POST"])
def updateBook():
    request_data = request.get_json()
    id_libro = request_data["id_book"]
    libro = Libro.query.filter_by(id_libro = id_libro).first()
    libro.titulo_libro = request_data["book"]
    libro.fecha_publicacion = request_data["date"]
    libro.numero_paginas = request_data["number"]
    libro.formato = request_data["format"]
    libro.id_editorial = request_data["editorials"]
    libro.id_genero = request_data["genders"]
    libro.id_autor = request_data["authors"]
    db.session.commit()
    return "Book updated"

## D E L E T E ##
@app.route("/deleteFavorite", methods=["POST"])
def deleteFavorite():
    request_data = request.get_json()
    id_favorito = request_data["id_favorito"]
    Favoritos.query.filter_by(id_favorito = id_favorito).delete()
    db.session.commit()
    return "Favorite delete" 


if __name__ == "__main__":

    db.create_all() #crea las tablas    
    app.run(debug = True)