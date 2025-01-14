<template>
    <div class="score-page">
        <h1>Score Page</h1>
        <p>Your score: {{ score }}</p>
    </div>
</template>

<script>
export default {
    name: 'ScorePage',
    data() {
        return {
            score: 0 // Replace with actual score logic
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