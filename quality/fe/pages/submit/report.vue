<template>
  <div class="container">
    <h1>测试报告</h1>
    <h3>一、目的和范围</h3>
    <p>
      1.1 目的
      本测试报告目的在于总结测试阶段的测试情况以及分析测试结果，描述系统是否符合需求，以便进一步跟进
      1.2 范围
      该文档适用于用户、测试人员、开发人员、项目管理者、和需要阅读本报告的高层领导
    </p>
    <h3>二、测试策略</h3>
    <a-form>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="操作系统"
      >
        <a-textarea
          v-model="os"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="浏览器"
      >
        <a-textarea
          v-model="browsers"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="机型"
      >
        <a-textarea
          v-model="phones"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="测试地址"
      >
        <a-textarea
          v-model="links"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="测试方法"
      >
        <a-textarea
          v-model="methods"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
    </a-form>
    <h3>三、测试结果分析</h3>
    <a-row>
      <a-col :span="12">
        <ve-pie :data="numberPie"></ve-pie>
      </a-col>
      <a-col :span="12">
        <a-card title="bug状态统计">
          <a-card-grid style="width:16%;textAlign:'center'">
            等级
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            致命
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            严重
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            一般
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            低级
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            建议
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            数量
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="numberPie.rows[0].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            <a-input-number
              v-model="numberPie.rows[1].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="numberPie.rows[2].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="numberPie.rows[3].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="numberPie.rows[4].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
        </a-card>
      </a-col>
    </a-row>
    <a-row>
      <a-col :span="12">
        <ve-pie :data="statusPie"></ve-pie>
      </a-col>
      <a-col :span="12">
        <a-card title="bug状态统计">
          <a-card-grid style="width:16%;textAlign:'center'">
            状态
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            新开
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            进行
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            已解
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            拒绝
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            关闭
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            数量
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="statusPie.rows[0].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            <a-input-number
              v-model="statusPie.rows[1].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="statusPie.rows[2].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="statusPie.rows[3].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:17%;textAlign:'center'">
            <a-input-number
              v-model="statusPie.rows[4].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
        </a-card>
      </a-col>
    </a-row>
    <a-row>
      <a-col :span="12">
        <ve-pie :data="typePie"></ve-pie>
      </a-col>
      <a-col :span="12">
        <a-card title="bug分类统计">
          <a-card-grid style="width:16%;textAlign:'center'">
            分类
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            功能
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            数据
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            界面
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            兼容
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            性能
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            安全
          </a-card-grid>
          <a-card-grid style="width:16%;textAlign:'center'">
            数量
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            <a-input-number
              v-model="typePie.rows[0].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            <a-input-number
              v-model="typePie.rows[1].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            <a-input-number
              v-model="typePie.rows[2].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            <a-input-number
              v-model="typePie.rows[3].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            <a-input-number
              v-model="typePie.rows[4].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
          <a-card-grid style="width:14%;textAlign:'center'">
            <a-input-number
              v-model="typePie.rows[5].value"
              :min="0"
              :max="100"
            />
          </a-card-grid>
        </a-card>
      </a-col>
    </a-row>
    <a-form>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="测试总结评估及改进建议"
      >
        <a-textarea
          v-model="summary"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 12 }"
        label="备注"
      >
        <a-textarea
          v-model="remark"
          v-decorator="[
            'note',
            { rules: [{ required: true, message: 'Please input your note!' }] },
          ]"
        />
      </a-form-item>
    </a-form>
    <div>
      <a-button @click="save" type="primary">保存</a-button>
    </div>
  </div>
</template>

<script>
import VePie from 'v-charts/lib/pie.common'

