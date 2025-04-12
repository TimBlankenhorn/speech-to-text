<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card elevation="2" class="pa-4">
          <v-card-title class="text-center">Audio Transcription</v-card-title>
          
          <v-file-upload
            v-model="selectedFile"
            accept=".wav"
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
          
          <v-card-subtitle class="pb-0">Transcribed Text 
            <v-chip v-if="transcriptionSource" 
                   size="small" 
                   class="ml-2" 
                   variant="flat"
                   :color="transcriptionSource === 'database' ? 'primary' : 'green'">
              {{ transcriptionSource }}
            </v-chip>
          </v-card-subtitle>
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
  const selectedFile = ref(null);
  const apiUrl = import.meta.env.VITE_API_URL;
  const transcriptionSource = ref('')

  async function transcribeAudio(){
    transcriptionSource.value = ""
    console.log(selectedFile.value.name);
    if (!selectedFile.value) return;

    const formData = new FormData();
    formData.append('audio_file', selectedFile.value);

    // Show loading state
    transcribedText.value = 'Transcribing...';

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }
      
      const data = await response.json();
      console.log(data)
      transcribedText.value = data.content || 'No transcription returned';
      transcriptionSource.value = data.origin || ''
    } catch (error) {
      console.error('Error during transcription:', error);
      transcribedText.value = 'Error during transcription. Please try again.';
    }
  }
  
</script>
