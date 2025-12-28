SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS `lead` (
  `lead_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT NOT NULL DEFAULT 1,
  `phone_encrypted` VARBINARY(128) NOT NULL,
  `phone_enc_iv` VARBINARY(24) NOT NULL,
  `phone_enc_key_id` VARCHAR(64) NOT NULL,
  `phone_search_hash` CHAR(64) NOT NULL,
  `pool_type` VARCHAR(20) NOT NULL,
  `owner_user_id` BIGINT DEFAULT NULL,
  `status` VARCHAR(20) NOT NULL DEFAULT 'new',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `assigned_at` DATETIME DEFAULT NULL,
  `first_contact_at` DATETIME DEFAULT NULL,
  `last_contact_at` DATETIME DEFAULT NULL,
  `next_followup_time` DATETIME DEFAULT NULL,
  `invalid_flag` TINYINT(1) DEFAULT 0,
  `visited_flag` TINYINT(1) DEFAULT 0,
  `quoted_flag` TINYINT(1) DEFAULT 0,
  `is_active` TINYINT AS (CASE WHEN invalid_flag=0 THEN 1 ELSE 0 END) STORED,
  `is_private_active` TINYINT AS (CASE WHEN pool_type='private' AND invalid_flag=0 THEN 1 ELSE 0 END) STORED,
  `version` INT DEFAULT 1,
  PRIMARY KEY (`lead_id`),
  UNIQUE KEY `uk_tenant_phone` (`tenant_id`, `phone_search_hash`),
  KEY `idx_assigned_at` (`assigned_at`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_public_pool_sort` (`pool_type`, `intention_level`, `created_at`),
  KEY `idx_private_active_follow` (`is_private_active`, `owner_user_id`, `next_followup_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `handover_batch` (
  `batch_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT NOT NULL DEFAULT 1,
  `handover_type` VARCHAR(20) NOT NULL,
  `from_user_id` BIGINT NOT NULL,
  `strategy` VARCHAR(20) NOT NULL,
  `filters_snapshot` JSON,
  `total_selected` INT DEFAULT 0,
  `total_transferred` INT DEFAULT 0,
  `total_failed` INT DEFAULT 0,
  `status` VARCHAR(20) NOT NULL DEFAULT 'draft',
  `created_by` BIGINT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `handover_item` (
  `item_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `batch_id` BIGINT UNSIGNED NOT NULL,
  `lead_id` BIGINT UNSIGNED NOT NULL,
  `from_user_id` BIGINT NOT NULL,
  `to_user_id` BIGINT NOT NULL,
  `result` VARCHAR(20),
  `fail_reason` VARCHAR(255),
  `transferred_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`item_id`),
  KEY `idx_batch` (`batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `file_object` (
  `file_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT NOT NULL DEFAULT 1,
  `file_class` VARCHAR(20) NOT NULL,
  `storage_path` VARCHAR(500) NOT NULL,
  `sha256_hash` CHAR(64) NOT NULL,
  `uploaded_by` BIGINT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `audit_log` (
  `log_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tenant_id` BIGINT NOT NULL DEFAULT 1,
  `user_id` BIGINT NOT NULL,
  `action` VARCHAR(50) NOT NULL,
  `resource_type` VARCHAR(50) NOT NULL,
  `resource_id` BIGINT NOT NULL,
  `before_json` JSON DEFAULT NULL,
  `after_json` JSON DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`, `created_at`)
) ENGINE=InnoDB 
PARTITION BY RANGE (YEAR(created_at) * 100 + MONTH(created_at)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p_max VALUES LESS THAN MAXVALUE
);

SET FOREIGN_KEY_CHECKS = 1;
