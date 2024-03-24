<template>
  <v-card align="left" class="my-5" max-width="1000" :color="userType.cardColor" variant="tonal">
    <v-row dense class="pa-5" align="center">
      <v-col cols="auto">
        <v-avatar size="large" :color="userType.iconColor">
          <v-icon size="x-large" :icon="userType.icon" />
        </v-avatar>
      </v-col>
      <v-col>
        <v-card-text v-if="chatMessage.content">
          <div class="text-white" v-html="parsedMessage"></div>
        </v-card-text>
        <v-progress-circular v-else color="primary" size="x-small" class="ml-5" indeterminate />
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import type { ChatMessage } from '@/scripts/ChatMessage'
import { computed } from 'vue'
import { parse } from 'marked'
import sanitizeHtml from 'sanitize-html'

const props = defineProps<{
  chatMessage: ChatMessage
}>()

const parsedMessage = computed(() => {
  const html: string = parse(props.chatMessage.content).toString()

  const regex = /<a href="([^"]+)">/g;
  const replacement = '<a href="$1" target="_blank">'
  const resultString = html.replace(regex, replacement)

  return sanitizeHtml(resultString)
})

const userType = computed(() => {
  if (props.chatMessage.role === 'assistant') {
    return {
      icon: 'mdi-robot-excited',
      iconColor: 'primary',
      cardColor: 'botMessage'
    }
  }
  return {
    icon: 'mdi-account',
    iconColor: 'secondary',
    cardColor: 'userMessage'
  }
})
</script>

<style scoped>
/* Ensure that lists within the rendered HTML have indents */
.html-content ul,
.html-content ol {
  padding-left: 20px;
  margin-left: 20px;
}
.html-content li {
  margin-bottom: 4px; /* Adjust spacing between list items if needed */
}
</style>
