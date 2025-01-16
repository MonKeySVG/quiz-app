<template>
    <div class="score-page">
        <h1>Score Page</h1>
        <p>Your score: {{ score }}</p>
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
}
</style>