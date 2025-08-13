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
import { storeApi, type Store, type CreateStoreParams } from '@/api'

const stores = ref<Store[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const formData = reactive<CreateStoreParams>({
  owner: '',
  name: '',
  createdTime: new Date().toISOString(),
  displayName: '',
  storageProvider: '',
  storageSubpath: '',
  modelProvider: '',
  embeddingProvider: '',
})

const resetForm = () => {
  formData.owner = ''
  formData.name = ''
  formData.createdTime = new Date().toISOString()
  formData.displayName = ''
  formData.storageProvider = ''
  formData.storageSubpath = ''
  formData.modelProvider = ''
  formData.embeddingProvider = ''
}

const fetchStores = async () => {
  loading.value = true
  try {
    const response = await storeApi.getStores(pagination.pageSize, pagination.currentPage)
    stores.value = response.items
    pagination.total = response.total
  } catch (error) {
    console.error('Failed to fetch stores:', error)
    stores.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  pagination.currentPage = page
  fetchStores()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.currentPage = 1
  fetchStores()
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = 'Add Store'
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (store: Store) => {
  isEdit.value = true
  dialogTitle.value = 'Edit Store'
  Object.assign(formData, {
    owner: store.owner,
    name: store.name,
    createdTime: store.createdTime,
    displayName: store.displayName,
    storageProvider: store.storageProvider,
    storageSubpath: store.storageSubpath,
    modelProvider: store.modelProvider,
    embeddingProvider: store.embeddingProvider,
  })
  dialogVisible.value = true
}

const handleDelete = async (store: Store) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this store?', 'Warning', {
      type: 'warning',
    })
    await storeApi.deleteStore(store.owner, store.name)
    ElMessage.success('Deleted successfully')
    await fetchStores()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete store:', error)
      ElMessage.error('Failed to delete')
    }
  }
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await storeApi.updateStore(formData.owner, formData.name, formData)
      ElMessage.success('Updated successfully')
    } else {
      await storeApi.addStore(formData)
      ElMessage.success('Added successfully')
    }
    dialogVisible.value = false
    await fetchStores()
  } catch (error) {
    console.error(isEdit.value ? 'Failed to update store:' : 'Failed to add store:', error)
    ElMessage.error(isEdit.value ? 'Failed to update' : 'Failed to add')
  }
}

onMounted(() => {
  fetchStores()
})
</script>

<template>
  <div class="stores-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Stores Management</span>
          <el-button type="primary" @click="handleAdd">Add Store</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="stores" style="width: 100%">
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="owner" label="Owner" />
        <el-table-column prop="createdTime" label="Created Time" />
        <el-table-column prop="displayName" label="Display Name" />
        <el-table-column prop="storageProvider" label="Storage Provider" />
        <el-table-column label="Actions" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">Edit</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)"
              >Delete</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>

    </el-card>

    <!-- Add/Edit Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="formData" label-width="120px">
        <el-form-item label="Owner">
          <el-input v-model="formData.owner" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="formData.name" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="Display Name">
          <el-input v-model="formData.displayName" />
        </el-form-item>
        <el-form-item label="Storage Provider">
          <el-select v-model="formData.storageProvider" style="width: 100%">
            <el-option label="Local Storage" value="local" />
            <el-option label="S3 Storage" value="s3" />
          </el-select>
        </el-form-item>
        <el-form-item label="Storage Path">
          <el-input v-model="formData.storageSubpath" />
        </el-form-item>
        <el-form-item label="Model Provider">
          <el-input v-model="formData.modelProvider" />
        </el-form-item>
        <el-form-item label="Embedding Provider">
          <el-input v-model="formData.embeddingProvider" />
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
.stores-container {
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
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
