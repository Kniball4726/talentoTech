productos = []

def agregarProducto(clave, valor):
    productos.append({clave: valor})
    return productos


agregar_producto = agregarProducto("id", 1)

print (agregar_producto)