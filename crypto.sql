-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 09 avr. 2022 à 11:42
-- Version du serveur : 8.0.27
-- Version de PHP : 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `crypto`
--

-- --------------------------------------------------------

--
-- Structure de la table `mes_cryptos`
--

CREATE TABLE `mes_cryptos` (
  `id` int NOT NULL,
  `crypto` varchar(255) NOT NULL,
  `quantite` float NOT NULL,
  `prix` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `mes_cryptos`
--

INSERT INTO `mes_cryptos` (`id`, `crypto`, `quantite`, `prix`) VALUES
(1, 'BTC', 3, 80000),
(2, 'ETH', 1, 20000);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `mes_cryptos`
--
ALTER TABLE `mes_cryptos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `mes_cryptos`
--
ALTER TABLE `mes_cryptos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
