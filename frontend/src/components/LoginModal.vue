<template>
    <div v-if="modelValue" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
        <div class="bg-zinc-50 w-full max-w-2xl border-2 border-zinc-600 relative shadow-[0_0_50px_rgba(0,0,0,0.5)]"
            style="clip-path: polygon(0 0, 100% 0, 100% 95%, 95% 100%, 0 100%)">
            <div class="bg-zinc-900 text-white px-6 py-3 flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <i data-lucide="terminal" class="w-4 h-4 text-yellow-400"></i>
                    <span class="font-mono font-bold tracking-widest uppercase">IDENTITY VERIFICATION</span>
                </div>
                <button @click="close" class="hover:text-yellow-400 transition-colors"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div class="p-8">
                <form @submit.prevent="isRegistering ? register() : login()" class="space-y-6">
                    <div class="text-center mb-8">
                        <div class="w-16 h-16 bg-zinc-100 rounded-full mx-auto flex items-center justify-center mb-4 border-2 border-zinc-900">
                            <i data-lucide="lock" class="w-6 h-6 text-zinc-400"></i>
                        </div>
                        <p class="text-sm font-bold text-zinc-500 tracking-widest">PLEASE ENTER CREDENTIALS</p>
                    </div>
                    
                    <div class="space-y-2">
                        <label class="text-xs font-bold text-zinc-400 uppercase">Username</label>
                        <input v-model="authForm.username" class="w-full bg-zinc-100 border-2 border-zinc-200 p-3 font-mono text-xl focus:border-yellow-400 focus:outline-none transition-colors" placeholder="DR.NAME">
                    </div>
                    <div class="space-y-2">
                        <label class="text-xs font-bold text-zinc-400 uppercase">Password</label>
                        <input type="password" v-model="authForm.password" class="w-full bg-zinc-100 border-2 border-zinc-200 p-3 font-mono text-xl focus:border-yellow-400 focus:outline-none transition-colors" placeholder="******">
                    </div>

                    <div class="flex justify-between items-center pt-4">
                        <a @click="isRegistering = !isRegistering" class="text-xs font-bold text-zinc-500 cursor-pointer hover:text-black underline">
                            {{ isRegistering ? 'Switch to Login' : 'Request New Access' }}
                        </a>
                        <button type="submit" class="relative px-6 py-3 font-bold uppercase tracking-widest text-sm transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-zinc-900 text-white border-zinc-900 hover:bg-zinc-800" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                            {{ isRegistering ? 'REGISTER' : 'ACCESS TERMINAL' }}
                        </button>
                    </div>
                </form>
            </div>
            <div class="absolute bottom-0 right-0 w-4 h-4 bg-yellow-400"></div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onUpdated, nextTick } from 'vue'
import axios from 'axios'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue', 'login-success'])

const isRegistering = ref(false)
const authForm = reactive({ username: '', password: '' })

const close = () => emit('update:modelValue', false)

const login = async () => {
  try {
    const formData = new FormData()
    formData.append('username', authForm.username)
    formData.append('password', authForm.password)
    const response = await axios.post('/api/token', formData)
    emit('login-success', response.data.access_token)
    close()
    authForm.username = ''
    authForm.password = ''
  } catch (error) {
    alert('Login failed: ' + (error.response?.data?.detail || error.message))
  }
}

const register = async () => {
  try {
    await axios.post('/api/register', authForm)
    alert('Registration successful! Please login.')
    isRegistering.value = false
  } catch (error) {
    alert('Registration failed: ' + (error.response?.data?.detail || error.message))
  }
}

// Ensure icons render when modal opens
onUpdated(() => {
    if (props.modelValue) {
        nextTick(() => {
            if (window.lucide) window.lucide.createIcons()
        })
    }
})
</script>
