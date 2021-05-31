<template>
  <div class="user-wrapper">
    <div class="content-box">
      <a-dropdown>
        <span class="action ant-dropdown-link user-dropdown-menu">
          <!-- <a-avatar class="avatar" size="small" :src="avatar" /> -->
          <span>{{ user.name }}</span>
        </span>
        <a-menu slot="overlay" class="user-dropdown-menu-wrapper">
          <a-menu-item key="2" disabled>
            <a-icon
              type="setting"
              style="margin-right: 0; vertical-align: middle"
            />
            <span>不可修改</span>
          </a-menu-item>
          <a-menu-divider />
          <a-menu-item key="3">
            <a @click="handleLogout" href="javascript:;">
              <a-icon type="logout" style="vertical-align: middle" />
              <span>退出登录</span>
            </a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'UserMenu',
  computed: {
    ...mapGetters({ user: 'user/currentUser' }),
  },
  methods: {
    ...mapActions({ userSignOut: 'user/signOut' }),
    handleLogout() {
      this.$confirm({
        title: '提示',
        content: '真的要注销登录吗 ?',
        onOk: () => {
          this.userSignOut({})
          this.$router.push('/login')
        },
        onCancel() {},
      })
    },
  },
}
</script>
