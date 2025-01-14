<template>
  <div class="new-quiz-container">
    <h1>Participer au Quiz</h1>
    <form @submit.prevent="launchNewQuiz">
      <p>Entrez votre nom :</p>
      <input type="text" v-model="username" class="form-control" placeholder="Nom du joueur" required />
      <button type="submit" class="btn btn-primary mt-3" @click="launchNewQuiz">Démarrer le Quiz</button>
    </form>


  </div>
</template>

<script setup>
import { ref } from 'vue';
import participationStorageService from '@/services/ParticipationStorageService';
import { useRouter } from 'vue-router';

const router = useRouter();

// Variable pour stocker le nom du joueur
const username = ref('');

// Fonction appelée lors du clic sur le bouton
function launchNewQuiz() {
  console.log("Launch new quiz with", username.value);
  participationStorageService.savePlayerName(username.value);
  router.push('/questions'); // Redirection vers la page des questions
}
</script>

<style>
.new-quiz-container {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
  padding: 2rem;
}
</style>
