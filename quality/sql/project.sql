create table if not exists defect(
  id varchar(48) not null primary key comment 'Jira ID',
  business varchar(48) not null comment '业务线',
  endpoint varchar(48) not null comment '模块',
  classify varchar(48) not null comment '类型',
  sprint varchar(48) not null comment 'Sprint',
  summary varchar(1024) not null comment 'Jira标题',
  priority varchar(48) not null comment '问题等级',
  status varchar(48) not null comment '问题状态',
  reporter_name varchar(48) not null comment 'QA负责人拼音',
  reporter_display_name varchar(48) not null comment 'QA负责人中文',
  assignee_name varchar(48) not null comment 'RD负责人拼音',
  assignee_display_name varchar(48) not null comment 'RD负责人中文',
  created datetime not null comment '创建时间',
  updated datetime not null comment '更新时间',
  url varchar(1024) not null comment '问题链接'
);
