<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card elevation="2" class="pa-4">
          <v-card-title class="text-center">Audio Transcription</v-card-title>
          
          <v-file-upload
            v-model="selectedFile"
            accept="audio/*"
            outlined
            density="comfortable"
            variant="outlined"
            class="mt-4"
            hide-details
          ></v-file-upload>
          <v-btn
            color="primary"
            class="mt-3"
            block
            @click="transcribeAudio"
            :disabled="!selectedFile"
          >
            Transcribe Audio
          </v-btn>
          <v-divider class="my-4"></v-divider>
          
          <v-card-subtitle class="pb-0">Transcribed Text</v-card-subtitle>
          <v-card-text class="pt-2">
            <div v-if="transcribedText" class="text-body-1 pa-2 rounded bg-grey-lighten-4">{{ transcribedText }}</div>
            <div v-else class="text-caption text-grey text-center pa-4">No transcribed text available</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { ref } from 'vue';

  const transcribedText = ref('');
  transcribedText.value = 'Transcribed text will beaa displayed here.';

</script>
