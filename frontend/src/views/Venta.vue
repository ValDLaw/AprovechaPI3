<template>
  <div>
    <div class="cart">
      <h3>Carrito de compras</h3>
      <ul>
        <li v-for="item in this.cart" :key="item.id">
          <span> {{ item.name }} - {{ item.new_price }}</span>
        </li>
      </ul>
      <div class="cart-total">
        Total: 5 
      </div>

      <button @click="compra()">COMPRAR</button>
      <p v-if="orderPlaced">¡Compra realizada con éxito!</p>
      <router-link v-if="orderPlaced" to="/">
        <button >Volver a Comprar</button>
      </router-link>
    
    </div>
  </div>
</template>


<script>
import { mapGetters } from 'vuex';

export default {
  data(){
    return {
      cart : null,
      total : 0,
      searchQuery: "",
      selectedCategory: "",
      selectedProduct: null,
      showPlaceOrderButton: true,
      orderPlaced: false
    }
  },
  computed : {
    ...mapGetters(['getCart']),
  },
  methods : {
    compra(){
      console.log("Hola")
      this.orderPlaced = true
    }
  },
  mounted() {
    this.cart = this.getCart
    console.log(this.cart);
  }
}
</script>

<style >

</style>
