<script lang="ts" setup>
import { useDatasetStore } from '@/stores/dataset'
import { computed } from '@vue/reactivity'
import { Table, type TableColumnsType } from 'ant-design-vue'
import { onMounted, onUnmounted, watch } from 'vue'
import initSQL, {
  type QueryExecResult,
  type SqlJsStatic,
  Database,
} from 'sql.js'
import { ref } from 'vue'
import { generate_table_statement } from '@/libs/generate_table_statement'
import { useToast } from 'vue-toastification'

const props = defineProps({
  sql: {
    type: String,
  },
})

const store = useDatasetStore()
const toast = useToast()

const sql = ref<SqlJsStatic>()
const db = ref<Database>()

const dataSource = ref<unknown[]>(store.dataset || [])

watch([store.dataset], ([dataset]) => {
  dataSource.value = dataset || []
})

const columns = computed<TableColumnsType>(() =>
  Object.keys((dataSource.value[0] || {}) as object)
    .filter((key) => !!key)
    .map((key) => ({
      dataIndex: key,
      title: key.toLocaleLowerCase().replace(' ', '_'),
      ellipsis: true,
    })),
)

watch(
  () => props.sql,
  (sql) => {
    if (!db.value) return
    let res: QueryExecResult[] = []
    try {
      res = db.value.exec(sql || 'SELECT * from tech_challenge;')
      console.log(res, sql)
    } catch (e) {
      console.error(e)
      toast.error('Query executed failed: ' + (e as any).message)
      return
    }

    const parsed = res[0]?.values.map((value) =>
      value.reduce(
        (obj, v, index) => ({ ...obj, [res[0].columns[index]]: v }),
        {},
      ),
    )

    dataSource.value = parsed || []
  },
)

onMounted(async () => {
  sql.value = await initSQL({
    locateFile: () => `/sql-wasm.wasm`,
  })

  db.value?.close()
  db.value = new sql.value.Database()
  const statement = generate_table_statement(
    store.dataset![0] as object,
    store.dataset as object[],
  )

  try {
    db.value.run(statement)
    toast.success('Insert data from dataset succeeded')
  } catch (e) {
    console.error(e)
    toast.error(`Database Error: ${(e as any).message}`)
  }
})

onUnmounted(() => {
  db.value?.close()
})
</script>

<template>
  <div class="border border-emerald-600 rounded-md p-4 h-fit">
    <div class="text-[17px]m mb-4">
      <div v-if="!props.sql">Initial Dataset</div>
      <div v-else>Query Result</div>
    </div>

    <Table
      :data-source="dataSource"
      :columns="columns"
      :bordered="true"
      :scroll="{ y: 225 }"
      :pagination="{
        pageSize: 10,
        showLessItems: true,
        showSizeChanger: false,
      }"
    >
    </Table>
  </div>
</template>
