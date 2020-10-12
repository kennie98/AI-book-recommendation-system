<template>
  <div id="app">
    <img alt="hpl logo" src="./assets/HPL.png">
    <h1>AI Recommendation System</h1>
    <TodoList />
  </div>
</template>

<script>
import TodoList from "./components/TodoList.vue"
export default {
  name: "App",
  components: {
    TodoList
  }
}
</script>

<style>
body {
  background-color: rgb(66,66,66);
  color: aliceblue;
}
</style>