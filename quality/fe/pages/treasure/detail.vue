<template>
  <a-form :form="form">
    <a-row type="flex" justify="center" align="middle">
      <a-col :span="12">
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="包        名"
          >
            {{ data.name }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="平        台"
          >
            {{ data.platform }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="版  本  号"
          >
            {{ data.version_name }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="使用环境"
          >
            {{ data.type }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="提  交  人"
          >
            {{ data.submitter }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="代码分支"
          >
            {{ data.branch }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="创建时间"
          >
            {{ data.created }}
          </a-form-item>
        </a-row>
        <a-row justify="space-around" align="middle">
          <a-form-item
            :label-col="{ span: 12 }"
            :wrapper-col="{ span: 12 }"
            label="Commit Hash"
          >
            {{ data.commit_id }}
          </a-form-item>
        </a-row>
      </a-col>
      <a-col :span="12">
        <a-form-item>
          <img :src="data.image" />
        </a-form-item>
      </a-col>
    </a-row>
  </a-form>
</template>

<script>
export default {
  data() {
    return {
      data: {},
      prefix: '/static/img/qrcode/',
      formLayout: 'horizontal',
      form: this.$form.createForm(this, { name: 'coordinated' }),
    }
  },
  mounted() {
    this.fetch()
  },
  methods: {
    fetch() {
      console.log(this.$route.query.id)
      this.loading = true
      this.$axios
        .get('/treasure/app/search', {
          params: { id: this.$route.query.id },
        })
        .then(res => {
          this.loading = false
          console.log('data:', res)
          this.data = res.data.data
          this.data.image = this.prefix + this.data.image
        })
    },
  },
}
</script>

<style>
img {
  margin: 0 auto;
}
</style>
