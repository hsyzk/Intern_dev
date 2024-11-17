<template>
    <div>
        <h1>フィードバック</h1>
        <div class="feedback-space">
            <div>
                <label>商品を選択してください</label>
                <select v-model="product">
                    <option v-for="product in productlist" :key="product.product_id" :value="product.product_id">{{ product.product_name }}</option>
                </select>
            </div>
            <textarea v-model="feedback" placeholder="フィードバックを入力してください..."></textarea>
            <button @click="submitFeedBack">送信</button>
        </div>
        <div v-if="report" class="feedback-space">
            <!-- ここをlambdaに合わせて変更する(ターゲット分析) -->
            <h2>フィードバック分析結果</h2>
            <p>フィードバック: {{ report.body.sentiment }}</p>
            <template v-if="report.body.targeted_sentiment">
                <div v-for="(value, key) in report.body.targeted_sentiment" :key="key">
                    {{ key }} : {{ value }}
                </div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FeedbackForm',
    data() {
        return {
            feedback: '',
            product: '',
            productlist: [],
            report: null,
        };
    },
    created() {
        this.getproductlist()
    },
    methods: {
        async submitFeedBack() {
            try{
                const response = await fetch('https://ox9dywe4wl.execute-api.us-east-1.amazonaws.com/stage-hase-dev01', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        feedback: this.feedback,
                        product: this.product,
                    })
                });
                if (!response.ok) {
                    throw new Error(`HTTPエラー: ${response.status}`);
                }
                this.report = await response.json();
                console.log("report", this.report);
            } catch (error) {
                console.error('APIリクエストエラー:', error)
            }
        },
        async getproductlist() {
            try{
                const get = await fetch('https://01ea74ont4.execute-api.us-east-1.amazonaws.com/stage-hase',{
                    method: 'GET',
                })
                const data = await get.json()
                this.productlist = data.body;
                console.log('APIレスポンス:',data.body)
            } catch (error) {
                console.error('APIリクエストエラー:', error)
            }
        },
    },
}
</script>

<style scoped>
.feedback-space {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}
.feedback-space h2 {
    font-size: 1.5rem;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    margin-top: 100px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

select {
    width: 50%;
    height: 20px;
    margin-bottom: 10px;
    text-align: center;
    font-size: 1rem;
}

textarea {
    width: 100%;
    height: 140px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: none;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 10px;
}

button:hover {
    background-color: #238328;
}

.report-section {
    background-color: #e7f3fe;
    padding: 10px;
    border-radius: 4px;
    margin-top: 20px;
}
</style>