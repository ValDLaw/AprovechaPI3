import { createStore } from 'vuex'

const state = {
  user: null,
  error: null,
  nombre : null,
  isAuthenticated: false
};

const getters = {
  userExists(state){
    return state.user !== null
  },
  getUser(state){
    return state.user
  },
  isAuthenticatedExists(state) {
    return state.isAuthenticated;
  },
  getName(state){
    return state.nombre 
  }
};

const actions = {
  async login({commit}, user){
    console.log(user)
    fetch("http://127.0.0.1:5000/users/login", {
    method: "POST",
    body: JSON.stringify({
      body : {
        correo: user.email,
        password: user.password,
      }
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((resJson) => {
      if (resJson["success"]) {
        commit("setAuthenticated" , true)
        commit("setUser" , resJson["id"])
        let name = resJson["nombres"] + " " + resJson["apellidos"] 
        console.log("USUARIO " , name)
        commit("setName", name)
        console.log(this.state.user)
        router.push("/");
      }
    })
  },
  logout({commit}){
    console.log("LOGOUT")
    console.log(this.state.user)
    commit("setAuthenticated" , false)
    commit("setUser" , null)
    console.log(this.state.user)
    router.push("users/login")
  },
};

const mutations = {
  setUser(state, payload){
    state.user = payload
  },
  setError(state, payload){
    state.error = payload
  },
  setAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  },
  setName(state, payload){
    state.nombre = payload
  }
};

export default {
  state,
  getters,
  actions,
  mutations,
};