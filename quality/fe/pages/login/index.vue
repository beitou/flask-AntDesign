<template>
  <el-form :model="user" :rules="loginRule" class="form-login">
    <h3 class="title">
      小帮质量平台
    </h3>
    <el-form-item prop="username">
      <el-input v-model="user.username" placeholder="账号" clearable></el-input>
    </el-form-item>

    <el-form-item prop="password">
      <el-input
        v-model="user.password"
        @keyup.enter.native="loginSubmit"
        placeholder="密码"
        clearable
        show-password
      ></el-input>
    </el-form-item>

    <el-form-item style="width: 100%">
      <el-button
        @click.native.prevent="loginSubmit"
        :disabled="disabled"
        :loading="logining"
        style="width: 100%"
        size="medium"
        type="success"
      >
        立即登录
      </el-button>
    </el-form-item>
    <el-form-item style="width: 100%">
      <el-button
        @click.native.prevent="loginAdminUser(true)"
        :loading="loginingWx"
        style="width: 100%"
        size="medium"
      >
        企业微信授权
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  layout: 'login',
  name: 'Login',
  data() {
    return {
      logining: false,
      loginingWx: false,
      user: {
        username: '',
        password: '',
      },
      loginRule: {
        username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      },
    }
  },
  computed: {
    disabled() {
      if (this.user.username && this.user.password) {
        return false
      } else {
        return true
      }
    },
  },
  mounted() {
    if (this.$route.query.check_workwx) {
      this.loginAdminUser()
    }
  },
  methods: {
    workWxAuth() {
      window.location.href =
        'https://api.xiaobangtouzi.com/admin-user/wechat/auth-auto-env?url=' +
        btoa(window.location.origin + '/login/?check_workwx=1')
    },
    loginAdminUser(redirect = false) {
      this.loginingWx = true
      this.$axios
        .get('/login_workwx/')
        .then(res => {
          this.loginingWx = false
          if (res.data.status === 0) {
            const name = res.data.data.name
            res.data.data.name = res.data.data.display_name
            res.data.data.display_name = name
            this.$store.commit('user/signIn', res.data.data)
            this.$router.push('/')
            return
          }
          const err = new Error('未登录')
          err.response = res
          throw err
        })
        .catch(error => {
          if (redirect) {
            this.workWxAuth()
            return
          }
          this.loginingWx = false
          this.$message.error(error.response.data.msg)
          this.user.username = ''
          this.user.password = ''
        })
    },
    loginSubmit() {
      this.logining = true
      this.$axios
        .post('/login/', this.user)
        .then(res => {
          this.logining = false
          if (res.data.status === 0) {
            const name = res.data.data.name
            res.data.data.name = res.data.data.display_name
            res.data.data.display_name = name
            this.$store.commit('user/signIn', res.data.data)
            this.$router.push('/')
          } else {
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.logining = false
          this.$message.error('服务异常，请联系管理员姜成龙！')
          this.user.username = ''
          this.user.password = ''
        })
      // e.preventDefault();
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
body {
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #eee;
}

.form-login {
  max-width: 280px;
  padding: 15px;
  margin: 180px auto;
}
.form-login .title {
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}
</style>
