import { defineStore } from 'pinia'

type Store = {
  dataset: unknown[] | undefined
  name: string | undefined
}

export enum DatasetActions {
  SET_DATASET = 'set_dataset',
  SET_NAME = 'set_name',
  CLEAR_DATASET = 'clear_dataset',
}

type Action = {
  [DatasetActions.SET_DATASET]: (v: unknown[] | undefined) => void
  [DatasetActions.SET_NAME]: (v: string | undefined) => void
  [DatasetActions.CLEAR_DATASET]: () => void
}

export const useDatasetStore = defineStore<string, Store, {}, Action>({
  id: 'selected_dataset',
  state: () => ({
    dataset: undefined,
    name: undefined,
  }),
  actions: {
    [DatasetActions.SET_DATASET](v: any) {
      this.dataset = v
    },
    [DatasetActions.SET_NAME](v: any) {
      this.name = v
    },
    [DatasetActions.CLEAR_DATASET]() {
      ;(this.name = undefined), (this.dataset = undefined)
    },
  },
})
