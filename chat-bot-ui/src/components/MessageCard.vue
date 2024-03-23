<template>
  <v-card align="left" :color="message.color" class="my-5" max-width="1000">
    <v-row dense class="pa-5" align="center">
      <v-col cols="auto">
        <v-avatar color="primary" size="large">
          <v-icon size="x-large" :icon="message.profileIcon"></v-icon>
        </v-avatar>
      </v-col>
      <v-col>
        <v-card-text v-if="message.message">
          {{ message.message }}
        </v-card-text>
        <v-progress-circular color="primary" size="x-small" class="ml-5" v-else indeterminate />
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import type { Message } from '@/scripts/Message'

defineProps<{
  message: Message
}>()
</script>
