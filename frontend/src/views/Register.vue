<template>
    <div class="container">
      <h1 class="animate__animated fadeInDown">¡Bienvenid@ a Aprovecha!</h1>
  
      <div>
        <div class="form-header">
          <h1>Registrar</h1>
        </div>
        <form id="login-form" @submit.prevent="register()">
          <label>Nombre</label>
          <input
            id="first_name"
            name="first_name"
            type="text"
            required
            v-model="first_name"
          />    
          <label>Apellidos</label>
          <input
            id="last_name"
            name="last_name"
            type="text"
            required
            v-model="last_name"
          />    
          <label>Correo</label>
          <input
            id="email"
            name="email"
            type="email"
            required
            v-model="email"
          />
          <label>DNI</label>
          <input
            id="dni"
            name="dni"
            type="text"
            required
            v-model="dni"
          />
          <label>Clave</label>
          <input
            id="clave"
            name="clave"
            type="password"
            required
            v-model="password"
          />
          <label>Celular</label>
          <input
            id="celular"
            name="celular"
            type="text"
            required
            v-model="phone"
          />
          <label>Direccion</label>
          <input
            id="direccion"
            name="direccion"
            type="text"
            required
            v-model="address"
          />
  
          <label for="id_sex">Sexo </label>
                  <select id="id_sex" name="sex" required v-model="sex">
                      <option value="F">Femenino</option>
                      <option value="M">Masculino</option>
                      <option value="O">Otro</option>
                  </select>

            <label for="id_major">Institucion Esducativa </label>
            <select id="educational_institution" name="educational_institution" required v-model="educational_institution">
              <option value="UTEC">Universidad de Ingenieria y Tecnologia</option>
              <option value="PUCP">Pontificia Universidad Catolica del Peru</option>
              <option value="UNI">Universidad Nacional de Ingenieria</option>
              <option value="UNMSM">Universidad Nacional Mayor de San Marcos</option>
              <option value="UPC">Universiad de Ciencias Aplicadas</option>
              <option value="ULima">Universidad de Lima</option>
              <option value="UCV">Universidad Cesar Vallejo</option>
              <option value="USIL">Universidad San Ignacio de Loyola</option>
            </select>
          
            <input
              type="submit"
              value="Registrar"
              class="btn btn-primary btn-lg"
            />

          </form>
  
        <div class="d-flex mt-3 align-items-center">
          <div class="p-2">¿Ya tienes una cuenta de Aprovecha?</div>
          <div class="p-2">
            <router-link to="/login">Login</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
  import { mapActions } from 'vuex'
  export default {
    name: "Registro",
    data() {
      return {
        dni: "", 
        email: "", 
        password: "", 
        first_name: "", 
        last_name: "",
        phone: "",
        sex: "", 
        address: "",
        educational_institution: ""
      };
    },
    mounted() {
      this.showElements();
    },
    methods:{
      ...mapActions(['login']),
      register() {
        console.log("dni:", this.dni);
        console.log("email:", this.email);
        console.log("password:", this.password);
        console.log("first_name:", this.first_name);
        console.log("last_name:", this.last_name);
        console.log("phone:", this.phone);
        console.log("sex:", this.sex);
        console.log("address:", this.address);
        console.log("educational_institution:", this.educational_institution);

        fetch("http://127.0.0.1:5000/users/register", {
          method: "POST",
          body: JSON.stringify({
              dni: this.dni, 
              email: this.email , 
              password: this.password, 
              first_name: this.first_name, 
              last_name: this.last_name,
              phone: this.phone, 
              sex: this.sex,
              address: this.address, 
              educational_institution: this.educational_institution
          }),
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((res) => res.json())
          .then((resJson) => {
            if (resJson["id"]) {
              const temp = {
                email :this.email,
                password: this.password,
              }
              this.$store.dispatch('login', temp);
              
            } 
          }).catch(erro => console.log(erro))
      },
      showElements() {
        const elements = document.querySelectorAll('.fadeInDown, .fadeInUp');
        elements.forEach((element) => {
          element.classList.add('show');
        });
      },
    }, 
  }
  </script>
  
  <style>
 
  .container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    background-color: white;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  h2 {
    font-size: 18px;
    margin-bottom: 10px;
  }
  
  h3 {
    font-size: 16px;
    margin-bottom: 20px;
    color: #888;
  }
  
  .fadeInDown {
    opacity: 0;
    transform: translateY(-20px);
    transition: opacity 1s ease, transform 1s ease;
  }
  
  .fadeInDown.show {
    opacity: 1;
    transform: translateY(0);
  }
  
  .fadeInUp {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 1s ease, transform 1s ease;
  }
  
  .fadeInUp.show {
    opacity: 1;
    transform: translateY(0);
  }
  
  .form-header {
    background-color: #f0f0f0;
    padding: 10px;
    margin-bottom: 20px;
  }
  
  form {
    text-align: left;
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input,
  select {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  input[type="submit"] {
    background-color: #4caf50;
    color: #fff;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #8c00ff;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
  }
  
  .btn-primary:hover {
    background-color: #9500ff;
  }
  
  .d-flex {
    display: flex;
    justify-content: center;
  }
  
  .mt-3 {
    margin-top: 15px;
  }
  
  .align-items-center {
    align-items: center;
  }
  
  .p-2 {
    padding: 5px;
  }
  
  </style>