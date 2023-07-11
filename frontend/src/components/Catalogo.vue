<template>
  <div class="container">
    <div class="logout">
      <button
        prepend-icon="mdi-brain"
        class="black"
        variant="outlined"
        @click="logout"
      >
        Salir
      </button>
    </div>
    <div class="header">
      <img :src="require('@/assets/logo.jpeg')" alt="Logo de Aprovecha!" class="logo" />
    </div>
    <div class="nombre">
      <h2>Hola, {{this.getName}}. Bienvenida de vuelta</h2>
    </div>
    <div class="content">
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Buscar producto" />
      </div>
      <div class="product-list">
        <div v-for="product in filteredProducts" :key="product.id" class="product-item">
          <div class="product-info">
            <h3>{{ product.name }}</h3>
            <p>
              <span style="color: rgb(37, 34, 34); font-size: 16px; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;"> {{ product.category }}</span>
            </p>
            <p>
              <span style="color: rgb(37, 34, 34); font-size: 16px; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;"> Antes: {{ product.old_price }}</span>
            </p>
            <p>
              <span style="color: #3f8880; font-size: 20px; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; font-weight: bold;"> Ahora: {{ product.new_price }}</span>
            </p>
            <p>
              <span style="color: rgb(37, 34, 34); font-size: 16px; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;"> Origen: {{ product.origen }}</span>
            </p>
            <p>
              <span style="color: rgb(37, 34, 34); font-size: 18px; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;"> Fecha de vencimiento: {{ product.vencimiento }}</span>
            </p>
            <button @click="addToCart(product)">Agregar al carrito</button>
          </div>
          <div class="product-image">
            <img :src="product.image" :alt="product.name" />
          </div>
        </div>
      </div>
      <div v-if="selectedProduct" class="product-details">
        <h2>{{ selectedProduct.name }}</h2>
        <p>{{ selectedProduct.description }}</p>
        <p>{{ selectedProduct.price }}</p>
        <img :src="selectedProduct.image" :alt="selectedProduct.name" />
        <button @click="addToCart(selectedProduct)">Agregar al carrito</button>
      </div>
    </div>
    <div class="cart">
      <h3>Carrito de compras</h3>
      <ul>
        <li v-for="item in cart" :key="item.id">
          <span>{{ item.name }} - {{ item.new_price }}</span>
          <button @click="removeFromCart(item)">Eliminar</button>
        </li>
      </ul>
      <div class="cart-total">
        Total: {{ calculateTotal() }}
      </div>
      
      <div class="delivery-options">
        <h4>Opciones de entrega:</h4>
        <label for="pickup">Recoger en punto de recojo:</label>
        <input type="radio" id="pickup" value="pickup" v-model="deliveryOption" @change="updateDeliveryOption('pickup')">
        
        <label for="delivery">Delivery:</label>
        <input type="radio" id="delivery" value="delivery" v-model="deliveryOption" @change="updateDeliveryOption('delivery')">
        
        <div v-if="deliveryOption === 'pickup'" class="pickup-options">
          <label for="pickupLocation">Selecciona el punto de recojo:</label>
          <select id="pickupLocation" v-model="selectedPickupLocation">
            <option value="">Seleccionar punto de recojo</option>
            <option v-for="location in pickupLocations" :key="location">{{ location }}</option>
          </select>
        </div>
        
        <div v-else-if="deliveryOption === 'delivery'" class="delivery-address">
          <label for="address">Dirección de entrega:</label>
          <input type="text" id="address" v-model="deliveryAddress" placeholder="Ingrese su dirección">
        </div>
      </div>
    </div>
    <button @click="placeOrder" v-show="showPlaceOrderButton">Realizar pedido</button>

    <div class="order-success" v-show="orderPlaced">
      <span>Tu pedido fue un éxito</span>
      <span>¡Gracias por colaborar con el ambiente!</span>
    </div>
  </div>
</template>

