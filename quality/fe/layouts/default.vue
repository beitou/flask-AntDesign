<template>
  <div
    id="app"
    v-if="loginChecked"
    @mousemove="moveEvent"
    @click="moveEvent"
    class="nav-theme-light nav-layout-left flex"
  >
    <a-layout class="overflow-x-hidden overflow-y-scroll flex-grow">
      <a-layout-header style="background: #fff; padding: 0">
        <Header />
      </a-layout-header>
      <router-view></router-view>
      <a-layout-footer style="background: #fff; padding: 0">
        <Footer />
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import { linkVuexState } from 'vue-set-get'
import Header from './Header'
import Footer from './Footer'

export default {
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      timer: null,
      loginChecked: false,
    }
  },
  computed: {
    collapsed: linkVuexState('menu.isCollapsed'),
    ...mapGetters({
      user: 'user/currentUser',
      userSignedIn: 'user/signedIn',
    }),
  },
  mounted() {
    if (this.userSignedIn) {
      this.loginChecked = true
      return
    }
    this.$axios.get('/login/').then(res => {
      // eslint-disable-next-line no-debugger
      if (res.status === 200) {
        this.loginChecked = true
        this.signUserIn(res.data.data)
      } else {
        this.signUserOut()
        this.$router.push('/login/')
      }
    })
  },
  methods: {
    ...mapMutations({
      signUserIn: 'user/signIn',
      signUserOut: 'user/signOut',
      setRoutes: 'menu/setRoutes',
      toggleCollapsed: 'menu/toggleCollapse',
    }),
    moveEvent() {
      clearTimeout(this.timer)
      this.init()
    },
    init() {
      this.timer = setTimeout(() => {
        this.$router.push('/login/')
      }, 30 * 60 * 1000)
    },
    logout() {
      this.signUserOut()
      this.$axios
        .get('/logout/')
        .then(res => {
          if (res.data.code === 200) {
            this.$router.push('/login/')
          }
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
}
</script>

<style>
html,
body,
#__nuxt,
#__layout,
#app {
  @apply w-screen h-screen;
}
#app > .ant-layout {
  background: #fff;
  padding-left: 50px;
  padding-right: 50px;
}
body {
  @apply overflow-x-hidden overflow-y-scroll;
  backgroud-color: 'ffffff';
}
</style>

<style scoped lang="less">
.trigger {
  padding: 0 20px;
  line-height: 64px;
  font-size: 20px;

  &:hover {
    background: #eeeeee;
  }
}
</style>
