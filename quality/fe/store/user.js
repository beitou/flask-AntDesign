export const namespaced = true

export const state = () => ({
  current: {},
})

export const getters = {
  currentUser: ({ current }) => current,
  signedIn: ({ current }) => !!current.name,
}

export const mutations = {
  signIn(state, user) {
    state.current = user
  },
  signOut(state) {
    state.current = {}
    document.cookie = ''
  },
}
