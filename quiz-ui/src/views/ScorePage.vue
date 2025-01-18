<template>
    <div class="score-page">
        <h1>Your score:</h1>
        <h2>{{ score }}</h2>
        <div class="button-container">
            <router-link to="/new-quiz" class="button shadow">Rejouer</router-link>
        </div>
    </div>

</template>

<script>

import participationStorageService from '@/services/ParticipationStorageService';

export default {
    name: 'ScorePage',
    data() {
        console.log(participationStorageService.getPlayerScore());
        return {
            score: participationStorageService.getPlayerScore(),
        };
    }
};
</script>

<style scoped>
    .score-page {
        text-align: center;
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .button-container {
        margin-top: 50px;
    }
</style>