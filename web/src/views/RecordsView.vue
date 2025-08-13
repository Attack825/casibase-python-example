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
import { recordApi, type Record, type CreateRecordParams } from '@/api'

const records = ref<Record[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const formData = reactive<CreateRecordParams>({
  owner: '',
  name: '',
  createdTime: new Date().toISOString(),
  organization: '',
  clientIp: '',
  userAgent: '',
  user: '',
  method: '',
  requestUri: '',
  action: '',
  language: '',
  region: '',
  city: '',
})

const resetForm = () => {
  formData.owner = ''
  formData.name = ''
  formData.createdTime = new Date().toISOString()
  formData.organization = ''
  formData.clientIp = ''
  formData.userAgent = ''
  formData.user = ''
  formData.method = ''
  formData.requestUri = ''
  formData.action = ''
  formData.language = ''
  formData.region = ''
  formData.city = ''
}

const fetchRecords = async () => {
  loading.value = true
  try {
    const response = await recordApi.getRecords(
      pagination.pageSize.toString(),
      pagination.currentPage.toString()
    )
    records.value = response.items
    pagination.total = response.total
  } catch (error) {
    console.error('Failed to fetch records:', error)
    records.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}


const handlePageChange = (page: number) => {
  pagination.currentPage = page
  fetchRecords()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.currentPage = 1
  fetchRecords()
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = 'Add Record'
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (record: Record) => {
  isEdit.value = true
  dialogTitle.value = 'Edit Record'
  Object.assign(formData, {
    owner: record.owner,
    name: record.name,
    createdTime: record.createdTime,
    organization: record.organization,
    clientIp: record.clientIp,
    userAgent: record.userAgent,
    user: record.user,
    method: record.method,
    requestUri: record.requestUri,
    action: record.action,
    language: record.language,
    region: record.region,
    city: record.city,
  })
  dialogVisible.value = true
}

const handleDelete = async (record: Record) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this record?', 'Warning', {
      type: 'warning',
    })
    await recordApi.deleteRecord( record.name)
    ElMessage.success('Deleted successfully')
    await fetchRecords()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete record:', error)
      ElMessage.error('Failed to delete')
    }
  }
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await recordApi.updateRecord(formData.owner, formData.name, formData)
      ElMessage.success('Updated successfully')
    } else {
      await recordApi.addRecord(formData)
      ElMessage.success('Added successfully')
    }
    dialogVisible.value = false
    await fetchRecords()
  } catch (error) {
    console.error(isEdit.value ? 'Failed to update record:' : 'Failed to add record:', error)
    ElMessage.error(isEdit.value ? 'Failed to update' : 'Failed to add')
  }
}

onMounted(() => {
  fetchRecords()
})
</script>

<template>
  <div class="records-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Records Management</span>
          <el-button type="primary" @click="handleAdd">Add Record</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="records" style="width: 100%">
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="owner" label="Owner" />
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
        <el-form-item label="Organization">
          <el-input v-model="formData.organization" />
        </el-form-item>
        <el-form-item label="Client IP">
          <el-input v-model="formData.clientIp" />
        </el-form-item>
        <el-form-item label="User Agent">
          <el-input v-model="formData.userAgent" />
        </el-form-item>
        <el-form-item label="User">
          <el-input v-model="formData.user" />
        </el-form-item>
        <el-form-item label="Method">
          <el-input v-model="formData.method" />
        </el-form-item>
        <el-form-item label="Request URI">
          <el-input v-model="formData.requestUri" />
        </el-form-item>
        <el-form-item label="Action">
          <el-input v-model="formData.action" />
        </el-form-item>
        <el-form-item label="Language">
          <el-input v-model="formData.language" />
        </el-form-item>
        <el-form-item label="Region">
          <el-input v-model="formData.region" />
        </el-form-item>
        <el-form-item label="City">
          <el-input v-model="formData.city" />
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
.records-container {
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
