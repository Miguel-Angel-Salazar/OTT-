
-- tabla de perfiles

CREATE TABLE profiles (

    id UUID PRIMARY KEY REFERENCES auth.users(id),

    nombre VARCHAR(100) NOT NULL,

    region VARCHAR(30) NOT NULL,

    suscripcion VARCHAR(20) NOT NULL DEFAULT 'Sin plan',

    created_at TIMESTAMP DEFAULT now()

);

-- tabla de peliculas

CREATE TABLE movies (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    titulo VARCHAR(150) NOT NULL,

    descripcion TEXT,

    categoria VARCHAR(50),

    region VARCHAR(30),

    video_url TEXT,

    imagen_url TEXT

);

-- tabla de favoritos

CREATE TABLE favorites (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    usuario_id UUID REFERENCES profiles(id) ON DELETE CASCADE,

    pelicula_id BIGINT REFERENCES movies(id) ON DELETE CASCADE

);

-- tabla de historial

CREATE TABLE watch_history (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    usuario_id UUID REFERENCES profiles(id) ON DELETE CASCADE,

    pelicula_id BIGINT REFERENCES movies(id) ON DELETE CASCADE,

    minuto INTEGER DEFAULT 0

);