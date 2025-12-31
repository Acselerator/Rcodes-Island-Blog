<template>
  <div id="app" class="bg-[#f2f2f2] text-zinc-900 overflow-x-hidden selection:bg-yellow-400 selection:text-black min-h-screen font-sans">
    <!-- 背景层 -->
    <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        <div class="absolute top-[10%] -left-[5%] text-[20vw] font-black text-zinc-200/50 leading-none select-none tracking-tighter opacity-50" style="writing-mode: vertical-rl">
            RHODES
        </div>
        
        <!-- 立绘层 (仅在列表页显示) -->
        <transition enter-active-class="transition duration-1000 ease-out" enter-from-class="opacity-0 translate-x-20" enter-to-class="opacity-80 translate-x-0" leave-active-class="transition duration-500 ease-in" leave-from-class="opacity-80 translate-x-0" leave-to-class="opacity-0 translate-x-20">
            <div v-show="currentView === 'list'" class="absolute bottom-[-10%] right-[-12%] w-[110vh] h-[120vh] z-0 opacity-80 hidden lg:block">
               <img 
                src="/amiya_skin1.png" 
                alt="Operator Art"
                class="w-full h-full object-contain object-bottom mix-blend-multiply filter grayscale-[30%] contrast-125 drop-shadow-xl" 
                style="mask-image: linear-gradient(to bottom, black 80%, transparent 100%)"
              />
            </div>
        </transition>

        <!-- 几何装饰 -->
        <div class="absolute top-0 right-[20%] w-[1px] h-screen bg-zinc-300"></div>
        <div class="absolute bottom-10 right-10 w-32 h-32 bg-yellow-400 mix-blend-multiply opacity-50 z-0"></div>
    </div>

    <!-- 顶部导航 -->
    <header :class="['fixed top-0 left-0 w-full z-50 transition-all duration-300', scrolled ? 'py-2 bg-white/90 backdrop-blur-md border-b border-zinc-200' : 'py-6 bg-transparent']">
        <div class="w-full mx-auto px-6 flex justify-between items-center">
            <!-- Logo / Home Button -->
            <div @click="switchView('list')" class="flex items-center gap-4 cursor-pointer group">
                <div class="w-10 h-10 bg-black text-white flex items-center justify-center font-bold text-xl transition-transform group-hover:scale-110" style="clip-path: polygon(0 0, 100% 0, 100% 75%, 75% 100%, 0 100%)">
                    <span class="font-mono">R</span>
                </div>
                <div class="leading-none">
                    <h1 class="text-xl font-black tracking-tighter uppercase group-hover:text-zinc-600 transition-colors">Rcodes Island</h1>
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] font-bold tracking-[0.3em] text-zinc-500">TERMINAL SYSTEM</span>
                        <span v-if="user" class="text-[10px] bg-yellow-400 text-black px-1 font-bold">ADMIN</span>
                    </div>
                </div>
            </div>

            <!-- 面包屑 / 状态栏 -->
            <div class="hidden md:flex items-center gap-4">
                <div v-if="currentView !== 'list'" class="flex items-center gap-2 text-xs font-mono font-bold text-zinc-500 animate-pulse">
                    <i data-lucide="activity" class="w-4 h-4 text-yellow-500"></i>
                    <span>{{ currentView === 'detail' ? 'READING_MODE' : 'EDITING_MODE' }}</span>
                </div>
            </div>

            <!-- User Status -->
            <div class="flex items-center gap-4">
                <div class="text-right hidden sm:block">
                    <div class="text-xs font-bold text-zinc-900">
                        {{ user ? user.username : 'GUEST USER' }}
                    </div>
                    <div class="text-[10px] font-mono bg-zinc-200 px-1 inline-block">
                        {{ user ? 'CLEARANCE: LV.08' : 'CLEARANCE: LV.00' }}
                    </div>
                </div>
                
                <button v-if="user" @click="logout" class="p-2 border-2 border-zinc-900 bg-zinc-900 text-white hover:bg-red-600 hover:border-red-600 transition-colors" title="Logout">
                    <i data-lucide="unlock" class="w-5 h-5"></i>
                </button>
                <button v-else @click="isLoginOpen = true" class="p-2 border-2 border-zinc-900 hover:bg-yellow-400 transition-colors" title="Login">
                    <i data-lucide="lock" class="w-5 h-5"></i>
                </button>
            </div>
        </div>
    </header>

    <!-- 主内容容器 -->
    <main class="relative z-10 pt-32 pb-20 px-6 w-full mx-auto min-h-[80vh]">
        
        <!-- ================= VIEW: LIST (列表页) ================= -->
        <div v-if="currentView === 'list'" class="grid grid-cols-12 gap-8 animate-fade-in">
            <!-- 左侧面板 -->
            <aside class="col-span-12 lg:col-span-3 flex flex-col gap-8">
                <!-- Profile Card -->
                <div class="bg-white border-2 border-zinc-900 p-6 relative shadow-[8px_8px_0_0_rgba(0,0,0,0.1)] transition-transform hover:-translate-y-1">
                    <div :class="['absolute top-0 left-0 text-xs font-bold px-2 py-1 border-r-2 border-b-2 border-zinc-900', user ? 'bg-yellow-400' : 'bg-zinc-200']">
                        ID: {{ user ? 'PRTS-001' : 'GUEST-000' }}
                    </div>
                    <div class="mt-6 mb-4">
                        <div class="w-20 h-20 bg-zinc-100 border-2 border-zinc-900 rounded-full overflow-hidden flex items-center justify-center mb-4">
                            <i data-lucide="user" class="w-10 h-10 text-zinc-400"></i>
                        </div>
                        <h2 class="text-3xl font-black uppercase leading-none">
                            {{ user ? 'DOCTOR' : 'VISITOR' }}
                        </h2>
                        <p class="text-xs font-bold text-zinc-400 mt-1 tracking-widest">
                            {{ user ? 'NEURAL NETWORK ADMIN' : 'READ ONLY ACCESS' }}
                        </p>
                    </div>
                    <div class="h-[2px] w-full bg-zinc-900 mb-4"></div>
                    <p class="text-xs font-serif italic text-zinc-600 leading-relaxed">
                        "{{ user ? 'MAY I ENJOY MY LIFE and PRACTICE my art.' : 'Connection Established. Waiting for input.' }}"
                    </p>
                </div>
                
                <!-- 资源面板 -->
                <div class="bg-zinc-900 text-white p-6" style="clip-path: polygon(0 0, 100% 0, 100% 90%, 90% 100%, 0 100%)">
                    <div class="flex justify-between items-center mb-4 border-b border-zinc-700 pb-2">
                        <span class="text-xs font-bold text-yellow-400">SYSTEM STATUS</span>
                        <i data-lucide="activity" class="w-3.5 h-3.5 text-yellow-400"></i>
                    </div>
                    <div class="space-y-3 font-mono text-xs">
                        <div class="flex justify-between">
                            <span class="text-zinc-500">DB_CONNECTION</span>
                            <span class="text-green-500">ONLINE</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-zinc-500">RECORDS</span>
                            <span>{{ posts.length }} FILES</span>
                        </div>
                    </div>
                </div>

                <!-- Weekly Operations -->
                <div class="bg-white border-2 border-zinc-900 p-6 shadow-[8px_8px_0_0_rgba(0,0,0,0.1)] transition-transform hover:-translate-y-1">
                    <div class="text-[10px] font-bold text-zinc-500 mb-4 uppercase tracking-wider flex items-center justify-between">
                        <span>Weekly Operations</span>
                        <i data-lucide="refresh-cw" class="w-3 h-3 animate-spin-slow"></i>
                    </div>
                    <div class="space-y-3">
                        <div v-for="i in 3" :key="i" class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-yellow-400 rounded-full"></div>
                            <div class="h-2 flex-1 bg-zinc-200 rounded-full overflow-hidden">
                                <div class="h-full bg-zinc-400" :style="{ width: Math.random() * 100 + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>

            <!-- 中间文章流 -->
            <section class="col-span-12 lg:col-span-6 space-y-12">
                <div class="flex justify-between items-end border-b-4 border-zinc-900 pb-2 mb-8">
                    <div>
                        <div class="text-4xl md:text-6xl font-black text-zinc-900 leading-none tracking-tighter">
                            最新记录
                        </div>
                        <div class="text-sm font-mono font-bold text-zinc-500 tracking-widest uppercase mt-2">
                            RECENT LOGS
                        </div>
                    </div>
                    <button v-if="user" @click="openEditor(null)" class="mb-2 relative px-6 py-3 font-bold uppercase tracking-widest text-sm transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-yellow-400 text-black border-yellow-400 hover:bg-yellow-300 hover:border-yellow-300 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                        <i data-lucide="plus" class="w-4 h-4"></i> New Record
                    </button>
                </div>

                <div class="space-y-8">
                    <div v-if="loading" class="text-center py-20">Loading...</div>
                    <div v-else-if="posts.length === 0" class="text-center py-20 border-2 border-dashed border-zinc-300 text-zinc-400 font-mono">
                        NO RECORDS FOUND <br/> <span class="text-xs">System waiting for input...</span>
                    </div>
                    
                    <article 
                        v-else 
                        v-for="(post, index) in posts" 
                        :key="post.id" 
                        @click="openDetail(post)"
                        class="group relative bg-white border-2 border-transparent hover:border-zinc-900 transition-all duration-300 p-8 shadow-sm hover:shadow-[8px_8px_0_0_#000] cursor-pointer"
                    >
                        <!-- 装饰编号 -->
                        <div class="absolute top-0 right-4 text-9xl font-black text-zinc-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 select-none pointer-events-none -z-10">
                            {{ String(index + 1).padStart(2, '0') }}
                        </div>

                        <div class="flex gap-4 items-baseline mb-2">
                            <span class="text-xs font-black bg-black text-white px-2 py-1 uppercase">{{ post.category || 'LOG' }}</span>
                            <span class="text-sm font-mono font-bold text-zinc-400">{{ post.date }} / {{ post.year }}</span>
                        </div>

                        <h3 class="text-3xl font-bold mb-2 leading-tight group-hover:text-zinc-700 transition-colors">
                            {{ post.title }}
                        </h3>
                        
                        <div class="h-1 w-12 bg-yellow-400 mb-6 mt-4"></div>

                        <!-- 截断显示摘要 -->
                        <p class="text-zinc-600 leading-relaxed mb-6 font-medium line-clamp-3 whitespace-pre-line">{{ stripHtml(post.content) }}</p>

                        <div class="flex justify-between items-center">
                            <div class="flex gap-2">
                                <span v-for="tag in (post.tags ? post.tags.split(',') : [])" :key="tag" class="text-[10px] font-bold text-zinc-400 border border-zinc-200 px-2 py-1 rounded-full uppercase">
                                    #{{ tag }}
                                </span>
                            </div>
                            <div class="bg-yellow-400 text-black p-2 group-hover:bg-black group-hover:text-white transition-colors">
                                <i data-lucide="chevron-right" class="w-5 h-5"></i>
                            </div>
                        </div>
                    </article>
                </div>
            </section>
            
            <!-- 右侧装饰 -->
            <aside class="hidden lg:block col-span-3 relative">
                <!-- Empty to preserve layout -->
            </aside>
        </div>

        <!-- ================= VIEW: DETAIL (详情页) ================= -->
        <div v-else-if="currentView === 'detail' && activePost" class="max-w-4xl mx-auto animate-fade-in">
            <!-- 返回栏 -->
            <div class="flex justify-between items-center mb-6">
                <button @click="switchView('list')" class="flex items-center gap-2 text-sm font-bold text-zinc-500 hover:text-black transition-colors uppercase tracking-widest">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i> Return to Database
                </button>
                
                <div class="flex gap-2" v-if="user && user.id === activePost.owner_id">
                    <button @click="openEditor(activePost)" class="relative px-4 py-2 font-bold uppercase tracking-widest text-xs transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-blue-500 text-white border-blue-500 hover:bg-blue-600 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                        <i data-lucide="edit" class="w-4 h-4"></i> Edit
                    </button>
                    <button @click="deletePost(activePost.id)" class="relative px-4 py-2 font-bold uppercase tracking-widest text-xs transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-red-500 text-white border-red-500 hover:bg-red-600 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                        <i data-lucide="trash-2" class="w-4 h-4"></i> Delete
                    </button>
                </div>
            </div>

            <!-- 档案主体 -->
            <div class="bg-white border-2 border-zinc-900 shadow-[12px_12px_0_0_#18181b] relative overflow-hidden">
                <!-- 顶部机密条 -->
                <div class="bg-zinc-900 text-white px-8 py-2 flex justify-between items-center">
                     <span class="font-mono text-xs tracking-[0.2em] text-yellow-500">/// CONFIDENTIAL RECORD ///</span>
                     <span class="font-mono text-xs text-zinc-500">ID: {{ activePost.id }}</span>
                </div>

                <div class="p-8 md:p-12 relative z-10">
                    <!-- 头部元数据 -->
                    <div class="grid grid-cols-1 md:grid-cols-12 gap-8 mb-12 border-b-2 border-zinc-100 pb-8">
                        <div class="md:col-span-8">
                            <div class="flex gap-3 mb-4">
                                <span class="bg-yellow-400 text-black px-2 py-0.5 text-xs font-bold uppercase tracking-wider">{{ activePost.category || 'LOG' }}</span>
                                <span class="bg-zinc-100 text-zinc-500 px-2 py-0.5 text-xs font-bold uppercase tracking-wider font-mono">{{ activePost.date }} . {{ activePost.year }}</span>
                            </div>
                            <h1 class="text-4xl md:text-5xl font-black text-zinc-900 mb-2 leading-tight tracking-tight">{{ activePost.title }}</h1>
                            <div class="h-1 w-24 bg-yellow-400 mt-4"></div>
                        </div>
                        <div class="md:col-span-4 flex flex-col justify-end items-start md:items-end gap-2">
                            <div class="text-right">
                                <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest mb-1">Authorization</div>
                                <div class="text-sm font-bold">LEVEL 03</div>
                            </div>
                            <div class="text-right">
                                 <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest mb-1">Tags</div>
                                 <div class="flex flex-wrap justify-end gap-1">
                                    <span v-for="tag in (activePost.tags ? activePost.tags.split(',') : [])" :key="tag" class="text-[10px] border border-zinc-300 px-1 text-zinc-500 uppercase">{{ tag }}</span>
                                 </div>
                            </div>
                        </div>
                    </div>

                    <!-- 正文内容 -->
                    <div class="prose prose-zinc max-w-none">
                        <div class="font-serif text-lg leading-loose text-zinc-800" v-html="activePost.content"></div>
                    </div>
                    
                    <!-- 评论区 -->
                    <div class="mt-12 pt-8 border-t border-dashed border-zinc-300">
                        <h3 class="text-xl font-black uppercase mb-6">Comments</h3>
                        
                        <div class="space-y-4 mb-8">
                            <div v-if="!activePost.comments || activePost.comments.length === 0" class="text-zinc-400 italic">No comments yet.</div>
                            <div v-else v-for="comment in activePost.comments" :key="comment.id" class="bg-zinc-50 p-4 border border-zinc-200">
                                <div class="flex justify-between items-start mb-2">
                                    <span class="font-bold text-sm">{{ comment.owner.username }}</span>
                                    <button v-if="user && comment.owner_id === user.id" @click="deleteComment(activePost, comment.id)" class="text-xs text-red-500 hover:underline">DELETE</button>
                                </div>
                                <p class="text-zinc-700">{{ comment.content }}</p>
                            </div>
                        </div>

                        <div v-if="user" class="flex gap-4">
                            <input v-model="activePost.newComment" class="flex-1 bg-zinc-100 border-2 border-zinc-200 p-3 focus:border-yellow-400 outline-none" placeholder="Add a comment..." @keyup.enter="addComment(activePost)">
                            <button @click="addComment(activePost)" class="bg-zinc-900 text-white px-6 font-bold uppercase hover:bg-zinc-700">Post</button>
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

        <!-- ================= VIEW: EDITOR (编辑器) ================= -->
        <div v-else-if="currentView === 'editor'" class="max-w-5xl mx-auto animate-fade-in">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-black uppercase flex items-center gap-3">
                    <i data-lucide="edit-3" class="w-6 h-6"></i>
                    {{ isEditing ? 'Edit Record' : 'Create New Record' }}
                </h2>
                <button @click="switchView('list')" class="text-xs font-bold text-red-500 hover:text-red-700 uppercase tracking-widest">
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
                                <input v-model="newPost.title" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 text-white font-bold outline-none transition-colors" placeholder="ENTER TITLE...">
                            </div>
                        </div>
                        
                        <!-- 分类与标签 -->
                        <div class="space-y-4 md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="space-y-1">
                                <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Category</label>
                                <div class="flex gap-2">
                                    <button v-for="cat in ['LOG', 'REPORT', 'INTEL', 'NEWS']" 
                                        @click="newPost.category = cat"
                                        :class="['px-3 py-1 text-xs font-bold border transition-all', newPost.category === cat ? 'bg-yellow-400 text-black border-yellow-400' : 'border-zinc-600 text-zinc-500 hover:border-zinc-400']">
                                        {{ cat }}
                                    </button>
                                </div>
                            </div>
                            <div class="space-y-1">
                                <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Tags (Separate by comma)</label>
                                <input v-model="newPost.tags" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 font-mono text-sm outline-none transition-colors" placeholder="e.g. URSUS, LORE">
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
                                v-model:content="newPost.content" 
                                contentType="html" 
                                :options="quillOptions" 
                                theme="snow"
                                class="h-96" 
                            />
                        </div>
                    </div>

                    <!-- 底部操作栏 -->
                    <div class="flex justify-end gap-4 border-t border-zinc-700 pt-6">
                        <button @click="createPost" class="relative px-6 py-3 font-bold uppercase tracking-widest text-sm transition-all duration-300 border-2 flex items-center justify-center gap-2 bg-yellow-400 text-black border-yellow-400 hover:bg-yellow-300 hover:border-yellow-300 shadow-[4px_4px_0_0_#000]" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                            <i data-lucide="save" class="w-4 h-4"></i>
                            TRANSMIT RECORD
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-zinc-900 text-zinc-400 py-8 px-6 relative overflow-hidden mt-auto">
        <div class="absolute top-0 left-0 w-full h-2 bg-[repeating-linear-gradient(45deg,#eab308,#eab308_20px,#000_20px,#000_40px)]"></div>
        <div class="w-full mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="col-span-2">
                <h2 class="text-2xl font-black text-white uppercase tracking-tighter mb-4">Rcodes Island</h2>
                <p class="text-xs leading-relaxed max-w-md font-mono text-zinc-500">
                    CONFIDENTIALITY NOTICE: The information contained in this terminal system is intended only for the use of the individual or entity to whom it is assigned.
                </p>
            </div>
            <div class="text-right flex flex-col justify-between md:col-start-4">
                <div class="text-4xl font-black text-zinc-800">2025</div>
            </div>
        </div>
    </footer>

    <!-- Login Modal -->
    <div v-if="isLoginOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
        <div class="bg-zinc-50 w-full max-w-2xl border-2 border-zinc-600 relative shadow-[0_0_50px_rgba(0,0,0,0.5)]"
            style="clip-path: polygon(0 0, 100% 0, 100% 95%, 95% 100%, 0 100%)">
            <div class="bg-zinc-900 text-white px-6 py-3 flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <i data-lucide="terminal" class="w-4 h-4 text-yellow-400"></i>
                    <span class="font-mono font-bold tracking-widest uppercase">IDENTITY VERIFICATION</span>
                </div>
                <button @click="isLoginOpen = false" class="hover:text-yellow-400 transition-colors"><i data-lucide="x" class="w-5 h-5"></i></button>
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

    <!-- Music Player Ball -->
    <div class="fixed bottom-8 right-8 z-50">
        <audio ref="audioPlayer" loop muted>
            <source src="/bgm.mp3" type="audio/mpeg">
        </audio>
        <div class="w-12 h-12 rounded-full border-2 border-zinc-900 shadow-[4px_4px_0_0_#000] transition-transform duration-300 hover:scale-110 bg-white overflow-hidden">
            <button 
                @click="toggleMusic" 
                :class="['w-full h-full flex items-center justify-center', isPlaying ? 'bg-yellow-400 animate-spin-slow' : 'bg-white']"
                title="Music Player"
            >
                <i data-lucide="music" :class="['w-5 h-5', isPlaying ? 'text-black' : 'text-zinc-400']"></i>
            </button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch, onUpdated } from 'vue'
