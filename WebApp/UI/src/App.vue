<script setup lang="ts">
import { onUnmounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useDatasetStore, DatasetActions } from './stores/dataset'

const store = useDatasetStore()
const router = useRouter()

const unsub = store.$onAction(({ name, after, args }) => {
  if (name === DatasetActions.SET_NAME) {
    after(() => {
      const dataset_name = args[0]

      if (!dataset_name) {
        router.push('/')
        return
      }

      router.push(`/dataset/${args[0]}`)
    })
  }
})

onUnmounted(() => {
  unsub()
})
</script>

<template>
  <RouterView />
</template>

<style>
@import '@/assets/tailwind.css';

.anticon {
  transform: translateY(-3px);
}
</style>
