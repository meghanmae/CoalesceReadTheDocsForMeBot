import type { ChatMessage } from './ChatMessage'
import axios from 'axios'

const postUrl = 'http://127.0.0.1:5000/chat';

async function sendQuestionAsync(question: string, chatHistory: ChatMessage[]): Promise<string> {
  const payload = {
    message: question,
    chat_history: chatHistory
  }

  const customHeaders = {
    'Content-Type': 'application/json',
  };
  
  const response = await axios.post(postUrl, payload, { headers: customHeaders });
  return response.data;
}

export function useAxios() {
  return {
    sendQuestionAsync
  }
}
