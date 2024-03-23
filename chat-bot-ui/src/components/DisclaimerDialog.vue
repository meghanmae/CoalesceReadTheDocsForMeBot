<template>
<v-dialog v-model="showDocumentList" max-width="500">
    <v-card>
        <v-sheet color="primary">
            <v-card-title class="text-wrap">
                Documents used by this model
            </v-card-title>
        </v-sheet>

        <v-card-text>
            <ul>
                <li v-for="document in documents">
                    <a :href="document.link" target="_blank"> {{ document.title }} </a>
                </li>
            </ul>
        </v-card-text>

        <v-card-text>
            Links to these documents may be outdated, you should consider information found at <a href="https://meadowwoodhoa.com/" target="_blank"> www.MeadowWoodHoa.com </a> to be the soruce of truth.
        </v-card-text>

        <v-card-actions>
            <v-spacer />
            <v-btn color="primary" variant="elevated" @click="showDocumentList=false">
                Close
            </v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>

<v-dialog :model-value="modelValue"
    @update:model-value="close"
    max-width="800"
    transition="dialog-top-transition">
    <v-card>
        <v-sheet color="primary">
            <v-card-title class="text-wrap">
                Welcome to the <i>Unoffical</i> MeadowWood HOA Chat Bot
            </v-card-title>
        </v-sheet>

        <v-card-text>
            <h2><strong>FAQ</strong></h2>
            <ul>
                <template v-for="faq in faqs">
                    <li>
                        <strong>{{ faq.question }}</strong> 
                        <p v-html="faq.answer"></p>
                    </li>
                    <br />
                </template>
            </ul>

            <v-btn @click="showDocumentList = true" color="primary" class="mb-5">
                View Training Document List
            </v-btn>

            <br />
            <h2><strong>Disclaimers</strong></h2>
            <p>
                This chatbot may produce inaccurate or outdated information about people, places, or facts. Always refer to the <a href="https://meadowwoodhoa.com/" target="_blank"> MeadowWood Hoa </a> website as the source of truth.
            </p>
        </v-card-text>

        <v-divider />

        <v-card-actions>
            <v-spacer />
            <v-btn variant ="elevated" color="primary" @click="close">
                I Understand
            </v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
    modelValue: boolean; 
}>();

const showDocumentList = ref(false);

const emit = defineEmits<{
    (e: "update:modelValue", value: boolean): void;
}>();

function close(){
    emit("update:modelValue", false);
}

const faqs = [
    {
        question: "Unoffical?",
        answer: "Yes, unoffical. This is a home made project by a MWHOA member to more eaisly parse the bylaws, RCWs and various HOA documents."
    },
    {
        question: "What is this?",
        answer: "This website is a chat bot that uses natural language processing and <a href='https://platform.openai.com/docs/guides/gpt' target='_blank'>OpenAI's</a> API for the <a href='https://chat.openai.com/' target='_blank'>Chat GPT</a> engine to answer questions and interact with you in a conversational manor. It is capable of answering most questions you may have about the MeadowWood HOA bylaws and Washington RCWs regarding HOAs."
    },
    {
        question: "How up to date is this information?",
        answer: "The information used by this chat bot was last updated 07/21/2023."
    },
    {
        question: "How does it work?",
        answer: "You simply ask a question in provided textbox at the bottom of the screen and the bot should respond to you with an answer. Sometimes you may need to re-ask or re-phrase your question."
    },
    {
        question: "Can I view the source code?",
        answer: "Yes, I have the sourcecode, along with the relevant training documents, posted on my <a href='https://github.com/mmwoodfo/hoa-chat-bot' target='_blank'>GitHub</a>!"
    }
]

const documents = [
    {
        link: "https://app.leg.wa.gov/RCW/default.aspx?cite=64.38",
        title: "The Washington RCWs for HOAs"
    },
    {
        link: "http://meadowwoodhoa.com/wp-content/uploads/2021/11/MW-By-Laws-Revised-Oct-21.pdf",
        title: "Association By-Laws (Oct 2021)"
    },
    {
        link: "http://meadowwoodhoa.com/wp-content/uploads/2021/12/MW-Parking-Resolution-18-Dec-21-Signed.pdf",
        title: "HOA Parking Resolution"
    },
    {
        link: "https://www.libertylakewa.gov/DocumentCenter/View/4540/STREET-TREES-AND-SIDEWALK-MAINTENANCE-Updated-5-2-19?bidId=",
        title: "Tree Trimming & Sidewalk Maint (City Ordinance)"
    },
    {
        link: "http://meadowwoodhoa.com/wp-content/uploads/2022/04/Rules-and-Regs-Revision-16-Feb-22.pdf",
        title: "Rules & Regulations"
    },
    {
        link: "https://robertsrules.org/robertsrules.pdf",
        title: "Roberts Rules of Order"
    },
]
</script>
