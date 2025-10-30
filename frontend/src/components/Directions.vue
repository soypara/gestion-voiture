<template>
  <div class="page-container">
    <!-- User info en haut -->
    <div class="user-info">
      <div class="user-circle">{{ userInitial }}</div>
      <span class="user-name">{{ userName }}</span>
    </div>

    <h1>Directions</h1>
    <p>Ici, vous pourrez visualiser les directions de la société.</p>

    <!-- Tableau des directions -->
    <div class="directions-table">
      <button
        v-for="(direction, index) in directions"
        :key="index"
        class="direction-btn"
        @click="goToCrud(direction)"
      >
        <div class="abbr">{{ direction.abbr }}</div>
        <div class="fullname">{{ direction.name }}</div>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "DirectionsMndpt",
  data() {
    return {
      userName: "", // sera rempli depuis le token
      directions: [], // directions à afficher
    };
  },
  computed: {
    userInitial() {
      return this.userName ? this.userName[0].toUpperCase() : "?";
    },
  },
  mounted() {
    this.getUserName();
    this.loadDirections();
  },
  methods: {
    getUserName() {
      const token = localStorage.getItem("access");
      if (token) {
        try {
          const decoded = JSON.parse(atob(token.split(".")[1]));
          this.userName = decoded.name || "User";
        } catch (e) {
          this.userName = "User";
        }
      }
    },
    loadDirections() {
      // Exemple temporaire : tableau vide pour l'instant
      this.directions = [
        // Exemple à remplir par l'admin plus tard
        // { abbr: "HR", name: "Human Resources" },
      ];
    },
    goToCrud(direction) {
      // Navigation vers le CRUD de la direction
      console.log("Aller au CRUD pour", direction);
      // this.$router.push(`/directions/${direction.id}`);
    },
  },
};
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #42b983, #2c3e50, #3aa17e);
  background-size: 300% 300%;
  animation: moveGradient 8s ease infinite;
  color: white;
}

@keyframes moveGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.user-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ff6b6b; /* couleur random temporaire */
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.user-name {
  font-weight: bold;
  font-size: 1.2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.directions-table {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.direction-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  padding: 1rem 2rem;
  text-align: left;
  cursor: pointer;
  border-radius: 10px;
  transition: 0.3s;
  color: white;
}

.direction-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.abbr {
  font-weight: bold;
  text-decoration: underline;
  font-size: 1.2rem;
}

.fullname {
  font-size: 1rem;
}
</style>
