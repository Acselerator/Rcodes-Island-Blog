<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rhodes Island Terminal [Vue Version]</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons (Global) -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        /* 自定义动画与样式 */
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
        [v-cloak] {
            display: none;
        }
        /* 模拟扫描线效果 */
        .scanline {
            background: linear-gradient(to bottom, transparent 50%, rgba(0, 0, 0, 0.05) 50%);
            background-size: 100% 4px;
        }
    </style>
</head>
<body class="bg-[#f2f2f2] text-zinc-900 overflow-x-hidden selection:bg-yellow-400 selection:text-black min-h-screen">

    <div id="app" v-cloak>
        <!-- 背景层 -->
        <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
            <div class="absolute top-[10%] -left-[5%] text-[20vw] font-black text-zinc-200/50 leading-none select-none tracking-tighter opacity-50" style="writing-mode: vertical-rl">
                RHODES
            </div>
            
            <!-- 立绘层 (仅在列表页显示，避免阅读干扰) -->
            <transition enter-active-class="transition duration-1000 ease-out" enter-from-class="opacity-0 translate-x-20" enter-to-class="opacity-80 translate-x-0" leave-active-class="transition duration-500 ease-in" leave-from-class="opacity-80 translate-x-0" leave-to-class="opacity-0 translate-x-20">
                <div v-show="currentView === 'list'" class="absolute bottom-0 right-[-5%] w-[80vh] h-[90vh] z-0 opacity-80 hidden lg:block">
                   <img 
                    src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/150.svg" 
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
            <div class="max-w-[1600px] mx-auto px-6 flex justify-between items-center">
                <!-- Logo / Home Button -->
                <div @click="switchView('list')" class="flex items-center gap-4 cursor-pointer group">
                    <div class="w-10 h-10 bg-black text-white flex items-center justify-center font-bold text-xl transition-transform group-hover:scale-110" style="clip-path: polygon(0 0, 100% 0, 100% 75%, 75% 100%, 0 100%)">
                        <span class="font-mono">R</span>
                    </div>
                    <div class="leading-none">
                        <h1 class="text-xl font-black tracking-tighter uppercase group-hover:text-zinc-600 transition-colors">Rhodes Island</h1>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] font-bold tracking-[0.3em] text-zinc-500">TERMINAL SYSTEM</span>
                            <span v-if="isAdmin" class="text-[10px] bg-yellow-400 text-black px-1 font-bold">ADMIN</span>
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
                            {{ isAdmin ? 'Dr. DOCTOR' : 'GUEST USER' }}
                        </div>
                        <div class="text-[10px] font-mono bg-zinc-200 px-1 inline-block">
                            {{ isAdmin ? 'CLEARANCE: LV.08' : 'CLEARANCE: LV.00' }}
                        </div>
                    </div>
                    
                    <button v-if="isAdmin" @click="handleLogout" class="p-2 border-2 border-zinc-900 bg-zinc-900 text-white hover:bg-red-600 hover:border-red-600 transition-colors" title="Logout">
                        <i data-lucide="unlock" class="w-5 h-5"></i>
                    </button>
                    <button v-else @click="isLoginOpen = true" class="p-2 border-2 border-zinc-900 hover:bg-yellow-400 transition-colors" title="Login">
                        <i data-lucide="lock" class="w-5 h-5"></i>
                    </button>
                </div>
            </div>
        </header>

        <!-- 主内容容器 -->
        <main class="relative z-10 pt-32 pb-20 px-6 max-w-[1600px] mx-auto min-h-[80vh]">
            
            <!-- ================= VIEW: LIST (列表页) ================= -->
            <div v-if="currentView === 'list'" class="grid grid-cols-12 gap-8 animate-fade-in">
                <!-- 左侧面板 -->
                <aside class="col-span-12 lg:col-span-3 flex flex-col gap-8">
                    <!-- Profile Card -->
                    <div class="bg-white border-2 border-zinc-900 p-6 relative shadow-[8px_8px_0_0_rgba(0,0,0,0.1)] transition-transform hover:-translate-y-1">
                        <div :class="['absolute top-0 left-0 text-xs font-bold px-2 py-1 border-r-2 border-b-2 border-zinc-900', isAdmin ? 'bg-yellow-400' : 'bg-zinc-200']">
                            ID: {{ isAdmin ? 'PRTS-001' : 'GUEST-000' }}
                        </div>
                        <div class="mt-6 mb-4">
                            <div class="w-20 h-20 bg-zinc-100 border-2 border-zinc-900 rounded-full overflow-hidden flex items-center justify-center mb-4">
                                <i data-lucide="user" class="w-10 h-10 text-zinc-400"></i>
                            </div>
                            <h2 class="text-3xl font-black uppercase leading-none">
                                {{ isAdmin ? 'DOCTOR' : 'VISITOR' }}
                            </h2>
                            <p class="text-xs font-bold text-zinc-400 mt-1 tracking-widest">
                                {{ isAdmin ? 'NEURAL NETWORK ADMIN' : 'READ ONLY ACCESS' }}
                            </p>
                        </div>
                        <div class="h-[2px] w-full bg-zinc-900 mb-4"></div>
                        <p class="text-xs font-serif italic text-zinc-600 leading-relaxed">
                            "{{ isAdmin ? 'MAY I ENJOY MY LIFE and PRACTICE my art.' : 'Connection Established. Waiting for input.' }}"
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
                        <cut-corner-button v-if="isAdmin" @click="openEditor(null)" variant="primary" class="mb-2">
                            <i data-lucide="plus" class="w-4 h-4"></i> New Record
                        </cut-corner-button>
                    </div>

                    <div class="space-y-8">
                        <div v-if="posts.length === 0" class="text-center py-20 border-2 border-dashed border-zinc-300 text-zinc-400 font-mono">
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
                                <span class="text-xs font-black bg-black text-white px-2 py-1 uppercase">{{ post.category }}</span>
                                <span class="text-sm font-mono font-bold text-zinc-400">{{ post.date }} / {{ post.year }}</span>
                            </div>

                            <h3 class="text-3xl font-bold mb-2 leading-tight group-hover:text-zinc-700 transition-colors">
                                <glitch-text :text="post.title"></glitch-text>
                            </h3>

                            <h4 class="text-xs font-bold text-zinc-400 tracking-widest uppercase mb-6 border-b border-dashed border-zinc-300 pb-4 w-full">
                                {{ post.enTitle }}
                            </h4>

                            <!-- 截断显示摘要 -->
                            <p class="text-zinc-600 leading-relaxed mb-6 font-medium line-clamp-3">{{ post.excerpt }}</p>

                            <div class="flex justify-between items-center">
                                <div class="flex gap-2">
                                    <span v-for="tag in post.tags" :key="tag" class="text-[10px] font-bold text-zinc-400 border border-zinc-200 px-2 py-1 rounded-full uppercase">
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
                    <div class="absolute top-0 right-0 w-full">
                        <div class="bg-white/80 backdrop-blur-sm border-2 border-zinc-900/10 p-4 mb-4">
                            <div class="text-[10px] font-bold text-zinc-500 mb-2 uppercase tracking-wider flex items-center justify-between">
                                <span>Weekly Operations</span>
                                <i data-lucide="refresh-cw" class="w-3 h-3 animate-spin-slow"></i>
                            </div>
                            <div class="space-y-2">
                                <div v-for="i in 3" :key="i" class="flex items-center gap-2">
                                    <div class="w-2 h-2 bg-yellow-400 rounded-full"></div>
                                    <div class="h-2 flex-1 bg-zinc-200 rounded-full overflow-hidden">
                                        <div class="h-full bg-zinc-800" :style="{ width: Math.random() * 100 + '%' }"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </aside>
            </div>

            <!-- ================= VIEW: DETAIL (详情页) ================= -->
            <div v-else-if="currentView === 'detail' && activePost" class="max-w-4xl mx-auto animate-fade-in">
                <!-- 返回栏 -->
                <div class="flex justify-between items-center mb-6">
                    <button @click="switchView('list')" class="flex items-center gap-2 text-sm font-bold text-zinc-500 hover:text-black transition-colors uppercase tracking-widest">
                        <i data-lucide="arrow-left" class="w-4 h-4"></i> Return to Database
                    </button>
                    
                    <div class="flex gap-2" v-if="isAdmin">
                        <cut-corner-button @click="deletePost(activePost.id)" variant="danger" class="!py-2 !px-4 text-xs">
                            <i data-lucide="trash-2" class="w-4 h-4"></i> Delete
                        </cut-corner-button>
                        <cut-corner-button @click="openEditor(activePost)" variant="primary" class="!py-2 !px-4 text-xs">
                            <i data-lucide="edit" class="w-4 h-4"></i> Edit Record
                        </cut-corner-button>
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
                                    <span class="bg-yellow-400 text-black px-2 py-0.5 text-xs font-bold uppercase tracking-wider">{{ activePost.category }}</span>
                                    <span class="bg-zinc-100 text-zinc-500 px-2 py-0.5 text-xs font-bold uppercase tracking-wider font-mono">{{ activePost.date }} . {{ activePost.year }}</span>
                                </div>
                                <h1 class="text-4xl md:text-5xl font-black text-zinc-900 mb-2 leading-tight tracking-tight">{{ activePost.title }}</h1>
                                <h2 class="text-lg font-mono font-bold text-zinc-400 uppercase tracking-widest">{{ activePost.enTitle }}</h2>
                            </div>
                            <div class="md:col-span-4 flex flex-col justify-end items-start md:items-end gap-2">
                                <div class="text-right">
                                    <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest mb-1">Authorization</div>
                                    <div class="text-sm font-bold">LEVEL 03</div>
                                </div>
                                <div class="text-right">
                                     <div class="text-[10px] uppercase text-zinc-400 font-bold tracking-widest mb-1">Tags</div>
                                     <div class="flex flex-wrap justify-end gap-1">
                                        <span v-for="tag in activePost.tags" class="text-[10px] border border-zinc-300 px-1 text-zinc-500 uppercase">{{ tag }}</span>
                                     </div>
                                </div>
                            </div>
                        </div>

                        <!-- 正文内容 (支持 Markdown 风格的简单换行) -->
                        <div class="prose prose-zinc max-w-none">
                            <div class="font-serif text-lg leading-loose text-zinc-800 whitespace-pre-wrap">{{ activePost.excerpt }}</div>
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
                        {{ isEditing ? 'Edit Existing Record' : 'Create New Record' }}
                    </h2>
                    <button @click="handleEditorCancel" class="text-xs font-bold text-red-500 hover:text-red-700 uppercase tracking-widest">
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
                            <div class="space-y-4">
                                <div class="space-y-1">
                                    <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Record Title</label>
                                    <input v-model="editorForm.title" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 text-white font-bold outline-none transition-colors" placeholder="ENTER TITLE...">
                                </div>
                                <div class="space-y-1">
                                    <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Subtitle (EN)</label>
                                    <input v-model="editorForm.enTitle" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 font-mono text-sm uppercase outline-none transition-colors" placeholder="ENTER SUBTITLE...">
                                </div>
                            </div>
                            
                            <!-- 分类与标签 -->
                            <div class="space-y-4">
                                <div class="space-y-1">
                                    <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Category</label>
                                    <div class="flex gap-2">
                                        <button v-for="cat in ['LOG', 'REPORT', 'INTEL', 'NEWS']" 
                                            @click="editorForm.category = cat"
                                            :class="['px-3 py-1 text-xs font-bold border transition-all', editorForm.category === cat ? 'bg-yellow-400 text-black border-yellow-400' : 'border-zinc-600 text-zinc-500 hover:border-zinc-400']">
                                            {{ cat }}
                                        </button>
                                    </div>
                                </div>
                                <div class="space-y-1">
                                    <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Tags (Separate by comma)</label>
                                    <input v-model="editorForm.tagsInput" class="w-full bg-zinc-800 border-b-2 border-zinc-600 focus:border-yellow-400 p-2 font-mono text-sm outline-none transition-colors" placeholder="e.g. URSUS, LORE">
                                </div>
                            </div>
                        </div>

                        <!-- 正文编辑 -->
                        <div class="space-y-2 mb-8">
                            <label class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest flex justify-between">
                                <span>Record Content</span>
                                <span>LINES: {{ editorForm.excerpt.split('\n').length }}</span>
                            </label>
                            <textarea v-model="editorForm.excerpt" class="w-full h-96 bg-zinc-800 border-2 border-zinc-700 p-4 font-mono text-sm leading-relaxed text-zinc-300 focus:border-yellow-400 outline-none resize-none" placeholder="Begin typing entry data..."></textarea>
                        </div>

                        <!-- 底部操作栏 -->
                        <div class="flex justify-end gap-4 border-t border-zinc-700 pt-6">
                            <cut-corner-button @click="handleEditorSave" :active="true" variant="primary">
                                <i data-lucide="save" class="w-4 h-4"></i>
                                {{ isEditing ? 'UPDATE DATABASE' : 'TRANSMIT RECORD' }}
                            </cut-corner-button>
                        </div>
                    </div>
                </div>
            </div>

        </main>

        <!-- Footer -->
        <footer class="bg-zinc-900 text-zinc-400 py-12 px-6 relative overflow-hidden mt-auto">
            <div class="absolute top-0 left-0 w-full h-2 bg-[repeating-linear-gradient(45deg,#eab308,#eab308_20px,#000_20px,#000_40px)]"></div>
            <div class="max-w-[1600px] mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
                <div class="col-span-2">
                    <h2 class="text-2xl font-black text-white uppercase tracking-tighter mb-4">Rhodes Island</h2>
                    <p class="text-xs leading-relaxed max-w-md font-mono text-zinc-500">
                        CONFIDENTIALITY NOTICE: The information contained in this terminal system is intended only for the use of the individual or entity to whom it is assigned.
                    </p>
                </div>
                <div class="text-right flex flex-col justify-between md:col-start-4">
                    <div class="text-4xl font-black text-zinc-800">2025</div>
                </div>
            </div>
        </footer>

        <!-- Login Modal (保持弹窗形式) -->
        <modal :is-open="isLoginOpen" @close="isLoginOpen = false" title="IDENTITY VERIFICATION">
            <form @submit.prevent="handleLogin" class="space-y-6">
                <div class="text-center mb-8">
                    <div class="w-16 h-16 bg-zinc-100 rounded-full mx-auto flex items-center justify-center mb-4 border-2 border-zinc-900">
                        <i data-lucide="lock" class="w-6 h-6 text-zinc-400"></i>
                    </div>
                    <p class="text-sm font-bold text-zinc-500 tracking-widest">PLEASE ENTER AUTHORIZATION CODE</p>
                </div>
                
                <div class="space-y-2">
                    <label class="text-xs font-bold text-zinc-400 uppercase">Passcode</label>
                    <input 
                        type="password" 
                        class="w-full bg-zinc-100 border-2 border-zinc-200 p-3 font-mono text-xl focus:border-yellow-400 focus:outline-none transition-colors"
                        placeholder="******"
                        v-model="passwordInput"
                        autofocus
                    />
                    <div class="text-[10px] text-zinc-400">Hint: Try 'doctor'</div>
                </div>

                <div v-if="loginError" class="bg-red-50 text-red-600 p-2 text-xs font-bold border border-red-200 flex items-center gap-2">
                    <i data-lucide="activity" class="w-3 h-3"></i> {{ loginError }}
                </div>

                <div class="flex justify-end pt-4">
                    <cut-corner-button type="submit" :active="true">
                        ACCESS TERMINAL
                    </cut-corner-button>
                </div>
            </form>
        </modal>
    </div>

    <!-- 逻辑层 -->
    <script type="module">
        import { createApp, ref, reactive, onMounted, computed, watch, nextTick } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
        import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js';
        import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js';
        import { getFirestore, collection, addDoc, onSnapshot, doc, updateDoc, deleteDoc, serverTimestamp } from 'https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js';

        const firebaseConfig = JSON.parse(__firebase_config);
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const db = getFirestore(app);
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

        // Components
        const CutCornerButton = {
            props: { active: Boolean, variant: { type: String, default: 'default' } },
            template: `
                <button class="relative px-6 py-3 font-bold uppercase tracking-widest text-sm transition-all duration-300 border-2 flex items-center justify-center gap-2"
                    :class="classes" style="clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%)">
                    <slot></slot>
                </button>
            `,
            setup(props) {
                const classes = computed(() => {
                    const variants = {
                        default: props.active 
                            ? 'bg-zinc-900 text-white border-zinc-900 translate-x-1 -translate-y-1 shadow-[4px_4px_0_0_#eab308]' 
                            : 'bg-white text-zinc-900 border-zinc-900 hover:bg-zinc-100 hover:translate-x-1 hover:-translate-y-1 hover:shadow-[4px_4px_0_0_#zinc-300]',
                        primary: 'bg-yellow-400 text-black border-yellow-400 hover:bg-yellow-300 hover:border-yellow-300 shadow-[4px_4px_0_0_#000]',
                        danger: 'bg-red-500 text-white border-red-500 hover:bg-red-600 shadow-[4px_4px_0_0_#000]',
                        ghost: 'bg-transparent border-zinc-300 text-zinc-500 hover:border-zinc-900 hover:text-zinc-900'
                    };
                    return variants[props.variant] || variants.default;
                });
                return { classes };
            }
        };

        const GlitchText = {
            props: ['text'],
            template: `
                <span class="relative inline-block group">
                    <span class="relative z-10">{{ text }}</span>
                    <span class="absolute top-0 left-0 -ml-0.5 translate-x-[1px] text-red-500 opacity-70 animate-pulse z-0 hidden group-hover:block">{{ text }}</span>
                    <span class="absolute top-0 left-0 -ml-0.5 -translate-x-[1px] text-cyan-500 opacity-70 animate-pulse delay-75 z-0 hidden group-hover:block">{{ text }}</span>
                </span>
            `
        };

        const Modal = {
            props: ['isOpen', 'title'],
            emits: ['close'],
            template: `
                <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
                    <div class="bg-zinc-50 w-full max-w-2xl border-2 border-zinc-600 relative shadow-[0_0_50px_rgba(0,0,0,0.5)]"
                        style="clip-path: polygon(0 0, 100% 0, 100% 95%, 95% 100%, 0 100%)">
                        <div class="bg-zinc-900 text-white px-6 py-3 flex justify-between items-center">
                            <div class="flex items-center gap-2">
                                <i data-lucide="terminal" class="w-4 h-4 text-yellow-400"></i>
                                <span class="font-mono font-bold tracking-widest uppercase">{{ title }}</span>
                            </div>
                            <button @click="$emit('close')" class="hover:text-yellow-400 transition-colors"><i data-lucide="x" class="w-5 h-5"></i></button>
                        </div>
                        <div class="p-8"><slot></slot></div>
                        <div class="absolute bottom-0 right-0 w-4 h-4 bg-yellow-400"></div>
                    </div>
                </div>
            `,
            updated() { lucide.createIcons(); }
        };

        createApp({
            components: { CutCornerButton, GlitchText, Modal },
            setup() {
                const user = ref(null);
                const posts = ref([]);
                const isAdmin = ref(false);
                const scrolled = ref(false);
                const isLoginOpen = ref(false);
                
                // === View State Management ===
                const currentView = ref('list'); // 'list' | 'detail' | 'editor'
                const activePost = ref(null); // Used for Detail view
                const isEditing = ref(false); // Used for Editor view mode
                
                // === Editor Form Data ===
                const editorForm = reactive({
                    id: null,
                    title: '',
                    enTitle: '',
                    category: 'LOG',
                    tagsInput: '',
                    excerpt: ''
                });

                // Login Data
                const passwordInput = ref('');
                const loginError = ref('');

                // === Lifecycle & Navigation ===
                const switchView = (view) => {
                    currentView.value = view;
                    window.scrollTo(0, 0);
                    nextTick(() => lucide.createIcons());
                };

                const openDetail = (post) => {
                    activePost.value = post;
                    switchView('detail');
                };

                const openEditor = (post = null) => {
                    if (post) {
                        // Edit Mode
                        isEditing.value = true;
                        editorForm.id = post.id;
                        editorForm.title = post.title;
                        editorForm.enTitle = post.enTitle;
                        editorForm.category = post.category;
                        editorForm.tagsInput = post.tags ? post.tags.join(', ') : '';
                        editorForm.excerpt = post.excerpt;
                    } else {
                        // Create Mode
                        isEditing.value = false;
                        editorForm.id = null;
                        editorForm.title = '';
                        editorForm.enTitle = '';
                        editorForm.category = 'LOG';
                        editorForm.tagsInput = '';
                        editorForm.excerpt = '';
                    }
                    switchView('editor');
                };

                const handleEditorCancel = () => {
                    if(confirm('DISCARD CHANGES?')) {
                        switchView('list');
                    }
                };

                // === Actions ===
                const handleEditorSave = async () => {
                    if (!editorForm.title || !editorForm.excerpt) {
                        alert("ERROR: MISSING REQUIRED FIELDS");
                        return;
                    }

                    const tags = editorForm.tagsInput.split(',').map(t => t.trim()).filter(t => t);
                    const now = new Date();
                    const docData = {
                        title: editorForm.title,
                        enTitle: editorForm.enTitle || 'UNTITLED',
                        excerpt: editorForm.excerpt,
                        category: editorForm.category,
                        tags: tags,
                        updatedAt: serverTimestamp()
                    };

                    try {
                        if (isEditing.value && editorForm.id) {
                            // Update
                            await updateDoc(doc(db, 'artifacts', appId, 'public', 'data', 'posts', editorForm.id), docData);
                            activePost.value = { ...activePost.value, ...docData, id: editorForm.id }; // Optimistic update
                            switchView('detail'); // Return to detail view
                        } else {
                            // Create
                            docData.createdAt = serverTimestamp();
                            docData.date = `${now.getMonth() + 1}.${now.getDate()}`;
                            docData.year = `${now.getFullYear()}`;
                            await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'posts'), docData);
                            switchView('list'); // Return to list view
                        }
                    } catch (err) {
                        console.error(err);
                        alert("TRANSMISSION FAILED");
                    }
                };

                const deletePost = async (id) => {
                    if(!confirm('WARNING: PERMANENTLY DELETE RECORD?')) return;
                    try {
                        await deleteDoc(doc(db, 'artifacts', appId, 'public', 'data', 'posts', id));
                        switchView('list');
                    } catch(err) {
                        alert("DELETION FAILED");
                    }
                };

                // === Init & Auth ===
                onMounted(() => {
                    const initAuth = async () => {
                        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
                            await signInWithCustomToken(auth, __initial_auth_token);
                        } else {
                            await signInAnonymously(auth);
                        }
                    };
                    initAuth();
                    onAuthStateChanged(auth, (u) => user.value = u);

                    window.addEventListener('scroll', () => { scrolled.value = window.scrollY > 50; });
                    lucide.createIcons();
                });

                watch(user, (newUser) => {
                    if (!newUser) return;
                    const q = collection(db, 'artifacts', appId, 'public', 'data', 'posts');
                    onSnapshot(q, (snapshot) => {
                        const loaded = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
                        loaded.sort((a, b) => (b.createdAt?.seconds || 0) - (a.createdAt?.seconds || 0));
                        posts.value = loaded;
                        nextTick(() => lucide.createIcons());
                    });
                });

                const handleLogin = () => {
                    if (passwordInput.value === 'doctor') {
                        isAdmin.value = true;
                        isLoginOpen.value = false;
                        passwordInput.value = '';
                        loginError.value = '';
                    } else {
                        loginError.value = 'ACCESS DENIED';
                    }
                };
                const handleLogout = () => { isAdmin.value = false; switchView('list'); };

                return {
                    user, posts, isAdmin, scrolled, isLoginOpen,
                    currentView, activePost, isEditing, editorForm,
                    passwordInput, loginError,
                    switchView, openDetail, openEditor, handleEditorCancel, handleEditorSave, deletePost, handleLogin, handleLogout
                };
            },
            updated() { lucide.createIcons(); }
        }).mount('#app');
    </script>
</body>
</html>