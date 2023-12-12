import http.client
import json
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertForSequenceClassification
from googletrans import Translator
import pandas as pd
import matplotlib.pyplot as plt


categories = ['general', 'health', 'economy', 'world', 'technology']

for category in categories:
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 3AnueuwpbrHKJtAWgpvp5N:2a7gv6X0nteuoaIGM1fN7V"
    }

    conn.request("GET", f"/news/getNews?country=tr&tag={category}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # JSON verilerini al ve bir liste oluştur
    json_data = json.loads(data.decode("utf-8"))
    news_list = json_data.get('result', [])

    # CSV dosyası oluştur ve verileri yaz
    csv_file = f'news_{category}_data.csv'

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'description', 'url'])
        writer.writeheader()

        for news in news_list:
            writer.writerow({'title': news.get('title', ''),
                             'description': news.get('description', ''),
                             'url': news.get('url', '')})


for category in categories:
    # Veri setini yükleme (örnek olarak CSV dosyası kullanılıyor)
    df = pd.read_csv(f'news_{category}_data.csv')

    # BERT tokenizer'ını yükleme
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Çeviri için Google Translator
    translator = Translator()

    # Duygu analizi için duygu listesi
    sentiments = {'Pozitif': 0, 'Nötr': 0, 'Negatif': 0}

    # Her bir satırdaki cümleleri işleme
    for index, row in df.iterrows():
        description = row['description']
        
        try:
            # Eğer description alanı boş değilse
            if pd.notnull(description) and isinstance(description, str):
                # Metni tokenlara ayırma ve çeviri
                tokens = tokenizer.encode(description, add_special_tokens=True, truncation=True, padding=True)
                translated_description = translator.translate(description, src='tr', dest='en').text

                # Duygu analizi
                blob = TextBlob(translated_description)
                polarity = blob.sentiment.polarity

                # Pozitif, negatif, nötr sonuçları say
                if polarity > 0:
                    sentiments['Pozitif'] += 1
                elif polarity < 0:
                    sentiments['Negatif'] += 1
                else:
                    sentiments['Nötr'] += 1
            else:
                print("Boş Açıklama")
        except Exception as e:
            print(f"Hata oluştu: {e}")

    # Grafik oluştur
    labels = sentiments.keys()
    sizes = [sentiments[label] for label in labels]
    colors = ['blue', 'grey', 'red']

    plt.figure(figsize=(8, 6))
    plt.bar(labels, sizes, color=colors)
    plt.ylabel('Miktar')
    plt.title(f'{category} Konu Başlıklı Haberlerin Duygu Analizi')
    plt.show()

