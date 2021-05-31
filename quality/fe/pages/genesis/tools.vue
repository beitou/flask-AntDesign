<template>
  <div class="container">
    <a-row>
      <a-col :span="12">
        <a-form-item
          :label-col="{ span: 8 }"
          :wrapper-col="{ span: 16 }"
          label="这里输入TOKEN"
        >
          <a-input v-model="token" />
        </a-form-item>
        <a-button
          v-for="(item, index) in data"
          @click="createQuestionaire(item)"
          :key="index"
          type="primary"
        >
          {{ item.button }}
        </a-button>
      </a-col>
      <a-col :span="12">
        <a-form-item
          :label-col="{ span: 8 }"
          :wrapper-col="{ span: 16 }"
          label="请输入手机号"
        >
          <a-input v-model="phone" />
        </a-form-item>
        <a-button
          @click="queryCaptchaCode()"
          style="float:right;"
          type="primary"
        >
          查询验证码
        </a-button>
      </a-col>
    </a-row>
    <a-divider />
    <a-row :gutter="30">
      <a-col :span="12">
        <WaitYou />
      </a-col>
      <a-col :span="12">
        <Varibale />
      </a-col>
    </a-row>
  </div>
</template>

<script>
import WaitYou from '~/components/WaitYou.vue'
import Varibale from '~/components/Variable.vue'

export default {
  components: {
    WaitYou,
    Varibale,
  },
  data() {
    return {
      data: [],
      token: '',
      environment: 'qa',
      phone: '',
    }
  },
  mounted() {
    this.fetch()
  },
  methods: {
    createQuestionaire(item) {
      console.log(item)
      this.$axios
        .post('/genesis/api/v1/create_leads', {
          database: 'quality',
          table: 'genesis',
          page: 0,
          size: 1000,
          token: this.token,
          id: item.id,
        })
        .then(res => {
          console.log(res)
          this.data = res.data.data
        })
    },
    handleEnvironmentChange(value) {
      this.environment = value
    },
    queryCaptchaCode() {
      this.$axios
        .post('/captcha/code', {
          environment: this.environment,
          phone: this.phone,
        })
        .then(res => {
          console.log(res)
          if (res.data.status === 0) {
            this.$message.success(res.data.message)
          } else {
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.$message.error('服务异常，请联系管理员！')
        })
    },
    fetch(params = {}) {
      console.log(this.pagination)
      this.loading = true
      this.$axios
        .get('/genesis/api/v1/leads', {
          params: {
            database: 'quality',
            table: 'genesis',
          },
        })
        .then(res => {
          console.log(res)
          this.data = res.data.data
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
</style>
