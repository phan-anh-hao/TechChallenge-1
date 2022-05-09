<script lang="ts" setup>
import { useDatasetStore } from '@/stores/dataset'
import { computed } from '@vue/reactivity'
import { onUnmounted, ref, watch } from 'vue'

const store = useDatasetStore()
const model_version = ref<string>('baseline')

const keys = computed(() => {
  return Object.keys(store.dataset![0] as object).filter((key) => !!key)
})

const selectedQueries = ref<string[]>([])
const queries = ref<Record<string, string>>({})

const stopWatchQueries = watch(selectedQueries, (keys) => {
  queries.value = keys.reduce((res, key) => {
    let value: any
    try {
      value = JSON.parse((store.dataset![0] as Record<string, any>)[key])
    } catch (e) {
      value = ''
    }

    return {
      ...res,

      [key.replace(' ', '_').toLocaleLowerCase()]: typeof value,
    }
  }, {})
})

const handleQuerySelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.checked) {
    selectedQueries.value = [
      ...new Set([...selectedQueries.value, target.name]),
    ]
  }

  if (!target.checked) {
    selectedQueries.value = selectedQueries.value.filter(
      (query) => query !== target.name,
    )
  }
}

defineExpose({
  model_version,
  queries,
})

onUnmounted(() => {
  stopWatchQueries()
})
</script>

<template>
  <div
    class="flex flex-col items-center py-8 px-6 border-[1.7px] border-dashed border-emerald-600 rounded-md h-fit"
  >
    <div class="p-2 px-4 bg-emerald-600 text-white rounded-md self-start ml-4">
      <span class="fa fa-database mr-2" />
      {{ store.name }}
    </div>

    <div class="w-full mt-8 px-4">
      <div class="mb-4">
        <label for="model_version" class="select-none">Model Version:</label>

        <select
          v-model="model_version"
          id="model_version"
          class="w-full rounded-md mt-2"
        >
          <option value="baseline">Baseline</option>
        </select>
      </div>

      <div>
        <label class="select-none"> Query On:</label>
        <div
          class="grid grid-cols-[repeat(auto-fit,minmax(150px,150px))] gap-2 mt-2"
        >
          <div
            v-for="props in keys"
            :key="props"
            class="flex gap-2 items-center"
          >
            <input
              class="translate-y-[2px] text-emerald-600 rounded-md"
              type="checkbox"
              :checked="selectedQueries.some((query) => query === props)"
              @change="handleQuerySelect"
              :name="props"
              :id="props"
            />
            <label :for="props" class="select-none">{{
              props.toLocaleLowerCase().replace(' ', '_')
            }}</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