<script>
import { mapGetters , mapMutations} from 'vuex';
import {mapActions} from "vuex"
import router  from "../router/index.js"
export default {
  name: "Catalogo",
  data() {
    return {
      deliveryOption: 'pickup',
      selectedPickupLocation: '',
      deliveryAddress: '',
      products: [
        { id: 1, name: "Manzana", category: "Frutas", vencimiento: "12/07", origen: "Plaza Vea", old_price: 5.0, new_price: 2.5, description: "Una deliciosa manzana", image: require('@/assets/manzanas.jpeg') },
        { id: 2, name: "Tofu", category: "Verduras", vencimiento: "12/07", origen: "Metro", old_price: 13.9, new_price: 7.9, description: "Una fresca zanahoria", image: require('@/assets/tofu.jpg') },
        { id: 3, name: "Tomates", category: "Verduras", vencimiento: "13/07", origen: "Vivanda", old_price: 4.0, new_price: 2.0, description: "Filete de pollo jugoso", image: require('@/assets/tomates.webp') },
        { id: 4, name: "Yogurt", category: "Lacteos", vencimiento: "13/07", origen: "Mercado de Surquillo", old_price: 42.90, new_price: 31.50, description: "Lentejas nutritivas", image: require('@/assets/yogurt.jpg') },
        { id: 5, name: "Plátano", category: "Frutas", vencimiento: "14/07", origen: "Metro", old_price: 3.5, new_price: 2.0, description: "Un plátano maduro", image: require('@/assets/platano.jpeg') },
        { id: 6, name: "Lechuga", category: "Verduras", vencimiento: "15/07", origen: "Wong 2 de Mayo", old_price: 2.0, new_price: 1.5, description: "Lechuga fresca y crujiente", image: require('@/assets/lechuga.jpg') },
        { id: 7, name: "Pollo", category: "Carnes", vencimiento: "16/07", origen: "Vega", old_price: 9.5, new_price: 7.5, description: "Pechuga de pollo jugosa", image: require('@/assets/pollo.jpg') },
        { id: 8, name: "Lentejas", category: "Menestras", vencimiento: "17/07", origen: "Metro", old_price: 1.8, new_price: 1.2, description: "Lentejas ricas en proteínas", image: require('@/assets/lentejas.jpg') },
        { id: 9, name: "Leche", category: "Lacteos", vencimiento: "18/07", origen: "Vivanda", old_price: 5.9, new_price: 4.5, description: "Leche fresca de vaca", image: require('@/assets/leche.webp') },
        { id: 10, name: "Uvas", category: "Frutas", vencimiento: "19/07", origen: "Tottus", old_price: 7.0, new_price: 4.0, description: "Uvas jugosas y dulces", image: require('@/assets/uvas.webp') },
        { id: 11, name: "Espinaca", category: "Verduras", vencimiento: "20/07", origen: "Plaza Vea", old_price: 2.5, new_price: 1.8, description: "Espinacas frescas y saludables", image: require('@/assets/espinaca.webp') },
        { id: 12, name: "Carne de res", category: "Carnes", vencimiento: "21/07", origen: "Metro", old_price: 15.0, new_price: 11.5, description: "Filete de carne de res tierna", image: require('@/assets/carne.jpg') },
        { id: 13, name: "Garbanzos", category: "Menestras", vencimiento: "22/07", origen: "Vega", old_price: 1.5, new_price: 1.0, description: "Garbanzos nutritivos y sabrosos", image: require('@/assets/garbanzos.jpeg') },
        { id: 14, name: "Queso", category: "Lacteos", vencimiento: "22/07", origen: "Mercado de Barranco", old_price: 8.5, new_price: 6.5, description: "Queso delicioso y cremoso", image: require('@/assets/queso.jpeg') },
        { id: 15, name: "Sandía", category: "Frutas", vencimiento: "24/07", origen: "Tottus", old_price: 6.5, new_price: 4.5, description: "Sandía jugosa y refrescante", image: require('@/assets/sandia.jpg') },
        { id: 16, name: "Espinacas", category: "Verduras", vencimiento: "25/07", origen: "Mercado de Surquillo", old_price: 3.0, new_price: 2.2, description: "Espinacas frescas y llenas de nutrientes", image: require('@/assets/espinacas.jpg') },
        { id: 17, name: "Pavo", category: "Carnes", vencimiento: "26/07", origen: "Tottus", old_price: 11.0, new_price: 8.5, description: "Pechuga de pavo magra y saludable", image: require('@/assets/pavo.jpg') },
        { id: 18, name: "Frijoles", category: "Menestras", vencimiento: "27/07", origen: "Wong Ovalo Gutierrez", old_price: 1.2, new_price: 0.8, description: "Frijoles sabrosos y nutritivos", image: require('@/assets/frijoles.jpg') },
        { id: 19, name: "Mango", category: "Frutas", vencimiento: "29/07", origen: "Mercado de Barrano", old_price: 4.5, new_price: 3.0, description: "Mango dulce y jugoso", image: require('@/assets/mango.jpg') },
        { id: 20, name: "Brócoli", category: "Verduras", vencimiento: "30/07", origen: "Vega", old_price: 2.8, new_price: 2.0, description: "Brócoli fresco y lleno de vitaminas", image: require('@/assets/brocoli.jpg') },
        { id: 21, name: "Cerdo", category: "Carnes", vencimiento: "01/08", origen: "Mercado de Surquillo", old_price: 9.0, new_price: 6.5, description: "Chuletas de cerdo tiernas y jugosas", image: require('@/assets/cerdo.webp') },
        { id: 22, name: "Guisantes", category: "Menestras", vencimiento: "02/08", origen: "Tottus", old_price: 1.3, new_price: 0.9, description: "Guisantes verdes y tiernos", image: require('@/assets/guisantes.webp') },
        { id: 23, name: "Piña", category: "Frutas", vencimiento: "03/08", origen: "Mercado de Barranco", old_price: 5.5, new_price: 3.5, description: "Piña jugosa y tropical", image: require('@/assets/piña.jpg') },
        { id: 24, name: "Calabacín", category: "Verduras", vencimiento: "04/08", origen: "Tottus", old_price: 2.3, new_price: 1.7, description: "Calabacín fresco y versátil", image: require('@/assets/calabacin.jpg') },
        { id: 25, name: "Cordero", category: "Carnes", vencimiento: "10/08", origen: "Vega", old_price: 12.5, new_price: 10.0, description: "Cordero tierno y sabroso", image: require('@/assets/cordero.jpg') },
        { id: 26, name: "Lentejas rojas", category: "Menestras", vencimiento: "12/08", origen: "Metro", old_price: 1.4, new_price: 1.0, description: "Lentejas rojas suaves y fáciles de cocinar", image: require('@/assets/lentejas-rojas.jpg') },
        { id: 27, name: "Naranja", category: "Frutas", vencimiento: "14/08", origen: "Wong 2 de Mayo", old_price: 3.0, new_price: 2.0, description: "Naranja jugosa y llena de vitamina C", image: require('@/assets/naranja.jpg') },
        { id: 28, name: "Pepino", category: "Verduras", vencimiento: "15/08", origen: "Metro", old_price: 1.8, new_price: 1.3, description: "Pepino refrescante y crujiente", image: require('@/assets/pepino.jpeg') },
        { id: 29, name: "Cerdo ahumado", category: "Carnes", vencimiento: "16/09", origen: "Wong 2 de Mayo", old_price: 10.5, new_price: 8.0, description: "Cerdo ahumado lleno de sabor", image: require('@/assets/cerdo-ahumado.webp') },
        { id: 30, name: "Frijoles negros", category: "Menestras", vencimiento: "17/08", origen: "Mercado de Surquillo", old_price: 1.5, new_price: 1.0, description: "Frijoles negros cremosos y deliciosos", image: require('@/assets/frijoles-negros.jpg') }
      ],
      categories: ["Frutas", "Verduras", "Carnes", "Menestras", "Lacteos"],
      pickupLocations: ["Universidad de Ingenieria y Teconologia", "Universidad de Ciencias Aplicadas - San Isidro", "Parque Kennedy", "Universidad de Lima", "Universidad del Pacifico"],
      searchQuery: "",
      selectedCategory: "",
      selectedProduct: null,
      cart: [],
      showPlaceOrderButton: true,
      orderPlaced: false
    };
  },

  computed: {
    ...mapGetters(['getName']),
    filteredProducts() {
      let filtered = this.products;
      if (this.searchQuery) {
        filtered = filtered.filter(product => product.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
      }
      if (this.selectedCategory) {
        filtered = filtered.filter(product => product.category === this.selectedCategory);
      }
      return filtered;
    }
  }
  ,
  methods: {
    ...mapMutations(['setCart']),
    ...mapActions(['logout']),
    addToCart(product) {
      this.cart.push(product);
    },
    updateDeliveryOption(option) {
      this.deliveryOption = option;
    },
    removeFromCart(item) {
      const index = this.cart.indexOf(item);
      if (index !== -1) {
        this.cart.splice(index, 1);
      }
    },
    calculateTotal() {
      return this.cart.reduce((total, item) => total + item.new_price, 0);
    },
    placeOrder() {
      console.log(this.cart)
      this.setCart(this.cart)
      // Lógica para realizar el pedido

      router.push("/venta", { name: 'cart', params: { cart: this.cart } })
      // Después de realizar el pedido, establecer orderPlaced en true y ocultar el 
    }
  }
};
</script>

<style>
.container {
    height: auto;
    width: max-content;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 8px;
}



.header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  height: max-content;
}

