<template>
    <div class="question-display">
      <h2>{{ currentQuestion.text }}</h2>

      <div class="question-container">
        <div class="img-container">
            <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question image" class="question-image shadow"/>
        </div>
  
        <div class="answers">
            <button
            v-for="(answer, index) in currentQuestion.possibleAnswers"
            :key="index"
            @click="emit('answer-clicked', index)"
            class="button shadow answer-button"
            >
            {{ answer.text }}
            </button>
        </div>
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

  h3 {
    margin-top: 50px;
  }

    .question-container {
        display: flex;
        justify-content: center;
        gap: 50px;
        align-items: center;
        margin-top: 50px;
    }

    .question-display {
        
    }
    
    .img-container {

    }

    .answers {

        display: grid;
        grid-template-columns: repeat(2, 200px);
        gap: 20px;
    }
    
    button {
        cursor: pointer;
    }

    .answer-button {
        padding: 25px 50px;
    }

    .question-image {
        max-width: 300px;
        border-radius: 4px;
    }
  </style>
  