<template>
    <div class="about-page">
        <h1>A propos</h1>
        <h2>Le projet</h2>
        <p>Une application web de quiz simple implémentant un système de score et de classement des joueurs</p>
        <h2>Les technologies utilisées</h2>
        <div>
            <span>Frontend</span>
            <span>: Vue 3, Vite, Axios</span>
        </div>
        <div>
            <span>Backend</span>
            <span>: Python, Flask, SQLite</span>
        </div>
        <div>
            <span>Déploiement</span>
            <span>: Docker, Nginx</span>
        </div>
        <div class="button-container">
            <a href="https://github.com/MonKeySVG/quiz-app" class="button shadow">Github</a>
        </div>
    </div>

</template>

<script>


</script>

<style scoped>
    .about-page {
        text-align: center;
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }

    .button-container {
        margin-top: 50px;
    }

    div > span:first-child {
        font-weight: bold;
    }

    p, span {
        font-size: 1.2rem;
    }

    p {
        width: 50%;
    }
</style>