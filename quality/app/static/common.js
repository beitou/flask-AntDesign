
function http(url, method, data, success, error) {
  var data = method == 'GET' ? data : JSON.stringify(data)
  $.ajax({
    url: url,
    type: method,
    data: data,
    contentType: "application/json;charset=UTF-8",
    dataType: "json",
    success: success || function(data) {
      console.log(result);
    },
    error: error || function(data) {
      console.log(data);
    }
  });
}

function circle(id, title, result) {
  var myChart = echarts.init(document.getElementById(id));
  console.log(result['legend'])
  console.log(result['data'])
  option = {
    title : {
      text: title,
      x:'center'
    },
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: result['legend']
    },
    series : [
      {
        name: '质量数据',
        type: 'pie',
        radius : '55%',
        center: ['50%', '60%'],
        data: result['data'],
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  myChart.setOption(option);
}