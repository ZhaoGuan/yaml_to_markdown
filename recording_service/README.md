表attributes
CREATE TABLE `attributes` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `info` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

表elements
CREATE TABLE `elements` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

表recording
CREATE TABLE `recording` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `test_case` varchar(255) DEFAULT NULL,
  `executor` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT 'pass',
  `message` longtext,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

表type_attribute
CREATE TABLE `type_attribute` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `element_id` int(11) DEFAULT NULL,
  `attribute_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
