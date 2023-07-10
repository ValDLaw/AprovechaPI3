<template>
    <div>
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Buscar producto" />
      </div>
      <div class="filter-bar">
        <select v-model="selectedCategory">
          <option value="">Todas las categorías</option>
          <option v-for="category in categories" :value="category">{{ category }}</option>
        </select>
      </div>
      <div class="product-list">
        <div v-for="product in filteredProducts" :key="product.id" class="product-item">
          <h3>{{ product.name }}</h3>
          <p>{{ product.category }}</p>
          <p>{{ product.price }}</p>
          <img :src="product.image" :alt="product.name" />
          <button @click="addToCart(product)">Agregar al carrito</button>
        </div>
      </div>
      <div v-if="selectedProduct" class="product-details">
        <h2>{{ selectedProduct.name }}</h2>
        <p>{{ selectedProduct.description }}</p>
        <p>{{ selectedProduct.price }}</p>
        <img :src="selectedProduct.image" :alt="selectedProduct.name" />
        <button @click="addToCart(selectedProduct)">Agregar al carrito</button>
      </div>
      <div class="cart">
        <h3>Carrito de compras</h3>
        <ul>
          <li v-for="item in cart" :key="item.id">
            {{ item.name }} - {{ item.price }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name : 'Catalogo',
    data() {
      return {
        products: [
          { id: 1, name: "Manzana", category: "Frutas", price: 1.5, description: "Una deliciosa manzana", image: "ruta-de-la-imagen" },
          { id: 2, name: "Zanahoria", category: "Verduras", price: 0.8, description: "Una fresca zanahoria", image: "ruta-de-la-imagen" },
          { id: 3, name: "Pollo", category: "Carnes", price: 5.0, description: "Filete de pollo jugoso", image: "ruta-de-la-imagen" },
          { id: 4, name: "Lentejas", category: "Menestras", price: 2.3, description: "Lentejas nutritivas", image: "ruta-de-la-imagen" }
        ],
        categories: ["Frutas", "Verduras", "Carnes", "Menestras"],
        searchQuery: "",
        selectedCategory: "",
        selectedProduct: null,
        cart: []
      };
    },
    computed: {
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
    },
    methods: {
      addToCart(product) {
        this.cart.push(product);
      }
    }
  };
  </script>
  
  <style>
  /* Estilos CSS según tu preferencia */
  </style>
  