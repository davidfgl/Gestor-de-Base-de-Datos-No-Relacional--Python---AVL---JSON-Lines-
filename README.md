# PROYECTO FINAL CC1

## Descripción general

Este proyecto implementa un **gestor de base de datos no relacional** que:

- Almacena **objetos JSON**.
- Usa un **árbol AVL** como índice por clave principal (`id`).
- Guarda los datos en un **archivo de texto plano** usando formato **JSON por línea** (JSON Lines).

Permite realizar operaciones básicas de una BD:

- Insertar registros.
- Buscar por clave principal.
- Actualizar registros.
- Eliminar registros.
- Consultar por criterios (búsqueda lineal por otros campos).

---

## Estructura del proyecto

├── avl_tree.py # Implementación del árbol AVL (índice en memoria)

├── storage_manager.py # Manejo de archivo JSON por línea (persistencia)

├── database_manager.py # Lógica del gestor: coordina AVL + archivo

├── main.py # Interfaz de consola para probar el sistema

└── data.jsonl # Archivo de datos (persistencia) – opcional inicial

### 1. `avl_tree.py` – Árbol AVL

- Define:
  - `AVLNode`: nodo del árbol (clave, valor, hijos, altura).
  - `AVLTree`: estructura que mantiene el árbol balanceado.
- Operaciones principales:
  - `insert(key, value)`: inserta o actualiza un registro.
  - `search(key)`: busca por clave, en tiempo O(log n).
  - `delete(key)`: elimina un nodo manteniendo el balance.
- Internamente:
  - Mantiene `height` en cada nodo.
  - Calcula factor de balance.
  - Usa rotaciones simples y dobles (LL, RR, LR, RL) para garantizar que la altura del árbol sea O(log n).

**Rol:** es el **índice en memoria** para acceder rápido a los registros por `id`.

---

### 2. `storage_manager.py` – Persistencia en archivo

- Clase: `StorageManager(file_path, id_field="id")`.
- Formato de archivo: **JSON Lines**  
  Cada línea contiene un objeto JSON independiente, por ejemplo:

{"id": 1, "nombre": "Ana", "edad": 20}
{"id": 2, "nombre": "Luis", "edad": 25}

- Métodos principales:
- `load_all() -> list[dict]`  
  Lee el archivo completo y devuelve una lista de diccionarios.
- `save_all(records: list[dict])`  
  Sobrescribe el archivo con todos los registros.
- `find_by_id(id_value)`  
  Búsqueda lineal por id (opcional).
- `filter_by_predicate(predicate)`  
  Recorre el archivo y devuelve los registros que cumplen el predicado.

**Rol:** es la capa de **acceso a disco**: leer y escribir todos los objetos JSON.

---

### 3. `database_manager.py` – Gestor de la base de datos

- Clase: `DatabaseManager(file_path, id_field="id")`.
- Componentes internos:
- `self.storage`: instancia de `StorageManager`.
- `self.tree`: instancia de `AVLTree`.

#### Carga inicial

Al crear `DatabaseManager`:

1. Llama a `storage.load_all()`.
2. Inserta cada registro en el `AVLTree` usando su `id`.

Así, al arrancar el programa, el árbol AVL queda sincronizado con el archivo.

#### Operaciones CRUD

- `insert(record: dict)`  
- Verifica que el registro tenga `id`.
- Inserta/actualiza en el AVL.
- Carga todos los registros del archivo, actualiza o agrega el registro y vuelve a guardar con `save_all`.

- `get_by_id(key)`  
- Busca directamente en el `AVLTree` (O(log n)).

- `update(key, new_record: dict)`  
- Verifica que exista un registro con ese `id`.
- Fuerza que `new_record["id"] = key`.
- Actualiza en el árbol con `insert`.
- Recorre la lista del archivo, reemplaza el registro y guarda todo de nuevo.

- `delete(key)`  
- Llama a `tree.delete(key)` para eliminar del índice.
- Filtra la lista de registros del archivo, removiendo el que tiene ese `id`, y guarda.

#### Consultas por criterios

- `find_by_predicate(predicate)`  
- Delegado a `StorageManager.filter_by_predicate`.
- Hace una **búsqueda lineal en el archivo**, útil para buscar por cualquier campo:
  - Ejemplo: `db.find_by_predicate(lambda o: o.get("edad", 0) > 18)`.

- `get_all()`  
- Devuelve todos los registros desde el archivo.

**Rol:** es la **capa de lógica de negocio** que expone una API sencilla y mantiene sincronizados el árbol AVL (índice) y el archivo (persistencia).

---

### 4. `main.py` – Interfaz de consola

Proporciona un menú simple para interactuar con el gestor:

Opciones:

1. **Insertar registro**  
 - El usuario escribe un objeto JSON en una línea (ej: `{"id": 1, "nombre": "Ana"}`).
 - Llama a `db.insert(record)`.

2. **Buscar por id**  
 - Pide el id y llama a `db.get_by_id(id)`.

3. **Actualizar registro**  
 - Pide el id del registro a actualizar.
 - Pide un nuevo objeto JSON (sin preocuparse por el `id`).
 - Llama a `db.update(id, new_record)`.

4. **Eliminar registro**  
 - Pide el id y llama a `db.delete(id)`.

5. **Listar todos**  
 - Llama a `db.get_all()` y muestra todos los registros.

6. **Consultar por criterio (campo == valor)**  
 - Pide nombre de campo y valor.
 - Construye un predicado simple y llama a `db.find_by_predicate(predicate)`.

0. **Salir**

**Rol:** es la **interfaz de usuario** mínima para demostrar:

- Inserción, búsqueda, actualización y eliminación.
- Persistencia real en el archivo `data.jsonl`.
- Consultas por otros campos.

---

## Cómo ejecutar el proyecto

1. Clonar o copiar los archivos del proyecto en una carpeta.
2. (Opcional) Crear un archivo `data.jsonl` inicial con algunos registros, por ejemplo:

{"id": 1, "nombre": "Ana", "edad": 20}
{"id": 2, "nombre": "Luis", "edad": 25}

3. En la terminal, situarse en la carpeta del proyecto y ejecutar:

python main.py

4. Usar el menú para:
- Insertar nuevos registros.
- Buscar por `id`.
- Actualizar y eliminar registros.
- Consultar por criterios simples.
- Ver que los cambios se reflejan en el archivo `data.jsonl` incluso después de cerrar y volver a ejecutar el programa.

---

## Decisiones de diseño

- **Árbol AVL**:  
Garantiza que la altura del árbol se mantenga O(log n) gracias al balanceo automático, por lo que las operaciones por `id` (búsqueda, inserción, borrado) son eficientes incluso en el peor caso.

- **JSON por línea (JSON Lines)**:  
- Fácil de leer y escribir secuencialmente.
- Permite reconstruir el índice AVL al iniciar leyendo línea a línea.
- Facilita las búsquedas lineales por otros campos (consultas por criterios).

- **Arquitectura modular**:  
- Cada archivo tiene una responsabilidad clara (estructura de datos, persistencia, lógica de negocio, interfaz).
- Facilita el mantenimiento, pruebas y extensión del proyecto.

---

## Posibles extensiones

- Validación de esquema de los objetos JSON.
- Soporte para múltiples índices (por ejemplo, índice por otro campo).
- Interfaz gráfica o API REST sobre la misma lógica de `DatabaseManager`.
- Manejo de logs y manejo de errores más detallado.
