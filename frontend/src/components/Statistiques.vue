<template>
  <div class="page-container">
    <h1>Statistiques des Voitures</h1>

    <!-- Bouton Ajouter Voiture -->
    <button class="add-btn" @click="showModal = true">Ajouter une voiture</button>

    <!-- Tabs -->
    <div class="tabs">
      <button :class="{ active: currentTab === 'generales' }" @click="currentTab = 'generales'">Stat Générales</button>
      <button :class="{ active: currentTab === 'services' }" @click="currentTab = 'services'">Stat Services</button>
      <button :class="{ active: currentTab === 'directions' }" @click="currentTab = 'directions'">Stat Directions</button>
    </div>

    <!-- Contenu des Tabs -->
    <div v-if="currentTab === 'generales'">
      <h2>Statistiques Générales</h2>
      <div v-for="v in voitures" :key="v.id" 
           :class="['voiture-card', { expanded: expandedVoiture && expandedVoiture.id === v.id }]" 
           @click="toggleExpand(v)">
        <strong>{{ v.immatriculation }}</strong> - {{ v.marque }} - {{ v.etat }}
        <transition name="fade-slide">
          <div v-if="expandedVoiture && expandedVoiture.id === v.id" class="voiture-actions">
            <button class="btn-blue" @click.stop="modifyVoiture(v)">Modifier</button>
            <button class="btn-red" @click.stop="deleteVoiture(v)">Supprimer</button>
          </div>
        </transition>
      </div>
    </div>

    <div v-if="currentTab === 'services'">
      <h2>Statistiques par Service</h2>
      <div v-for="v in voitures" :key="v.id"
           :class="['voiture-card', { expanded: expandedVoiture && expandedVoiture.id === v.id }]" 
           @click="toggleExpand(v)">
        <strong>{{ v.immatriculation }}</strong> - {{ v.direction }} - {{ v.etat }}
        <transition name="fade-slide">
          <div v-if="expandedVoiture && expandedVoiture.id === v.id" class="voiture-actions">
            <button class="btn-blue" @click.stop="modifyVoiture(v)">Modifier</button>
            <button class="btn-red" @click.stop="deleteVoiture(v)">Supprimer</button>
          </div>
        </transition>
      </div>
    </div>

    <div v-if="currentTab === 'directions'">
      <h2>Statistiques par Direction</h2>
      <div v-for="dir in directions" :key="dir.id" class="direction-card">
        <h3>{{ dir.nom }} ({{ voituresParDirection(dir).length }} voitures)</h3>
        <div v-for="v in voituresParDirection(dir)" :key="v.id"
             :class="['voiture-card', { expanded: expandedVoiture && expandedVoiture.id === v.id }]" 
             @click="toggleExpand(v)">
          <strong>{{ v.immatriculation }}</strong> - {{ v.marque }} - {{ v.etat }}
          <transition name="fade-slide">
            <div v-if="expandedVoiture && expandedVoiture.id === v.id" class="voiture-actions">
              <button class="btn-blue" @click.stop="modifyVoiture(v)">Modifier</button>
              <button class="btn-red" @click.stop="deleteVoiture(v)">Supprimer</button>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- Modal Ajouter Voiture -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>Ajouter une Voiture</h2>
        <input v-model="newVoiture.immatriculation" placeholder="Immatriculation"/>
        <input v-model="newVoiture.marque" placeholder="Marque"/>

        <select v-model="newVoiture.direction">
          <option value="">Choisir une direction</option>
          <option v-for="dir in directions" :key="dir.id" :value="dir.nom">{{ dir.nom }}</option>
        </select>

        <select v-model="newVoiture.detenteur">
          <option value="">Aucun détenteur</option>
          <option v-for="d in detenteurs" :key="d.id" :value="d.id">{{ d.nom }}</option>
        </select>

        <select v-model="newVoiture.chauffeur">
          <option value="">Aucun chauffeur</option>
          <option v-for="d in detenteurs" :key="d.id" :value="d.id">{{ d.nom }}</option>
        </select>

        <input v-model="newVoiture.origine" placeholder="Origine"/>

        <select v-model="newVoiture.etat">
          <option value="bon etat">Bon état</option>
          <option value="moyen">Moyen</option>
          <option value="en panne">En panne</option>
        </select>

        <textarea v-model="newVoiture.observation" placeholder="Observation"></textarea>

        <select v-model="newVoiture.livret">
          <option value="fait">Fait</option>
          <option value="non fait">Non fait</option>
          <option value="SLM">SLM</option>
        </select>

        <select v-model="newVoiture.carte_grise">
          <option value="Carte Grise">Carte Grise</option>
          <option value="SCG">SCG</option>
          <option value="Carte rose">Carte rose</option>
          <option value="Carte rose(CG en cours)">Carte rose(CG en cours)</option>
          <option value="attestation">Attestation</option>
          <option value="lieux">Lieux</option>
        </select>

        <div class="modal-actions">
          <button class="btn-blue" @click="addVoiture">Ajouter</button>
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
  name: "StatistiquesPage",
  data() {
    return {
      voitures: [],
      directions: [],
      detenteurs: [],
      currentTab: "generales",
      showModal: false,
      expandedVoiture: null,
      newVoiture: {
        immatriculation: "",
        marque: "",
        direction: "",
        detenteur: "",
        chauffeur: "",
        origine: "",
        etat: "bon etat",
        observation: "",
        livret: "non fait",
        carte_grise: "Carte Grise"
      },
    };
  },
  mounted() {
    this.loadDirections();
    this.loadVoitures();
    this.loadDetenteurs();
  },
  methods: {
    async loadVoitures() {
      try {
        const res = await axios.get("http://localhost:8000/api/voitures/");
        this.voitures = res.data;
      } catch (e) {
        console.error(e);
        Swal.fire("Erreur 😕", "Impossible de charger les voitures.", "error");
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
    async loadDetenteurs() {
      try {
        const res = await axios.get("http://localhost:8000/api/detenteurs/");
        this.detenteurs = res.data;
      } catch (e) {
        console.error(e);
        Swal.fire("Erreur 😕", "Impossible de charger les détenteurs.", "error");
      }
    },
    voituresParDirection(dir) {
      return this.voitures.filter(v => v.direction === dir.nom);
    },
    toggleExpand(v) {
      this.expandedVoiture = this.expandedVoiture && this.expandedVoiture.id === v.id ? null : v;
    },
    async addVoiture() {
      if (!this.newVoiture.immatriculation || !this.newVoiture.marque || !this.newVoiture.direction) {
        Swal.fire("⚠️ Oups", "Immatriculation, marque et direction obligatoires !", "warning");
        return;
      }
      try {
        const res = await axios.post("http://localhost:8000/api/voitures/", this.newVoiture);
        this.voitures.push(res.data);
        Swal.fire("✅ Succès", "Voiture ajoutée !", "success");
        this.showModal = false;
        this.newVoiture = {
          immatriculation: "",
          marque: "",
          direction: "",
          detenteur: "",
          chauffeur: "",
          origine: "",
          etat: "bon etat",
          observation: "",
          livret: "non fait",
          carte_grise: "Carte Grise"
        };
      } catch (e) {
        console.error(e);
        Swal.fire("❌ Erreur", "Problème lors de l’ajout de la voiture.", "error");
      }
    },
    async modifyVoiture(v) {
      const { value: newMarque } = await Swal.fire({
        title: `Modifier la marque de ${v.immatriculation}`,
        input: "text",
        inputValue: v.marque,
        showCancelButton: true,
      });
      if (!newMarque || newMarque.trim() === "") return;

      try {
        await axios.put(`http://localhost:8000/api/voitures/${v.id}/`, { ...v, marque: newMarque });
        this.loadVoitures();
        Swal.fire("✅ Succès", "Voiture modifiée !", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("❌ Erreur", "Problème lors de la modification.", "error");
      }
    },
    async deleteVoiture(v) {
      const confirm = await Swal.fire({
        title: `Supprimer ${v.immatriculation}?`,
        text: "Cette action est irréversible !",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Oui, supprimer",
        cancelButtonText: "Annuler",
      });
      if (!confirm.isConfirmed) return;

      try {
        await axios.delete(`http://localhost:8000/api/voitures/${v.id}/`);
        this.loadVoitures();
        Swal.fire("🗑️ Supprimée", "Voiture supprimée.", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("❌ Erreur", "Problème lors de la suppression.", "error");
      }
    },
  },
};
</script>

<style scoped>
/* CSS inchangé - garde ton style actuel */
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
.add-btn { background: #3498db; color: white; padding: 0.5rem 1rem; border: none; border-radius: 10px; cursor: pointer; margin-bottom: 1rem; }
.tabs { display: flex; gap: 1rem; margin-bottom: 1rem; }
.tabs button { padding: 0.5rem 1rem; border-radius: 8px; border: none; cursor: pointer; background: rgba(255,255,255,0.1); color: white; }
.tabs button.active { border-bottom: 2px solid #fff; }
.voiture-card { padding: 0.5rem; background: rgba(255,255,255,0.1); margin-bottom: 0.5rem; border-radius: 8px; }
.voiture-card.expanded { background: rgba(255,255,255,0.2); padding: 1rem; }
.voiture-actions { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
.direction-card { margin-bottom: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.15); border-radius: 10px; }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.3s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-enter-to { opacity: 1; transform: translateY(0); }
.fade-slide-leave-from { opacity: 1; transform: translateY(0); }
.fade-slide-leave-to { opacity: 0; transform: translateY(10px); }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; }
.modal { background: #2c3e50; padding: 2.5rem; border-radius: 15px; width: 90%; max-width: 400px; display: flex; flex-direction: column; gap: 1rem; }
.modal input, .modal select, .modal textarea { padding: 0.5rem; border-radius: 8px; border: none; }
.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; }
.btn-blue, .btn-red { color: white; padding: 0.5rem 1rem; border-radius: 8px; border: none; cursor: pointer; }
.btn-blue { background-color: #3498db; }
.btn-red { background-color: #e74c3c; }
</style>
