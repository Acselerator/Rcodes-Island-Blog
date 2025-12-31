<template>
    <div class="max-w-5xl mx-auto animate-fade-in">
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

                <!-- 正文编辑 -->
                <div class="space-y-2 mb-8">
                    <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest flex justify-between">
                        <span>Record Content</span>
                    </label>
                    <div class="bg-white text-black border-2 border-zinc-700">
                        <QuillEditor 
                            ref="quillEditorRef"
                            v-model:content="form.content" 
                            contentType="html" 
                            :options="quillOptions" 
                            theme="snow"
                            class="h-96" 
                        />
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
import { reactive, ref, onMounted, onUpdated, nextTick } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import axios from 'axios'

const props = defineProps(['post', 'isEditing', 'token'])
const emit = defineEmits(['cancel', 'save'])

const quillEditorRef = ref(null)
const form = reactive({ title: '', content: '', category: 'LOG', tags: '' })

onMounted(() => {
    if (props.isEditing && props.post) {
        form.title = props.post.title
        form.content = props.post.content
        form.category = props.post.category || 'LOG'
        form.tags = props.post.tags || ''
        
        // Manually set content for Quill if needed, though v-model should handle it
        if (quillEditorRef.value) {
            quillEditorRef.value.setHTML(props.post.content)
        }
    }
    refreshIcons()
})

const refreshIcons = () => {
  nextTick(() => {
    if (window.lucide) window.lucide.createIcons()
  })
}

onUpdated(refreshIcons)

const imageHandler = () => {
  const input = document.createElement('input')
  input.setAttribute('type', 'file')
  input.setAttribute('accept', 'image/*')
  input.click()
  input.onchange = async () => {
    const file = input.files[0]
    if (/^image\//.test(file.type)) {
      const formData = new FormData()
      formData.append('file', file)
      try {
        const res = await axios.post('/api/upload', formData, {
           headers: { Authorization: `Bearer ${props.token}` }
        })
        const url = res.data.url
        const quill = quillEditorRef.value.getQuill()
        const range = quill.getSelection(true)
        if (range) {
            quill.insertEmbed(range.index, 'image', url)
            quill.setSelection(range.index + 1)
        } else {
            const length = quill.getLength()
            quill.insertEmbed(length, 'image', url)
        }
      } catch (e) {
        console.error('Image upload failed', e)
        alert('Image upload failed')
      }
    } else {
      console.warn('You could only upload images.')
    }
  }
}

const quillOptions = {
  modules: {
    toolbar: {
      container: [
        ['bold', 'italic', 'underline', 'strike'],
        ['blockquote', 'code-block'],
        [{ 'header': 1 }, { 'header': 2 }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        [{ 'direction': 'rtl' }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'font': [] }],
        [{ 'align': [] }],
        ['clean'],
        ['link', 'image', 'video']
      ],
      handlers: {
        image: imageHandler
      }
    }
  },
  theme: 'snow'
}

const save = () => {
    emit('save', { ...form })
}
</script>
