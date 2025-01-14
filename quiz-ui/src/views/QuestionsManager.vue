<template>
    <div class="questions-manager">
      <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
      <QuestionDisplay
        v-if="currentQuestion"
        :currentQuestion="currentQuestion"
        @answer-clicked="answerClickedHandler"
      />
  
      <div v-else>
        <p>Chargement des questions...</p>
      </div>
    </div>
  </template>
  

  <script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import QuestionDisplay from '@/components/QuestionDisplay.vue';

// Variables réactives
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const questions = ref([]);

// Fonction appelée à l'initialisation
onMounted(async () => {
  const quizInfo = await quizApiService.getAllQuestions();
  questions.value = quizInfo.data;
  totalNumberOfQuestions.value = quizInfo.data.length;
  console.log('Questions loaded:', questions.value);
  await loadQuestionByPosition(currentQuestionPosition.value);
});

// Fonction pour charger une question par position
async function loadQuestionByPosition(position) {
  const questionData = await quizApiService.getQuestion(position);
  currentQuestion.value = questionData.data;
}

// Gestionnaire pour les réponses sélectionnées
function answerClickedHandler(selectedAnswerIndex) {
  console.log(`Réponse sélectionnée : ${selectedAnswerIndex}`);
  
  // Charger la question suivante ou terminer le quiz
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

// Fonction pour terminer le quiz
function endQuiz() {
  console.log('Quiz terminé !');
  // Ajoutez la logique pour afficher les résultats ou rediriger
}
</script>


<style>
.questions-manager {
  text-align: center;
  padding: 20px;
}
</style>
