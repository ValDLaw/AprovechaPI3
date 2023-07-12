<template>
  <div>
    <div class="cart">
      <div class="carrito_content">
      <h3>Carrito de compras</h3>
      <ul>
        <li v-for="item in this.cart" :key="item.id">
          <span> {{ item.name }} - {{ item.new_price }}</span>
        </li>
      </ul>
        <li>Delivery :  3.5</li>
      <div class="cart-total">
        Total: {{sumaArray + 3.5}}
      </div>
    </div>

    <div >
      <button v-if="showComprabutton"  @click="compra()">COMPRAR</button>

      <div v-else    >
        <span>Tu pedido fue un éxito</span>
        <span>¡Gracias por colaborar con el ambiente!</span>
      </div>
    </div>
      <router-link v-if="orderPlaced" to="/">
        <button >Volver a Comprar</button>
      </router-link>
    

    </div>
  </div>
</template>


<script>
import { mapGetters } from 'vuex';
import {mapActions} from "vuex"

export default {
  data(){
    return {
      cart : null,
      total : 0,
      searchQuery: "",
      selectedCategory: "",
      selectedProduct: null,
      showComprabutton: true,
      orderPlaced: false
    }
  },
  computed : {
    ...mapGetters(['getCart']),
    sumaArray() {
      if (this.cart && this.cart.length > 0) {
        return this.cart.reduce((total, item) => total + item.new_price, 0);
      } else {
        return 0;
      }
    }
  },
  methods : {
    compra(){

      setTimeout(() => {
        this.orderPlaced = true;
        this.showComprabutton = false;
    }, 5000); 
    }
  },
  mounted() {
    this.cart = this.getCart
    console.log(this.cart);

  }
}
</script>

<style >

/* Estilos generales */
body {
  font-family: 'Roboto';
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
  display: flex;
  font-size: large;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  padding: 20px;
}


h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* Estilos específicos para el carrito de compras */
.carrito_content {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.carrito_content li {
  margin-bottom: 10px;
}

.carrito_content span {
  font-weight: bold;
}

.cart-total {
  margin-top: 20px;
  text-align: right;
  font-weight: bold;
}

/* Estilos para la tienda de comida */
.food-item {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.food-item img {
  width: 100%;
  border-radius: 10px;
}

.food-item h4 {
  font-size: 20px;
  color: #333;
  margin-top: 10px;
}

.food-item p {
  color: #777;
}

.food-item .price {
  font-size: 18px;
  color: #333;
  margin-top: 10px;
}

.food-item button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
}

.food-item button:hover {
  background-color: #0056b3;
}

/* Estilos para el carrito de compras en la tienda de comida */
.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  margin-bottom: 10px;
}

.cart-item img {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  margin-right: 10px;
}

.cart-item span {
  font-weight: bold;
}

.cart-item button {
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
}

.cart-item button:hover {
  background-color: #c82333;
}


</style>
