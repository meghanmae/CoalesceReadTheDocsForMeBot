<template>
  <v-app>
    <DisclaimerDialog v-model="dialog" />

    <span class="bg"></span>
    <v-app-bar :elevation="3">
      <template v-slot>
        <v-app-bar-title>
          <RouterLink to="/">
            <v-icon icon="mdi-robot-excited" color="primary" class="mb-2 mr-1" />
            <i>Unoffical</i> MeadowWood HOA Chat Bot
          </RouterLink>
        </v-app-bar-title>
        <v-spacer></v-spacer>
        <v-btn size="large" color="primary" icon="mdi-information" @click="dialog=true" />
      </template>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import DisclaimerDialog from '@/components/DisclaimerDialog.vue'

const dialog = ref(false)

dialog.value = true;
</script>
