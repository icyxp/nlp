# Introduce

## create table
```
CREATE TABLE `mapping` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `mapping` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
```

`modify db.conf`



## install
```
pip install virtualenv
virtualenv --no-site-packages hackathon
source hackathon/bin/active
pip install -r requirements.txt
```