import axios from 'axios'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

// 辅助函数：去除 HTML 标签
const stripHtml = (html) => {
  // 预处理：将块级元素结束标签替换为换行符，保留结构
  let processed = html
    .replace(/<\/p>/gi, '\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/li>/gi, '\n');
    
  const tmp = document.createElement("DIV")
  tmp.innerHTML = processed
  return (tmp.textContent || tmp.innerText || "").trim()
}

// 状态
const posts = ref([])
const loading = ref(false)
const token = ref(localStorage.getItem('token') || '')
const user = ref(null)
const isLoginOpen = ref(false)
const isRegistering = ref(false)
const scrolled = ref(false)

// 视图状态
const currentView = ref('list') // 'list', 'detail', 'editor'
const activePost = ref(null)
const isEditing = ref(false)
const editingId = ref(null)

// 音乐播放器状态
const isPlaying = ref(false)
const audioPlayer = ref(null)

// Quill Editor 配置
const quillEditorRef = ref(null)

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
           headers: { Authorization: `Bearer ${token.value}` }
        })
        const url = res.data.url
        const quill = quillEditorRef.value.getQuill()
        const range = quill.getSelection()
        quill.insertEmbed(range.index, 'image', url)
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

// 表单数据
const authForm = reactive({ username: '', password: '' })
const newPost = reactive({ title: '', content: '', category: 'LOG', tags: '' })

