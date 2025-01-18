<template>
  <div class="new-quiz-container">
    <h1>Participer au Quiz</h1>
    <form @submit.prevent="launchNewQuiz">
      <h2>Entrez votre nom :</h2>
      <input type="text" v-model="username" class="form-control shadow" placeholder="Nom du joueur" required />
      <div>
        <div class="button-container">
          <button type="submit" class="button shadow" @click="launchNewQuiz">Démarrer le Quiz</button>
        </div>
      </div>
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
    text-align: center;
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  form {
    display: flex;
    flex-direction: column;
    
  }

  input {
    font-family: 'Clash Display', sans-serif;
    text-align: center;
    margin-top: 20px;
    padding: 10px;
    border-radius: 4px;
    border: none;
    width: 50vw;
    font-size: 2vw;
    background-color: #333;
  }

  input:focus {
    outline: none;

  }

  input:focus::placeholder {
    opacity: 0;
}

  button {
    border: none;
    font-family: 'Clash Display', sans-serif;
    padding: 6px 24px;

  }
</style>
