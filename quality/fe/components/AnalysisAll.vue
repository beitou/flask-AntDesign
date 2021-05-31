<template>
  <div>
    <h2>产品质量：统计缺陷密度、严重级别分布、类型分布</h2>
    <a-row class="gutter">
      <a-table
        :columns="defectColumns"
        :dataSource="data.density"
        :pagination="false"
        bordered
      />
    </a-row>
    <a-row class="gutter">
      <a-table
        :columns="defectPriority"
        :dataSource="data.priority"
        :pagination="false"
        bordered
      />
    </a-row>
    <h2>研发过程质量：统计缺陷生存周期、开发光荣榜、开发质量预警</h2>
    <a-row class="gutter">
      <a-table
        :columns="defectPeriod"
        :dataSource="data.period"
        :pagination="false"
        bordered
      />
    </a-row>
    <a-row class="gutter">
      <div id="good_coder" style="width: 800px; height:600px;"></div>
    </a-row>
    <a-row class="gutter">
      <div id="bad_coder" style="width: 800px; height:600px;"></div>
    </a-row>
    <h2>
      测试过程质量：统计提交缺陷数量、缺陷有效率、测试光荣榜、测试质量预警
    </h2>
    <a-row class="gutter">
      <a-table
        :columns="defectQaRank"
        :dataSource="data.qa_rank"
        :pagination="false"
        bordered
      />
    </a-row>
    <a-row class="gutter">
      <div id="good_tester" style="width: 800px; height:600px;"></div>
    </a-row>
    <a-row class="gutter">
      <div id="bad_tester" style="width: 800px; height:600px;"></div>
    </a-row>
  </div>
</template>

<script>
const defectColumns = [
  {
    title: '缺陷密度统计',
    dataIndex: 'team',
    width: '25%',
  },
  {
    title: '缺陷密度',
    dataIndex: 'bpk',
    width: '25%',
  },
  {
    title: '缺陷数量',
    dataIndex: 'bugs',
    width: '25%',
  },
  {
    title: '缺陷占比',
    dataIndex: 'percent',
    width: '25%',
  },
]

const defectPriority = [
  {
    title: '缺陷严重级别分布',
    dataIndex: 'team',
    width: '20%',
  },
  {
    title: '致命',
    dataIndex: 'highest',
    width: '12%',
  },
  {
    title: '严重',
    dataIndex: 'high',
    width: '12%',
  },
  {
    title: '一般',
    dataIndex: 'medium',
    width: '12%',
  },
  {
    title: '低级',
    dataIndex: 'low',
    width: '12%',
  },
  {
    title: '建议',
    dataIndex: 'lowest',
    width: '12%',
  },
  {
    title: '严重问题占比',
    dataIndex: 'percent',
    width: '20%',
  },
]

const defectPeriod = [
  {
    title: '缺陷生存周期（h）',
    dataIndex: 'team',
    width: '20%',
  },
  {
    title: '平均生存周期',
    dataIndex: 'average',
    width: '12%',
  },
  {
    title: '最长生存周期',
    dataIndex: 'maximum',
    width: '12%',
  },
  {
    title: '最短生存周期',
    dataIndex: 'minimum',
    width: '12%',
  },
]

const defectQaRank = [
  {
    title: '测试过程质量（h）',
    dataIndex: 'user',
    width: '20%',
  },
  {
    title: '提交缺陷数量',
    dataIndex: 'total',
    width: '12%',
  },
  {
    title: '缺陷有效率',
    dataIndex: 'percent',
    width: '12%',
  },
  {
    title: '缺陷探测率',
    dataIndex: 'valid',
    width: '12%',
  },
]

