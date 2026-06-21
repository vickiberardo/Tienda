from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tienda"
    )


class ItemCarrito(BaseModel):
    id_producto: int
    cantidad: int

@app.get("/productos")
def obtener_productos():

    con = conexion()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    con.close()

    return productos


@app.get("/carrito")
def obtener_carrito():

    con = conexion()
    cursor = con.cursor(dictionary=True)

    sql = """
    SELECT
        c.id,
        p.nombre,
        p.precio,
        c.cantidad
    FROM carrito c
    INNER JOIN productos p
    ON c.id_producto = p.id
    """

    cursor.execute(sql)
    carrito = cursor.fetchall()

    cursor.close()
    con.close()

    return carrito

@app.post("/carrito/agregar")
def agregar_carrito(item: ItemCarrito):

    con = conexion()
    cursor = con.cursor(dictionary=True)

    cursor.execute(
        "SELECT stock FROM productos WHERE id = %s",
        (item.id_producto,)
    )

    producto = cursor.fetchone()

    if not producto:
        return {"mensaje": "Producto no encontrado"}

    if producto["stock"] < item.cantidad:
        return {"mensaje": "Stock insuficiente"}

    cursor.execute(
        """
        INSERT INTO carrito(id_producto, cantidad)
        VALUES(%s, %s)
        """,
        (item.id_producto, item.cantidad)
    )

    con.commit()

    cursor.close()
    con.close()

    return {"mensaje": "Producto agregado"}


@app.delete("/carrito/eliminar/{id}")
def eliminar_producto(id: int):

    con = conexion()
    cursor = con.cursor()

    cursor.execute(
        "DELETE FROM carrito WHERE id = %s",
        (id,)
    )

    con.commit()

    cursor.close()
    con.close()

    return {"mensaje": "Producto eliminado"}


@app.post("/carrito/finalizar")
def finalizar_compra():

    con = conexion()
    cursor = con.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_producto, cantidad
        FROM carrito
    """)

    productos = cursor.fetchall()

    for producto in productos:

        cursor.execute("""
            UPDATE productos
            SET stock = stock - %s
            WHERE id = %s
        """, (
            producto["cantidad"],
            producto["id_producto"]
        ))

    # Vaciar carrito
    cursor.execute("DELETE FROM carrito")

    con.commit()

    cursor.close()
    con.close()

    return {"mensaje": "Compra realizada correctamente"}