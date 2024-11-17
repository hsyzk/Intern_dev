import pymysql
import os
import json

# 環境変数設定済み
endpoint = os.environ['db_endpoint']
username = os.environ['db_username']
password = os.environ['db_password']
dbname = os.environ['db_name']

def lambda_handler(event, context):
    # DB接続設定
    conn = pymysql.connect(
        database=dbname,
        user=username,
        password=password,
        host=endpoint
    )
    cur = conn.cursor()

    # リクエストボディからproductを取得
    body = event
    productid = body['product']

    try:
        if productid:
            # productが指定されている場合
            cur.execute("""
                SELECT f.feedback_id, f.feedback_text, f.product_id, fd.split_text, fd.split_emotion
                FROM feedback f
                LEFT JOIN feedback_detail fd ON f.feedback_id = fd.feedback_id
                WHERE f.product_id = %s
            """, (productid,))
        else:
            # productが指定されていない場合
            cur.execute("""
                SELECT f.feedback_id, f.feedback_text, f.product_id, fd.split_text, fd.split_emotion
                FROM feedback f
                LEFT JOIN feedback_detail fd ON f.feedback_id = fd.feedback_id
            """)

        results = cur.fetchall()

        # 結果を整形
        feedback_list = []
        for row in results:
            feedback_id = row[0]
            feedback_text = row[1]
            product_id = row[2]
            translated_text = row[3]
            sentiment = row[4]

            feedback_entry = {
                'feedback_id': feedback_id,
                'feedback_text': feedback_text,
                'product_id': product_id,
                'details': []
            }

            # feedback_detailが存在する場合は追加
            if translated_text is not None:
                feedback_entry['details'].append({
                    'translated_text': translated_text,
                    'sentiment': sentiment
                })

            feedback_list.append(feedback_entry)

        return {
            'statusCode': 200,
            'body': feedback_list
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        cur.close()
        conn.close()