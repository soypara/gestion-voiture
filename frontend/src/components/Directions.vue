<template>
  <div class="page-container">
    <div class="user-info">
      <div class="user-circle">{{ userInitial }}</div>
      <span class="user-name">{{ userName }}</span>
    </div>
    <h1>Directions</h1>
    <button class="add-btn" @click="showModal=true">Ajouter Direction</button>

    <div class="directions-table">
      <div v-for="dir in sortedDirections" :key="dir.id"
           :class="['direction-btn', { expanded: expandedDir && expandedDir.id === dir.id }]"
           @click="goToCrud(dir)">
        
        <div class="abr">{{ dir.abr }}</div>
        <div class="fullname">{{ dir.nom }}</div>

        <!-- Actions visibles uniquement si cette direction est expand -->
        <transition name="fade-slide">
          <div v-if="expandedDir && expandedDir.id === dir.id" class="dir-actions">
            <button class="btn-blue" @click.stop="modifyDirection(dir)">Modifier</button>
            <button class="btn-red" @click.stop="deleteDirection(dir)">Supprimer</button>
            <button class="btn-green" @click.stop="viewStats(dir)">Stats</button>
          </div>
        </transition>

      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>Ajouter une Direction</h2>
        <input v-model="newDirection.abr" placeholder="Abréviation"/>
        <input v-model="newDirection.nom" placeholder="Nom complet"/>
        <div class="modal-actions">
          <button class="btn-blue" @click="addDirection">Ajouter</button>
          <button class="btn-red" @click="showModal=false">Annuler</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "DirectionsMndpt",
  data() {
    return {
      userName: "",
      directions: [],
      showModal: false,
      newDirection: { abr: "", nom: "" },
      expandedDir: null, // direction actuellement expand
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
        const res = await axios.get("http://localhost:8000/api/directions/");
        this.directions = res.data;
      } catch (e) {
        console.error(e);
        Swal.fire("Erreur 😕", "Impossible de charger les directions.", "error");
      }
    },

    async addDirection() {
      if (!this.newDirection.abr.trim() || !this.newDirection.nom.trim()) {
        Swal.fire("⚠️ Oups", "Tous les champs sont obligatoires !", "warning");
        return;
      }
      try {
        const res = await axios.post(
          "http://localhost:8000/api/directions/",
          this.newDirection
        );
        this.directions.push(res.data);
        Swal.fire("✅ Succès", "Direction ajoutée avec succès !", "success");
        this.showModal = false;
        this.newDirection = { abr: "", nom: "" };
      } catch (e) {
        console.error(e);
        Swal.fire("❌ Erreur", "Problème lors de l’ajout !", "error");
      }
    },

    // ========================== NOUVELLE FONCTION ==========================
    goToCrud(dir) {
      // Si clique sur la même direction => collapse
      if (this.expandedDir && this.expandedDir.id === dir.id) {
        this.expandedDir = null;
      } else {
        this.expandedDir = dir;
      }
      // Les boutons Modifier, Supprimer, Stats sont affichés via template
      // et appellent directement les fonctions existantes
    },

    async modifyDirection(dir) {
      const { value: newNom } = await Swal.fire({
        title: "Modifier le nom",
        input: "text",
        inputValue: dir.nom,
        showCancelButton: true,
      });
      if (!newNom || newNom.trim() === "") return;
      try {
        await axios.put(`http://localhost:8000/api/directions/${dir.id}/`, {
          abr: dir.abr,
          nom: newNom,
        });
        await this.loadDirections();
        Swal.fire("✅ Succès", "Direction modifiée avec succès !", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("❌ Erreur", "Problème lors de la modification.", "error");
      }
    },

    async deleteDirection(dir) {
      const confirm = await Swal.fire({
        title: `Supprimer ${dir.nom} ?`,
        text: "Cette action est irréversible !",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Oui, supprimer",
        cancelButtonText: "Annuler",
      });
      if (!confirm.isConfirmed) return;
      try {
        await axios.delete(`http://localhost:8000/api/directions/${dir.id}/`);
        await this.loadDirections();
        Swal.fire("🗑️ Supprimée", "Direction supprimée avec succès.", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("❌ Erreur", "Problème lors de la suppression.", "error");
      }
    },

    viewStats(dir) {
      Swal.fire("📊 Statistiques", `Voir stats pour ${dir.nom}`, "info");
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

/* ==================== CSS POUR EXPAND + ANIMATION ==================== */
.direction-btn {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.direction-btn.expanded {
  background: rgba(255, 255, 255, 0.2);
  padding: 1.5rem;
}

.dir-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

/* Animation fade + slide pour les boutons */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.btn-blue,
.btn-red,
.btn-green {
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.btn-blue { background-color: #3498db; }
.btn-red { background-color: #e74c3c; }
.btn-green { background-color: #2ecc71; }

/* ==================== RESTE DU CSS ORIGINAL ==================== */
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
.modal input {
  padding: 0.5rem;
  border-radius: 8px;
  border: none;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
