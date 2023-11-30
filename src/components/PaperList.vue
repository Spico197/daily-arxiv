<script setup>
import { computed, ref, watch, onMounted } from 'vue'

import cat2papers from '../../papers_with_style.json'
import rawCat2papers from '../../papers.json'
import settings from '../../settings.json'

// cat2papers: { "cs.CL": [{"title": ""}, ...], "cs.AI": [{"title": "", ...}, ...] }
const categories = ref(Object.keys(cat2papers))
const papers = ref([])
const categoryString = ref("")
const isChecked = ref([])
const showAbs = ref([])
const paperDates = ref("")

// Compute the number of papers for each category
const paperNum = ref({})
Object.keys(cat2papers).forEach((category) => {
  paperNum.value[category] = cat2papers[category].length
})

const showPapers = (category) => {
  papers.value = cat2papers[category]
  categoryString.value = category
  isChecked.value = Array(paperNum.value[category]).fill(false)
  showAbs.value = Array(paperNum.value[category]).fill(false)
  const uniqueDates = [...new Set(papers.value.map((paper) => paper.date))]
  paperDates.value = uniqueDates.join(', ')
}

let allIsSelected = false
const selectAllButtonString = ref("Select All")
const selectAll = () => {
  allIsSelected = !allIsSelected
  isChecked.value = Array(paperNum.value[categoryString.value]).fill(allIsSelected)
  selectAllButtonString.value = allIsSelected ? "Unselect All" : "Select All"
}

const numSelected = computed(() => {
  return isChecked.value.filter((item) => item).length
})

const noteMsg = ref("")
const exportToClipboard = () => {
  const selectedPapers = rawCat2papers[categoryString.value].filter((_, index) => isChecked.value[index])
  const paperString = selectedPapers.map((paper) => {
    return `"${paper.title}\n\n${paper.url}"`
  }).join('\n')
  navigator.clipboard.writeText(paperString)
  noteMsg.value = `Successfully export ${numSelected.value} papers of ${categoryString.value} to clipboard~`
}

watch(noteMsg, (newValue) => {
  if (newValue) {
    setTimeout(() => {
      noteMsg.value = ""
    }, 2000)
  }
})

const lastUpdate = ref("")

onMounted(getLatestCommitDateTime)


async function getLatestCommitDateTime() {
  try {
    const apiUrl = `https://api.github.com/repos/${settings.owner}/${settings.repo}/branches/${settings.branch}`
    const response = await fetch(apiUrl)

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }

    const branchData = await response.json()
    const commit = branchData.commit.commit
    const commitDate = new Date(commit.committer.date)
    const formattedDate = commitDate.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZone: 'Asia/Shanghai' })
    lastUpdate.value = formattedDate
    console.log(`Last update date: ${formattedDate}`)
  } catch (error) {
    console.error('Error:', error.message)
  }
}

function navigateToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

</script>

<template>
  <!-- Existing code... -->
  <div class="button-group">
    <button @click="exportToClipboard"><i class="fas fa-file-export"></i> Export to Clipboard</button>
    <button @click="selectAll"><i class="fas fa-check-square"></i> {{ selectAllButtonString }}</button>
  </div>
  <p v-if="noteMsg" class="bold">{{ noteMsg }}</p>
  <div class="button-group">
    <button v-for="category in categories" :key="category" @click="showPapers(category)">{{ category }} ({{
      paperNum[category] }})</button>
  </div>
  <p>Last update time: {{ lastUpdate }}</p>
  <div v-if="categoryString">
    <p>Selected {{ numSelected }} / {{ paperNum[categoryString] }} from {{ categoryString }}</p>
    <p>Paper dates: {{ paperDates }}</p>
  </div>
  <div class="paper-list">
    <div v-for="(paper, index) in papers" :key="paper.url">
      <div class="row title" @click="isChecked[index] = !isChecked[index]">
        <label class="col">{{ index }} - <input type="checkbox" v-model="isChecked[index]" /></label>
        <p class="col no-margin" v-html="paper.title"></p>
      </div>
      <p class="no-margin"><span class="bold">Authors: </span><span v-html="paper.authors.join(', ')"></span></p>
      <p class="no-margin" v-if="paper.comment"><span class="bold">Comment: </span><span v-html="paper.comment"></span>
      </p>
      <div class="no-margin">
        <a class="badge badge-link" :href="paper.url" target="_blank">Link</a>
        <a class="badge badge-pdf" :href="paper.pdf_url" target="_blank">PDF</a>
        <a class="badge badge-abs" @click="showAbs[index] = !showAbs[index]">Abstract</a>
        <p class="text-block" v-if="showAbs[index]" v-html="paper.abstract"></p>
      </div>
    </div>
  </div>
  <div>
    <!-- Floating "Navigate to Top" button -->
    <button class="navigate-top-button" @click="navigateToTop">
      <i class="fas fa-arrow-up"></i>
    </button>
  </div>
</template>

<style>
.title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 1rem;
  margin-bottom: 0;
}

.title:hover {
  cursor: pointer;
}

.no-margin {
  margin: 0;
}

.bold {
  font-weight: bold;
}

.emph {
  color: #d05130;
  font-style: italic;
}

.navigate-top-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #333;
  color: #fff;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.navigate-top-button:hover {
  background-color: #555;
}

</style>
