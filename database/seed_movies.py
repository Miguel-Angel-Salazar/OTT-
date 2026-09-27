"""
Script para poblar el catalogo de peliculas en la base de datos PostgreSQL.
Inserta las 20 peliculas y series con sus respectivos posters y videos locales.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.db_config import get_connection

PELICULAS = [
    {
        "titulo": "Monos",
        "descripcion": "En una remota montaña, ocho adolescentes armados custodian a una rehén estadounidense y una vaca lechera mientras sobreviven al aislamiento.",
        "categoria": "Drama, Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/monos.jpg",
        "video_url": "/static/videos/monos.mp4",
        "hero_url": "/static/images/posters/monos.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "El olvido que seremos",
        "descripcion": "Relata la vida de Héctor Abad Gómez, un destacado médico colombiano y activista por los derechos humanos en Medellín.",
        "categoria": "Drama, Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/el_olvido_que_seremos.jpg",
        "video_url": "/static/videos/el_olvido_que_seremos.mp4",
        "hero_url": "/static/images/posters/el_olvido_que_seremos.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "La vendedora de rosas",
        "descripcion": "Mónica, una niña que vive en las calles de Medellín, intenta sobrevivir vendiendo rosas durante la noche de Navidad.",
        "categoria": "Drama, Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/la_vendedora_de_rosas.jpg",
        "video_url": "/static/videos/la_vendedora_de_rosas.mp4",
        "hero_url": "/static/images/posters/la_vendedora_de_rosas.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Pájaros de verano",
        "descripcion": "Durante la bonanza marimbera en Colombia, una familia wayuu se ve atrapada en una sangrienta guerra por el control del narcotráfico.",
        "categoria": "Drama, Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/pajaros_de_verano.jpg",
        "video_url": "/static/videos/pajaros_de_verano.mp4",
        "hero_url": "/static/images/posters/pajaros_de_verano.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "El páramo",
        "descripcion": "Un comando especial es enviado a una base militar aislada en un páramo desolado en busca de respuestas.",
        "categoria": "Terror, Cine Colombiano",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/el_paramo.jpg",
        "video_url": "/static/videos/el_paramo.mp4",
        "hero_url": "/static/images/posters/el_paramo.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Roma",
        "descripcion": "Retrato íntimo y conmovedor de la vida de una familia y su empleada doméstica en el México de los años 70.",
        "categoria": "Drama, Cine Independiente",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/roma.jpg",
        "video_url": "/static/videos/roma.mp4",
        "hero_url": "/static/images/posters/roma.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Narcos",
        "descripcion": "La cruda crónica del auge y caída de los principales carteles de narcotráfico y su lucha contra las autoridades.",
        "categoria": "Crimen, Drama, Suspenso",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/narcos.jpg",
        "video_url": "/static/videos/narcos.mp4",
        "hero_url": "/static/images/posters/narcos.jpg",
        "tipo": "Serie"
    },
    {
        "titulo": "A través de mi ventana",
        "descripcion": "La atracción de Raquel hacia su misterioso vecino Ares se convierte en una apasionada e intensa historia.",
        "categoria": "Romance, Drama",
        "region": "LATAM",
        "imagen_url": "/static/images/posters/a_traves_de_mi_ventana.jpg",
        "video_url": "/static/videos/a_traves_de_mi_ventana.mp4",
        "hero_url": "/static/images/posters/a_traves_de_mi_ventana.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "La casa de papel",
        "descripcion": "Un grupo de atracadores guiados por 'El Profesor' ejecuta el asalto más ambicioso a la Fábrica Nacional de Moneda.",
        "categoria": "Acción, Suspenso",
        "region": "EUROPA",
        "imagen_url": "/static/images/posters/la_casa_de_papel.jpg",
        "video_url": "/static/videos/la_casa_de_papel.mp4",
        "hero_url": "/static/images/posters/la_casa_de_papel.jpg",
        "tipo": "Serie"
    },
    {
        "titulo": "Dark",
        "descripcion": "La desaparición de dos niños en Winden desvela un intrincado misterio temporal que une a cuatro familias.",
        "categoria": "Ciencia Ficción, Suspenso",
        "region": "EUROPA",
        "imagen_url": "/static/images/posters/dark.jpg",
        "video_url": "/static/videos/dark.mp4",
        "hero_url": "/static/images/posters/dark.jpg",
        "tipo": "Serie"
    },
    {
        "titulo": "Peaky Blinders",
        "descripcion": "En el Birmingham de entreguerras, Thomas Shelby dirige a una sanguinaria banda dispuesta a llegar a la cima del poder.",
        "categoria": "Drama, Crimen",
        "region": "EUROPA",
        "imagen_url": "/static/images/posters/peaky_blinders.jpg",
        "video_url": "/static/videos/peaky_blinders.mp4",
        "hero_url": "/static/images/posters/peaky_blinders.jpg",
        "tipo": "Serie"
    },
    {
        "titulo": "Sherlock",
        "descripcion": "El legendario detective Sherlock Holmes resuelve los crímenes más intrincados en el Londres actual.",
        "categoria": "Misterio, Suspenso",
        "region": "EUROPA",
        "imagen_url": "/static/images/posters/sherlock.jpg",
        "video_url": "/static/videos/sherlock.mp4",
        "hero_url": "/static/images/posters/sherlock.jpg",
        "tipo": "Serie"
    },
    {
        "titulo": "El laberinto del fauno",
        "descripcion": "En la España de la posguerra, una niña descubre un mundo mágico y oscuro que pondrá a prueba su valor.",
        "categoria": "Fantasía, Drama",
        "region": "EUROPA",
        "imagen_url": "/static/images/posters/el_laberinto_del_fauno.jpg",
        "video_url": "/static/videos/el_laberinto_del_fauno.mp4",
        "hero_url": "/static/images/posters/el_laberinto_del_fauno.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Avatar",
        "descripcion": "Un marine parapléjico enviado a la luna Pandora debe decidir entre cumplir su misión o proteger a la civilización Na'vi.",
        "categoria": "Ciencia Ficción, Acción",
        "region": "USA",
        "imagen_url": "/static/images/posters/avatar.jpg",
        "video_url": "/static/videos/avatar.mp4",
        "hero_url": "/static/images/posters/avatar.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Interestelar",
        "descripcion": "Ante la extinción de la Tierra, un grupo de exploradores viaja a través de un agujero de gusano para salvar a la humanidad.",
        "categoria": "Ciencia Ficción, Aventura",
        "region": "USA",
        "imagen_url": "/static/images/posters/interestelar.jpg",
        "video_url": "/static/videos/interestelar.mp4",
        "hero_url": "/static/images/posters/interestelar.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Forrest Gump",
        "descripcion": "Las extraordinarias vivencias de un hombre inocente con un corazón bondadoso que atraviesa las décadas clave de EE.UU.",
        "categoria": "Drama, Comedia",
        "region": "USA",
        "imagen_url": "/static/images/posters/forrest_gump.jpg",
        "video_url": "/static/videos/forrest_gump.mp4",
        "hero_url": "/static/images/posters/forrest_gump.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "John Wick",
        "descripcion": "Un implacable exasesino vuelve al bajo mundo criminal cuando le arrebatan el último regalo de su difunta esposa.",
        "categoria": "Acción, Suspenso",
        "region": "USA",
        "imagen_url": "/static/images/posters/john_wick.jpg",
        "video_url": "/static/videos/john_wick.mp4",
        "hero_url": "/static/images/posters/john_wick.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Breaking Bad",
        "descripcion": "Walter White, profesor de química con cáncer terminal, entra al negocio de la metanfetamina para asegurar a su familia.",
        "categoria": "Drama, Crimen",
        "region": "USA",
        "imagen_url": "/static/images/posters/breaking_bad.jpg",
        "video_url": "/static/videos/breaking_bad.mp4",
        "hero_url": "/static/images/posters/breaking_bad.jpg",
        "tipo": "Serie"
    },
    {
        "titulo": "Toy Story",
        "descripcion": "El vaquero Woody y el astronauta Buzz Lightyear compiten por el afecto de Andy antes de forjar una amistad inseparable.",
        "categoria": "Animación, Familiar",
        "region": "USA",
        "imagen_url": "/static/images/posters/toy_story.jpg",
        "video_url": "/static/videos/toy_story.mp4",
        "hero_url": "/static/images/posters/toy_story.jpg",
        "tipo": "Película"
    },
    {
        "titulo": "Hasta el último hombre",
        "descripcion": "La inspiradora historia de Desmond Doss, un soldado que salvó a 75 compañeros en la sangrienta batalla de Okinawa sin disparar un arma.",
        "categoria": "Bélico, Drama, Acción",
        "region": "USA",
        "imagen_url": "/static/images/posters/hacksaw_ridge.jpg",
        "video_url": "/static/videos/hacksaw_ridge.mp4",
        "hero_url": "/static/images/posters/hacksaw_ridge.jpg",
        "tipo": "Película"
    }
]


def seed():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as total FROM movies")
    count = cur.fetchone()["total"]
    if count > 0:
        print(f"La tabla movies ya tiene {count} registros.")
        cur.close()
        conn.close()
        return

    print("Insertando peliculas en PostgreSQL...")
    insert_sql = """
        INSERT INTO movies (titulo, descripcion, categoria, region, imagen_url, video_url, hero_url, tipo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for p in PELICULAS:
        cur.execute(
            insert_sql,
            (
                p["titulo"],
                p["descripcion"],
                p["categoria"],
                p["region"],
                p["imagen_url"],
                p["video_url"],
                p["hero_url"],
                p["tipo"]
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f" ¡{len(PELICULAS)} películas y series insertadas exitosamente!")


if __name__ == "__main__":
    seed()
