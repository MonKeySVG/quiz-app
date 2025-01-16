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
import participationStorageService from '@/services/ParticipationStorageService';
import { useRouter } from 'vue-router';

const router = useRouter();

// Variables réactives
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const questions = ref([]);
let score = 0;

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

    // Vérifier si la réponse est correcte et mettre à jour le score
    if (isAnswerCorrect(selectedAnswerIndex)) {
        score++;
        console.log('Score mis à jour :', score);
    }
  
  // Charger la question suivante ou terminer le quiz
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

function isAnswerCorrect(selectedAnswerIndex) {
    // const currentQuestion = this.questions[this.currentQuestionPosition];
    console.log('Current question:', currentQuestion);
    console.log('Current question value:', currentQuestion.value.possibleAnswers[selectedAnswerIndex].isCorrect);
    if (currentQuestion.value.possibleAnswers[selectedAnswerIndex].isCorrect) {
        return true;
    } else {
        return false;
    }
}

// Fonction pour terminer le quiz
function endQuiz() {
  console.log('Quiz terminé !');
  // push le score et le nom du joueur dans la base de données
  const playerName = participationStorageService.getPlayerName();
  participationStorageService.saveParticipationScore(playerName, score);
  participationStorageService.savePlayerScore(score);
  console.log('Nom du joueur:', playerName);
  router.push('/score');
}
</script>


<style>
.questions-manager {
  text-align: center;
  padding: 20px;
}
</style>