export default {
  components: {
    VePie,
  },
  data() {
    return {
      os: '',
      browsers: '',
      phones: '',
      links: '',
      methods: '',
      summary: '',
      remark: '',
      numberPie: {
        columns: ['name', 'value'],
        rows: [
          { name: '致命', value: 0 },
          { name: '严重', value: 0 },
          { name: '一般', value: 0 },
          { name: '低级', value: 0 },
          { name: '建议', value: 0 },
        ],
      },
      statusPie: {
        columns: ['name', 'value'],
        rows: [
          { name: '新开', value: 0 },
          { name: '进行中', value: 0 },
          { name: '已解决', value: 0 },
          { name: '已拒绝', value: 0 },
          { name: '已关闭', value: 0 },
        ],
      },
      typePie: {
        columns: ['name', 'value'],
        rows: [
          { name: '功能操作', value: 0 },
          { name: '数据问题', value: 0 },
          { name: '界面优化', value: 0 },
          { name: '兼容性问题', value: 0 },
          { name: '性能优化', value: 0 },
          { name: '安全问题', value: 0 },
        ],
      },
    }
  },
  mounted() {
    this.getReport()
  },
  methods: {
    getReport() {
      this.$axios
        .get('/submit/api/v1/testreport/data/search', {
          params: { submit_data_id: this.$route.query.id },
        })
        .then(res => {
          if (res.data.status === 0) {
            this.os = res.data.data[0].t_os_name
            this.browsers = res.data.data[0].t_browsers
            this.phones = res.data.data[0].t_phones
            this.links = res.data.data[0].t_link
            this.methods = res.data.data[0].t_methods
            this.summary = res.data.data[0].t_summary
            this.remark = res.data.data[0].t_memo
            this.numberPie.rows[0].value = res.data.data[0].bug_fatal
            this.numberPie.rows[1].value = res.data.data[0].bug_serious
            this.numberPie.rows[2].value = res.data.data[0].bug_general
            this.numberPie.rows[3].value = res.data.data[0].bug_low
            this.numberPie.rows[4].value = res.data.data[0].bug_suggest
            this.statusPie.rows[0].value = res.data.data[0].bug_new
            this.statusPie.rows[1].value = res.data.data[0].bug_processing
            this.statusPie.rows[2].value = res.data.data[0].bug_resolve
            this.statusPie.rows[3].value = res.data.data[0].bug_refuse
            this.statusPie.rows[4].value = res.data.data[0].bug_closed
            this.typePie.rows[0].value = res.data.data[0].bug_function
            this.typePie.rows[1].value = res.data.data[0].bug_data
            this.typePie.rows[2].value = res.data.data[0].bug_ui
            this.typePie.rows[3].value = res.data.data[0].bug_compatibility
            this.typePie.rows[4].value = res.data.data[0].bug_performance
            this.typePie.rows[5].value = res.data.data[0].bug_security
          } else {
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.$message.error('服务异常，请联系管理员姜成龙！')
        })
    },
    save() {
      const data = {
        t_os_name: this.os,
        t_browsers: this.browsers,
        t_phones: this.phones,
        t_link: this.links,
        t_methods: this.methods,
        t_summary: this.summary,
        t_memo: this.remark,
        bug_fatal: this.numberPie.rows[0].value,
        bug_serious: this.numberPie.rows[1].value,
        bug_general: this.numberPie.rows[2].value,
        bug_low: this.numberPie.rows[3].value,
        bug_suggest: this.numberPie.rows[4].value,
        bug_new: this.statusPie.rows[0].value,
        bug_processing: this.statusPie.rows[1].value,
        bug_resolve: this.statusPie.rows[2].value,
        bug_refuse: this.statusPie.rows[3].value,
        bug_closed: this.statusPie.rows[4].value,
        bug_function: this.typePie.rows[0].value,
        bug_data: this.typePie.rows[1].value,
        bug_ui: this.typePie.rows[2].value,
        bug_compatibility: this.typePie.rows[3].value,
        bug_performance: this.typePie.rows[4].value,
        bug_security: this.typePie.rows[5].value,
        submit_data_id: this.$route.query.id,
      }
      console.log(data)
      this.$axios
        .post('/submit/api/v1/save/testreport/data', data)
        .then(res => {
          console.log(res)
          if (res.data.status === 0) {
            this.$notification.open({
              message: '保存数据成功',
              description: '首次保存后将自动发送测试报告，请注意查收！',
            })
          } else {
            this.$notification.error({
              message: '保存失败',
              description: '错误' + res.data.status + '：' + res.data.message,
            })
          }
        })
    },
  },
}
</script>

<style>
.container {
  padding-left: 100px;
  padding-right: 100px;
}
.ant-card {
  width: 660px;
}
.ant-input-number {
  margin: -24px;
}
</style>
