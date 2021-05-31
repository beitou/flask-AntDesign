import uuidv4 from 'uuid-random'
import routes from '@/components/routes'

export const namespaced = true

export const state = () => {
  return {
    isCollapsed: false,
    routes: [],
    selectedKeysMap: {},
    openKeysMap: {},
    openKeys: [],
  }
}

export const getters = {}

export const mutations = {
  toggleCollapse(state) {
    state.isCollapsed = !state.isCollapsed
  },
  setRoutes(state, allowedUrls) {
    state.routes = routes
      .map(item => {
        const children =
          item.children &&
          item.children
            .filter(child => true) // allowedUrls.includes(child.path))
            .map(child => ({
              ...child,
              uuid: uuidv4(),
            }))
        return {
          ...item,
          uuid: uuidv4(),
          children,
        }
      })
      .filter(
        item =>
          true /*
          allowedUrls.includes(item.path) ||
          (item.children && item.children.length)*/
      )
    state.routes.forEach(route => {
      const uuids = [route.uuid]
      state.selectedKeysMap[route.path] = uuids
      state.openKeysMap[route.path] = []
      if (route.children && route.children.length) {
        route.children.forEach(child => {
          state.selectedKeysMap[child.path] = [child.uuid]
          state.openKeysMap[child.path] = uuids
        })
      }
    })
  },
}

export const actions = {
  async init({ commit }) {
    /*
    const res = await this.$axios.get('/user/menu')
    console.log(res.data)
    if (res.data && res.data.data && res.data.data.length) {
      commit('setRoutes', res.data.data)
    }
    */
    commit('setRoutes') // , res.data.data)
  },
}
