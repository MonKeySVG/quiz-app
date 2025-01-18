<script setup>
import { ref, onMounted, computed } from 'vue';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

const registeredScores = ref([]);

const sortedScores = computed(() => {
    return [...registeredScores.value].sort((a, b) => b.score - a.score);
});

const top7Scores = computed(() => {
    return sortedScores.value.slice(0, 7);
});

onMounted(async () => {
    const response = await participationStorageService.getParticipationScores();
    if (response) {
        registeredScores.value = response.data;
    }
    console.log("Home page mounted");
});
</script>

<template>
  <div class="home-page-container">
    <h1>PokeQuizz AI</h1>

    <!-- Affichage des scores -->
     <div class="scores-container">
      <h2>Classement</h2>

      <div v-for="scoreEntry in top7Scores" v-bind:key="scoreEntry.date" class="score-entry">
        <div class="player-name">{{ scoreEntry.playerName }}</div>
        <div class="separator"></div>
        <div class="score-value">{{ scoreEntry.score }}</div>
      </div>
    </div>
   

    <!-- Lien pour démarrer un nouveau quiz -->
    <router-link to="/new-quiz" class="button shadow">Démarrer le quiz !</router-link>
  </div>
</template>

<style>

.home-page-container {
    text-align: center;
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

h1 {
    color: #333;
    font-size: 7vw;

}

h2 {
  font-size: 3vw;
  color: #E46B2D;
  margin-bottom: 20px;
}

.scores-container {
  width: 80%;
}

.score-entry {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 2vw;
    
}

.player-name {
    font-weight: bold;
    flex: 2;
    text-align: left;
}

.score-value {
    flex: 1;
    text-align: right;
    
}

.separator {

    height: 1px;

    border-bottom: 2px dotted #333;
    flex: 7;
}

.button {
  text-decoration: none;
  color: white;
  background-color: #333;
  font-size: 1.2rem;
  padding: 6px 24px;
  border-radius: 4px;
  margin-top: 40px;
}

</style>