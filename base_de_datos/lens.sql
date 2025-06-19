-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-06-2025 a las 01:41:52
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `lens`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentarios`
--

CREATE TABLE `comentarios` (
  `id_comentario` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tmdb_id` int(11) NOT NULL,
  `nombre_pelicula` text NOT NULL,
  `comentario` text NOT NULL,
  `valoracion` int(11) DEFAULT NULL CHECK (`valoracion` between 1 and 5),
  `fecha_comentario` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comentarios`
--

INSERT INTO `comentarios` (`id_comentario`, `id_usuario`, `tmdb_id`, `nombre_pelicula`, `comentario`, `valoracion`, `fecha_comentario`) VALUES
(1, 1, 1426776, 'Harta', '¡Excelente película!', 5, '2024-06-10'),
(2, 1, 1087891, 'Amateur', 'Muy entretenida.', 4, '2024-06-10'),
(3, 1, 552524, 'Lilo y Stitch', 'La volvería a ver.', 5, '2024-06-10'),
(4, 2, 1376434, 'Predator: Asesino de asesinos', 'Buena trama.', 4, '2024-06-11'),
(5, 2, 870028, 'El contable 2', 'Me gustó mucho.', 5, '2024-06-11'),
(6, 2, 1087192, 'Cómo entrenar a tu dragón', 'Recomendada.', 4, '2024-06-11'),
(7, 3, 1379587, 'Utopia', 'No me convenció.', 2, '2024-06-12'),
(8, 3, 1315988, 'Mikaela', 'Visualmente increíble.', 5, '2024-06-12'),
(9, 3, 1450599, 'K.O.', 'Historia original.', 4, '2024-06-12'),
(10, 4, 1225916, '3ão: Uma História Sem Fim', 'Gran actuación.', 5, '2024-06-13'),
(11, 4, 1239193, 'Deep Cover: Actores encubiertos', 'Esperaba más.', 3, '2024-06-13'),
(12, 4, 713364, 'Clown in a Cornfield', 'Muy divertida.', 4, '2024-06-13'),
(13, 5, 1233413, 'Los pecadores', 'Perfecta para la familia.', 5, '2024-06-14'),
(14, 5, 1017163, 'Fuerza bruta: Castigo', 'Un poco lenta.', 3, '2024-06-14'),
(15, 5, 1289601, 'Lucha por tu vida', 'Me encantó.', 5, '2024-06-14');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entradas`
--

