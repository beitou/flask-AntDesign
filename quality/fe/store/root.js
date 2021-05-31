import { SET_STATE } from 'vue-set-get'

import * as menu from './menu'
import * as user from './user'

export default {
  modules: {
    menu,
    user,
  },

  state: () => ({
    name: '',
    isCollapse: false,
  }),

  getters: {},

  mutations: {
    SET_STATE,
  },
}
