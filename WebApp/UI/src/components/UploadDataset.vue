<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import Papa from 'papaparse'
import { useDatasetStore } from '@/stores/dataset'

const VALID_EXTENSIONS = ['.csv', '.xls', '.xlsx']
const SIZE_LIMIT = 1024 * 1024 * 1024 * 150 //150 MB

const toast = useToast()
const inputRef = ref<HTMLInputElement | null>(null)

const store = useDatasetStore()

const openUpload = () => {
  inputRef.value?.click()
}

const handleFileChange = () => {
  const target = inputRef.value?.files?.[0]
  if (!target) return

  const targetExt = `.${target.name.split('.').slice(-1)[0]}`
  if (!VALID_EXTENSIONS.some((ext) => targetExt === ext)) {
    toast.error('Unsupported Dataset: Unknown file type.')
    return
  }

  if (target.size > SIZE_LIMIT) {
    toast.error('Unsupported Dataset: File is too big.')
    return
  }

  Papa.parse(target, {
    header: true,
    complete: (result) => {
      store.set_dataset(result.data)
      store.set_name(target.name)
    },
    error: () => {
      toast.error('System Error: Parse file failed.')
    },
  })
}
</script>

<template>
  <input
    ref="inputRef"
    type="file"
    hidden
    multiple="false"
    @accept="VALID_EXTENSIONS.join(',')"
    @change="handleFileChange"
  />

  <button
    @click="openUpload"
    class="px-6 py-2 border rounded-md text-white bg-emerald-600 hover:shadow-md"
  >
    <span class="fa fa-upload mr-2"></span>
    Upload
  </button>
</template>
