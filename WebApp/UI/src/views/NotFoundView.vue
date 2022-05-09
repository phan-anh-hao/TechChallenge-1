<script lang="ts" setup>
import NotfoundVue from '@/components/icons/Notfound.vue'
import { useRouter } from 'vue-router'

const { push } = useRouter()
</script>

<template>
  <main class="min-h-screen grid place-content-center gap-2">
    <NotfoundVue class="w-[250px] h-fit" />

    <div
      class="uppercase text-center text-2xl text-emerald-600 font-semibold mt-4"
    >
      Page not found
    </div>
    <div class="-mt-2">We are truly sorry for such inconvenient!</div>

    <button
      class="px-6 py-2 text-white bg-emerald-600 w-fit mx-auto rounded-md mt-3"
      @click="push('/')"
    >
      <span class="fa fa-home mr-2" />Home
    </button>
  </main>
</template>
