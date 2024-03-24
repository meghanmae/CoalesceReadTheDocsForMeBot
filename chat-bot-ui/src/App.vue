<template>
  <v-app>
    <span class="bg"></span>
    <v-app-bar :elevation="3">
      <template v-slot>
        <v-app-bar-title>
          <h3>
            <v-icon icon="mdi-robot-excited" color="primary" class="mb-2 mr-1" />
            Coalesce Read the Docs <i>For Me</i>
          </h3>
        </v-app-bar-title>
      </template>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup lang="ts" />
