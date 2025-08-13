<!--Copyright 2025 The Casibase Authors. All Rights Reserved.-->

<!--Licensed under the Apache License, Version 2.0 (the "License");-->
<!--you may not use this file except in compliance with the License.-->
<!--You may obtain a copy of the License at-->

<!--     http://www.apache.org/licenses/LICENSE-2.0 -->

<!--Unless required by applicable law or agreed to in writing, software-->
<!--distributed under the License is distributed on an "AS IS" BASIS,-->
<!--WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.-->
<!--See the License for the specific language governing permissions and-->
<!--limitations under the License.-->

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { taskApi, type Task, type CreateTaskParams } from '@/api'

const tasks = ref<Task[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)

const formData = reactive<CreateTaskParams>({
  owner: 'admin', // Default admin user
  name: '',
  createdTime: new Date().toISOString(),
  displayName: '',
  provider: '',
  type: '',
  subject: '',
  topic: '',
})

const resetForm = () => {
  formData.owner = 'admin'
  formData.name = ''
  formData.createdTime = new Date().toISOString()
  formData.displayName = ''
  formData.provider = ''
  formData.type = ''
  formData.subject = ''
  formData.topic = ''
}

const fetchTasks = async () => {
  loading.value = true
  try {
    tasks.value = await taskApi.getTasks('admin')
  } catch (error) {
    console.error('Failed to fetch tasks:', error)
    tasks.value = []
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = 'Add Task'
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (task: Task) => {
  isEdit.value = true
  dialogTitle.value = 'Edit Task'
  Object.assign(formData, {
    owner: task.owner,
    name: task.name,
    createdTime: task.createdTime,
    displayName: task.displayName,
    provider: task.provider,
    type: task.type,
    subject: task.subject,
    topic: task.topic,
  })
  dialogVisible.value = true
}

const handleDelete = async (task: Task) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this task?', 'Warning', {
      type: 'warning',
    })
    await taskApi.deleteTask(task.owner, task.name)
    ElMessage.success('Deleted successfully')
    await fetchTasks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete task:', error)
      ElMessage.error('Failed to delete')
    }
  }
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await taskApi.updateTask(formData.owner, formData.name, formData)
      ElMessage.success('Updated successfully')
    } else {
      await taskApi.addTask(formData)
      ElMessage.success('Added successfully')
    }
    dialogVisible.value = false
    await fetchTasks()
  } catch (error) {
    console.error(isEdit.value ? 'Failed to update task:' : 'Failed to add task:', error)
    ElMessage.error(isEdit.value ? 'Failed to update' : 'Failed to add')
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<template>
  <div class="tasks-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Tasks Management</span>
          <el-button type="primary" @click="handleAdd">Add Task</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="tasks" style="width: 100%">
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="owner" label="Owner" />
        <el-table-column prop="displayName" label="Display Name" />
        <el-table-column prop="provider" label="Provider" />
        <el-table-column prop="type" label="Type" />
        <el-table-column prop="createdTime" label="Created Time" />
        <el-table-column label="Actions" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">Edit</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)"
              >Delete</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Add/Edit Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="Owner">
          <el-input v-model="formData.owner" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="formData.name" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="Display Name">
          <el-input v-model="formData.displayName" />
        </el-form-item>
        <el-form-item label="Provider">
          <el-input v-model="formData.provider" />
        </el-form-item>
        <el-form-item label="Type">
          <el-input v-model="formData.type" />
        </el-form-item>
        <el-form-item label="Subject">
          <el-input v-model="formData.subject" />
        </el-form-item>
        <el-form-item label="Topic">
          <el-input v-model="formData.topic" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="handleSubmit">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.tasks-container {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
