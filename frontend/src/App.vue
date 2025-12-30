<template>
  <div class="container">
    <h1>My Personal Blog</h1>
    
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

    <!-- 文章列表 -->
    <div class="card">
      <h2>Posts ({{ posts.length }})</h2>
      <div v-if="loading && posts.length === 0">Loading...</div>
      <div v-else-if="posts.length === 0">No posts yet.</div>
      <div v-else class="post-list">
        <div v-for="post in posts" :key="post.id" class="post-item">
          <div class="post-header">
            <h3>{{ post.title }}</h3>
            <div class="post-actions">
              <button @click="startEdit(post)" class="btn-small btn-edit">Edit</button>
              <button @click="deletePost(post.id)" class="btn-small btn-delete">Delete</button>
            </div>
          </div>
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
const postForm = ref({ title: '', content: '' })
const loading = ref(false)
const isEditing = ref(false)
const editingId = ref(null)

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

// 保存文章 (创建或更新)
const savePost = async () => {
  if (!postForm.value.title || !postForm.value.content) return
  
  loading.value = true
  try {
    if (isEditing.value) {
      // 更新模式
      await axios.put(`/api/posts/${editingId.value}`, postForm.value)
    } else {
      // 创建模式
      await axios.post('/api/posts/', postForm.value)
    }
    
    // 重置表单并刷新
    cancelEdit()
    await fetchPosts()
  } catch (error) {
    alert(`Error ${isEditing.value ? 'updating' : 'creating'} post: ` + error.message)
  } finally {
    loading.value = false
  }
}

// 开始编辑
const startEdit = (post) => {
  isEditing.value = true
  editingId.value = post.id
  postForm.value = { title: post.title, content: post.content }
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false
  editingId.value = null
  postForm.value = { title: '', content: '' }
}

// 删除文章
const deletePost = async (id) => {
  if (!confirm('Are you sure you want to delete this post?')) return

  loading.value = true
  try {
    await axios.delete(`/api/posts/${id}`)
    await fetchPosts()
  } catch (error) {
    alert('Error deleting post: ' + error.message)
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

/* 按钮样式 */
button { background-color: #42b983; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; }
button:disabled { background-color: #ccc; cursor: not-allowed; }
button:hover:not(:disabled) { opacity: 0.9; }

.button-group { display: flex; gap: 10px; }
.btn-secondary { background-color: #6c757d; }
.btn-small { padding: 5px 10px; font-size: 0.9em; }
.btn-edit { background-color: #3498db; }
.btn-delete { background-color: #e74c3c; }

.post-item { border-bottom: 1px solid #eee; padding: 15px 0; }
.post-header { display: flex; justify-content: space-between; align-items: center; }
.post-actions { display: flex; gap: 8px; }
</style>
