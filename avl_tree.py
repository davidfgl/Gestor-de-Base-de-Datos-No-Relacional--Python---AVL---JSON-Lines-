class AVLNode:
    def __init__(self, key, value):
        self.key = key          # clave principal (id)
        self.value = value      # objeto JSON representado como dict
        self.left = None
        self.right = None
        self.height = 1         # altura del nodo para el balance AVL


class AVLTree:
    def __init__(self):
        self.root = None

    # ========== Operaciones públicas ==========

    def insert(self, key, value):
        """Inserta (key, value) en el árbol AVL."""
        self.root = self._insert(self.root, key, value)

    def search(self, key):
        """Devuelve el value asociado a key, o None si no existe."""
        node = self._search(self.root, key)
        return node.value if node else None

    def delete(self, key):
        """Elimina la clave key si existe en el árbol."""
        self.root = self._delete(self.root, key)

    # ========== Utilidades internas de altura/balance ==========

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._get_height(node.left),
                              self._get_height(node.right))

    # ========== Rotaciones ==========

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # rotación
        x.right = y
        y.left = T2

        # actualizar alturas
        self._update_height(y)
        self._update_height(x)

        # nueva raíz del subárbol
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # rotación
        y.left = x
        x.right = T2

        # actualizar alturas
        self._update_height(x)
        self._update_height(y)

        # nueva raíz del subárbol
        return y

    # ========== Inserción AVL (recursiva) ==========

    def _insert(self, node, key, value):
        # inserción BST normal
        if not node:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # clave ya existe: actualizar valor
            node.value = value
            return node

        # actualizar altura del ancestro
        self._update_height(node)

        # obtener factor de balance
        balance = self._get_balance(node)

        # Caso 1: Left-Left
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        # Caso 2: Right-Right
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        # Caso 3: Left-Right
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso 4: Right-Left
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        # nodo sin desbalance
        return node

    # ========== Búsqueda BST simple ==========

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # ========== Eliminación AVL (recursiva) ==========

    def _delete(self, node, key):
        # eliminación BST normal
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # nodo encontrado
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # nodo con dos hijos: usar mínimo del subárbol derecho
                min_larger = self._min_node(node.right)
                node.key = min_larger.key
                node.value = min_larger.value
                node.right = self._delete(node.right, min_larger.key)

        # si solo había un nodo, ya hemos retornado antes
        if not node:
            return node

        # actualizar altura
        self._update_height(node)

        # obtener factor de balance
        balance = self._get_balance(node)

        # Caso 1: Left-Left
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Caso 2: Left-Right
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso 3: Right-Right
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Caso 4: Right-Left
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # ========== Utilidad para mínimo ==========

    def _min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
