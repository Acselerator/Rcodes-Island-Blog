<template>
  <div class="container">
    <header class="header">
      <h1>My Personal Blog</h1>
      <div class="user-info">
        <div v-if="user">
          <span>Welcome, {{ user.username }}</span>
          <button @click="logout" class="btn-small btn-secondary">Logout</button>
        </div>
        <div v-else>
          <button @click="showLogin = true" class="btn-small">Login</button>
          <button @click="showLogin = false" class="btn-small btn-secondary">Register</button>
        </div>
      </div>
    </header>

    <!-- 登录/注册区域 -->
    <div v-if="!user" class="auth-container card">
      <h2>{{ showLogin ? 'Login' : 'Register' }}</h2>
      <div class="form-group">
        <input v-model="authForm.username" placeholder="Username" />
      </div>
      <div class="form-group">
        <input v-model="authForm.password" type="password" placeholder="Password" />
      </div>
      <button @click="handleAuth" :disabled="loading">
        {{ showLogin ? 'Login' : 'Register' }}
      </button>
      <p class="toggle-auth" @click="showLogin = !showLogin">
        {{ showLogin ? 'Need an account? Register' : 'Have an account? Login' }}
      </p>
    </div>

    <!-- 内容区域 (仅登录后显示发布框，列表始终显示) -->
    <div v-else class="content-area">
      <!-- 发布/编辑文章表单 -->
      <div class="card">
        <h2>{{ isEditing ? 'Edit Post' : 'New Post' }}</h2>
        <div class="form-group">
          <input v-model="postForm.title" placeholder="Title" />
        </div>
        <div class="form-group">
          <textarea v-model="postForm.content" placeholder="Content"></textarea>
        </div>
        <div class="button-group">
          <button @click="savePost" :disabled="loading">
            {{ isEditing ? 'Update' : 'Publish' }}
          </button>
          <button v-if="isEditing" @click="cancelEdit" class="btn-secondary" :disabled="loading">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="card">
      <h2>Posts ({{ posts.length }})</h2>
      <div v-if="loading && posts.length === 0">Loading...</div>
      <div v-else-if="posts.length === 0">No posts yet.</div>
      <div v-else class="post-list">
        <div v-for="post in posts" :key="post.id" class="post-item">
          <div class="post-header">
            <h3>{{ post.title }}</h3>
            <div class="post-actions" v-if="user && post.owner_id === user.id">
              <button @click="startEdit(post)" class="btn-small btn-edit">Edit</button>
              <button @click="deletePost(post.id)" class="btn-small btn-delete">Delete</button>
            </div>
          </div>
          <p>{{ post.content }}</p>
          <small>ID: {{ post.id }} | Author ID: {{ post.owner_id }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- 状态 ---
const user = ref(null)
const token = ref(localStorage.getItem('token'))
const showLogin = ref(true)
const authForm = ref({ username: '', password: '' })

const posts = ref([])
const postForm = ref({ title: '', content: '' })
const loading = ref(false)
const isEditing = ref(false)
const editingId = ref(null)

// --- Axios 配置 ---
// 添加请求拦截器，自动携带 Token
axios.interceptors.request.use(config => {
  if (token.value) {
    config.headers.Authorization = `Bearer ${token.value}`
  }
  return config
})

// 添加响应拦截器，处理 401
axios.interceptors.response.use(response => response, error => {
  if (error.response && error.response.status === 401) {
    logout()
  }
  return Promise.reject(error)
})

// --- 认证逻辑 ---
const handleAuth = async () => {
  if (!authForm.value.username || !authForm.value.password) return
  loading.value = true
  try {
    if (showLogin.value) {
      // 登录
      // OAuth2PasswordRequestForm 需要 form-data 格式
      const formData = new FormData()
      formData.append('username', authForm.value.username)
      formData.append('password', authForm.value.password)
      
      const response = await axios.post('/api/token', formData)
      token.value = response.data.access_token
      localStorage.setItem('token', token.value)
      await fetchCurrentUser()
    } else {
      // 注册
      await axios.post('/api/register', authForm.value)
      alert('Registration successful! Please login.')
      showLogin.value = true
    }
  } catch (error) {
    alert('Auth error: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const fetchCurrentUser = async () => {
  if (!token.value) return
  try {
    const response = await axios.get('/api/users/me')
    user.value = response.data
  } catch (error) {
    console.error('Failed to fetch user', error)
    logout()
  }
}

const logout = () => {
  user.value = null
  token.value = null
  localStorage.removeItem('token')
}

// --- 文章逻辑 ---
const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/posts/')
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts', error)
  } finally {
    loading.value = false
  }
}

const savePost = async () => {
  if (!postForm.value.title || !postForm.value.content) return
  
  loading.value = true
  try {
    if (isEditing.value) {
      await axios.put(`/api/posts/${editingId.value}`, postForm.value)
    } else {
      await axios.post('/api/posts/', postForm.value)
    }
    cancelEdit()
    await fetchPosts()
  } catch (error) {
    alert(`Error: ` + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const startEdit = (post) => {
  isEditing.value = true
  editingId.value = post.id
  postForm.value = { title: post.title, content: post.content }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const cancelEdit = () => {
  isEditing.value = false
  editingId.value = null
  postForm.value = { title: '', content: '' }
}

const deletePost = async (id) => {
  if (!confirm('Are you sure?')) return
  loading.value = true
  try {
    await axios.delete(`/api/posts/${id}`)
    await fetchPosts()
  } catch (error) {
    alert('Error: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (token.value) {
    await fetchCurrentUser()
  }
  await fetchPosts()
})
</script>

<style>
.container { max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.user-info { display: flex; gap: 10px; align-items: center; }
.card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
.form-group { margin-bottom: 10px; }
input, textarea { width: 100%; padding: 8px; box-sizing: border-box; }
textarea { height: 100px; }

button { background-color: #42b983; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; }
button:disabled { background-color: #ccc; cursor: not-allowed; }
.button-group { display: flex; gap: 10px; }
.btn-secondary { background-color: #6c757d; }
.btn-small { padding: 5px 10px; font-size: 0.9em; }
.btn-edit { background-color: #3498db; }
.btn-delete { background-color: #e74c3c; }

.post-item { border-bottom: 1px solid #eee; padding: 15px 0; }
.post-header { display: flex; justify-content: space-between; align-items: center; }
.post-actions { display: flex; gap: 8px; }
.toggle-auth { color: #42b983; cursor: pointer; text-decoration: underline; margin-top: 10px; }
</style>
