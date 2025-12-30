<template>
  <div class="container">
    <h1>My Personal Blog</h1>
    
    <!-- 发布文章表单 -->
    <div class="card">
      <h2>New Post</h2>
      <div class="form-group">
        <input v-model="newPost.title" placeholder="Title" />
      </div>
      <div class="form-group">
        <textarea v-model="newPost.content" placeholder="Content"></textarea>
      </div>
      <button @click="createPost" :disabled="loading">Publish</button>
    </div>

    <!-- 文章列表 -->
    <div class="card">
      <h2>Posts ({{ posts.length }})</h2>
      <div v-if="loading">Loading...</div>
      <div v-else-if="posts.length === 0">No posts yet.</div>
      <div v-else class="post-list">
        <div v-for="post in posts" :key="post.id" class="post-item">
          <h3>{{ post.title }}</h3>
          <p>{{ post.content }}</p>
          <small>ID: {{ post.id }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])
const newPost = ref({ title: '', content: '' })
const loading = ref(false)

// 获取文章列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/posts/')
    posts.value = response.data
  } catch (error) {
    alert('Error fetching posts: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 创建文章
const createPost = async () => {
  if (!newPost.value.title || !newPost.value.content) return
  
  loading.value = true
  try {
    await axios.post('/api/posts/', newPost.value)
    newPost.value = { title: '', content: '' } // 清空表单
    await fetchPosts() // 刷新列表
  } catch (error) {
    alert('Error creating post: ' + error.message)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<style>
.container { max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
.card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
.form-group { margin-bottom: 10px; }
input, textarea { width: 100%; padding: 8px; box-sizing: border-box; }
textarea { height: 100px; }
button { background-color: #42b983; color: white; border: none; padding: 10px 20px; cursor: pointer; }
button:disabled { background-color: #ccc; }
.post-item { border-bottom: 1px solid #eee; padding: 10px 0; }
</style>
