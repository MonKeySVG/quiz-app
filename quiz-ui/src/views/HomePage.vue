<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
    const response = await quizApiService.getQuizInfo();
    if (response) {
        registeredScores.value = response.data;
    }
    console.log("Home page mounted");
});
</script>

<template>
  <div>
    <h1>Home page</h1>

    <!-- Affichage des scores -->
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>

    <!-- Lien pour démarrer un nouveau quiz -->
    <router-link to="/new-quiz">Démarrer le quiz !</router-link>
  </div>
</template>

<style>
h1 {
    color: #333;
    font-size: 2rem;
    margin-bottom: 1rem;
}

div {
    margin: 5px 0;
}

router-link {
    display: block;
    margin-top: 1rem;
    color: #007BFF;
    text-decoration: none;
}

router-link:hover {
    text-decoration: underline;
}
</style>