export default {
  props: {
    data: {
      type: Object,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: {},
    },
    year: {
      type: String,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: '2020',
    },
    month: {
      type: String,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: '01',
    },
  },
  data() {
    return {
      defectColumns: defectColumns,
      defectPriority: defectPriority,
      defectPeriod: defectPeriod,
      defectQaRank: defectQaRank,
    }
  },
  mounted() {
    this.good_coder()
    this.bad_coder()
    this.good_tester()
    this.bad_tester()
  },
  methods: {
    good_coder(data) {
      let parameter = {
        year: this.year,
        good_coder: 'good_coder',
      }

      if (this.month !== 'all') {
        parameter.month = this.month
      }

      this.$axios
        .get('/analysis/api/v1/search', {
          params: parameter,
        })
        .then(res => {
          if (res.data.status === 0) {
            let data = {
              user: [],
              common: [],
              serious: [],
              total: [],
              percent: [],
            }

            for (const user in res.data.data) {
              data.user.push(user)
              data.common.push(res.data.data[user].common)
              data.serious.push(res.data.data[user].serious)
              data.total.push(res.data.data[user].total)
              data.percent.push(res.data.data[user].percent)
            }
            let goodCoder = this.$echarts.init(
              document.getElementById('good_coder')
            )

            const option = {
              toolbox: {
                feature: {
                  saveAsImage: {},
                },
              },
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  // 坐标轴指示器，坐标轴触发有效
                  type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                },
                formatter: '{c}%',
              },
              legend: {
                data: ['一般问题', '严重问题'],
              },
              grid: {
                left: '4%',
                right: '4%',
                bottom: '4%',
                containLabel: true,
              },
              xAxis: {
                type: 'category',
                data: data.user,
              },
              yAxis: [
                {
                  type: 'value',
                  name: '一般/严重问题个数',
                  min: 0,
                  max: 50,
                },
                {
                  type: 'value',
                  name: '严重问题占比',
                  min: 0,
                  max: 50,
                  position: 'right',
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
              ],
              series: [
                {
                  name: '一般',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#61a0a8',
                    },
                  },
                  data: data.common,
                },
                {
                  name: '严重',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#c23531',
                    },
                  },
                  data: data.serious,
                },
                {
                  name: '严重问题占比',
                  type: 'line',
                  label: {
                    normal: {
                      show: true,
                      position: 'top',
                      formatter: '{c}%',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#2f4554',
                    },
                  },
                  data: data.percent,
                },
              ],
            }

            goodCoder.setOption(option)
          } else {
            this.$message.error(res.data.message)
          }
        })
    },
    bad_coder(data) {
      let parameter = {
        year: this.year,
        bad_coder: 'bad_coder',
      }

      if (this.month !== 'all') {
        parameter.month = this.month
      }

      this.$axios
        .get('/analysis/api/v1/search', {
          params: parameter,
        })
        .then(res => {
          if (res.data.status === 0) {
            let data = {
              user: [],
              common: [],
              serious: [],
              total: [],
              percent: [],
            }

            for (const user in res.data.data) {
              data.user.push(user)
              data.common.push(res.data.data[user].common)
              data.serious.push(res.data.data[user].serious)
              data.total.push(res.data.data[user].total)
              data.percent.push(res.data.data[user].percent)
            }

            let badCoder = this.$echarts.init(
              document.getElementById('bad_coder')
            )

            let option = {
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  // 坐标轴指示器，坐标轴触发有效
                  type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                },
                formatter: '{c}%',
                textStyle: {
                  fontSize: 30,
                },
              },
              legend: {
                data: ['一般问题', '严重问题'],
              },
              grid: {
                left: '4%',
                right: '4%',
                bottom: '4%',
                containLabel: true,
              },
              xAxis: {
                type: 'category',
                data: data.user,
              },
              yAxis: [
                {
                  type: 'value',
                  name: '一般/严重问题个数',
                  min: 0,
                  max: 100,
                },
                {
                  type: 'value',
                  name: '严重问题占比',
                  min: 0,
                  max: 100,
                  position: 'right',
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
              ],
              series: [
                {
                  name: '一般',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#61a0a8',
                    },
                  },
                  data: data.common,
                },
                {
                  name: '严重',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#c23531',
                    },
                  },
                  data: data.serious,
                },
                {
                  name: '严重问题占比',
                  type: 'line',
                  label: {
                    normal: {
                      show: true,
                      position: 'top',
                      formatter: '{c}%',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#2f4554',
                    },
                  },
                  data: data.percent,
                },
              ],
            }

            badCoder.setOption(option)
          } else {
            this.$message.error(res.data.message)
          }
        })
    },
    good_tester(data) {
      let parameter = {
        year: this.year,
        good_tester: 'good_tester',
      }

      if (this.month !== 'all') {
        parameter.month = this.month
      }

      this.$axios
        .get('/analysis/api/v1/search', {
          params: parameter,
        })
        .then(res => {
          if (res.data.status === 0) {
            let data = {
              user: [],
              common: [],
              serious: [],
              total: [],
              percent: [],
            }

            for (const user in res.data.data) {
              data.user.push(user)
              data.common.push(res.data.data[user].common)
              data.serious.push(res.data.data[user].serious)
              data.total.push(res.data.data[user].total)
              data.percent.push(res.data.data[user].percent)
            }

            let goodTester = this.$echarts.init(
              document.getElementById('good_tester')
            )

            let option = {
              toolbox: {
                feature: {
                  saveAsImage: {},
                },
              },
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  // 坐标轴指示器，坐标轴触发有效
                  type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                },
                formatter: '{c}%',
              },
              legend: {
                data: ['一般问题', '严重问题'],
              },
              grid: {
                left: '4%',
                right: '4%',
                bottom: '4%',
                containLabel: true,
              },
              xAxis: {
                type: 'category',
                data: data.user,
              },
              yAxis: [
                {
                  type: 'value',
                  name: '一般/严重问题个数',
                  min: 0,
                  max: 120,
                },
                {
                  type: 'value',
                  name: '严重问题占比',
                  min: 0,
                  max: 120,
                  position: 'right',
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
              ],
              series: [
                {
                  name: '一般',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#61a0a8',
                    },
                  },
                  data: data.common,
                },
                {
                  name: '严重',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#c23531',
                    },
                  },
                  data: data.serious,
                },
                {
                  name: '严重问题占比',
                  type: 'line',
                  label: {
                    normal: {
                      show: true,
                      position: 'top',
                      formatter: '{c}%',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#2f4554',
                    },
                  },
                  data: data.percent,
                },
              ],
            }

            goodTester.setOption(option)
          } else {
            this.$message.error(res.data.message)
          }
        })
    },
    bad_tester() {
      let parameter = {
        year: this.year,
        bad_tester: 'bad_tester',
      }

      if (this.month !== 'all') {
        parameter.month = this.month
      }

      this.$axios
        .get('/analysis/api/v1/search', {
          params: parameter,
        })
        .then(res => {
          if (res.data.status === 0) {
            let data = {
              user: [],
              common: [],
              serious: [],
              total: [],
              percent: [],
            }

            for (const user in res.data.data) {
              data.user.push(user)
              data.common.push(res.data.data[user].common)
              data.serious.push(res.data.data[user].serious)
              data.total.push(res.data.data[user].total)
              data.percent.push(res.data.data[user].percent)
            }

            let badTester = this.$echarts.init(
              document.getElementById('bad_tester')
            )

            let option = {
              toolbox: {
                feature: {
                  saveAsImage: {},
                },
              },
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  // 坐标轴指示器，坐标轴触发有效
                  type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                },
                formatter: '{c}%',
                textStyle: {
                  fontSize: 30,
                },
              },
              legend: {
                data: ['一般问题', '严重问题'],
              },
              grid: {
                left: '4%',
                right: '4%',
                bottom: '4%',
                containLabel: true,
              },
              xAxis: {
                type: 'category',
                data: data.user,
              },
              yAxis: [
                {
                  type: 'value',
                  name: '一般/严重问题个数',
                  min: 0,
                  max: Math.max(data.total),
                  position: 'left',
                },
                {
                  type: 'value',
                  name: '严重问题占比',
                  min: 0,
                  max: Math.ceil(Math.max(data.total)),
                  position: 'right',
                  axisLabel: {
                    formatter: '{value} %',
                  },
                },
              ],
              series: [
                {
                  name: '一般',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#2f4554',
                    },
                  },
                  data: data.common,
                },
                {
                  name: '严重',
                  type: 'bar',
                  stack: '总量',
                  label: {
                    normal: {
                      show: true,
                      position: 'inside',
                    },
                  },
                  itemStyle: {
                    normal: {
                      color: '#c23531',
                    },
                  },
                  data: data.serious,
                },
                {
                  name: '严重问题占比',
                  type: 'line',
                  label: {
                    normal: {
                      show: true,
                      fontSize: 30,
                      position: 'top',
                      formatter: '{c}%',
                    },
                  },
                  data: data.percent,
                },
              ],
            }

            badTester.setOption(option)
          } else {
            this.$message.error(res.data.message)
          }
        })
    },
  },
}
</script>

<style scoped>
.gutter {
  padding-top: 20px;
  padding-bottom: 20px;
}
</style>
