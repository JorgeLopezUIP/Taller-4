''' Para instalar KeyDB en Docker y conectarlo con Redis-Py en Python, primero necesitas tener Docker '
'instalado. Si aún no lo tienes, puedes descargarlo desde docker.com. Luego, abre la terminal y ejecuta el '
'comando docker run -d --name keydb -p 6379:6379 eqalpha/keydb, que descargará la imagen de KeyDB y la '
'ejecutará en segundo plano. Para verificar que el contenedor está en funcionamiento, usa docker ps, y si '
'aparece en la lista, significa que KeyDB está corriendo correctamente. '

Guarda y ejecuta el script con python nombre_del_script.py. Si la conexión es exitosa, verás el mensaje '
'almacenado en KeyDB. Para detener KeyDB, usa docker stop keydb, y si quieres eliminarlo completamente, '
'docker rm keydb. Con esto, ya tienes un servidor KeyDB funcionando en Docker y accesible desde Python con '
'Redis-Py.'''



import redis
import json

keydb = redis.Redis(host="localhost", port=6379, decode_responses=True)

class Libro:
    def __init__(self, titulo, genero, autor, estado):
        self.titulo = titulo
        self.genero = genero
        self.autor = autor
        self.estado = estado

    def to_json(self):
        return json.dumps(self.__dict__)  

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)  
        return Libro(**data)


def agregar_libro():
    try:
        titulo = input("Título del libro: ").strip()
        genero = input("Género del libro: ").strip()
        autor = input("Nombre del autor: ").strip()
        estado = input("Estado del libro: ").strip()

        libro = Libro(titulo, genero, autor, estado)

       
        id_libro = keydb.incr("libro:id")
        key = f"libro:{id_libro}"

       
        keydb.set(key, libro.to_json())
        print(f"Libro agregado exitosamente con ID {id_libro}.")

    except Exception as e:
        print(f"Error al agregar libro: {e}")


def ver_libros():
    try:
        print("\nLista de libros:")
        for key in keydb.scan_iter("libro:*"):  
            libro_json = keydb.get(key)
            libro = Libro.from_json(libro_json)
            print(f"{key}: {libro.__dict__}")

    except Exception as e:
        print(f"Error al mostrar libros: {e}")


def buscar_libro():
    try:
        id_libro = input("Ingrese el ID del libro: ").strip()
        key = f"libro:{id_libro}"
        
        libro_json = keydb.get(key)
        if libro_json:
            libro = Libro.from_json(libro_json)
            print(f"Libro encontrado: {libro.__dict__}")
        else:
            print("Libro no encontrado.")

    except Exception as e:
        print(f"Error al buscar libro: {e}")


def eliminar_libro():
    try:
        id_libro = input("Ingrese el ID del libro a eliminar: ").strip()
        key = f"libro:{id_libro}"

        if keydb.delete(key):
            print("Libro eliminado con éxito.")
        else:
            print("Libro no encontrado.")

    except Exception as e:
        print(f"Error al eliminar libro: {e}")


while True:
    print("\n1. Ingresar libro")
    print("2. Ver libros")
    print("3. Buscar libro por ID")
    print("4. Eliminar libro")
    print("5. Salir")

    opcion = input("Elija una opción: ").strip()

    if opcion == "1":
        agregar_libro()
    elif opcion == "2":
        ver_libros()
    elif opcion == "3":
        buscar_libro()
    elif opcion == "4":
        eliminar_libro()
    elif opcion == "5":
        break
    else:
        print("Opción no válida.")