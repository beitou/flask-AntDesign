
function success(data) {

  console.log(data)

  serious = {
    'legend': [],
    'data': []
  }
  for (index in data['data']['serious']) {
    value = data['data']['serious'][index]
    serious['legend'].push(index)
    serious['data'].push({'value': value, 'name': index + '(' + value +')'})
  }
  circle("serious", "问题等级", serious)

  state = {
    'legend': [],
    'data': []
  }
  for (index in data['data']['status']) {
    value = data['data']['status'][index]
    state['legend'].push(index)
    state['data'].push({'value': value, 'name': index + '(' + value +')'})
  }
  circle("status", "问题状态", state)

  tester = {
    'legend': [],
    'data': []
  }
  for (index in data['data']['tester']) {
    value = data['data']['tester'][index]
    tester['legend'].push(index)
    tester['data'].push({'value': value, 'name': index + '(' + value +')'})
  }
  circle("tester", "测试人员", tester)

  developer = {
    'legend': [],
    'data': []
  }
  for (index in data['data']['developer']) {
    value = data['data']['developer'][index]
    developer['legend'].push(index)
    developer['data'].push({'value': value, 'name': index + '(' + value +')'})
  }
  circle("developer", "开发人员", developer)

  department = {
    'legend': [],
    'data': []
  }
  for (index in data['data']['department']) {
    value = data['data']['department'][index]
    department['legend'].push(index)
    department['data'].push({'value': value, 'name': index + '(' + value +')'})
  }
  circle("department", "部门数据", department)

//  smoke = []
//  for (level in data['data']['smoke']) {
//    value = data['data']['smoke'][level]
//    smoke.push({'value': value, 'name': level + '(' + value +')'})
//  }
//  circle("smoke", "冒烟用例通过率", smoke)

//  $('#bugs').bootstrapTable({
//    showHeader: true,
//    showLoading: true,
//    striped: true,
//    toolbar: '#toolbar',
//    pagination: true,
//    sortable: false,
//    sortOrder: "asc",
//    sidePagination: "server",
//    pageNumber: 1,
//    pageSize: 50,
//    pageList: [10, 20, 50],
//    search: false,
//    showExport: true,
//    data: data['data']['bugs'],
//    columns: [{
//      field: 'business',
//      title: '业务线'
//    }, {
//      field: 'endpoint',
//      title: '产品'
//    }, {
//      field: 'sprint',
//      title: '迭代'
//    }, {
//      field: 'priority',
//      title: '优先级'
//    }, {
//      field: 'summary',
//      title: '标题',
//      formatter: function(value, row, index) {
//        return '<a href="' + row.url + '" target="_blank">' + row.summary + '</a>';
//      }
//    }, {
//      field: 'status',
//      title: '状态'
//    }, {
//      field: 'reporter',
//      title: '报告人'
//    }, {
//      field: 'assignee',
//      title: '经办人'
//    }, {
//      field: 'created',
//      title: '创建时间'
//    }, {
//      field: 'updated',
//      title: '更新时间'
//    },]
//});
}

function error(data) {
  console.log(data)
}

$(function () {
  url = "/project/search"
  method = "get"
  data = {
    "sprint": "xxxx"
  }
  http(url, method, data, success, error)
})
