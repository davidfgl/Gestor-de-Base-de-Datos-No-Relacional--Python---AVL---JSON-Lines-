import json
from typing import List, Dict, Callable, Optional


class StorageManager:
    """
    Maneja la lectura y escritura de objetos JSON en un archivo
    usando el formato: un objeto JSON por línea (JSON Lines).
    """

    def __init__(self, file_path: str, id_field: str = "id"):
        self.file_path = file_path
        self.id_field = id_field

    # ========== Operaciones básicas sobre el archivo ==========

    def load_all(self) -> List[Dict]:
        """
        Lee todos los registros del archivo.
        Si el archivo no existe o está vacío, devuelve lista vacía.
        """
        records = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        records.append(obj)
                    except json.JSONDecodeError:
                        # aquí podrías loguear el error o ignorar líneas corruptas
                        continue
        except FileNotFoundError:
            # si no existe el archivo, comenzamos con lista vacía
            pass
        return records

    def save_all(self, records: List[Dict]) -> None:
        """
        Sobrescribe el archivo con todos los registros, 
        cada uno en una línea como JSON.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            for obj in records:
                line = json.dumps(obj, ensure_ascii=False)
                f.write(line + "\n")

    # ========== Operaciones de apoyo para el gestor ==========

    def find_by_id(self, id_value) -> Optional[Dict]:
        """
        Búsqueda lineal en archivo por id (por si la necesitas directa).
        """
        for obj in self.load_all():
            if obj.get(self.id_field) == id_value:
                return obj
        return None

    def filter_by_predicate(self, predicate: Callable[[Dict], bool]) -> List[Dict]:
        """
        Recorre linealmente el archivo y devuelve los objetos que
        cumplen el predicado (para consultas por criterios).
        """
        result = []
        for obj in self.load_all():
            try:
                if predicate(obj):
                    result.append(obj)
            except Exception:
                # si el predicado falla en algún objeto, lo ignoramos
                continue
        return result
