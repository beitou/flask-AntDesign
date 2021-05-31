import Vuex from 'vuex'
import rootStore from './root'

export default function createStore() {
  return new Vuex.Store({
    strict: true,
    ...rootStore,
  })
}
