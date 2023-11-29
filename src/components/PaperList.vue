<script setup>
import { computed, ref, watch } from 'vue'

import cat2papers from '../../papers_with_style.json'

// cat2papers: { "cs.CL": [{"title": ""}, ...], "cs.AI": [{"title": "", ...}, ...] }
const categories = ref(Object.keys(cat2papers))
const papers = ref([])
const categoryString = ref("")
const paperNum = ref(0)
const isChecked = ref([])
const showAbs = ref([])
const paperDates = ref("")

const showPapers = (category) => {
  papers.value = cat2papers[category]
  categoryString.value = category
  paperNum.value = papers.value.length
  isChecked.value = Array(paperNum.value).fill(false)
  showAbs.value = Array(paperNum.value).fill(false)
  const uniqueDates = [...new Set(papers.value.map((paper) => paper.date))]
  paperDates.value = uniqueDates.join(', ')
}

let allIsSelected = false
const selectAllButtonString = ref("Select All")
const selectAll = () => {
  allIsSelected = !allIsSelected
  isChecked.value = Array(paperNum.value).fill(allIsSelected)
  selectAllButtonString.value = allIsSelected ? "Unselect All" : "Select All"
}

const numSelected = computed(() => {
  return isChecked.value.filter((item) => item).length
})

const noteMsg = ref("")
const exportToClipboard = () => {
  const selectedPapers = papers.value.filter((_, index) => isChecked.value[index])
  const paperString = selectedPapers.map((paper) => {
    return `"${paper.title}\n\n${paper.url}"`
  }).join('\n')
  navigator.clipboard.writeText(paperString)
  noteMsg.value = `Successfully export ${numSelected.value} papers of ${categoryString.value} to clipboard~`
}

// const exportToClipboard = () => {
//   const selectedPapers = papers.value.filter((_, index) => isChecked.value[index])
//   const paperString = selectedPapers.map((paper) => {
//     // Format the title and URL as HTML
//     return `<td>${paper.title} <br style="mso-data-placement:same-cell;" /> <a href="${paper.url}">${paper.url}</a></td>`
//   }).join('</tr><tr>')
//   console.log(`<table><tr>${paperString}</tr></table>`)

//   const blob = new Blob([`<table><tr>${paperString}</tr></table>`], { type: 'text/html' })
//   const data = new ClipboardItem({ 'text/html': blob })

//   navigator.clipboard.write([data])
//     .then(() => {
//       console.log('Text copied to clipboard')
//       noteMsg.value = `Successfully export ${numSelected.value} papers of ${categoryString.value} to clipboard~`
//     })
//     .catch(err => {
//       noteMsg.value = `Error in copying text: ${err}`
//     })
// }

watch(noteMsg, (newValue) => {
  if (newValue) {
    setTimeout(() => {
      noteMsg.value = ""
    }, 2000)
  }
})

</script>

<template>
  <div class="button-group">
    <button @click="exportToClipboard"><i class="fas fa-file-export"></i> Export to Clipboard</button>
    <button @click="selectAll"><i class="fas fa-check-square"></i> {{ selectAllButtonString }}</button>
  </div>
  <p v-if="noteMsg" class="bold">{{ noteMsg }}</p>
  <div class="button-group">
    <button v-for="category in categories" :key="category" @click="showPapers(category)">{{ category }}</button>
  </div>
  <p>Papers under {{ categoryString }} : {{ paperNum }}, selected : {{ numSelected }}</p>
  <p>Paper dates: {{ paperDates }}</p>
  <div class="paper-list">
    <div v-for="(paper, index) in papers" :key="paper.url">
      <div class="row title" @click="isChecked[index] = !isChecked[index]">
        <label class="col">{{ index }} - <input type="checkbox" v-model="isChecked[index]" /></label>
        <p class="col no-margin" v-html="paper.title"></p>
      </div>
      <p class="no-margin"><span class="bold">Authors: </span><span v-html="paper.authors.join(', ')"></span></p>
      <p class="no-margin" v-if="paper.comment"><span class="bold">Comment: </span><span v-html="paper.comment"></span></p>
      <div class="no-margin">
        <a class="badge badge-link" :href="paper.url" target="_blank">Link</a>
        <a class="badge badge-pdf" :href="paper.pdf_url" target="_blank">PDF</a>
        <a class="badge badge-abs" @click="showAbs[index] = !showAbs[index]">Abstract</a>
        <p class="text-block" v-if="showAbs[index]">{{ paper.abstract }}</p>
      </div>
    </div>
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

</style>
