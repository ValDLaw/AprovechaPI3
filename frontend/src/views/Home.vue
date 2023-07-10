<template>
    <v-app>
      <v-main app>
        <v-container>
          <Catalogo/>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script > 
  import Catalogo from "../components/Catalogo.vue"
  
  import {mapActions} from "vuex"
  export default{
    name: "Home",
    methods: {
        ...mapActions(['logout']),
      },
    components:{
      Catalogo
    }
  }
  </script>
  
  