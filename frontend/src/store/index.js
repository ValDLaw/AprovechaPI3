import { createStore } from 'vuex'
import router from "../router/index"


const store = createStore({
  state : {
    user: null,
    error: null,
    nombre : null,
    isAuthenticated: false,
    cart: null
  },
  getters : {
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
    },
    getCart(state){
      return state.cart 
    }
  },
  mutations : {
    setUser(state, payload){
      state.user = payload
    },
    setError(state, payload){
      state.error = payload
    },
    
    setCart(state, payload){
      state.cart = payload
    },
    setAuthenticated(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    setName(state, payload){
      state.nombre = payload
    }
  },
  actions : {
    async login({commit}, user){
      console.log("user", user)
      fetch("http://127.0.0.1:5000/users/login", {
      method: "POST",
      body: JSON.stringify({
        email: user.email,
        password: user.password,

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
      }).catch((e) => {
        console.log("error , " , e)
      })
    },
    logout({commit}){
      console.log("LOGOUT")
      console.log(this.state.user)
      commit("setAuthenticated" , false)
      commit("setUser" , null)
      console.log(this.state.user)
      commit("setCart", null)
      router.push("/login")
    },
  }

  
})



export default store