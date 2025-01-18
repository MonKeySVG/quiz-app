<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>

    <div class="wrapper">

      <nav>
        <RouterLink to="/" class="navlink shadow">Home</RouterLink>
        <RouterLink to="/about" class="navlink shadow">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

template {
  display: flex;
  flex-direction: column;
  align-items: center;
}

nav {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.navlink  {
  text-decoration: none;
  color: white;
  background-color: #333;
  font-size: 1.2rem;
  padding: 6px 24px;
  border-radius: 4px;

  
}



</style>
