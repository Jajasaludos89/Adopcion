-- Database: gestion_adopciones

-- DROP DATABASE IF EXISTS gestion_adopciones;

CREATE TABLE persona (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

CREATE TABLE mascota (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(50),
    edad INTEGER CHECK (edad >= 0),
    descripcion TEXT,
    foto VARCHAR(255),
    adoptada BOOLEAN DEFAULT FALSE
);

CREATE TABLE adopcion (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER REFERENCES persona(id) ON DELETE CASCADE,
    mascota_id INTEGER REFERENCES mascota(id) ON DELETE CASCADE,
    fecha_adopcion DATE NOT NULL,
    observaciones TEXT
);

INSERT INTO persona (nombre, apellido, cedula, direccion, telefono, correo) VALUES
('Juan', 'Pérez', '1104789652', 'Av. Amazonas N25-48', '0998456321', 'juan.perez@mail.com'),
('María', 'Lopez', '1104789653', 'Calle 10 de Agosto 123', '0987456321', 'maria.lopez@mail.com'),
('Carlos', 'García', '1104789654', 'Av. Universitaria 33', '0991234567', 'carlos.garcia@mail.com'),
('Ana', 'Torres', '1104789655', 'Calle Sucre 101', '0978563214', 'ana.torres@mail.com'),
('Luis', 'Ramírez', '1104789656', 'Av. Latacunga 501', '0999988776', 'luis.ramirez@mail.com');

INSERT INTO mascota (nombre, especie, raza, edad, descripcion, foto, adoptada) VALUES
('Rocky', 'Perro', 'Labrador', 3, 'Juguetón y muy sociable', NULL, FALSE),
('Mishi', 'Gato', 'Siames', 2, 'Cariñoso y tranquilo', NULL, FALSE),
('Toby', 'Perro', 'Golden Retriever', 1, 'Cachorro activo y cariñoso', NULL, FALSE),
('Luna', 'Gato', 'Persa', 4, 'Tranquila y elegante', NULL, FALSE),
('Max', 'Perro', 'Bulldog', 5, 'Amigable con niños', NULL, FALSE);

CREATE OR REPLACE FUNCTION crear_persona(
    p_nombre VARCHAR,
    p_apellido VARCHAR,
    p_cedula VARCHAR,
    p_direccion TEXT,
    p_telefono VARCHAR,
    p_correo VARCHAR
)
RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
BEGIN
    INSERT INTO persona (nombre, apellido, cedula, direccion, telefono, correo)
    VALUES (p_nombre, p_apellido, p_cedula, p_direccion, p_telefono, p_correo)
    RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION leer_personas()
RETURNS TABLE(
    id INTEGER,
    nombre VARCHAR,
    apellido VARCHAR,
    cedula VARCHAR,
    direccion TEXT,
    telefono VARCHAR,
    correo VARCHAR
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM persona ORDER BY id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION actualizar_persona(
    p_id INTEGER,
    p_nombre VARCHAR,
    p_apellido VARCHAR,
    p_cedula VARCHAR,
    p_direccion TEXT,
    p_telefono VARCHAR,
    p_correo VARCHAR
)
RETURNS VOID AS $$
BEGIN
    UPDATE persona
    SET nombre = p_nombre,
        apellido = p_apellido,
        cedula = p_cedula,
        direccion = p_direccion,
        telefono = p_telefono,
        correo = p_correo
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION eliminar_persona(p_id INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM persona WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION crear_mascota(
    p_nombre VARCHAR,
    p_especie VARCHAR,
    p_raza VARCHAR,
    p_edad INTEGER,
    p_descripcion TEXT,
    p_foto VARCHAR
)
RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
BEGIN
    INSERT INTO mascota (nombre, especie, raza, edad, descripcion, foto)
    VALUES (p_nombre, p_especie, p_raza, p_edad, p_descripcion, p_foto)
    RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION leer_mascotas()
RETURNS TABLE(
    id INTEGER,
    nombre VARCHAR,
    especie VARCHAR,
    raza VARCHAR,
    edad INTEGER,
    descripcion TEXT,
    foto VARCHAR,
    adoptada BOOLEAN
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM mascota ORDER BY id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION actualizar_mascota(
    p_id INTEGER,
    p_nombre VARCHAR,
    p_especie VARCHAR,
    p_raza VARCHAR,
    p_edad INTEGER,
    p_descripcion TEXT,
    p_foto VARCHAR,
    p_adoptada BOOLEAN
)
RETURNS VOID AS $$
BEGIN
    UPDATE mascota
    SET nombre = p_nombre,
        especie = p_especie,
        raza = p_raza,
        edad = p_edad,
        descripcion = p_descripcion,
        foto = p_foto,
        adoptada = p_adoptada
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION eliminar_mascota(p_id INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM mascota WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION crear_adopcion(
    p_persona_id INTEGER,
    p_mascota_id INTEGER,
    p_fecha DATE,
    p_observaciones TEXT
)
RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
    ya_adoptada BOOLEAN;
BEGIN
    SELECT adoptada INTO ya_adoptada FROM mascota WHERE id = p_mascota_id;
    IF ya_adoptada THEN
        RAISE EXCEPTION 'La mascota ya fue adoptada.';
    END IF;

    INSERT INTO adopcion (persona_id, mascota_id, fecha_adopcion, observaciones)
    VALUES (p_persona_id, p_mascota_id, p_fecha, p_observaciones)
    RETURNING id INTO new_id;

    UPDATE mascota SET adoptada = TRUE WHERE id = p_mascota_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION leer_adopciones()
RETURNS TABLE(
    id INTEGER,
    persona_id INTEGER,
    mascota_id INTEGER,
    fecha_adopcion DATE,
    observaciones TEXT
) AS $$
BEGIN
    RETURN QUERY SELECT * FROM adopcion ORDER BY id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION actualizar_adopcion(
    p_id INTEGER,
    p_persona_id INTEGER,
    p_mascota_id INTEGER,
    p_fecha DATE,
    p_observaciones TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE adopcion
    SET persona_id = p_persona_id,
        mascota_id = p_mascota_id,
        fecha_adopcion = p_fecha,
        observaciones = p_observaciones
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_adopcion(p_id INTEGER)
RETURNS VOID AS $$
DECLARE
    m_id INTEGER;
BEGIN
    SELECT mascota_id INTO m_id FROM adopcion WHERE id = p_id;
    DELETE FROM adopcion WHERE id = p_id;
    UPDATE mascota SET adoptada = FALSE WHERE id = m_id;
END;
$$ LANGUAGE plpgsql;


SELECT crear_adopcion(1, 1, '2025-10-10', 'Adopción completada sin problemas.');

SELECT crear_adopcion(2, 2, '2025-10-11', 'Gato muy cariñoso.');

SELECT crear_adopcion(3, 3, '2025-10-12', 'Adopción formalizada en feria.');

ALTER TABLE IF EXISTS public.adopcion
    ADD CONSTRAINT adopcion_mascota_id_fkey FOREIGN KEY (mascota_id)
    REFERENCES public.mascota (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.adopcion
    ADD CONSTRAINT adopcion_persona_id_fkey FOREIGN KEY (persona_id)
    REFERENCES public.persona (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

END;

UPDATE mascota SET adoptada = FALSE;
DELETE FROM adopcion;


SELECT * FROM persona;
SELECT * FROM mascota;
SELECT * FROM adopcion;

