<script setup lang="ts">
import WelcomeVue from "@/components/icons/Welcome.vue";
import UploadDatasetVue from "@/components/UploadDataset.vue";
</script>

<template>
  <main>
    <div
      class="flex flex-col gap-8 w-full items-center justify-center min-h-screen"
    >
      <WelcomeVue class="w-[250px] h-fit" />

      <div class="flex flex-col items-center gap-2">
        <div class="text-emerald-600 text-2xl font-semibold">
          Welcome, SQL Starter!
        </div>

        <div class="text-center mb-3">
          Start everythings up by upload your dataset.
        </div>

        <UploadDatasetVue />

        <div class="text-center text-sm text-black/40 mt-3 italic">
          <div>Dataset Size Limit: 150MB</div>
          <div>Supported Dataset Types: CSV, XLS, XLSX</div>
        </div>
      </div>
    </div>
  </main>
</template>