// 监听滚动
window.addEventListener('scroll', () => {
  scrolled.value = window.scrollY > 50
})

// 视图切换
const switchView = (view) => {
  currentView.value = view
  window.scrollTo(0, 0)
  nextTick(() => {
    if (window.lucide) window.lucide.createIcons()
  })
}

const openDetail = async (post) => {
  activePost.value = post
  // 获取评论
  if (!post.comments) {
    try {
      const res = await axios.get(`/api/posts/${post.id}/comments/`)
      post.comments = res.data
    } catch (e) {
      console.error(e)
    }
  }
  switchView('detail')
}

const openEditor = (post = null) => {
  if (post) {
    isEditing.value = true
    editingId.value = post.id
    newPost.title = post.title
    newPost.content = post.content
    newPost.category = post.category || 'LOG'
    newPost.tags = post.tags || ''
  } else {
    isEditing.value = false
    editingId.value = null
    newPost.title = ''
    newPost.content = ''
    newPost.category = 'LOG'
    newPost.tags = ''
  }
  switchView('editor')
}

// API 操作
const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/posts/')
    posts.value = response.data.reverse()
  } catch (error) {
    console.error('Error fetching posts', error)
  } finally {
    loading.value = false
    nextTick(() => {
      if (window.lucide) window.lucide.createIcons()
    })
  }
}

