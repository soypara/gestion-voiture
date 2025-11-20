<template>
  <div class="page-container">

    <!-- TOP BAR + TITRE FIXE AVEC OMBRE -->
    <div class="top-container">
      <div class="top-bar">
        <div class="user-info">
          <div class="user-circle">{{ userInitial }}</div>
          <span class="user-name">{{ userName }}</span>
        </div>

        <button class="btn-blue add-btn" @click="openCreateForm">
          Ajouter un détenteur
        </button>
      </div>

      <h1 class="page-title">Liste des détenteurs</h1>
    </div>

    <!-- LISTE DES DÉTENTEURS (SEULE PARTIE SCROLLABLE) -->
    <div class="detenteurs-list">
      <div
        class="detenteur-card"
        v-for="d in detenteurs"
        :key="d.id"
        @click="toggleExpand(d.id)"
        :class="{ expanded: expandedId === d.id }"
      >
        <img :src="d.photo" class="profile-img" />

        <div class="detenteur-info">
          <div class="name">{{ d.nom }} {{ d.prenom }}</div>
          <div class="direction">Direction : {{ getDirectionName(d.direction) }}</div>
          <div class="fonction">Fonction : {{ d.fonction }}</div>

          <transition name="fade-slide">
            <div class="crud-buttons" v-if="expandedId === d.id">
              <button class="btn-green" @click.stop="openEditForm(d)">Modifier</button>
              <button class="btn-red" @click.stop="confirmDelete(d.id)">Supprimer</button>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- MODAL -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal">
        <h2>{{ editMode ? "Modifier un détenteur" : "Ajouter un détenteur" }}</h2>

        <div class="form-group">
          <label>Nom :</label>
          <input type="text" v-model="form.nom" />
        </div>

        <div class="form-group">
          <label>Prénom :</label>
          <input type="text" v-model="form.prenom" />
        </div>

        <div class="form-group">
          <label>Direction :</label>
          <select v-model="form.direction">
            <option v-for="d in listDirections" :key="d.id" :value="d.id">
              {{ d.nom }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Fonction :</label>
          <select v-model="form.fonction">
            <option value="detenteur">Détenteur</option>
            <option value="chauffeur">Chauffeur</option>
            <option value="les_deux">Les deux</option>
          </select>
        </div>

        <div class="form-group">
          <label>Photo :</label>
          <input type="file" @change="onImageSelect" />
        </div>

        <img v-if="previewImg" :src="previewImg" class="preview-img" />

        <div class="form-actions">
          <button class="btn-red" @click="closeForm">Annuler</button>
          <button class="btn-green" @click="submitForm">
            {{ editMode ? "Mettre à jour" : "Créer" }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "@/axios.js";

export default {
  name: "DetenteursPage",

  data() {
    return {
      detenteurs: [],
      listDirections: [],
      userName: "User",
      userInitial: "U",
      expandedId: null,
      showForm: false,
      editMode: false,
      form: {
        id: null,
        nom: "",
        prenom: "",
        direction: "",
        fonction: "",
        photo: null,
      },
      previewImg: null,
    };
  },

  mounted() {
    this.fetchDetenteurs();
    this.fetchDirections();
  },

  methods: {
    async fetchDetenteurs() {
      const res = await axios.get("http://localhost:8000/api/detenteurs/");
      this.detenteurs = res.data;
    },

    async fetchDirections() {
      const res = await axios.get("http://localhost:8000/api/directions/");
      this.listDirections = res.data;
    },

    getDirectionName(id) {
      const d = this.listDirections.find((x) => x.id === id);
      return d ? d.nom : "—";
    },

    toggleExpand(id) {
      this.expandedId = this.expandedId === id ? null : id;
    },

    onImageSelect(e) {
      const file = e.target.files[0];
      this.form.photo = file;
      this.previewImg = URL.createObjectURL(file);
    },

    openCreateForm() {
      this.editMode = false;
      this.showForm = true;
      this.form = {
        id: null,
        nom: "",
        prenom: "",
        direction: "",
        fonction: "",
        photo: null,
      };
      this.previewImg = null;
    },

    openEditForm(d) {
      this.editMode = true;
      this.showForm = true;
      this.form = {
        id: d.id,
        nom: d.nom,
        prenom: d.prenom,
        direction: d.direction,
        fonction: d.fonction,
        photo: null,
      };
      this.previewImg = d.photo;
    },

    closeForm() {
      this.showForm = false;
    },

    async submitForm() {
      const fd = new FormData();
      fd.append("nom", this.form.nom);
      fd.append("prenom", this.form.prenom);
      fd.append("direction", this.form.direction);
      fd.append("fonction", this.form.fonction);
      if (this.form.photo) fd.append("photo", this.form.photo);

      if (this.editMode) {
        await axios.put(`http://localhost:8000/api/detenteurs/${this.form.id}/`, fd);
      } else {
        await axios.post("http://localhost:8000/api/detenteurs/", fd);
      }

      this.closeForm();
      this.fetchDetenteurs();
    },

    confirmDelete(id) {
      if (confirm("Es-tu sûr de vouloir supprimer ce détenteur ?")) {
        this.deleteDetenteur(id);
      }
    },

    async deleteDetenteur(id) {
      await axios.delete(`http://localhost:8000/api/detenteurs/${id}/`);
      alert("Suppression effectuée ✅");
      this.fetchDetenteurs();
    },
  },
};
</script>

<style scoped>
/* BACKGROUND FULL SCREEN */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.page-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #42b983, #2c3e50, #3aa17e);
  background-size: 300% 300%;
  animation: moveGradient 8s ease infinite;
  color: white;
}

/* ANIMATION */
@keyframes moveGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* TOP FIXE + OMBRE + BLUR */
.top-container {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(8px);
  padding: 1rem 2rem;
  box-shadow: 0 6px 10px rgba(0,0,0,0.35);
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.user-circle {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: white;
  color: #1f5e3f;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}

.page-title {
  text-align: center;
  margin-top: 0.6rem;
  font-size: 1.6rem;
  font-weight: bold;
}

/* LISTE SCROLLABLE UNIQUEMENT */
.detenteurs-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* CARDS */
.detenteur-card {
  background: rgba(255, 255, 255, 0.12);
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  gap: 1rem;
  cursor: pointer;
  transition: 0.3s;
}

.detenteur-card.expanded {
  background: rgba(255, 255, 255, 0.22);
}

.profile-img {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  object-fit: cover;
}

.detenteur-info {
  flex: 1;
}

.name {
  font-weight: bold;
  font-size: 1.2rem;
  text-decoration: underline red;
}

.direction, .fonction {
  font-size: 0.95rem;
  color: #f1f1f1;
}

/* CRUD BUTTONS */
.crud-buttons {
  margin-top: 0.6rem;
  display: flex;
  gap: 0.7rem;
}

/* BOUTONS */
.btn-blue, .btn-green, .btn-red {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  color: white;
}

.btn-blue { background: #3498db; }
.btn-green { background: #2ecc71; }
.btn-red { background: #e74c3c; }

/* MODAL */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal {
  background: #2c3e50;
  padding: 2rem;
  border-radius: 16px;
  width: 90%;
  max-width: 480px;
}

/* FORM */
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.form-group label {
  margin-bottom: 0.3rem;
}

input[type="text"], select, input[type="file"] {
  padding: 0.5rem;
  border-radius: 8px;
  border: none;
}

.preview-img {
  width: 95px;
  height: 95px;
  border-radius: 12px;
  object-fit: cover;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
