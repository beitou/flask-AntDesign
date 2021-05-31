<template>
  <div>
    <a-row :gutter="20" class="gutter">
      <a-col :span="2">
        <a-select @change="handleYear" v-model="year" class="toolbar">
          <a-select-option value="2020">2020</a-select-option>
          <a-select-option value="2021">2021</a-select-option>
          <a-select-option value="2022">2022</a-select-option>
          <a-select-option value="2023">2023</a-select-option>
          <a-select-option value="2024">2024</a-select-option>
          <a-select-option value="2025">2025</a-select-option>
          <a-select-option value="2026">2026</a-select-option>
          <a-select-option value="2027">2027</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="2">
        <a-select @change="handleMonth" v-model="month" class="toolbar">
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="1">1月</a-select-option>
          <a-select-option value="2">2月</a-select-option>
          <a-select-option value="3">3月</a-select-option>
          <a-select-option value="4">4月</a-select-option>
          <a-select-option value="5">5月</a-select-option>
          <a-select-option value="6">6月</a-select-option>
          <a-select-option value="7">7月</a-select-option>
          <a-select-option value="8">8月</a-select-option>
          <a-select-option value="9">8月</a-select-option>
          <a-select-option value="10">10月</a-select-option>
          <a-select-option value="11">11月</a-select-option>
          <a-select-option value="12">12月</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="3">
        <a-select @change="handleTeam" v-model="team" class="toolbar">
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="基础服务">基础服务</a-select-option>
          <a-select-option value="保险服务">保险服务</a-select-option>
          <a-select-option value="保险供应链">保险供应链</a-select-option>
          <a-select-option value="财商基金">财商基金</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="2">
        <a-button @click="refresh" type="primary" class="toolbar">
          搜索
        </a-button>
      </a-col>
    </a-row>
    <div v-if="isAll">
      <AnalysisAll ref="analysisAll" :data="data" :year="year" :month="month" />
    </div>
    <div v-else>
      <AnalysisTeam :data="data" :year="year" :month="month" />
    </div>
  </div>
</template>

<script>
import AnalysisAll from '~/components/AnalysisAll.vue'
import AnalysisTeam from '~/components/AnalysisTeam.vue'

