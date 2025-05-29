-- --------------------------------------------------------
-- Host:                         panel.hostheaven.dk
-- Server version:               11.4.5-MariaDB-ubu2004 - mariadb.org binary distribution
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table s87_Radient.categorys
CREATE TABLE IF NOT EXISTS `categorys` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `label` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `emote` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `role_access` varchar(50) DEFAULT NULL,
  `channel_category` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table s87_Radient.categorys: ~11 rows (approximately)
REPLACE INTO `categorys` (`id`, `label`, `value`, `emote`, `description`, `role_access`, `channel_category`, `created_at`) VALUES
	(1, 'Support', 'support', '🔧', 'Alle supportere kan hjælpe dig med denne sag.', '1376312327514619995', '1376313403752054804', '2025-05-25 20:50:44'),
	(2, 'Bande', 'bande', '🕵️', 'En bandeansvarlig vil hjælpe dig med dette.', '1377046263769464983', '1376313403752054804', '2025-05-25 20:50:44'),
	(3, 'Firma', 'firma', '🏢', 'En firmaansvarlig vil hjælpe dig med dette.', '1377046342886625281', '1376313403752054804', '2025-05-25 20:50:44'),
	(4, 'CK', 'ck', '⚰️', 'En CK-ansvarlig vil hjælpe dig med dette.', '1377046373698109451', '1376313403752054804', '2025-05-25 20:50:44'),
	(5, 'Development', 'development', '💻', 'Et medlem af dev-teamet vil hjælpe dig her.', '1377046409290711080', '1376313403752054804', '2025-05-25 20:50:44'),
	(6, 'Content Creator', 'content creator', '🎥', 'En CC-ansvarlig vil hjælpe dig med dette.', '1377046910707175515', '1376313403752054804', '2025-05-25 20:50:44'),
	(7, 'Kompensation', 'kompensation', '💸', 'En kompensationsansvarlig vil hjælpe dig her.', '1377046438927925268', '1376313403752054804', '2025-05-25 20:50:44'),
	(8, 'Unban', 'unban', '🔓', 'En unban-ansvarlig vil hjælpe dig her.', '1377046534591610962', '1376313403752054804', '2025-05-25 20:50:44'),
	(9, 'Donation', 'donation', '💰', 'En donationsansvarlig vil hjælpe dig her.', '1377046571778179203', '1376313403752054804', '2025-05-25 20:50:44'),
	(10, 'Staff', 'Staff', '👥', 'En staff-ansvarlig vil hjælpe dig her.', '1377046609795350640', '1376313403752054804', '2025-05-25 20:50:44'),
	(11, 'Politi', 'politi', '🚔', 'En fra politiledelsen vil hjælpe dig her.', '1377046642892476468', '1376313403752054804', '2025-05-25 20:50:44');

-- Dumping structure for table s87_Radient.settings
CREATE TABLE IF NOT EXISTS `settings` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table s87_Radient.settings: ~5 rows (approximately)
REPLACE INTO `settings` (`id`, `name`, `value`) VALUES
	(1, 'support_role', '1376312327514619995'),
	(2, 'call_role', '1377057764475666615'),
	(3, 'call_support', 'true'),
	(4, 'close_time', '5'),
	(5, 'panel_role', '1376311994147147846');

-- Dumping structure for table s87_Radient.tickets
CREATE TABLE IF NOT EXISTS `tickets` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_name` varchar(50) DEFAULT NULL,
  `channel_id` varchar(50) DEFAULT NULL,
  `owner_username` varchar(50) DEFAULT NULL,
  `owner_id` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `transcript` longtext NOT NULL DEFAULT '[]',
  `claimed` int(11) DEFAULT 0,
  `claimed_by` varchar(50) DEFAULT '',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table s87_Radient.tickets: ~2 rows (approximately)
REPLACE INTO `tickets` (`id`, `channel_name`, `channel_id`, `owner_username`, `owner_id`, `category`, `transcript`, `claimed`, `claimed_by`, `created_at`) VALUES
	(1, 'ticket-ghost_the_killer24', '1377394950479548498', 'ghost_the_killer24', '676685347542925352', 'support', '[]', 0, NULL, '2025-05-28 21:15:47'),
	(2, 'ticket-officalsenior', '1377408345316655155', 'offical.senior', '793058463272927234', 'politi', '[]', 0, '', '2025-05-28 22:09:01');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
