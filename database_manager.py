from typing import Callable, Dict, List, Optional

from avl_tree import AVLTree
from storage_manager import StorageManager


class DatabaseManager:
    """
    Gestor de Base de Datos No Relacional:
    - Mantiene un AVL indexado por id.
    - Persiste los objetos en un archivo JSON por línea.
    """

    def __init__(self, file_path: str, id_field: str = "id"):
        self.id_field = id_field
        self.storage = StorageManager(file_path, id_field=id_field)
        self.tree = AVLTree()

        # Cargar datos existentes desde el archivo al árbol
        self._load_into_tree()

    def _load_into_tree(self):
        records = self.storage.load_all()
        for obj in records:
            key = obj.get(self.id_field)
            if key is not None:
                self.tree.insert(key, obj)

    # ========== Operaciones CRUD ==========

    def insert(self, record: Dict) -> None:
        """
        Inserta un nuevo objeto.
        - Debe contener el campo id_field.
        - Si el id ya existe, se sobrescribe.
        """
        key = record.get(self.id_field)
        if key is None:
            raise ValueError(f"El registro debe tener el campo '{self.id_field}'")

        # insertar/actualizar en árbol
        self.tree.insert(key, record)

        # sincronizar archivo: recargar lista, actualizar o agregar y guardar
        records = self.storage.load_all()

        # buscar si ya existe
        updated = False
        for i, obj in enumerate(records):
            if obj.get(self.id_field) == key:
                records[i] = record
                updated = True
                break

        if not updated:
            records.append(record)

        self.storage.save_all(records)

    def get_by_id(self, key) -> Optional[Dict]:
        """
        Busca un objeto por id usando el AVL.
        """
        return self.tree.search(key)

    def update(self, key, new_record: Dict) -> None:
        """
        Actualiza un objeto existente:
        - Si no existe, opcionalmente podrías lanzar error o insertarlo.
        - new_record debe tener el mismo id o se fuerza al id original.
        """
        existing = self.tree.search(key)
        if existing is None:
            raise KeyError(f"No existe un registro con id={key}")

        # asegurar que el id se mantenga
        new_record[self.id_field] = key

        # actualizar en árbol
        self.tree.insert(key, new_record)

        # actualizar en archivo
        records = self.storage.load_all()
        for i, obj in enumerate(records):
            if obj.get(self.id_field) == key:
                records[i] = new_record
                break

        self.storage.save_all(records)

    def delete(self, key) -> None:
        """
        Elimina un objeto por id, tanto del árbol como del archivo.
        """
        # eliminar del árbol
        self.tree.delete(key)

        # eliminar del archivo
        records = self.storage.load_all()
        records = [obj for obj in records if obj.get(self.id_field) != key]
        self.storage.save_all(records)

    # ========== Consultas por criterios ==========

    def find_by_predicate(self, predicate) -> List[Dict]:
        """
        Consulta lineal en el archivo, usando un predicado.
        Ejemplo de uso:
            db.find_by_predicate(lambda obj: obj.get("edad", 0) > 18)
        """
        return self.storage.filter_by_predicate(predicate)

    def get_all(self) -> List[Dict]:
        """
        Devuelve todos los registros (lectura desde archivo).
        Útil para debug o exportar.
        """
        return self.storage.load_all()
