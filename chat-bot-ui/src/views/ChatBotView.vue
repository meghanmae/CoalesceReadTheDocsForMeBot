<template>
  <v-container align="center">
    <MessageCard :message="message" v-for="(message, i) in messages" :key="i" />

    <MessageCard id="animated-block" :message="animatedMessage" v-if="animatedMessage.message || thinking" />
  </v-container>

  <v-sheet color="transparent" height="170px" />
  <v-card class="message-box mt-10">
    <v-text-field hide-details @keyup.enter="send" v-model="question" @click:append-inner="send"
      append-inner-icon="mdi-send" placeholder="Ask a question..." />
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MessageCard from '@/components/MessageCard.vue'
import type { Message } from '@/scripts/Message'
import axios from 'axios'

const thinking = ref(false)
const question = ref('')
const messages = ref<Message[]>([])
const history = ref([])
const animatedMessage = ref<Message>({
  message: '',
  profileIcon: 'mdi-robot-excited',
  color: 'botMessage'
})
const currentMessage = ref('')
const shouldAutoScroll = ref(true)
const typingInterval = ref<any>(null)

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
    } else {
      animatedMessage.value.message += text[currentIndex]
      currentIndex++
    }

    autoScroll()
  }, delay)
}

function sendQuestion() {
  messages.value.push({
    message: question.value,
    profileIcon: 'mdi-account',
    color: 'userMesssage'
  })

  const payload = {
    message: question.value,
    chat_history: history.value
  };

  const customHeaders = {
    'Content-Type': 'application/json',
  };

  const postUrl = 'http://127.0.0.1:5000/chat';

  question.value = ''
  thinking.value = true
  axios.post(postUrl, payload, { headers: customHeaders })
    .then(response => {

      history.value = response.data.chat_history
      currentMessage.value = history.value[history.value.length-1][1];
      thinking.value = false;

      animate(currentMessage.value, 30)
    })
    .catch(error => {
      console.error('Error:', error);
      // TODO: Handle the error
    });
}

async function send() {
  if (!question.value) return

  if (currentMessage.value) {
    messages.value.push({
      message: currentMessage.value,
      profileIcon: 'mdi-robot-excited',
      color: 'botMessage'
    })
    animatedMessage.value.message = ''
    currentMessage.value = ''
    clearInterval(typingInterval.value)
  }

  await sendQuestion()
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
