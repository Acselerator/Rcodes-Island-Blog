<template>
    <div class="max-w-4xl mx-auto animate-fade-in">
        <!-- 返回栏 -->
        <div class="flex justify-between items-center mb-6">
            <button @click="$emit('back')" class="flex items-center gap-2 text-sm font-bold text-zinc-500 hover:text-black transition-colors uppercase tracking-widest">
                <i data-lucide="arrow-left" class="w-4 h-4"></i> Return to Database
            </button>
            
            <div class="flex gap-2" v-if="user && user.id === post.owner_id">
                <button @click="$emit('edit')" class="relative px-4 py-2 font-bold uppercase tracking-widest text-xs transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-blue-500 text-white border-blue-500 hover:bg-blue-600 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                    <i data-lucide="edit" class="w-4 h-4"></i> Edit
                </button>
                <button @click="$emit('delete')" class="relative px-4 py-2 font-bold uppercase tracking-widest text-xs transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-red-500 text-white border-red-500 hover:bg-red-600 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                    <i data-lucide="trash-2" class="w-4 h-4"></i> Delete
                </button>
            </div>
        </div>

        <!-- 档案主体 -->
        <div class="bg-white border-2 border-zinc-900 shadow-[12px_12px_0_0_#18181b] relative overflow-hidden">
            <!-- 顶部机密条 -->
            <div class="bg-zinc-900 text-white px-8 py-2 flex justify-between items-center">
                    <span class="font-mono text-xs tracking-[0.2em] text-yellow-500">/// CONFIDENTIAL RECORD ///</span>
                    <span class="font-mono text-xs text-zinc-500">ID: {{ post.id }}</span>
            </div>

            <div class="p-8 md:p-12 relative z-10">
                <!-- 头部元数据 -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-8 mb-12 border-b-2 border-zinc-100 pb-8">
                    <div class="md:col-span-8">
                        <div class="flex gap-3 mb-4">
                            <span class="bg-yellow-400 text-black px-2 py-0.5 text-xs font-bold uppercase tracking-wider">{{ post.category || 'LOG' }}</span>
                            <span class="bg-zinc-100 text-zinc-500 px-2 py-0.5 text-xs font-bold uppercase tracking-wider font-mono">{{ post.created_at || `${post.year}-${post.date}` }}</span>
                        </div>
                        <h1 class="text-4xl md:text-5xl font-black text-zinc-900 mb-2 leading-tight tracking-tight">{{ post.title }}</h1>
                        <div class="flex items-center gap-4 mt-4">
                            <div class="h-1 w-24 bg-yellow-400"></div>
                            <span class="text-xs font-bold text-zinc-400 uppercase">AUTHOR: {{ post.owner ? post.owner.username : 'UNKNOWN' }}</span>
                        </div>
                    </div>
                    <div class="md:col-span-4 flex flex-col justify-end items-start md:items-end gap-4">
                        <div class="text-right">
                            <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest mb-1">Authorization</div>
                            <div class="text-sm font-bold">LEVEL 03</div>
                        </div>
                        <div class="text-right">
                                <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest mb-1">Tags</div>
                                <div class="flex flex-wrap justify-end gap-1">
                                <span 
                                    v-for="tag in (post.tags ? post.tags.split(',') : [])" 
                                    :key="tag" 
                                    @click="$emit('search-tag', tag)"
                                    class="text-[10px] border border-zinc-300 px-1 text-zinc-500 uppercase cursor-pointer hover:bg-zinc-900 hover:text-white hover:border-zinc-900 transition-colors"
                                >
                                    {{ tag }}
                                </span>
                                </div>
                        </div>
                        <!-- 互动数据 -->
                        <div class="flex gap-4">
                            <div class="text-center">
                                <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest">VIEWS</div>
                                <div class="text-xl font-black font-mono flex items-center gap-1 justify-center">
                                    <i data-lucide="eye" class="w-4 h-4"></i> {{ post.views || 0 }}
                                </div>
                            </div>
                            <button @click="$emit('like')" :class="['text-center group transition-colors cursor-pointer', post.is_liked ? 'text-yellow-500' : 'hover:text-yellow-500']">
                                <div :class="['text-[10px] uppercase font-bold tracking-widest', post.is_liked ? 'text-yellow-500' : 'text-zinc-400 group-hover:text-yellow-500']">LIKES</div>
                                <div class="text-xl font-black font-mono flex items-center gap-1 justify-center">
                                    <i data-lucide="thumbs-up" :class="['w-4 h-4', post.is_liked ? 'fill-yellow-500' : '']"></i> {{ post.likes || 0 }}
                                </div>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 正文内容 -->
                <div class="prose prose-zinc max-w-none">
                    <div class="font-serif text-lg leading-loose text-zinc-800" v-html="post.content"></div>
                </div>
                
                <!-- 评论区 -->
                <div class="mt-12 pt-8 border-t border-dashed border-zinc-300">
                    <h3 class="text-xl font-black uppercase mb-6">Comments</h3>
                    
                    <div class="space-y-4 mb-8">
                        <div v-if="!post.comments || post.comments.length === 0" class="text-zinc-400 italic">No comments yet.</div>
                        <div v-else v-for="comment in post.comments" :key="comment.id" class="bg-zinc-50 p-4 border border-zinc-200">
                            <div class="flex justify-between items-start mb-2">
                                <span class="font-bold text-sm">{{ comment.owner.username }}</span>
                                <button v-if="user && comment.owner_id === user.id" @click="$emit('delete-comment', comment.id)" class="text-xs text-red-500 hover:underline">DELETE</button>
                            </div>
                            <p class="text-zinc-700">{{ comment.content }}</p>
                        </div>
                    </div>

                    <div v-if="user" class="flex gap-4">
                        <input v-model="newComment" class="flex-1 bg-zinc-100 border-2 border-zinc-200 p-3 focus:border-yellow-400 outline-none" placeholder="Add a comment..." @keyup.enter="handleAddComment">
                        <button @click="handleAddComment" class="bg-zinc-900 text-white px-6 font-bold uppercase hover:bg-zinc-700">Post</button>
                    </div>
                </div>

                <!-- 底部签名区 -->
                <div class="mt-16 pt-8 border-t border-dashed border-zinc-300 flex justify-between items-end opacity-50">
                    <div class="font-mono text-xs text-zinc-400">
                        DATA INTEGRITY CHECK: PASS<br>
                        LAST MODIFIED: {{ new Date().toLocaleDateString() }}
                    </div>
                    <div class="w-32">
                        <div class="text-[10px] text-zinc-400 mb-4">APPROVED BY:</div>
                        <div class="font-handwriting text-2xl rotate-[-5deg] text-zinc-800 font-black">Kal'tsit</div>
                    </div>
                </div>
            </div>
            
            <!-- 背景水印 -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[15rem] font-black text-zinc-50 opacity-50 pointer-events-none select-none z-0 rotate-12">
                RHODES
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUpdated, nextTick } from 'vue'

const props = defineProps(['post', 'user'])
const emit = defineEmits(['back', 'edit', 'delete', 'like', 'add-comment', 'delete-comment'])

const newComment = ref('')

const handleAddComment = () => {
    if (!newComment.value) return
    emit('add-comment', newComment.value)
    newComment.value = ''
}

const refreshIcons = () => {
  nextTick(() => {
    if (window.lucide) window.lucide.createIcons()
  })
}

onMounted(refreshIcons)
onUpdated(refreshIcons)
</script>
