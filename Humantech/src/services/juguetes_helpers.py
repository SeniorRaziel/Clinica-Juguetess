from extensions import mysql


def obtener_categorias_activas():
    """
    Retorna únicamente categorías activas.
    """

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            id,
            nombre,
            slug
        FROM categorias
        WHERE activa = TRUE
        ORDER BY nombre
    """)

    categorias = cur.fetchall()

    cur.close()

    return categorias


def obtener_categorias():
    """
    Retorna todas las categorías.
    """

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            id,
            nombre,
            slug,
            activa,
            creado_en
        FROM categorias
        ORDER BY activa DESC, nombre
    """)

    categorias = cur.fetchall()

    cur.close()

    return categorias


def obtener_categoria_por_id(categoria_id):
    """
    Retorna una categoría por ID.
    """

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT
            id,
            nombre,
            slug,
            activa
        FROM categorias
        WHERE id = %s
    """,
        (categoria_id,),
    )

    categoria = cur.fetchone()

    cur.close()

    return categoria


def categoria_existe_por_slug(slug):
    """
    Verifica si ya existe una categoría con el slug.
    """

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT id
        FROM categorias
        WHERE slug = %s
    """,
        (slug,),
    )

    categoria = cur.fetchone()

    cur.close()

    return categoria is not None


def generar_slug(texto):
    """
    Genera un slug simple para categorías.
    """

    return (
        texto.strip()
        .lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace(" ", "_")
    )
