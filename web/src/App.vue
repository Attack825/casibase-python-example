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
import { RouterView } from "vue-router";
import { ref } from "vue";

const activeIndex = ref("/records");
</script>

<template>
  <el-container>
    <el-header>
      <div class="header-content">
        <h1>casibase-python-example-web</h1>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          router
          background-color="#ffffff"
          text-color="#303133"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/records">records</el-menu-item>
          <el-menu-item index="/stores">stores</el-menu-item>
          <el-menu-item index="/tasks">tasks</el-menu-item>
        </el-menu>
      </div>
    </el-header>

    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped>
.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  flex-wrap: nowrap;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.el-menu {
  border: none;
  flex: 1;
  justify-content: flex-end;
  min-width: 400px;
}

.el-menu-item {
  min-width: auto !important;
}

.el-main {
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
  padding: 20px;
}

h1 {
  margin: 0;
  font-size: 1.5em;
  color: #409eff;
  white-space: nowrap;
  margin-right: 20px;
}

@media screen and (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 10px 0;
  }

  .el-menu {
    width: 100%;
    min-width: auto;
    margin-top: 10px;
  }

  .el-header {
    height: auto;
    line-height: normal;
  }
}
</style>
