<template>
  <div>
    <h2>开发质量统计：缺陷数量、缺陷修复时长、缺陷状态、缺陷等级</h2>
    <a-row class="gutter">
      <a-table
        :columns="bugAnalysis"
        :dataSource="data.bug_analysis"
        :pagination="false"
        bordered
      />
    </a-row>

    <h2>测试质量统计：提交缺陷数量、缺陷有效率、缺陷探测率</h2>
    <a-row class="gutter">
      <a-table
        :columns="coderAnalysis"
        :dataSource="data.coder_analysis"
        :pagination="false"
        bordered
      />
    </a-row>

    <h2>缺陷统计：</h2>
    <a-row class="gutter">
      <a-table
        :columns="testerAnalysis"
        :dataSource="data.tester_analysis"
        :pagination="false"
        bordered
      />
    </a-row>
  </div>
</template>

<script>
const bugAnalysis = [
  {
    title: '缺陷等级',
    dataIndex: 'priority',
    width: '20%',
  },
  {
    title: '数量',
    dataIndex: 'priority_number',
    width: '15%',
  },
  {
    title: '占比',
    dataIndex: 'priority_percent',
    width: '15%',
  },
  {
    title: '缺陷等级',
    dataIndex: 'status',
    width: '20%',
  },
  {
    title: '数量',
    dataIndex: 'status_number',
    width: '15%',
  },
  {
    title: '占比',
    dataIndex: 'status_percent',
    width: '15%',
  },
]

const coderAnalysis = [
  {
    title: '开发质量统计',
    dataIndex: 'user',
    width: '20%',
  },
  {
    title: '缺陷数量',
    dataIndex: 'total',
    width: '15%',
  },
  {
    title: '缺陷数量占比',
    dataIndex: 'total_percent',
    width: '15%',
  },
  {
    title: '严重问题数量',
    dataIndex: 'serious',
    width: '15%',
  },
  {
    title: '严重问题占比',
    dataIndex: 'serious_percent',
    width: '15%',
  },
  {
    title: '缺陷修复时长(h)',
    dataIndex: 'cost',
    width: '20%',
  },
]

const testerAnalysis = [
  {
    title: '测试质量统计',
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
    dataIndex: 'valid',
    width: '12%',
  },
  {
    title: '缺陷探测率',
    dataIndex: 'data',
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
  },
  data() {
    return {
      bugAnalysis: bugAnalysis,
      coderAnalysis: coderAnalysis,
      testerAnalysis: testerAnalysis,
    }
  },
}
</script>

<style scoped>
.gutter {
  padding-top: 20px;
  padding-bottom: 20px;
}
</style>
