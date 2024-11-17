<template>
  <div class="container">
    <header class="header">
        <div class="menu" @click="toggleMenu">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </div>
        <div class="logo">
            <img src="./assets/logo.png" alt="ロゴ" />
        </div>
        <div class="title">
            <h1>顧客フィードバック分析</h1>
        </div>
    </header>
    <div class="dropdown" v-if="isMenuOpen">
        <ul>
            <li @click="switchComponent('FeedBack')">フィードバック送信</li>
            <li @click="switchComponent('FbAnalyze')">フィードバック一覧</li>
        </ul>
    </div>
    <div class="content" :class="{ 'content-shift': isMenuOpen }">
        <component :is="currentComponent" />
    </div>
  </div>
</template>

<script>
import FeedBack from './components/feedback.vue'
import FbAnalyze from './components/fb_analyze.vue'

export default {
  name: 'App',
  components: {
    FeedBack,
    FbAnalyze,
  },
  data() {
    return {
      currentComponent: 'FeedBack',
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    switchComponent(component) {
      this.currentComponent = component;
      this.isMenuOpen = false;
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
.container {
  margin: 0;
  padding: 0;
}

.header {
    display: flex;
    height: 100px;
    padding: 0px;
    align-items: center;
    margin-bottom: 20px;
    background-color: #3a3a3a;
    color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.logo img {
    height: 80px;
}

.title h1 {
    margin: 0;
    font-size: 27px;
    margin-right: 30px;
}

.menu {
    cursor: pointer;
    padding: 5px;
    margin-left: 20px;
    margin-right: auto;
}

.bar {
    display: block;
    width: 40px;
    height: 5px;
    margin: 5px auto;
    background-color: white;
}

.dropdown {
    position: absolute;
    left: 0;
    top: 100px;
    width: 15%;
    height: calc(100% - 100px);
    background-color: #ffffff;
    border-right: 1px solid #ffffff;
    box-shadow: 7px 0 5px rgba(0, 0, 0, 0.2);
    z-index: 1000;
}

.dropdown ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.dropdown li {
    padding: 20px 20px;
    font-size: 20px;
    cursor: pointer;
}

.dropdown li:hover {
    background-color: #f9f9f9;
}

.content {
    padding: 20px;
    transition: margin-left 0.3s ease;
}
</style>
