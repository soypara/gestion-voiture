<template>
  <div class="page-container">
    <div class="user-info">
      <div class="user-circle">{{ userInitial }}</div>
      <span class="user-name">{{ userName }}</span>
    </div>

    <h1>Directions</h1>
    <button class="add-btn" @click="showModal = true">Ajouter Direction</button>

    <div class="directions-table">
      <button
        v-for="dir in sortedDirections"
        :key="dir.id"
        class="direction-btn"
        @click="goToCrud(dir)"
      >
        <div class="abr">{{ dir.abr }}</div>
        <div class="fullname">{{ dir.nom }}</div>
      </button>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>Ajouter une Direction</h2>
        <input v-model="newDirection.abr" placeholder="Abréviation" />
        <input v-model="newDirection.nom" placeholder="Nom complet" />
        <div class="modal-actions">
          <button class="btn-blue" @click="addDirection">Ajouter</button>
          <button class="btn-red" @click="showModal = false">Annuler</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DirectionsMndpt",
  data() {
    return {
      userName: "",
      directions: [],
      showModal: false,
      newDirection: { abr: "", nom: "" },
    };
  },
  computed: {
    userInitial() {
      return this.userName ? this.userName[0].toUpperCase() : "?";
    },
    sortedDirections() {
      return [...this.directions].sort((a, b) => a.nom.localeCompare(b.nom));
    },
  },
  mounted() {
    this.getUserName();
    this.loadDirections();
  },
  methods: {
    getUserName() {
      const token = localStorage.getItem("access");
      if (!token || token.split(".").length !== 3) {
        this.userName = "User";
        return;
      }
      try {
        const decoded = JSON.parse(atob(token.split(".")[1]));
        this.userName = decoded.name || "User";
      } catch {
        this.userName = "User";
      }
    },

    async loadDirections() {
      try {
        const res = await axios.get("http://localhost:8000/api/directions/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("access")}` },
        });
        this.directions = res.data;
      } catch (e) {
        console.error(e);
        alert("Erreur lors du chargement des directions 😕");
      }
    },

    async addDirection() {
      if (!this.newDirection.abr || !this.newDirection.nom) {
        alert("Tous les champs sont obligatoires !");
        return;
      }
      try {
        const res = await axios.post(
          "http://localhost:8000/api/directions/",
          this.newDirection,
          { headers: { Authorization: `Bearer ${localStorage.getItem("access")}` } }
        );
        this.directions.push(res.data);
        alert("✅ Direction ajoutée !");
        this.showModal = false;
        this.newDirection = { abr: "", nom: "" };
      } catch (e) {
        console.error(e);
        alert("❌ Erreur lors de l’ajout !");
      }
    },

    goToCrud(direction) {
      const action = prompt(
        `Direction: ${direction.nom}\nChoisir action:\n1- Modifier\n2- Supprimer\n3- Stats`
      );
      switch (action) {
        case "1":
          this.modifyDirection(direction);
          break;
        case "2":
          this.deleteDirection(direction);
          break;
        case "3":
          this.viewStats(direction);
          break;
      }
    },

    async modifyDirection(direction) {
      const newNom = prompt("Nouveau nom :", direction.nom);
      if (!newNom) return;
      try {
        const res = await axios.put(
          `http://localhost:8000/api/directions/${direction.id}/`,
          { abr: direction.abr, nom: newNom },
          { headers: { Authorization: `Bearer ${localStorage.getItem("access")}` } }
        );
        this.directions = this.directions.map((d) =>
          d.id === direction.id ? res.data : d
        );
        alert("✅ Direction modifiée !");
      } catch (e) {
        console.error(e);
        alert("❌ Erreur lors de la modification !");
      }
    },

    async deleteDirection(direction) {
      if (!confirm(`Supprimer ${direction.nom} ?`)) return;
      try {
        await axios.delete(
          `http://localhost:8000/api/directions/${direction.id}/`,
          { headers: { Authorization: `Bearer ${localStorage.getItem("access")}` } }
        );
        this.directions = this.directions.filter((d) => d.id !== direction.id);
        alert("🗑️ Direction supprimée !");
      } catch (e) {
        console.error(e);
        alert("❌ Erreur lors de la suppression !");
      }
    },

    viewStats(direction) {
      alert(`📊 Voir statistiques pour ${direction.nom}`);
    },
  },
};
</script>

<style scoped>
.page-container {
  height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #42b983, #2c3e50, #3aa17e);
  background-size: 300% 300%;
  animation: moveGradient 8s ease infinite;
  color: white;
  overflow: hidden;
}
@keyframes moveGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 0.5rem;
}
.user-circle {
  background: white;
  color: #42b983;
  font-weight: bold;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.directions-table {
  max-height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.direction-btn {
  background: rgba(255,255,255,0.1);
  padding: 1rem;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}
.direction-btn:hover {
  background: rgba(255,255,255,0.2);
}

.abr { font-weight: bold; text-decoration: underline red; font-size: 1.2rem; }
.fullname { margin-top: 0.3rem; font-size: 1rem; }

.add-btn {
  background: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  background: #2c3e50;
  padding: 2.5rem;
  border-radius: 15px;
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.modal input { padding: 0.5rem; border-radius: 8px; border: none; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; }
.btn-blue, .btn-red {
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}
.btn-blue { background-color: #3498db; }
.btn-red { background-color: #e74c3c; }
</style>
