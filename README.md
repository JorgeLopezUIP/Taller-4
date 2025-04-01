# Taller-4

Para instalar KeyDB en Docker y conectarlo con Redis-Py en Python, primero necesitas tener Docker instalado. Si aún no lo tienes, puedes descargarlo desde docker.com. Luego, abre la terminal y ejecuta el comando docker run -d --name keydb -p 6379:6379 eqalpha/keydb, que descargará la imagen de KeyDB y la ejecutará en segundo plano. Para verificar que el contenedor está en funcionamiento, usa docker ps, y si aparece en la lista, significa que KeyDB está corriendo correctamente.

A continuación, instala la librería Redis-Py en Python con pip install redis. Para probar la conexión, crea un script en Python con el siguiente código:

import redis

keydb = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    keydb.ping()
    print(" Conexión exitosa a KeyDB")
except redis.ConnectionError:
    print(" Error al conectar a KeyDB")

keydb.set("mensaje", "Hola, KeyDB!")
print("Mensaje almacenado:", keydb.get("mensaje"))

Guarda y ejecuta el script con python nombre_del_script.py. Si la conexión es exitosa, verás el mensaje almacenado en KeyDB. Para detener KeyDB, usa docker stop keydb, y si quieres eliminarlo completamente, docker rm keydb. Con esto, ya tienes un servidor KeyDB funcionando en Docker y accesible desde Python con Redis-Py.
