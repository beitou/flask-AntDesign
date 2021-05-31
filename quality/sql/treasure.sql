create table if not exists treasure(
  id int auto_increment primary key not null,
  name varchar(48) not null comment 'App名称',
  version_name varchar(48) not null comment '版本号，正式版本',
  version bigint default 0 comment '版本号，升级使用',
  branch varchar(48) not null comment '代码分支',
  platform varchar(48) not null comment '平台[android|ios]',
  type varchar(48) not null comment '包类型',
  commit_id varchar(40) not null comment '最后提交ID',
  submitter varchar(48) not null comment '最后提交人',
  url varchar(1024) not null comment '下载地址',
  image varchar(48) not null comment '创建时间',
  created datetime not null comment '创建时间'
);
