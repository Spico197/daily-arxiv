<script setup>
import PaperList from './components/PaperList.vue'
</script>

<template>
  <header>
    <h1>Daily arXiv</h1>
    <p>Get the latest arXiv papers everyday.</p>
    <p>🌟 Star me on GitHub <a href="https://github.com/Spico197/daily-arxiv" target="_blank">Spico197/daily-arxiv</a></p>
    <hr />
    <p>Other paper lists:</p>
    <ul>
      <li><a href="https://huggingface.co/papers">huggingface.co/papers</a></li>
      <li><a href="https://github.com/dair-ai/ML-Papers-of-the-Week">dair-ai/ML-Papers-of-the-Week</a></li>
    </ul>
    <hr />
  </header>

  <main>
    <PaperList />
  </main>

  <footer>
    <hr />
    <p>Made by <a href="https://spico197.github.io/" target="_blank">Tong Zhu</a> w/ ❤️</p>
  </footer>
</template>

<style scoped></style>
