<template>
    <div class="max-w-6xl mx-auto animate-fade-in">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-black uppercase flex items-center gap-3">
                <i data-lucide="edit-3" class="w-6 h-6"></i>
                {{ isEditing ? 'Edit Record' : 'Create New Record' }}
            </h2>
            <button @click="$emit('cancel')" class="text-xs font-bold text-red-500 hover:text-red-700 uppercase tracking-widest">
                Cancel Operation
            </button>
        </div>

        <div class="bg-zinc-900 text-zinc-300 p-1 border-2 border-zinc-900 shadow-xl">
            <div class="border border-zinc-700 p-8 scanline relative">
                <!-- 装饰角标 -->
                <div class="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-yellow-500"></div>
                <div class="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-yellow-500"></div>
                <div class="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-yellow-500"></div>
                <div class="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-yellow-500"></div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <!-- 基础信息 -->
                    <div class="space-y-4 md:col-span-2">
                        <div class="space-y-1">
                            <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Record Title</label>
                            <input v-model="form.title" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 text-white font-bold outline-none transition-colors" placeholder="ENTER TITLE...">
                        </div>
                    </div>
                    
                    <!-- 分类与标签 -->
                    <div class="space-y-4 md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-1">
                            <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Category</label>
                            <div class="flex gap-2">
                                <button v-for="cat in ['LOG', 'REPORT', 'INTEL', 'NEWS']" 
                                    @click="form.category = cat"
                                    :class="['px-3 py-1 text-xs font-bold border transition-all', form.category === cat ? 'bg-yellow-400 text-black border-yellow-400' : 'border-zinc-600 text-zinc-500 hover:border-zinc-400']">
                                    {{ cat }}
                                </button>
                            </div>
                        </div>
                        <div class="space-y-1">
                            <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Tags (Separate by comma)</label>
                            <input v-model="form.tags" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 font-mono text-sm outline-none transition-colors" placeholder="e.g. URSUS, LORE">
                        </div>
                    </div>
                </div>

                <!-- 正文编辑 (Markdown Split View) -->
                <div class="space-y-2 mb-8">
                    <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest flex justify-between">
                        <span>Record Content (Markdown Supported)</span>
                        <span class="text-xs text-zinc-500">Drag & Drop images supported</span>
                    </label>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 h-[600px]">
                        <!-- Editor -->
                        <div class="relative h-full">
                            <textarea 
                                ref="editorRef"
                                v-model="form.content" 
                                @paste="handlePaste"
                                @drop.prevent="handleDrop"
                                class="w-full h-full bg-zinc-800 text-zinc-200 p-4 font-mono text-sm border-2 border-zinc-700 focus:border-yellow-400 outline-none resize-none"
                                placeholder="Write your markdown here..."
                            ></textarea>
                        </div>
                        <!-- Preview -->
                        <div class="h-full bg-white text-black p-4 border-2 border-zinc-700 overflow-y-auto prose prose-sm max-w-none">
                            <div v-html="compiledMarkdown"></div>
                        </div>
                    </div>
                </div>

                <!-- 底部操作栏 -->
                <div class="flex justify-end gap-4 border-t border-zinc-700 pt-6">
                    <button @click="save" class="relative px-6 py-3 font-bold uppercase tracking-widest text-sm transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-yellow-400 text-black border-yellow-400 hover:bg-yellow-300 hover:border-yellow-300 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                        <i data-lucide="save" class="w-4 h-4"></i>
                        TRANSMIT RECORD
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref, onMounted, onUpdated, nextTick, computed } from 'vue'
import { marked } from 'marked'
import axios from 'axios'

const props = defineProps(['post', 'isEditing', 'token'])
const emit = defineEmits(['cancel', 'save'])

const editorRef = ref(null)
const form = reactive({ title: '', content: '', category: 'LOG', tags: '' })

const compiledMarkdown = computed(() => {
    return marked(form.content || '')
})

onMounted(() => {
    if (props.isEditing && props.post) {
        form.title = props.post.title
        form.content = props.post.content
        form.category = props.post.category || 'LOG'
        form.tags = props.post.tags || ''
    }
    refreshIcons()
})

const refreshIcons = () => {
  nextTick(() => {
    if (window.lucide) window.lucide.createIcons()
  })
}

onUpdated(refreshIcons)

const uploadFile = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    try {
        const res = await axios.post('/api/upload', formData, {
            headers: { Authorization: `Bearer ${props.token}` }
        })
        return res.data.url
    } catch (e) {
        console.error('Image upload failed', e)
        alert('Image upload failed')
        return null
    }
}

const insertAtCursor = (text) => {
    const textarea = editorRef.value
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const before = form.content.substring(0, start)
    const after = form.content.substring(end)
    form.content = before + text + after
    nextTick(() => {
        textarea.selectionStart = textarea.selectionEnd = start + text.length
        textarea.focus()
    })
}

const handlePaste = async (e) => {
    const items = (e.clipboardData || e.originalEvent.clipboardData).items
    for (const item of items) {
        if (item.kind === 'file' && item.type.startsWith('image/')) {
            e.preventDefault()
            const file = item.getAsFile()
            const url = await uploadFile(file)
            if (url) {
                insertAtCursor(`![Image](${url})`)
            }
        }
    }
}

const handleDrop = async (e) => {
    const files = e.dataTransfer.files
    if (files.length > 0) {
        const file = files[0]
        if (file.type.startsWith('image/')) {
            const url = await uploadFile(file)
            if (url) {
                insertAtCursor(`![Image](${url})`)
            }
        }
    }
}

const save = () => {
    emit('save', { ...form })
}
</script>
