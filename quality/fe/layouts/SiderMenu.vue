<template>
  <div class="flex-grow min-h-0">
    <a-menu
      :selected-keys="selectedKeys"
      :open-keys.sync="openKeys"
      mode="horizontal"
      theme="light"
    >
      <template v-for="item in routes">
        <a-menu-item
          v-if="!item.children"
          :key="item.uuid"
          @click="() => $router.push({ path: item.path })"
        >
          <a-icon type="setting" style="horizontal-align: middle" />
          <span>{{ item.title }}</span>
        </a-menu-item>
        <sub-menu v-else :key="item.uuid" :menu-info="item" />
      </template>
    </a-menu>
  </div>
</template>

<script>
/*
 * recommend SubMenu.vue https://github.com/vueComponent/ant-design-vue/blob/master/components/menu/demo/SubMenu.vue
 * SubMenu1.vue https://github.com/vueComponent/ant-design-vue/blob/master/components/menu/demo/SubMenu1.vue
 * */
import { mapActions } from 'vuex'
import { linkVuexState } from 'vue-set-get'
import SubMenu from './SubMenu'
export default {
  components: {
    'sub-menu': SubMenu,
  },
  data() {
    this.cacheOpenKeys = []
    return {
      selectedKeys: [],
    }
  },
  computed: {
    collapsed: linkVuexState('menu.isCollapsed'),
    routes: linkVuexState('menu.routes'),
    selectedKeysMap: linkVuexState('menu.selectedKeysMap'),
    openKeysMap: linkVuexState('menu.openKeysMap'),
    openKeys: linkVuexState('menu.openKeys'),
  },
  watch: {
    '$route.path': function(val) {
      this.selectedKeys = this.selectedKeysMap[val]
      const openKeys = this.collapsed ? this.cacheOpenKeys : this.openKeys
      const openKeysMap = this.openKeysMap[val]
      if (!openKeysMap || !openKeysMap.length) {
        return
      }
      openKeysMap.forEach(key => {
        if (!openKeys.includes(key)) {
          openKeys.push(key)
        }
      })
      this[this.collapsed ? 'cachedOpenKeys' : 'openKeys'] = openKeys
    },
    collapsed(val) {
      if (val) {
        this.cacheOpenKeys = this.openKeys
        this.openKeys = []
      } else {
        this.openKeys = this.cacheOpenKeys
      }
    },
  },
  mounted() {
    this.initMenu().then(() => {
      this.selectedKeys = this.selectedKeysMap[this.$route.path]
      this.openKeys = this.collapsed ? [] : this.openKeysMap[this.$route.path]
    })
  },
  methods: {
    ...mapActions({
      initMenu: 'menu/init',
    }),
  },
}
</script>