export default {
  components: {
    AnalysisAll,
    AnalysisTeam,
  },
  data() {
    return {
      isAll: true,
      year: '2020',
      month: 'all',
      team: 'all',
      data: {},
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    handleYear(value) {
      this.year = value
    },
    handleMonth(value) {
      this.month = value
    },
    handleTeam(value) {
      this.team = value
    },
    handleATeam(data) {
      console.log(data)
      // 这里处理缺陷统计数据
      let bug_analysis = []
      const total = data.product.bug_analysis.total
      const status = data.product.bug_analysis.status
      const priority = data.product.bug_analysis.priority
      bug_analysis.push({
        priority: '致命',
        priority_number: priority.highest,
        priority_percent: ((100 * priority.highest) / total).toFixed(2) + '%',
        status: '新开',
        status_number: status.新开,
        status_percent: ((100 * status.新开) / total).toFixed(2) + '%',
      })
      bug_analysis.push({
        priority: '严重',
        priority_number: priority.high,
        priority_percent: ((100 * priority.high) / total).toFixed(2) + '%',
        status: '已解决',
        status_number: status.已解决,
        status_percent: ((100 * status.已解决) / total).toFixed(2) + '%',
      })
      bug_analysis.push({
        priority: '一般',
        priority_number: priority.medium,
        priority_percent: ((100 * priority.medium) / total).toFixed(2) + '%',
        status: '已关闭',
        status_number: status.已关闭,
        status_percent: ((100 * status.已关闭) / total).toFixed(2) + '%',
      })
      bug_analysis.push({
        priority: '低级',
        priority_number: priority.low,
        priority_percent: ((100 * priority.low) / total).toFixed(2) + '%',
        status: '已拒绝',
        status_number: status.已拒绝,
        status_percent: ((100 * status.已拒绝) / total).toFixed(2) + '%',
      })
      bug_analysis.push({
        priority: '建议',
        priority_number: priority.lowest,
        priority_percent: ((100 * priority.lowest) / total).toFixed(2) + '%',
        status: '重开',
        status_number: status.重开,
        status_percent: ((100 * status.重开) / total).toFixed(2) + '%',
      })
      data.product.bug_analysis = bug_analysis

      // 这里处理开发质量统计数据
      let coder_analysis = []
      for (const user in data.product.coder_analysis) {
        const item = data.product.coder_analysis[user]
        coder_analysis.push({
          user: user,
          total: item.total,
          total_percent: item.total_percent + '%',
          serious: item.serious,
          serious_percent: item.serious_percent + '%',
          cost: item.cost,
        })
      }
      data.product.coder_analysis = coder_analysis

      // 这里处理开发质量统计数据
      let tester_analysis = []
      for (const user in data.product.tester_analysis) {
        const item = data.product.tester_analysis[user]
        tester_analysis.push({
          user: user,
          total: item.total,
          valid: ((100 * item.valid) / item.total).toFixed(2) + '%',
          data: item.total,
        })
      }
      data.product.tester_analysis = tester_analysis

      this.data = data.product
    },
    handleAllTeam(data) {
      // 这里处理缺陷密度数据
      let density = []
      for (const team in data.product.density) {
        const item = data.product.density[team]
        density.push({
          team: team,
          bpk: item.bpk + '%',
          bugs: item.bugs,
          percent: item.percent + '%',
        })
      }
      data.product.density = density

      // 这里处理缺陷级别数据
      let priority = []
      for (const team in data.product.priority) {
        const item = data.product.priority[team]
        priority.push({
          team: team,
          highest: item.highest,
          high: item.high,
          medium: item.medium,
          low: item.low,
          lowest: item.lowest,
          percent: item.percent + '%',
          total: item.total,
        })
      }
      data.product.priority = priority

      // 这里处理缺陷周期数据
      let period = []
      for (const team in data.product.period) {
        const item = data.product.period[team]
        period.push({
          team: team,
          average: item.average,
          maximum: item.maximum,
          minimum: item.minimum,
        })
      }
      data.product.period = period

      // 这里处理缺陷按QA排名
      let qa_rank = []
      for (const user in data.product.qa_rank) {
        const item = data.product.qa_rank[user]
        qa_rank.push({
          user: user,
          percent: item.percent + '%',
          total: item.total,
          valid: item.valid,
        })
      }
      data.product.qa_rank = qa_rank

      let bad_tester = {
        user: [],
        common: [],
        serious: [],
        percent: [],
      }
      for (const user in this.data.product.bad_tester) {
        bad_tester.user.push(user)
        bad_tester.common.push(this.data.product.bad_tester[user].common)
        bad_tester.serious.push(this.data.product.bad_tester[user].serious)
        bad_tester.percent.push(this.data.product.bad_tester[user].percent)
      }
      console.log('bad_tester', bad_tester)
      this.$refs.analysisAll.bad_tester(bad_tester)

      this.data = data.product
    },
    refresh() {
      this.isAll = this.team === 'all'

      let parameter = {
        year: this.year,
      }

      if (this.month !== 'all') {
        parameter['month'] = this.month
      }

      if (this.team !== 'all') {
        parameter['department'] = this.team
      }

      this.$axios
        .get('/analysis/api/v1/search', {
          params: parameter,
        })
        .then(res => {
          this.loading = false
          if (res.data.status === 0) {
            this.data = res.data.data
            if (this.isAll) {
              this.handleAllTeam(this.data)
            } else {
              this.handleATeam(this.data)
            }
          } else {
            this.$message.error(res.data.message)
          }
        })
      // .catch(() => {
      //   this.$message.error('服务异常，请联系管理员姜成龙！')
      // })
    },
  },
  fillData() {
    this.$refs.analysisAll.good_coder()
    this.$refs.analysisAll.bad_coder()
    this.$refs.analysisAll.good_tester()
  },
}
</script>

<style scoped>
.toolbar {
  width: 100%;
}
</style>
