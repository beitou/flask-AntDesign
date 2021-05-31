create table if not exists gitlab(
  commit_id varchar(48) primary key not null comment 'commit id',
  project varchar(48) not null comment '项目名称',
  namespace varchar(48) not null comment '项目分组',
  branch varchar(48) not null comment '代码分支',
  created_at datetime not null comment 'create时间',
  committer varchar(48) not null comment '提交人',
  committer_email varchar(48) not null comment '提交人邮箱',
  committed_date datetime not null comment '提交时间',
  additions bigint default 0 comment '添加代码行数',
  deletions bigint default 0 comment '删除代码行数',
  total bigint default 0 comment '修改代码行数',
  status varchar(48) not null comment '状态'
);
