-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 27 mai 2022 à 02:56
-- Version du serveur : 10.4.24-MariaDB
-- Version de PHP : 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `stock`
--

-- --------------------------------------------------------

--
-- Structure de la table `categorie`
--

CREATE TABLE `categorie` (
  `Id_Categorie` varchar(50) NOT NULL,
  `Nom_Categorie` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `categorie`
--

INSERT INTO `categorie` (`Id_Categorie`, `Nom_Categorie`) VALUES
('1', 'CAT1'),
('2', 'CAT2'),
('3', 'CAT33'),
('4', 'CAT4'),
('5', 'CAT5');

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

CREATE TABLE `client` (
  `Id_Client` varchar(50) NOT NULL,
  `Nom_Client` varchar(50) DEFAULT NULL,
  `Prenom_Client` varchar(50) DEFAULT NULL,
  `Adresse_Client` varchar(250) DEFAULT NULL,
  `Telephone_Client` varchar(50) DEFAULT NULL,
  `Email_Client` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `client`
--

INSERT INTO `client` (`Id_Client`, `Nom_Client`, `Prenom_Client`, `Adresse_Client`, `Telephone_Client`, `Email_Client`) VALUES
('REFCLT1', 'SABT', 'HAJAR', 'MARRAKECH ', '0643103194', 'hajar@gmail.com'),
('REFCLT2', 'BENCHLIKHA', 'NOUH', 'KECHMID', '0678674539', 'nouh@gmail.com'),
('REFCLT3', 'ELBAZI', 'AMINE', 'kech', '0678675645', 'amine@gmail.com');

-- --------------------------------------------------------

--
-- Structure de la table `commande_achat`
--

CREATE TABLE `commande_achat` (
  `Id_Commande_Achat` int(11) NOT NULL,
  `Id_Produit` varchar(50) NOT NULL,
  `Date_Commande_Achat` date DEFAULT NULL,
  `Id_Fournisseur` varchar(50) DEFAULT NULL,
  `Quantite_A_Acheter` int(11) DEFAULT NULL,
  `TOTAL_HT` float DEFAULT NULL,
  `TVA` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `commande_achat`
--

INSERT INTO `commande_achat` (`Id_Commande_Achat`, `Id_Produit`, `Date_Commande_Achat`, `Id_Fournisseur`, `Quantite_A_Acheter`, `TOTAL_HT`, `TVA`) VALUES
(1111, 'REFP1', '2022-05-16', 'IDFR1', 124, 2000, 10),
(1111, 'REFP4', '2022-05-10', 'IDFR1', 125, 500, 5),
(2222, 'REFP1', '2022-05-05', 'IDFR3', 125, 200, 11),
(2222, 'REFP2', '2022-04-30', 'IDFR3', 125, 1200, 10);

-- --------------------------------------------------------

--
-- Structure de la table `commande_vente`
--

CREATE TABLE `commande_vente` (
  `Id_Commande_Vente` int(11) NOT NULL,
  `Id_Produit` varchar(50) NOT NULL,
  `Date_Commande_Vente` date DEFAULT NULL,
  `Id_Client` varchar(50) DEFAULT NULL,
  `Quantite_A_Vendre` int(11) DEFAULT NULL,
  `TOTAL_HT` float DEFAULT NULL,
  `TVA` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `commande_vente`
--

INSERT INTO `commande_vente` (`Id_Commande_Vente`, `Id_Produit`, `Date_Commande_Vente`, `Id_Client`, `Quantite_A_Vendre`, `TOTAL_HT`, `TVA`) VALUES
(1239, 'REFP2', '2022-05-13', 'REFCLT2', 11, 1200, 20),
(1934, 'REFP1', '2022-05-07', 'REFCLT3', 11, 500, 20),
(1934, 'REFP2', '2022-05-30', 'REFCLT3', 1000, 200, 10);

-- --------------------------------------------------------

--
-- Structure de la table `fournisseur`
--

CREATE TABLE `fournisseur` (
  `Id_Fournisseur` varchar(50) NOT NULL,
  `Nom_Fournisseur` varchar(50) DEFAULT NULL,
  `Prenom_Fournisseur` varchar(50) DEFAULT NULL,
  `Adresse_Fournisseur` varchar(250) DEFAULT NULL,
  `Telephone_Fournisseur` varchar(50) DEFAULT NULL,
  `Email_Fournisseur` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `fournisseur`
--

INSERT INTO `fournisseur` (`Id_Fournisseur`, `Nom_Fournisseur`, `Prenom_Fournisseur`, `Adresse_Fournisseur`, `Telephone_Fournisseur`, `Email_Fournisseur`) VALUES
('IDFR1', 'NABIH', 'AYMEN', 'KECHKECH', '0661293844', 'aymen@gmail.com'),
('IDFR2', 'SALIMI', 'NAJIB', 'CASA', '0678781215', 'najib@gmail.com'),
('IDFR3', 'BADIA', 'AHMED', 'FES', '0661293844', 'ahmed@gmail.com'),
('IDFR4', 'HINDOUS', 'NADA', 'FES', '0678081213', 'nada@gmail.com');

-- --------------------------------------------------------

--
-- Structure de la table `produit`
--

CREATE TABLE `produit` (
  `Id_Produit` varchar(50) NOT NULL,
  `Nom_Produit` varchar(50) DEFAULT NULL,
  `Quantite` int(11) DEFAULT NULL,
  `Prix` float DEFAULT NULL,
  `Id_Categorie` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `produit`
--

INSERT INTO `produit` (`Id_Produit`, `Nom_Produit`, `Quantite`, `Prix`, `Id_Categorie`) VALUES
('REFP1', 'PC', 15, 1300, '1'),
('REFP2', 'TELE', 66, 3900, '2'),
('REFP3', 'USB', 111, 3900, '3'),
('REFP4', 'CLAVIER', 67, 70, '2');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `Id_Utilisateur` varchar(50) NOT NULL,
  `Nom_Utilisateur` varchar(50) NOT NULL,
  `Mot_De_Passe` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`Id_Utilisateur`, `Nom_Utilisateur`, `Mot_De_Passe`) VALUES
('1', 'hajar', '1234');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `categorie`
--
ALTER TABLE `categorie`
  ADD PRIMARY KEY (`Id_Categorie`);

--
-- Index pour la table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`Id_Client`);

--
-- Index pour la table `commande_achat`
--
ALTER TABLE `commande_achat`
  ADD PRIMARY KEY (`Id_Commande_Achat`,`Id_Produit`),
  ADD KEY `FK5` (`Id_Fournisseur`),
  ADD KEY `FK12` (`Id_Produit`);

--
-- Index pour la table `commande_vente`
--
ALTER TABLE `commande_vente`
  ADD PRIMARY KEY (`Id_Commande_Vente`,`Id_Produit`),
  ADD KEY `FK2` (`Id_Client`),
  ADD KEY `FK6` (`Id_Produit`);

--
-- Index pour la table `fournisseur`
--
ALTER TABLE `fournisseur`
  ADD PRIMARY KEY (`Id_Fournisseur`);

--
-- Index pour la table `produit`
--
ALTER TABLE `produit`
  ADD PRIMARY KEY (`Id_Produit`),
  ADD KEY `FK1` (`Id_Categorie`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`Id_Utilisateur`);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `commande_achat`
--
ALTER TABLE `commande_achat`
  ADD CONSTRAINT `FK12` FOREIGN KEY (`Id_Produit`) REFERENCES `produit` (`Id_Produit`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK4` FOREIGN KEY (`Id_Produit`) REFERENCES `produit` (`Id_Produit`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK5` FOREIGN KEY (`Id_Fournisseur`) REFERENCES `fournisseur` (`Id_Fournisseur`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `commande_vente`
--
ALTER TABLE `commande_vente`
  ADD CONSTRAINT `FK3` FOREIGN KEY (`Id_Client`) REFERENCES `client` (`Id_Client`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK6` FOREIGN KEY (`Id_Produit`) REFERENCES `produit` (`Id_Produit`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
