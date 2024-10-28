-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-11-2023 a las 01:04:41
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `iadb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detected_images`
--

CREATE TABLE `detected_images` (
  `id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `classes_detected` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detected_images`
--

INSERT INTO `detected_images` (`id`, `image_path`, `classes_detected`, `created_at`) VALUES
(1, 'static/detected_image.jpg', '{\'car\': 2}', '2023-11-17 18:57:15'),
(2, 'static/detected_image.jpg', '{\'car\': 2}', '2023-11-17 18:57:17'),
(3, 'static/detected_image.jpg', '{\'car\': 3}', '2023-11-17 18:57:42'),
(4, 'static/detected_image.jpg', '{\'car\': 3, \'trafficLight-Green\': 1, \'pedestrian\': 1, \'trafficLight\': 1}', '2023-11-17 18:58:01'),
(5, 'static/detected_image.jpg', '{\'car\': 5, \'truck\': 1, \'biker\': 1, \'trafficLight-RedLeft\': 1, \'trafficLight-Red\': 1, \'trafficLight\': 1, \'trafficLight-Green\': 1}', '2023-11-17 20:03:14'),
(6, 'static/detected_image.jpg', '{\'car\': 2}', '2023-11-18 20:37:58'),
(7, 'static/detected_image.jpg', '{}', '2023-11-18 20:38:06'),
(8, 'static/detected_image.jpg', '{\'car\': 7, \'pedestrian\': 3}', '2023-11-18 20:38:14'),
(9, 'static/detected_image.jpg', '{\'car\': 3}', '2023-11-18 20:41:47'),
(10, 'static/detected_image.jpg', '{\'car\': 2}', '2023-11-18 20:42:12');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `detected_images`
--
ALTER TABLE `detected_images`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `detected_images`
--
ALTER TABLE `detected_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