const fetchCurrentUser = async () => {
  try {
    const response = await axios.get('/api/users/me', {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    user.value = response.data
  } catch (error) {
    console.error('Error fetching user', error)
    logout()
  }
}

const login = async () => {
  try {
    const formData = new FormData()
    formData.append('username', authForm.username)
    formData.append('password', authForm.password)
    const response = await axios.post('/api/token', formData)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    await fetchCurrentUser()
    isLoginOpen.value = false
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

const logout = () => {
  token.value = ''
  user.value = null
  localStorage.removeItem('token')
  switchView('list')
}

const createPost = async () => {
  if (!newPost.title || !newPost.content) return alert('Title and Content are required')
  try {
    if (isEditing.value) {
      await axios.put(`/api/posts/${editingId.value}`, newPost, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
    } else {
      await axios.post('/api/posts/', newPost, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
    }
    await fetchPosts()
    switchView('list')
  } catch (error) {
    alert('Error saving post')
  }
}

const deletePost = async (id) => {
  if (!confirm('Delete this record?')) return
  try {
    await axios.delete(`/api/posts/${id}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    posts.value = posts.value.filter(p => p.id !== id)
    switchView('list')
  } catch (error) {
    alert('Error deleting post')
  }
}

const addComment = async (post) => {
  if (!post.newComment) return
  try {
    const res = await axios.post(`/api/posts/${post.id}/comments/`, { content: post.newComment }, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    if (!post.comments) post.comments = []
    post.comments.push(res.data)
    post.newComment = ''
  } catch (error) {
    alert('Error adding comment')
  }
}

const deleteComment = async (post, commentId) => {
  if (!confirm('Delete comment?')) return
  try {
    await axios.delete(`/api/comments/${commentId}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    post.comments = post.comments.filter(c => c.id !== commentId)
  } catch (error) {
    alert('Error deleting comment')
  }
}

const toggleMusic = () => {
  if (isPlaying.value) {
    audioPlayer.value.pause()
  } else {
    audioPlayer.value.play().catch(e => console.log("Audio play failed:", e))
  }
  isPlaying.value = !isPlaying.value
}

onMounted(async () => {
  // 动态加载 Lucide 图标库
  const script = document.createElement('script')
  script.src = 'https://unpkg.com/lucide@latest'
  script.onload = () => {
    if (window.lucide) window.lucide.createIcons()
  }
  document.head.appendChild(script)

  // 动态加载 Tailwind (开发模式用 CDN，生产环境建议构建)
  const twScript = document.createElement('script')
  twScript.src = 'https://cdn.tailwindcss.com'
  document.head.appendChild(twScript)

  if (token.value) {
    await fetchCurrentUser()
  }
  await fetchPosts()

  // 尝试自动播放背景音乐
  if (audioPlayer.value) {
    // 1. 先尝试静音播放（成功率极高）
    audioPlayer.value.muted = true
    audioPlayer.value.play().then(() => {
      isPlaying.value = true
      console.log("Muted autoplay started")
    }).catch(e => {
      console.log("Muted autoplay failed:", e)
    })

    // 2. 监听用户首次交互，恢复声音
    const enableSound = () => {
      if (audioPlayer.value) {
        audioPlayer.value.muted = false
        audioPlayer.value.volume = 0.3
        // 如果之前静音播放失败了，这里再次尝试播放
        if (audioPlayer.value.paused) {
          audioPlayer.value.play().then(() => {
            isPlaying.value = true
          }).catch(e => console.log("Play on interaction failed:", e))
        }
      }
      // 移除监听器
      document.removeEventListener('click', enableSound)
      document.removeEventListener('touchstart', enableSound)
      document.removeEventListener('keydown', enableSound)
    }

    document.addEventListener('click', enableSound)
    document.addEventListener('touchstart', enableSound)
    document.addEventListener('keydown', enableSound)
  }
})

const refreshIcons = () => {
  nextTick(() => {
    if (window.lucide) {
      window.lucide.createIcons()
      // 再次尝试，确保 DOM 完全渲染
      setTimeout(() => window.lucide.createIcons(), 50)
    }
  })
}

onUpdated(refreshIcons)

watch([currentView, isLoginOpen, isRegistering], refreshIcons)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Noto+Sans+SC:wght@400;700;900&display=swap');

body {
    font-family: 'Noto Sans SC', sans-serif;
}
.font-mono {
    font-family: 'JetBrains Mono', monospace;
}
.animate-spin-slow {
    animation: spin 8s linear infinite;
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
/* 模拟扫描线效果 */
.scanline {
    background: linear-gradient(to bottom, transparent 50%, rgba(0, 0, 0, 0.05) 50%);
    background-size: 100% 4px;
}
</style>
