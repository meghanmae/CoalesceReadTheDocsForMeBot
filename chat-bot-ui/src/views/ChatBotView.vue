<template>
  <v-container align="center">
    <!-- Chat History -->
    <MessageCard :chatMessage="chatMessage" v-for="(chatMessage, i) in chatHistory" :key="i" />

    <!-- Used to load response & show a typing animation -->
    <MessageCard
      v-if="animatedBotMessage.content || thinking"
      :chatMessage="animatedBotMessage"
      id="animated-block"
    />
  </v-container>

  <v-sheet color="transparent" height="170px" />
  <v-card class="message-box mt-10">
    <v-text-field
      hide-details
      @keyup.enter="send"
      v-model="question"
      @click:append-inner="send"
      append-inner-icon="mdi-send"
      placeholder="Ask a question..."
    />
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MessageCard from '@/components/MessageCard.vue'
import type { ChatMessage } from '@/scripts/ChatMessage'
import { useAxios } from '@/scripts/useAxios'

const thinking = ref<boolean>(false)
const question = ref<string>('')
const chatHistory = ref<ChatMessage[]>([])

const typingInterval = ref<any>(null)
const animatedBotMessage = ref<ChatMessage>({
  role: 'assistant',
  content: ''
})

// Auto scroll & Animations
const shouldAutoScroll = ref<boolean>(true)

window.onscroll = function () {
  shouldAutoScroll.value = false
}

function autoScroll() {
  if (shouldAutoScroll.value) {
    // Always scroll the user to the bottom of the screen while typing
    document.getElementById('animated-block')?.scrollIntoView()
  }
}

function animate(text: string, delay: number) {
  let currentIndex = 0
  shouldAutoScroll.value = true

  typingInterval.value = setInterval(() => {
    if (currentIndex === text.length) {      
      clearInterval(typingInterval.value)

      // Save response to chat history & clear animation block
      animatedBotMessage.value.content = '';
      chatHistory.value.push({
        role: 'assistant',
        content: text
      })
    } else {
      animatedBotMessage.value.content += text[currentIndex]
      currentIndex++
    }
    autoScroll()
  }, delay)
}

// API Calls
const { sendQuestionAsync } = useAxios()

async function send() {
  if (!question.value) return

  thinking.value = true

  // Ask question & save question to chat history
  const questionToAsk: ChatMessage = {
    role: 'user',
    content: question.value
  }
  question.value = ''
  chatHistory.value.push(questionToAsk)

  const response = await sendQuestionAsync(questionToAsk.content, chatHistory.value)

  thinking.value = false

  // Animate the response & then clear the animation
  clearInterval(typingInterval.value)
  animate(response, 10)
}
</script>

<style scoped>
.message-box {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 1000px;
}
</style>
