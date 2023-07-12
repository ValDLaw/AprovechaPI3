<template>
    <div class="container">
      <h1>Acceso usuario</h1>
      <form @submit.prevent="login({ email, password})">
        <p>Correo</p>
        <input
          type="email"
          placeholder="Ingresa email"
          v-model="email"
        >
  
        <p>Contraseña</p>
        <input 
          type="password"
          placeholder="Ingresa Contraseña"
          v-model="password"
        >
  
  
        <div class="submit-button">
          <button type="submit">Login</button>
        </div>
      </form>
      <br/> <br/>
  
      <div>
          <div class>¿No tienes una cuenta de Aprovecha?</div>
          <div class>
            <router-link to="/register">Regístrate</router-link>
          </div>
        </div>
  
    </div>
  </template>
  
  
  <script >
  import {mapActions} from "vuex"
  
  export default{
    name: "Access",
    data(){
      return{
        email: "",
        password : ""
      }
    },
    methods: {
      ...mapActions(['login']),
    }
  
  }
  
  
  </script>
  
  <style>
  .container {
    max-width: 400px;
    height:auto;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
  }
  
  form {
    max-width: 300px;
    margin: 0 auto;
  }
  
  p {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 20px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  .submit-button {
    display: flex;
    justify-content: center;
  }
  
  button {
    background-color: #5493b4;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #2a86b7;
  }
  
  .d-flex {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  .d-flex > div {
    margin-right: 10px;
  }
  
  a {
    color: #4caf50;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  </style>