<template>
  <div id="register-page">
    <div class="register-box">
      <h1>Inscription</h1>
      <form @submit.prevent="registerUser">
        <input type="text" placeholder="Nom complet" v-model="name" required />
        <input type="email" placeholder="Email" v-model="email" required />
        <input type="password" placeholder="Mot de passe" v-model="password" required />
        <button type="submit">S'inscrire</button>
      </form>
      <p class="login-link">
        Déjà inscrit ? <span @click="$router.push('/login')">Connectez-vous</span>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterPage",
  data() {
    return {
      name: "",
      email: "",
      password: "",
    };
  },
  methods: {
    registerUser() {
      console.log("Form submitted:", this.name, this.email, this.password);
      // ici on connectera avec le backend plus tard
    },
    async handleRegister() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/users/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: this.email, name: this.name, password: this.password }),
      });
      const data = await response.json();
      if (response.ok) {
        alert("Compte créé !");
        this.$router.push("/login");
      } else {
        alert(data.error || "Erreur inscription");
      }
    } catch (err) {
      console.error(err);
    }
  },
  },
};

</script>

<style>
#register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;

  /* Même fond que ton app.vue */
  background: linear-gradient(135deg, #42b983, #2c3e50, #3aa17e);
  background-size: 300% 300%;
  animation: moveGradient 8s ease infinite;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
}

@keyframes moveGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.register-box {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  padding: 4rem 6rem; /* élargi pour style paysage */
  border-radius: 30px;
  box-shadow: 0 12px 24px rgba(0,0,0,0.25);
  width: 70%;
  max-width: 900px;
  text-align: center;
}

.register-box h1 {
  margin-bottom: 2rem;
  color: white;
  font-size: 2.2rem;
}

.register-box input {
  width: 100%;
  padding: 1rem;
  margin: 0.7rem 0;
  border-radius: 15px;
  border: none;
  font-size: 1rem;
}

.register-box button {
  width: 100%;
  padding: 1rem;
  margin-top: 1rem;
  border: none;
  border-radius: 25px;
  font-size: 1.2rem;
  background: white;
  color: #42b983;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.register-box button:hover {
  background: #2c3e50;
  color: white;
  transform: scale(1.05);
}

.login-link {
  margin-top: 1.5rem;
  color: white;
}

.login-link span {
  text-decoration: underline;
  cursor: pointer;
}
</style>
