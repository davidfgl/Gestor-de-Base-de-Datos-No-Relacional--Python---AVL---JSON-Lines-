import json
from database_manager import DatabaseManager

FILE_PATH = "data.jsonl"   # archivo de persistencia


def print_menu():
    print("\n=== Gestor de BD No Relacional (AVL + JSON Lines) ===")
    print("1. Insertar registro")
    print("2. Buscar por id")
    print("3. Actualizar registro")
    print("4. Eliminar registro")
    print("5. Listar todos")
    print("6. Consultar por criterio (campo == valor)")
    print("0. Salir")


def input_json_record():
    print("Introduce el objeto JSON (una sola línea):")
    line = input("> ")
    try:
        obj = json.loads(line)
        return obj
    except json.JSONDecodeError:
        print("JSON inválido. Intenta de nuevo.")
        return None


def main():
    db = DatabaseManager(FILE_PATH, id_field="id")

    while True:
        print_menu()
        option = input("Selecciona una opción: ").strip()

        if option == "1":
            # Insertar
            record = input_json_record()
            if record is None:
                continue
            try:
                db.insert(record)
                print("Registro insertado/actualizado correctamente.")
            except Exception as e:
                print(f"Error al insertar: {e}")

        elif option == "2":
            # Buscar por id
            key_str = input("Id a buscar: ")
            # puedes convertir a int si tus ids son enteros
            try:
                key = int(key_str)
            except ValueError:
                key = key_str

            result = db.get_by_id(key)
            if result is None:
                print("No se encontró ningún registro con ese id.")
            else:
                print("Registro encontrado:")
                print(json.dumps(result, ensure_ascii=False, indent=2))

        elif option == "3":
            # Actualizar
            key_str = input("Id del registro a actualizar: ")
            try:
                key = int(key_str)
            except ValueError:
                key = key_str

            print("Introduce el nuevo objeto JSON (ignora el id, se conservará el mismo):")
            new_record = input_json_record()
            if new_record is None:
                continue
            try:
                db.update(key, new_record)
                print("Registro actualizado correctamente.")
            except KeyError as e:
                print(str(e))
            except Exception as e:
                print(f"Error al actualizar: {e}")

        elif option == "4":
            # Eliminar
            key_str = input("Id del registro a eliminar: ")
            try:
                key = int(key_str)
            except ValueError:
                key = key_str

            try:
                db.delete(key)
                print("Registro eliminado (si existía).")
            except Exception as e:
                print(f"Error al eliminar: {e}")

        elif option == "5":
            # Listar todos
            records = db.get_all()
            if not records:
                print("No hay registros.")
            else:
                print("Registros actuales:")
                for obj in records:
                    print(json.dumps(obj, ensure_ascii=False))

        elif option == "6":
            # Consultar por criterio simple: campo == valor
            field = input("Nombre del campo: ").strip()
            value = input("Valor a buscar (como texto): ").strip()

            # intentamos castear a int o float si aplica
            cast_value = value
            if value.isdigit():
                cast_value = int(value)
            else:
                try:
                    cast_value = float(value)
                except ValueError:
                    cast_value = value

            def predicate(obj):
                return obj.get(field) == cast_value

            results = db.find_by_predicate(predicate)
            if not results:
                print("No se encontraron registros que cumplan el criterio.")
            else:
                print("Registros encontrados:")
                for obj in results:
                    print(json.dumps(obj, ensure_ascii=False))

        elif option == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
