# RecomStockSysByVNPY
通过tushare下载行情更新至数据库后作全行情回测，筛选出下单的股票进行邮件推荐

主函数：batch_stock.py

需要：
1、vnpy版本要求为2.1.*，没有升级最新的版本；
2、tushare token填写至GetStockKLineData.py的key；
3、邮件发送需要SMTP 服务，需要填写SMTP服务器、用户名、授权码、发件人、收件人；


附上MA_strategyV4_Share.py策略，需要放至vnpy strategy目录。
该策略利用移动平均线的差分公式计算其导数，判断导数大小下单。免责！
