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
        Total: {{sumaArray}}
      </div>


      <button v-if="showComprabutton"  @click="compra()">COMPRAR</button>

      <div v-else  >
        <span>Tu pedido fue un éxito</span>
        <span>¡Gracias por colaborar con el ambiente!</span>
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

</style>
