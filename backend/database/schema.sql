-- ============================================================
-- Schema para OTT - PostgreSQL directo (sin Supabase)
-- ============================================================

-- tabla de usuarios (reemplaza auth.users de supabase)

CREATE TABLE IF NOT EXISTS users (

    id SERIAL PRIMARY KEY,

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()

);

-- tabla de perfiles

CREATE TABLE IF NOT EXISTS profiles (

    id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,

    nombre VARCHAR(100) NOT NULL,

    region VARCHAR(30) NOT NULL,

    suscripcion VARCHAR(20) NOT NULL DEFAULT 'Sin plan',

    created_at TIMESTAMP DEFAULT NOW()

);

-- tabla de peliculas

CREATE TABLE IF NOT EXISTS movies (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    titulo VARCHAR(150) NOT NULL,

    descripcion TEXT,

    categoria VARCHAR(50),

    region VARCHAR(30),

    video_url TEXT,

    imagen_url TEXT,

    hero_url TEXT,

    tipo VARCHAR(50)

);

-- tabla de favoritos

CREATE TABLE IF NOT EXISTS favorites (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    usuario_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    pelicula_id BIGINT REFERENCES movies(id) ON DELETE CASCADE,

    UNIQUE(usuario_id, pelicula_id)

);

-- tabla de historial

CREATE TABLE IF NOT EXISTS watch_history (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    usuario_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    pelicula_id BIGINT REFERENCES movies(id) ON DELETE CASCADE,

    minuto INTEGER DEFAULT 0,

    UNIQUE(usuario_id, pelicula_id)

);

-- tabla de ratings

CREATE TABLE IF NOT EXISTS ratings (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    usuario_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    pelicula_id BIGINT REFERENCES movies(id) ON DELETE CASCADE,

    valor INTEGER NOT NULL,

    UNIQUE(usuario_id, pelicula_id)

);