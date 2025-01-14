<template>
    <div class="question-display">
      <h2>{{ currentQuestion.text }}</h2>
      <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question image" class="question-image"/>
  
      <div class="answers">
        <button
          v-for="(answer, index) in currentQuestion.possibleAnswers"
          :key="index"
          @click="emit('answer-clicked', index)"
          class="btn btn-secondary"
        >
          {{ answer.text }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  
  // Props pour recevoir la question courante
  const props = defineProps({
    currentQuestion: {
      type: Object,
      required: true,
    }
  });

  
  
  // Déclaration des événements émis
  const emit = defineEmits(['answer-clicked']);
  </script>
  
  <style>
  .question-display {
    text-align: center;
    margin: 20px auto;
  }
  
  .answers {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
  }
  
  button {
    cursor: pointer;
  }

  .question-image {
    max-width: 300px;
    margin-top: 20px;
    border-radius: 4px;
  }
  </style>
  