from flask import Flask, render_template, request, redirect, url_for
from basedatos import crear_tabla, guardar_usuario, mostrar_usuario,buscar_usuario, editar_usuario, eliminar_usuario
import os, uuid
app=Flask(__name__)
#este es otro comentario

#donde se guardaran las imagenes
CARPETA_IMAGENES=os.path.join(app.root_path, "static", "imagenes")

os.makedirs(CARPETA_IMAGENES, exist_ok=True)

@app.route("/")
def registro():
    return render_template('formulario.html')



#para almacenar los datos
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("tel", "").strip()
    correo = request.form.get("correo", "").strip()
    genero = request.form.get("genero", "").strip()
    lista_colores = request.form.getlist("colores")
    colores=','.join(lista_colores)
    ocupacion = request.form.get("ocupacion","").strip()
    archivo = request.files.get("imagen")

    if not nombre or not telefono or not correo or not genero or not lista_colores or not ocupacion or not archivo or archivo.filename=='':
        return "Todos los campos son obligatorios.", 400

    extension = os.path.splitext(archivo.filename)[1].lower()

    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        return "Formato de imagen no comatible", 400

    #crea un archivo unico
    nombre_archivo=(f"{uuid.uuid4().hex}{extension}")

    ruta_imagen=os.path.join(CARPETA_IMAGENES, nombre_archivo)
    archivo.save(ruta_imagen)



    guardar_usuario(nombre, telefono, correo, genero, colores, ocupacion, nombre_archivo)

    return """
        <h1>¡Registro guardado correctamente!</h1>
        <a href="/">Regresar al formulario</a>
    """

@app.route("/mostrar")
def mostrar():
    mis_usuarios=mostrar_usuario()
    return render_template('datos.html', usuarios=mis_usuarios)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method=="POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("tel", "").strip()
        correo = request.form.get("correo", "").strip()
        genero = request.form.get("genero", "").strip()
        lista_colores = request.form.getlist("colores")
        colores=','.join(lista_colores)
        ocupacion = request.form.get("ocupacion","").strip()
        archivo = request.files.get("imagen")

        extension = os.path.splitext(archivo.filename)[1].lower()
        
        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            return "Formato de imagen no comatible", 400
        
        #crea un archivo unico
        nombre_archivo=(f"{uuid.uuid4().hex}{extension}")
        ruta_imagen=os.path.join(CARPETA_IMAGENES, nombre_archivo)
        archivo.save(ruta_imagen)

        editar_usuario(id, nombre, telefono, correo, genero, colores, ocupacion, nombre_archivo)
        return redirect(url_for("mostrar"))
    usuario=buscar_usuario(id)
    return render_template("editar.html", usuario=usuario)


@app.route("/eliminar<int:id>", methods=["GET", "POST"])
def eliminar(id):
    eliminar_usuario(id, CARPETA_IMAGENES)
    return redirect(url_for("mostrar"))

    
if __name__=="__main__":
    crear_tabla()
    app.run(debug=True)

    