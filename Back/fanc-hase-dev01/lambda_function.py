import boto3
import json
import pymysql
import os
from botocore.config import Config

comprehend = boto3.client('comprehend')
translate = boto3.client('translate')

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
    
    body = event
    feedback = body['feedback']
    product = body['product']
    
    # フィードバックを翻訳
    translated_feedback = translate.translate_text(
        Text=feedback,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )['TranslatedText']
    
    # sentiment分析
    sentiment_response = comprehend.detect_sentiment(
        Text=feedback,
        LanguageCode='ja'
    )
    sentiment = convert_sentiment(sentiment_response['Sentiment'])

    # targeted_sentiment分析
    sentiment_targeted_response = comprehend.detect_targeted_sentiment(
        Text=translated_feedback,
        LanguageCode='en'
    )
    
    # 翻訳後の各単語を日本語に戻す
    translated_targeted_sentiment = {
        translate.translate_text(
            Text=mention['Text'],
            SourceLanguageCode='en',
            TargetLanguageCode='ja'
        )['TranslatedText']: convert_sentiment(mention['MentionSentiment']['Sentiment'])
        for entity in sentiment_targeted_response['Entities']
        for mention in entity['Mentions']
    }
    
    cur.execute("INSERT INTO feedback (feedback_text, emotion, product_id) VALUES (%s, %s, %s)", (feedback, sentiment, product))
    feedback_id = cur.lastrowid
    conn.commit()
    
    for translated_text, sentiment in translated_targeted_sentiment.items():
        if "私" not in translated_text:
            cur.execute("INSERT INTO feedback_detail (feedback_id, split_text, split_emotion) VALUES (%s, %s, %s)", (feedback_id, translated_text, sentiment))
    
    conn.commit() 

    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': {
            'feedback': feedback,
            'sentiment': sentiment,
            'targeted_sentiment': translated_targeted_sentiment
        }

    }


# 各sentimentを日本語に変換
def convert_sentiment(sentiment):
    sentiment_map = {
        'POSITIVE': '肯定的',
        'NEGATIVE': '否定的',
        'NEUTRAL': '中立',
        'MIXED': '混合'
    }
    return sentiment_map.get(sentiment, sentiment)