create table if not exists board(
  id int auto_increment primary key not null,
  platform varchar(48) not null comment '平台',
  host varchar(1024) not null comment '域名',
  path varchar(1024) not null comment '接口',
  method varchar(48) not null comment '方法',
  visited datetime not null comment '访问时间'
);
