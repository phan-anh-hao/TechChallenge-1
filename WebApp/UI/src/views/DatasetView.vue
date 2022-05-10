<script lang="ts" setup>
import QuerySettingsVue from '@/components/QuerySettings.vue'
import { ref } from 'vue'
import SqlResultVue from '@/components/SqlResult.vue'
import axios from 'axios'

const settingRef = ref<InstanceType<typeof QuerySettingsVue> | null>(null)

const query = ref('')
const sql = ref('')

const handleSubmit = async (e: Event) => {
  e.preventDefault()

  const version = settingRef.value?.model_version || 'baseline'
  const queries = settingRef.value?.queries || {}

  const db_schema = Object.entries(queries).map(
    ([key, value]) => `${key} : ${value}`,
  )

  const result = await axios.post<{ data: { sql: string }[] }>(
    `${import.meta.env.VITE_API}/gpt`,
    {
      db_schema,
      question: query.value,
      settings: {
        model_ver: version,
      },
    },
  )

  sql.value = result.data.data.at(0)?.sql || ''
}
</script>

<template>
  <div class="grid grid-cols-[3fr,7fr] min-h-screen px-12 py-[100px] gap-8">
    <QuerySettingsVue ref="settingRef" />
    <div>
      <div class="bg-gray-300 p-4 rounded-md min-h-[120px] mb-6">
        <form @submit="handleSubmit" class="flex gap-2">
          <input
            placeholder="Place you query here..."
            type="text"
            v-model="query"
            class="w-full rounded-md outline-none border-0"
          />

          <button
            class="w-12 aspect-square border border-emerald-600 text-emerald-600 hover:bg-emerald-600 hover:text-white rounded-md"
          >
            <span class="fa fa-check" />
          </button>
        </form>

        <div class="mt-2 px-3 font-medium text-lg text-white">
          <span class="fa fa-caret-right mr-2" />{{ sql }}
        </div>
      </div>

      <SqlResultVue :sql="sql.replace('TABLE', 'tech_challenge')" />
    </div>
  </div>
</template>
