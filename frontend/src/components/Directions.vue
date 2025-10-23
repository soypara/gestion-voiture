<template>
  <div class="page-container">
    <h1>Directions</h1>
    <p>Ici, vous pourrez gérer et visualiser les directions de la société.</p>
  </div>
</template>

<script>
export default {
  name: "DirectionsMndpt",
};
</script>

<style scoped>
.page-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #42b983, #2c3e50, #3aa17e);
  background-size: 300% 300%;
  animation: moveGradient 8s ease infinite;
  color: white;
  text-align: center;
  padding: 2rem;
}

@keyframes moveGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}
p {
  font-size: 1.5rem;
}
</style>
