export default [
  {
    path: '/',
    title: '首页',
    name: 'index',
  },
  {
    path: '/submit',
    title: '需求提测',
  },
  {
    path: '/analysis',
    title: '质量数据统计分析',
  },
  {
    path: '/genesis',
    title: '数据构造',
    children: [
      {
        path: '/genesis/digest',
        title: '埋点测试',
      },
      {
        path: '/genesis/tools',
        title: '小工具',
      },
      {
        path: '/genesis/delete',
        title: '删除线索',
      },
    ],
  },
  {
    path: '/treasure',
    title: '包管理',
  },
]
