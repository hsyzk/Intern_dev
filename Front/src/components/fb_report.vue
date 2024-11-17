<template>
    <div class="fb_report">
        <h1>フィードバック分析結果</h1>
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
    </div>
</template>

<script>
export default {
    name: 'FbRreport',
    data() {
        return {
            isChecked: true // チェックボックスの状態を管理するデータプロパティ
        };
    },
    watch: {
        isChecked(newValue) {
            if (newValue) {
                this.product = null; // isCheckedがfalseのときproductにnullを代入
            }
        }
    },
    created() {
        this.getproductlist()
    },
    methods: {
        async getproductlist() {
            try{
                const get = await fetch('https://01ea74ont4.execute-api.us-east-1.amazonaws.com/stage-hase',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        product: this.product,
                    })
                })
                const data = await get.json()
                this.productlist = data.body;
                console.log('APIレスポンス:',data.body)
            } catch (error) {
                console.error('APIリクエストエラー:', error)
            }
        },
    }
};
</script>

<style scoped>
.fb_report {
    align-items: center;
}
</style>