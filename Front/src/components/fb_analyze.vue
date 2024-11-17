<template>
    <div class="fb_analyze">
        <h1>フィードバック一覧</h1>
        <div class="product_select">
            <label>
                <input type="checkbox" v-model="isChecked" />
                全商品を表示
            </label>
            <template v-if="!isChecked">
                <div>
                    <label>商品を選択してください</label>
                    <select v-model="product">
                        <option v-for="product in productlist" :key="product.product_id" :value="product.product_id">{{ product.product_name }}</option>
                    </select>
                </div>
            </template>
        </div>
        <div v-if="feedbackList.length > 0">
            <div v-for="product in filteredProductList" :key="product.product_id">
                <h3>{{ product.product_name }}</h3>
                <div v-for="feedback in feedbackList.filter(f => f.product_id === product.product_id)" :key="feedback.feedback_id">
                    <p v-if="isUniqueFeedback(feedback.feedback_id)">{{ feedback.feedback_text }}: {{ feedback.emotion }}</p>
                    <ul>
                        <li v-for="(detail, index) in feedback.details" :key="`${feedback.feedback_id}-${index}`">
                            <span>対象: {{ detail.translated_text }}</span> - <span>{{ detail.sentiment }}</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div v-else>
            <p>フィードバックがありません。</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FbAnalyze',
    data() {
        return {
            product: null,
            isChecked: true,
            feedbackList: [],
            uniqueFeedbacks: new Set()
        };
    },
    computed: {
        filteredProductList() {
            return this.isChecked ? this.productlist : this.productlist.filter(product => product.product_id === this.product);
        }
    },
    watch: {
        isChecked(newValue) {
            if (newValue) {
                this.product = null;
                this.fetchFeedback();
            }
        },
        product(newValue) {
            if (newValue) {
                this.fetchFeedback();
            }
        }
    },
    created() {
        this.getproductlist();
        this.fetchFeedback();
    },
    methods: {
        async getproductlist() {
            try {
                const get = await fetch('https://01ea74ont4.execute-api.us-east-1.amazonaws.com/stage-hase', {
                    method: 'GET'
                });
                const data = await get.json();
                this.productlist = data.body;
                console.log('APIレスポンス:', data.body);
            } catch (error) {
                console.error('APIリクエストエラー:', error);
            }
        },
        async fetchFeedback() {
            try {
                const response = await fetch('https://tstxafiscb.execute-api.us-east-1.amazonaws.com/stage-hase', { // Lambda関数のエンドポイントを指定
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        product: this.product
                    })
                });
                const data = await response.json();
                this.feedbackList = data.body; // APIからのレスポンスをフィードバックリストに格納
                console.log('フィードバックレスポンス:', this.feedbackList);
                this.uniqueFeedbacks.clear(); // 新しいフィードバックを取得したらセットをクリア
            } catch (error) {
                console.error('フィードバック取得エラー:', error);
            }
        },
        isUniqueFeedback(feedbackText) {
            if (this.uniqueFeedbacks.has(feedbackText)) {
                return false;
            } else {
                this.uniqueFeedbacks.add(feedbackText);
                return true;
            }
        }
    }
};
</script>

<style scoped>
.fb_analyze {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.product_select {
    margin-bottom: 20px;
}

h1, h3 {
    color: #333;
}

p {
    color: #666;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    background-color: #e9ecef;
    margin: 5px 0;
    padding: 10px;
    border-radius: 5px;
}
</style>