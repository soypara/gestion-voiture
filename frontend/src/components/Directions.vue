<template>
  <div class="page-container">
    <div class="user-info">
      <div class="user-circle">{{ userInitial }}</div>
      <span class="user-name">{{ userName }}</span>
    </div>

    <h1>Directions</h1>
    <button class="add-btn" @click="showModal = true">Ajouter Direction</button>

    <!-- Tableau scrollable -->
    <div class="directions-table">
      <button
        v-for="dir in sortedDirections"
        :key="dir.id"
        class="direction-btn"
        @click="goToCrud(dir)"
      >
        <div class="abbr">{{ dir.abbr }}</div>
        <div class="fullname">{{ dir.name }}</div>
      </button>
    </div>

    <!-- Modal Ajouter -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>Ajouter une Direction</h2>
        <input v-model="newDirection.abbr" placeholder="Abréviation" />
        <input v-model="newDirection.name" placeholder="Nom complet" />
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
      newDirection: { abbr: "", name: "" },
    };
  },
  computed: {
    userInitial() {
      return this.userName ? this.userName[0].toUpperCase() : "?";
    },
    sortedDirections() {
      return [...this.directions].sort((a, b) => a.name.localeCompare(b.name));
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
        } catch {
          this.userName = "User";
        }
      }
    },
    async loadDirections() {
      try {
        const res = await axios.get("http://localhost:8000/api/directions/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("access")}` },
        });
        this.directions = res.data;
      } catch (e) { console.error(e); }
    },
    async addDirection() {
      if (!this.newDirection.abbr || !this.newDirection.name) {
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
        this.showModal = false;
        this.newDirection = { abbr: "", name: "" };
      } catch (e) { console.error(e); }
    },
    goToCrud(direction) {
      const action = prompt(
        `Direction: ${direction.name}\nChoisir action:\n1- Modifier\n2- Supprimer\n3- Stats`
      );
      switch(action) {
        case "1": this.modifyDirection(direction); break;
        case "2": this.deleteDirection(direction); break;
        case "3": this.viewStats(direction); break;
      }
    },
    async modifyDirection(direction) {
      const newName = prompt("Nouveau nom :", direction.name);
      if (!newName) return;
      try {
        await axios.put(
          `http://localhost:8000/api/directions/${direction.id}/`,
          { abbr: direction.abbr, name: newName },
          { headers: { Authorization: `Bearer ${localStorage.getItem("access")}` } }
        );
        this.loadDirections();
      } catch (e) { console.error(e); }
    },
    async deleteDirection(direction) {
      if (!confirm(`Supprimer ${direction.name} ?`)) return;
      try {
        await axios.delete(
          `http://localhost:8000/api/directions/${direction.id}/`,
          { headers: { Authorization: `Bearer ${localStorage.getItem("access")}` } }
        );
        this.loadDirections();
      } catch (e) { console.error(e); }
    },
    viewStats(direction) {
      alert(`Voir statistiques voitures pour ${direction.name}`);
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
  overflow: hidden; /* page ne défile pas */
}

.directions-table {
  max-height: 400px; /* hauteur tableau scrollable */
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.direction-btn {
  display: flex;
  flex-direction: column;
  text-align: center;
  background: rgba(255,255,255,0.1);
  padding: 1rem;
  border-radius: 10px;
  color: white;
  cursor: pointer;
}

.abbr {
  font-weight: bold;
  text-decoration: underline red;
  font-size: 1.2rem;
}

.fullname {
  margin-top: 0.3rem;
  font-size: 1rem;
}

.add-btn { background: #3498db; color:white; padding:0.5rem 1rem; border:none; border-radius:10px; cursor:pointer; }

.modal-overlay { position: fixed; inset:0; background: rgba(0,0,0,0.6); display:flex; justify-content:center; align-items:center; }
.modal { background:#2c3e50; padding:2.5rem; border-radius:15px; width:400px; display:flex; flex-direction:column; gap:1rem; }
.modal input { padding:0.5rem; border-radius:8px; border:none; }
.modal-actions { display:flex; justify-content:flex-end; gap:1rem; }
.btn-blue { background-color:#3498db;color:white;padding:0.5rem 1rem;border-radius:10px;border:none;cursor:pointer; }
.btn-red { background-color:#e74c3c;color:white;padding:0.5rem 1rem;border-radius:10px;border:none;cursor:pointer; }
</style>
