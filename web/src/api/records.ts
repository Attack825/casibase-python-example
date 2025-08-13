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

export interface Record {
  owner: string
  name: string
  createdTime: string
  organization?: string
  clientIp?: string
  userAgent?: string
  user?: string
  method?: string
  requestUri?: string
  action?: string
  language?: string
  region?: string
  city?: string
}

export interface CreateRecordParams {
  owner: string
  name: string
  createdTime: string
  organization?: string
  clientIp?: string
  userAgent?: string
  user?: string
  method?: string
  requestUri?: string
  action?: string
  language?: string
  region?: string
  city?: string
}

interface RecordResponse {
  items: Record[]
  total: number
}

export const recordApi = {

  getRecords(pageSize: string = "100", p: string = "1") {
    return api.get<RecordResponse>('/get-records', { params: { page_size: pageSize, p } })
  },

  getRecord(owner: string, name: string) {
    return api.get<Record>('/get-record', { params: { id: `${owner}/${name}` } })
  },

  addRecord(params: CreateRecordParams) {
    return api.post<Record>('/add-record', params)
  },

  updateRecord(owner: string, name: string, params: CreateRecordParams) {
    return api.post<Record>('/update-record', params, { params: { id: `${owner}/${name}` } })
  },

  deleteRecord(name: string) {
    return api.post('/delete-record', {}, { params: { id: `${name}` } })
  }
}
