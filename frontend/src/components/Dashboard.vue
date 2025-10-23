<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1 class="welcome-title">
        Bienvenue dans l'application de gestion de voiture<br />
        <span class="m">M</span><span class="n">N</span><span class="d">D</span><span class="p">P</span><span class="t">T</span>
      </h1>
    </div>

    <div class="carousel-container">
      <div
        v-for="(item, index) in menus"
        :key="index"
        class="carousel-item"
        :class="{ active: index === currentIndex }"
        :style="getItemStyle(index)"
        @click="selectMenu(index)"
      >
        <div
          class="menu-background"
          :style="{ backgroundImage: `url(${item.image})` }"
        ></div>
        <div class="menu-content">
          <h2 class="menu-title">{{ item.title }}</h2>
          <div class="title-underline"></div>
          <p class="menu-desc">{{ item.desc }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CarDashboard",
  data() {
    return {
      menus: [
        {
          title: "Directions",
          desc: "Gérez et visualisez les directions de la société.",
          image: require("@/assets/direction.jpg"),
          route: "/directions",
        },
        {
          title: "Détenteurs",
          desc: "Consultez les détenteurs actuels de chaque véhicule.",
          image: require("@/assets/detenteur.jpg"),
          route: "/CarDetenteur",
        },
        {
          title: "Statistiques des Voitures",
          desc: "Les voitures seront répertoriées et analysées ici.",
          image: require("@/assets/statistique.jpg"),
          route: "/VoitureStats",
        },
      ],
      currentIndex: 0,
      autoScroll: null,
    };
  },
  mounted() {
    this.startAutoScroll();
    window.addEventListener("keydown", this.handleKey);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKey);
    clearInterval(this.autoScroll);
  },
  methods: {
    startAutoScroll() {
      this.autoScroll = setInterval(() => {
        this.currentIndex = (this.currentIndex + 1) % this.menus.length;
      }, 3000);
    },
    stopAutoScroll() {
      clearInterval(this.autoScroll);
    },
    handleKey(e) {
      this.stopAutoScroll();
      if (e.key === "ArrowRight") {
        this.currentIndex = (this.currentIndex + 1) % this.menus.length;
      } else if (e.key === "ArrowLeft") {
        this.currentIndex =
          (this.currentIndex - 1 + this.menus.length) % this.menus.length;
      } else if (e.key === "Enter") {
        this.$router.push(this.menus[this.currentIndex].route);
      }
    },
    selectMenu(index) {
      this.currentIndex = index;
      this.$router.push(this.menus[index].route);
    },
    getItemStyle(index) {
      const position = (index - this.currentIndex + this.menus.length) % this.menus.length;
      const baseZ = 10 - position;
      if (position === 0) {
        return {
          transform: "translateX(0) scale(1)",
          filter: "blur(0px)",
          zIndex: baseZ,
          opacity: 1,
        };
      } else if (position === 1) {
        return {
          transform: "translateX(50%) scale(0.9)",
          filter: "blur(3px)",
          zIndex: baseZ,
          opacity: 0.8,
        };
      } else {
        return {
          transform: "translateX(-50%) scale(0.9)",
          filter: "blur(3px)",
          zIndex: baseZ,
          opacity: 0.8,
        };
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  /* 💫 Même fond que le login */
  background: linear-gradient(135deg, #42b983, #2c3e50, #3aa17e);
  background-size: 300% 300%;
  animation: moveGradient 8s ease infinite;
}

@keyframes moveGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.welcome-section {
  height: 30%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: transparent; /* ❗Fond uniforme maintenant */
}

.welcome-title {
  font-size: 3rem;
  font-weight: 900;
  line-height: 1.5;
  color: white;
  text-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
}

/* Couleurs lettres MNDPT */
.m, .n, .d { color: #ff0000; }
.p { color: #ffcc00; }
.t { color: #00ff00; }

/* --- Carousel --- */
.carousel-container {
  position: relative;
  height: 80%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1200px;
}

.carousel-item {
  position: absolute;
  width: 70%;
  height: 85%;
  border-radius: 20px;
  overflow: hidden;
  transition: all 1s ease;
  cursor: pointer;
}

.menu-background {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(70%);
}

.menu-content {
  position: absolute;
  bottom: 15%;
  left: 10%;
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.6);
}

.menu-title {
  font-size: 2.5rem;
  font-weight: bold;
  text-transform: uppercase;
}

.title-underline {
  width: 150px;
  height: 7px;
  background-color: red;
  margin-top: 5px;
  margin-bottom: 15px;
  border-radius: 3px;
}

.menu-desc {
  font-size: 1.3rem;
  width: 80%;
}
</style>