.logo {
  width: 400px;
  height: auto;
  justify-content: center;
  object-fit: cover;
}

.content {
  display: flex;
  flex-direction: column;
  width: 100%;

}

.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.search-bar input {
  width: 300px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  background-color: #f8f8f8;
  transition: box-shadow 0.3s ease-in-out;
  animation: fadeIn 1s;
}

.search-bar input:focus {
  outline: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}


.product-list {
  display: flex;
  margin-top: 70px;
  flex-wrap: wrap;
  justify-content: space-between;
}

.product-item {
  width: calc(16% - 20px);
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #fef6cd;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.product-item .product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.product-item h3 {
  margin-bottom: 5px;
}

.product-item p {
  margin-bottom: 10px;
}

.product-item .product-image img {
  width: 100px;
  height: 100px;
  object-fit: cover;
}

.product-item button {
  padding: 10px 20px;
  background-color: #20c67a;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.product-item button:hover {
  background-color: #3f8880;
}

.product-details {
  flex: 1;
}

.cart {
  padding: 20px;
  background-color: #9dc09d;
  margin-top: 40px;
  width: 300px;
  display: flex;
  flex-direction: column;
  justify-items: center;
  justify-content: center;
  text-align: center;
}

.cart h3 {
  margin-bottom: 10px;
  text-align: center;
}

