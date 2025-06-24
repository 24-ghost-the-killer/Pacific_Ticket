CREATE DATABASE IF NOT EXISTS `pacific_database`;
USE `pacific_database`;

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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

REPLACE INTO `categorys` (`id`, `label`, `value`, `emote`, `description`, `role_access`, `channel_category`, `created_at`) VALUES
	(1, 'Support', 'support', '🔧', 'Alle supportere kan hjælpe dig med denne sag.', '1376312327514619995', '1376313403752054804', '2025-05-25 18:50:44'),
	(2, 'Bande', 'bande', '🕵️', 'En bandeansvarlig vil hjælpe dig med dette.', '1377046263769464983', '1383908083096617123', '2025-05-25 18:50:44'),
	(3, 'Firma', 'firma', '🏢', 'En firmaansvarlig vil hjælpe dig med dette.', '1377046342886625281', '1383908101018751017', '2025-05-25 18:50:44'),
	(4, 'CK', 'ck', '⚰️', 'En CK-ansvarlig vil hjælpe dig med dette.', '1377046373698109451', '1383908120899621085', '2025-05-25 18:50:44'),
	(5, 'Development', 'development', '💻', 'Et medlem af dev-teamet vil hjælpe dig her.', '1377046409290711080', '1383908142911586424', '2025-05-25 18:50:44'),
	(6, 'Content Creator', 'content creator', '🎥', 'En CC-ansvarlig vil hjælpe dig med dette.', '1377046910707175515', '1383908176956489920', '2025-05-25 18:50:44'),
	(7, 'Kompensation', 'kompensation', '💸', 'En kompensationsansvarlig vil hjælpe dig her.', '1377046438927925268', '1383908277154480148', '2025-05-25 18:50:44'),
	(8, 'Unban', 'unban', '🔓', 'En unban-ansvarlig vil hjælpe dig her.', '1377046534591610962', '1383908293008818267', '2025-05-25 18:50:44'),
	(9, 'Donation', 'donation', '💰', 'En donationsansvarlig vil hjælpe dig her.', '1377046571778179203', '1383908308892520458', '2025-05-25 18:50:44'),
	(10, 'Staff', 'Staff', '👥', 'En staff-ansvarlig vil hjælpe dig her.', '1377046609795350640', '1383908335169966211', '2025-05-25 18:50:44'),
	(11, 'Politi', 'politi', '🚔', 'En fra politiledelsen vil hjælpe dig her.', '1377046642892476468', '1383908348960833607', '2025-05-25 18:50:44');

CREATE TABLE IF NOT EXISTS `settings` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `disabled` int(11) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

REPLACE INTO `settings` (`id`, `name`, `value`, `disabled`) VALUES
	(1, 'support_role', '1376312327514619995', 0),
	(2, 'call_role', '1377057764475666615', 0),
	(3, 'call_support', 'true', 0),
	(4, 'close_time', '5', 0),
	(5, 'panel_role', '1376311994147147846', 0),
	(6, 'ticket_channel', '1376288663545188364', 0),
	(7, 'logging_channel', '1385586289340059729', 0),
	(8, 'support_channel', '1377058139928793088', 0);

CREATE TABLE IF NOT EXISTS `tickets` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_name` varchar(50) DEFAULT NULL,
  `channel_id` varchar(50) DEFAULT NULL,
  `owner_username` varchar(50) DEFAULT NULL,
  `owner_id` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `transcript` longtext NOT NULL DEFAULT '[]',
  `open` int(11) DEFAULT 1,
  `claimed` int(11) DEFAULT 0,
  `claimed_by` varchar(50) DEFAULT '',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;