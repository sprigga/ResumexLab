<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
/* Updated on 2025-12-02 - Added global reset and background */
/* Reason: Ensure no white margins and consistent gradient background */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
  /* Apply gradient background to body */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%) !important;
}

#app {
  min-height: 100vh;
  width: 100%;
  /* Ensure app container also has the gradient background */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%) !important;
}
</style>