CREATE TABLE `entradas` (
  `id_entrada` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tmdb_id` int(11) NOT NULL,
  `nombre_pelicula` text NOT NULL,
  `fila` varchar(1) NOT NULL,
  `numero_asiento` int(11) NOT NULL,
  `fecha_compra` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entradas`
--

INSERT INTO `entradas` (`id_entrada`, `id_usuario`, `tmdb_id`, `nombre_pelicula`, `fila`, `numero_asiento`, `fecha_compra`) VALUES
(1, 1, 1426776, 'Harta', 'A', 1, '2024-06-10 15:00:00'),
(2, 1, 1426776, 'Harta', 'A', 2, '2024-06-10 15:01:00'),
(3, 1, 1426776, 'Harta', 'A', 3, '2024-06-10 15:02:00'),
(4, 1, 1426776, 'Harta', 'A', 4, '2024-06-10 15:03:00'),
(5, 1, 1426776, 'Harta', 'A', 5, '2024-06-10 15:04:00'),
(6, 1, 1426776, 'Harta', 'A', 6, '2024-06-10 15:05:00'),
(7, 1, 1426776, 'Harta', 'A', 7, '2024-06-10 15:06:00'),
(8, 1, 1426776, 'Harta', 'A', 8, '2024-06-10 15:07:00'),
(9, 1, 1426776, 'Harta', 'A', 9, '2024-06-10 15:08:00'),
(10, 1, 1426776, 'Harta', 'A', 10, '2024-06-10 15:09:00'),
(11, 2, 1087891, 'Amateur', 'B', 1, '2024-06-11 16:00:00'),
(12, 2, 1087891, 'Amateur', 'B', 2, '2024-06-11 16:01:00'),
(13, 2, 1087891, 'Amateur', 'B', 3, '2024-06-11 16:02:00'),
(14, 2, 1087891, 'Amateur', 'B', 4, '2024-06-11 16:03:00'),
(15, 2, 1087891, 'Amateur', 'B', 5, '2024-06-11 16:04:00'),
(16, 3, 552524, 'Lilo y Stitch', 'C', 1, '2024-06-12 17:00:00'),
(17, 3, 552524, 'Lilo y Stitch', 'C', 2, '2024-06-12 17:01:00'),
(18, 3, 552524, 'Lilo y Stitch', 'C', 3, '2024-06-12 17:02:00'),
(19, 3, 552524, 'Lilo y Stitch', 'C', 4, '2024-06-12 17:03:00'),
(20, 3, 552524, 'Lilo y Stitch', 'C', 5, '2024-06-12 17:04:00'),
(21, 3, 552524, 'Lilo y Stitch', 'C', 6, '2024-06-12 17:05:00'),
(22, 4, 1376434, 'Predator: Asesino de asesinos', 'D', 1, '2024-06-13 18:00:00'),
(23, 4, 1376434, 'Predator: Asesino de asesinos', 'D', 2, '2024-06-13 18:01:00'),
(24, 4, 1376434, 'Predator: Asesino de asesinos', 'D', 3, '2024-06-13 18:02:00'),
(25, 5, 870028, 'El contable 2', 'E', 1, '2024-06-14 19:00:00'),
(26, 5, 870028, 'El contable 2', 'E', 2, '2024-06-14 19:01:00'),
(27, 5, 870028, 'El contable 2', 'E', 3, '2024-06-14 19:02:00'),
(28, 5, 870028, 'El contable 2', 'E', 4, '2024-06-14 19:03:00'),
(29, 5, 870028, 'El contable 2', 'E', 5, '2024-06-14 19:04:00'),
(30, 1, 1087192, 'Cómo entrenar a tu dragón', 'A', 11, '2024-06-15 15:00:00'),
(31, 2, 1379587, 'Utopia', 'B', 6, '2024-06-15 16:00:00'),
(32, 3, 1315988, 'Mikaela', 'C', 7, '2024-06-15 17:00:00'),
(33, 4, 1450599, 'K.O.', 'D', 4, '2024-06-15 18:00:00'),
(34, 5, 1225916, '3ão: Uma História Sem Fim', 'E', 6, '2024-06-15 19:00:00'),
(35, 1, 1239193, 'Deep Cover: Actores encubiertos', 'A', 12, '2024-06-16 15:00:00'),
(36, 2, 713364, 'Clown in a Cornfield', 'B', 7, '2024-06-16 16:00:00'),
(37, 3, 1233413, 'Los pecadores', 'C', 8, '2024-06-16 17:00:00'),
(38, 4, 1017163, 'Fuerza bruta: Castigo', 'D', 5, '2024-06-16 18:00:00'),
(39, 5, 1289601, 'Lucha por tu vida', 'E', 7, '2024-06-16 19:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_usuario`, `email`, `password_hash`, `fecha_registro`) VALUES
(1, 'nombre1', 'nombre1@gmail.com', '$2y$10$wHk7Qw6QK6pQw6QK6pQw6uQw6QK6pQw6QK6pQw6QK6pQw6QK6pQw6', '2024-06-01 10:00:00'),
(2, 'nombre2', 'nombre2@gmail.com', '$2y$10$wHk7Qw6QK6pQw6QK6pQw6uQw6QK6pQw6QK6pQw6QK6pQw6QK6pQw6', '2024-06-02 11:00:00'),
(3, 'nombre3', 'nombre3@gmail.com', '$2y$10$wHk7Qw6QK6pQw6QK6pQw6uQw6QK6pQw6QK6pQw6QK6pQw6QK6pQw6', '2024-06-03 12:00:00'),
(4, 'nombre4', 'nombre4@gmail.com', '$2y$10$wHk7Qw6QK6pQw6QK6pQw6uQw6QK6pQw6QK6pQw6QK6pQw6QK6pQw6', '2024-06-04 13:00:00'),
(5, 'nombre5', 'nombre5@gmail.com', '$2y$10$wHk7Qw6QK6pQw6QK6pQw6uQw6QK6pQw6QK6pQw6QK6pQw6QK6pQw6', '2024-06-05 14:00:00'),
(6, 'tomi', 'tomasiezzi16@gmail.com', '$2y$10$bOVTmtayv.k84u5zM3NeYezV9QlYkDZlsxeYUgYbLsKL5z/DeZvl2', '2025-06-17 20:40:01');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD PRIMARY KEY (`id_comentario`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `entradas`
--
ALTER TABLE `entradas`
  ADD PRIMARY KEY (`id_entrada`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comentarios`
--
ALTER TABLE `comentarios`
  MODIFY `id_comentario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `entradas`
--
ALTER TABLE `entradas`
  MODIFY `id_entrada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD CONSTRAINT `comentarios_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `entradas`
--
ALTER TABLE `entradas`
  ADD CONSTRAINT `entradas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
