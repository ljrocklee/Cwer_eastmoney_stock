CREATE TABLE `t_py_stocklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eastmoney_code` varchar(8) DEFAULT NULL,
  `stock_code` varchar(8) DEFAULT NULL,
  `stock_name` varchar(20) DEFAULT NULL,
  `yes_values` varchar(10) DEFAULT NULL,
  `open_values` varchar(10) DEFAULT NULL,
  `new_values` varchar(10) DEFAULT NULL,
  `high_values` varchar(10) DEFAULT NULL,
  `low_values` varchar(10) DEFAULT NULL,
  `turnover_value` varchar(15) DEFAULT NULL,
  `turnover` varchar(15) DEFAULT NULL,
  `pricechange_value` varchar(15) DEFAULT NULL,
  `pricechange_ratio` varchar(15) DEFAULT NULL,
  `average_price` varchar(15) DEFAULT NULL,
  `amplitude` varchar(15) DEFAULT NULL,
  `weibi` varchar(15) DEFAULT NULL,
  `insert_date` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