.cart ul {
  list-style: none;
  background-color: white;
  text-align: center;
  justify-content: center;
  padding: 0;
}

.cart li {
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: center;
  margin-bottom: 5px;
}

.cart li button {
  padding: 5px 10px;
  background-color: #ff0000;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cart li button:hover {
  background-color: #ff3333;
}

.cart-total {
  margin-top: 20px;
  font-weight: bold;
  text-align: right;
}

.delivery-options {
  margin-top: 20px;
}

.delivery-options h4 {
  margin-bottom: 10px;
}

.delivery-options label {
  display:flex;
  margin-bottom: 5px;
}

.delivery-options input[type="radio"] {
  margin-right: 5px;
}

.pickup-options label,
.delivery-address label {
  display: block;
  margin-bottom: 5px;
}

.pickup-options select,
.delivery-address input[type="text"] {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

button {
  padding: 10px 20px;
  background-color: #20c67a;
  color: #fff;
  border: none;
  justify-content: center;
  text-align: center;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #3f8880;
}

.order-success {
  display: none;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: #00FF00;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  z-index: 9999;
  animation: slideIn 1s;
}

.order-success span {
  display: block;
  margin-bottom: 10px;
}

@keyframes slideIn {
  0% {
    transform: translateY(-50px);
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes fade-in-out {
  0% {
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
.nombre {
  text-align: center;
  margin-top: 50px;
}

.nombre h2 {
  color: black;
  font-size: 30px;
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

</style>