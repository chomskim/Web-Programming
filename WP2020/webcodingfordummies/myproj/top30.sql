select pt.`date`, jm.`name`, pt.close_price from price_table pt, jongmok_master jm
where pt.`code`=jm.`code` and `date` >= '2018-09-01'
and pt.`code` in (
'A005930', 'A000660', 'A005380', 'A005490', 'A028260',
'A035420', 'A105560', 'A017670', 'A051910', 'A055550',
'A034730', 'A012330', 'A096770', 'A032830', 'A051900',
'A018260', 'A006400', 'A015760', 'A010950', 'A033780',
'A086790', 'A000270', 'A000810', 'A090430', 'A003550',
'A251270', 'A066570', 'A036570', 'A035720', 'A030200')
order by `date`, jm.`name`;