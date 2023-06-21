<template>
    <div class="text-center">
        <v-btn
            :disabled="dialog"
            :loading="dialog"
            color="purple-darken-2"
            @click="dialog = true"
        > Upload </v-btn>
        <v-dialog
            v-model="dialog"
            :scrim="false"
            persistent
            width="auto"
        >
            <v-card color="white">
                <v-card-text>
                    analyzing...(Please wait!)
                    <v-progress-linear
                        indeterminate
                        color="black"
                        class="mb-0"
                    ></v-progress-linear>
                </v-card-text>
            </v-card>
        </v-dialog>
    </div>
</template>

<script setup>
    import { ref, watch } from 'vue'

    const dialog = ref(false)
    watch(dialog, val => {
        if (!val) return
        setTimeout(() => (dialog.value = false), 4000)
    })
</script>

<script>
    export default {
        data () {
            return {
                dialog: false,
            }
        },

        watch: {
            dialog (val) {
                if (!val) return

                setTimeout(() => (this.dialog = false), 4000)
            },
        },
    }
</script>