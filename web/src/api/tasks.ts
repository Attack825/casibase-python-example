// Copyright 2025 The Casibase Authors. All Rights Reserved.

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import api from './config'

export interface Task {
  owner: string
  name: string
  createdTime: string
  displayName: string
  provider?: string
  providers?: string[]
  type?: string
  subject?: string
  topic?: string
  result?: string
  activity?: string
  grade?: string
  application?: string
  path?: string
  text?: string
  example?: string
  labels?: string[]
  log?: string
}

export interface CreateTaskParams {
  owner: string
  name: string
  createdTime: string
  displayName: string
  provider?: string
  type?: string
  subject?: string
  topic?: string
  status?: string
}

export const taskApi = {

  getTasks(owner: string) {
    return api.get<Task[]>('/get-tasks', { params: { owner } })
  },

  getTask(owner: string, name: string) {
    return api.get<Task>('/get-task', { params: { id: `${owner}/${name}` } })
  },

  addTask(params: CreateTaskParams) {
    return api.post<Task>('/add-task', params)
  },

  updateTask(owner: string, name: string, params: CreateTaskParams) {
    return api.post<Task>('/update-task', params, { params: { id: `${owner}/${name}` } })
  },

  deleteTask(owner: string, name: string) {
    return api.post('/delete-task', {}, { params: { id: `${owner}/${name}` } })
  }
}
