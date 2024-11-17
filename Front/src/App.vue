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
    margin-bottom: 20px; /* マージンを減らしてコンパクトに */
    background-color: #3a3a3a; /* ヘッダーの背景色 */
    color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.logo img {
    height: 80px; /* ロゴの高さを減らす */
}

.title h1 {
    margin: 0;
    font-size: 27px; /* タイトルのフォントサイズを減らす */
    margin-right: 30px;
}

.menu {
    cursor: pointer;
    padding: 5px; /* メニューのパディングを減らす */
    margin-left: 20px;
    margin-right: auto;
}

.bar {
    display: block;
    width: 40px; /* バーの幅を減らす */
    height: 5px;
    margin: 5px auto; /* バーの間隔を減らす */
    background-color: white;
}

.dropdown {
    position: absolute;
    left: 0; /* 左側に配置 */
    top: 100px; /* ヘッダーの下に配置 */
    width: 15%; /* 画面の3分の1を占める */
    height: calc(100% - 100px); /* 高さを100%からヘッダーの高さを引いた分に設定 */
    background-color: #ffffff;
    border-right: 1px solid #ffffff;
    box-shadow: 7px 0 5px rgba(0, 0, 0, 0.2);
    z-index: 1000; /* メニューが他の要素の上に表示されるように */
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
    background-color: #f9f9f9; /* ホバー時の背景色 */
}

.content {
    padding: 20px;
    transition: margin-left 0.3s ease; /* スライドアニメーション */
}
</style>