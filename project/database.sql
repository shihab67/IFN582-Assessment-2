-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: grocery_delivery
-- ------------------------------------------------------
-- Server version	8.0.42
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;

/*!50503 SET NAMES utf8 */
;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */
;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */
;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */
;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */
;

--
-- Table structure for table `categories`
--
DROP TABLE IF EXISTS `categories`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE `categories` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `image` varchar(255) DEFAULT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `categories`
--
INSERT INTO
    `categories` (
        `id`,
        `name`,
        `image`,
        `created_at`,
        `updated_at`
    )
VALUES
    (
        1,
        'Beverages',
        'beverages.jpg',
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    ),
    (
        2,
        'Snacks',
        'snacks.jpg',
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    );

--
-- Table structure for table `items`
--
DROP TABLE IF EXISTS `items`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE `items` (
    `id` int NOT NULL AUTO_INCREMENT,
    `category_id` int DEFAULT NULL,
    `name` varchar(255) NOT NULL,
    `description` longtext NOT NULL,
    `price` float NOT NULL,
    `image` varchar(255) NOT NULL,
    `status` tinyint DEFAULT '1',
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `category_id` (`category_id`),
    CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 16 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `items`
--
INSERT INTO
    `items` (
        `id`,
        `category_id`,
        `name`,
        `description`,
        `price`,
        `image`,
        `status`,
        `created_at`,
        `updated_at`
    )
VALUES
    (
        1,
        1,
        'Coca-Cola 330ml',
        'Classic soft drink',
        1.5,
        'coca_cola.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        2,
        1,
        'Pepsi 330ml',
        'Refreshing cola beverage',
        1.4,
        'pepsi.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        3,
        1,
        'Orange Juice 500ml',
        'Freshly squeezed orange juice',
        2.5,
        'orange_juice.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        4,
        1,
        'Green Tea',
        'Organic green tea drink',
        2,
        'green_tea.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        5,
        1,
        'Energy Drink',
        'Boost your energy quickly',
        2.2,
        'energy_drink.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        6,
        1,
        'Mineral Water 1L',
        'Natural mineral water',
        1,
        'mineral_water.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        7,
        1,
        'Iced Coffee',
        'Cold brewed coffee drink',
        2.8,
        'iced_coffee.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        8,
        1,
        'Lemonade 500ml',
        'Sparkling lemon-flavored drink',
        1.7,
        'lemonade.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        9,
        2,
        'Potato Chips',
        'Salted crunchy potato chips',
        1.8,
        'potato_chips.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        10,
        2,
        'Chocolate Bar',
        'Rich milk chocolate',
        1.5,
        'chocolate_bar.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        11,
        2,
        'Trail Mix',
        'Healthy nut and fruit mix',
        2.5,
        'trail_mix.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        12,
        2,
        'Granola Bar',
        'Oats and honey bar',
        1.6,
        'granola_bar.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        13,
        2,
        'Popcorn',
        'Microwave butter popcorn',
        1.2,
        'popcorn.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        14,
        2,
        'Cookies',
        'Choco-chip cookies pack',
        2,
        'cookies.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    ),
    (
        15,
        2,
        'Gummy Bears',
        'Fruit-flavored gummy candy',
        1.3,
        'gummy_bears.jpg',
        1,
        '2025-05-21 19:05:53',
        '2025-05-21 19:05:53'
    );

--
-- Table structure for table `order_items`
--
DROP TABLE IF EXISTS `order_items`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE `order_items` (
    `id` int NOT NULL AUTO_INCREMENT,
    `order_id` int DEFAULT NULL,
    `item_id` int DEFAULT NULL,
    `item_name` varchar(255) NOT NULL,
    `category_name` varchar(255) NOT NULL,
    `quantity` int NOT NULL,
    `unit_price` float NOT NULL,
    `total_price` float NOT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `order_id` (`order_id`),
    KEY `item_id` (`item_id`),
    CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
    CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `order_items`
--
--
-- Table structure for table `orders`
--
DROP TABLE IF EXISTS `orders`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE `orders` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` int DEFAULT NULL,
    `user_address_id` int DEFAULT NULL,
    `total_amount` float NOT NULL,
    `delivery_method` enum('click & collect', 'express', 'eco-friendly') DEFAULT NULL,
    `delivery_fee` float DEFAULT NULL,
    `payment_status` enum('paid', 'unpaid', 'failed') DEFAULT NULL,
    `placed_at` timestamp NOT NULL,
    `delivered_at` timestamp NULL DEFAULT NULL,
    `notes` varchar(255) DEFAULT NULL,
    `status` enum(
        'pending',
        'processing',
        'shipped',
        'delivered',
        'cancelled'
    ) DEFAULT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `orders`
--
--
-- Table structure for table `user_addresses`
--
DROP TABLE IF EXISTS `user_addresses`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE `user_addresses` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` int DEFAULT NULL,
    `address` varchar(255) NOT NULL,
    `suburb` varchar(255) NOT NULL,
    `state` enum('NSW', 'QLD', 'Victoria', 'WA', 'Tasmania', 'SA') NOT NULL,
    `postcode` int NOT NULL,
    `country` varchar(255) NOT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `user_addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `user_addresses`
--
--
-- Table structure for table `users`
--
DROP TABLE IF EXISTS `users`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE `users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `first_name` varchar(255) NOT NULL,
    `last_name` varchar(255) NOT NULL,
    `email` varchar(255) DEFAULT NULL,
    `phone_number` varchar(255) DEFAULT NULL,
    `password` varchar(255) NOT NULL,
    `role` enum('admin', 'customer') DEFAULT 'customer',
    `status` tinyint DEFAULT '1',
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE = InnoDB AUTO_INCREMENT = 15 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `users`
--
INSERT INTO
    `users` (
        `id`,
        `first_name`,
        `last_name`,
        `email`,
        `phone_number`,
        `password`,
        `role`,
        `status`,
        `created_at`,
        `updated_at`
    )
VALUES
    (
        3,
        'Admin',
        'One',
        'admin@gmail.com',
        '0400000001',
        '$0bed214b8eb8c2f1a1d857d7534a3e93ab924d9bff7ae13dcc69ac02814cc1a5cb5ff8f72e144014cf30e3a7827d6dd7588ae8ba2752b158f640f614f16f0efd',
        'admin',
        1,
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    ),
    (
        4,
        'Admin',
        'Two',
        'admin2@gmail.com',
        '0400000002',
        '$0bed214b8eb8c2f1a1d857d7534a3e93ab924d9bff7ae13dcc69ac02814cc1a5cb5ff8f72e144014cf30e3a7827d6dd7588ae8ba2752b158f640f614f16f0efd',
        'admin',
        1,
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    ),
    (
        5,
        'John',
        'Doe',
        'john@gmail.com',
        '0400000003',
        '$0bed214b8eb8c2f1a1d857d7534a3e93ab924d9bff7ae13dcc69ac02814cc1a5cb5ff8f72e144014cf30e3a7827d6dd7588ae8ba2752b158f640f614f16f0efd',
        'customer',
        1,
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    ),
    (
        6,
        'Jane',
        'Smith',
        'jane@gmail.com',
        '0400000004',
        '$0bed214b8eb8c2f1a1d857d7534a3e93ab924d9bff7ae13dcc69ac02814cc1a5cb5ff8f72e144014cf30e3a7827d6dd7588ae8ba2752b158f640f614f16f0efd',
        'customer',
        1,
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    ),
    (
        7,
        'Alice',
        'Brown',
        'alice@gmail.com',
        '0400000005',
        '$0bed214b8eb8c2f1a1d857d7534a3e93ab924d9bff7ae13dcc69ac02814cc1a5cb5ff8f72e144014cf30e3a7827d6dd7588ae8ba2752b158f640f614f16f0efd',
        'customer',
        1,
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    ),
    (
        8,
        'Bob',
        'Johnson',
        'bob@gmail.com',
        '0400000006',
        '$0bed214b8eb8c2f1a1d857d7534a3e93ab924d9bff7ae13dcc69ac02814cc1a5cb5ff8f72e144014cf30e3a7827d6dd7588ae8ba2752b158f640f614f16f0efd',
        'customer',
        1,
        '2025-05-21 19:03:25',
        '2025-05-21 19:03:25'
    );

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */
;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */
;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */
;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */
;

-- Dump completed