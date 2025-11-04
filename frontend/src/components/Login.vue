<template>
  <div class="login-page">
    <div class="center-box">
      <p class="intro-text">Connecte-toi à ton compte MNDPT 🚗</p>
      <form @submit.prevent="handleLogin">
        <input type="email" placeholder="Email" v-model="email" required />
        <input type="password" placeholder="Mot de passe" v-model="password" required />
        <button type="submit">Se connecter</button>
      </form>
      <p>Pas encore de compte ? <router-link to="/register">Inscris-toi</router-link></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginMndpt",
  data() {
    return { email: "", password: "" };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, password: this.password }),
        });
        const data = await response.json();
        if (response.ok) {
          localStorage.setItem("access", data.access);
          localStorage.setItem("refresh", data.refresh);
          alert("Connexion réussie !");
          this.$router.push("/directions");
        } else alert(data.detail || "Erreur login");
      } catch (err) {
        console.error(err);
        alert("Erreur réseau : impossible de contacter le serveur");
      }
    },
  },
};
</script>

<style scoped>
.login-page { display:flex; justify-content:center; align-items:center; height:100vh; background:linear-gradient(135deg,#42b983,#2c3e50,#3aa17e); background-size:300% 300%; animation:moveGradient 8s ease infinite; }
@keyframes moveGradient {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.center-box { background:rgba(255,255,255,0.1); backdrop-filter:blur(10px); padding:3rem; border-radius:30px; width:60%; }
.intro-text { font-size:1.3rem; margin-bottom:2rem; color:white; }
input { display:block; width:100%; padding:1rem; margin-bottom:1rem; border-radius:10px; border:none; }
button { font-size:1.2rem; padding:1rem 2rem; border:none; border-radius:25px; background:white; color:#42b983; font-weight:bold; cursor:pointer; transition:all 0.3s ease; }
button:hover { background:#2c3e50; color:white; transform:scale(1.05); }
a { color:#42b983; text-decoration:underline; }
</style>
