import axios from "axios";
import QuizapiService from "./QuizApiService";

const instance = axios.create({
	baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
    clear() {
      window.localStorage.clear();
    },
    savePlayerName(playerName) {
      window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {
      return window.localStorage.getItem("playerName");
    },
    saveParticipationScore(player_name, score) {
        const data = {
            playerName: player_name,
            score: score
        };
        return QuizapiService.call('post', 'participations', data);
    },
    getParticipationScores() {
      return QuizapiService.call('get', 'participations');
    },

    savePlayerScore(score) {
      window.localStorage.setItem("Score", score);
    },
    getPlayerScore() {
      return window.localStorage.getItem("Score");
    },
  };
  