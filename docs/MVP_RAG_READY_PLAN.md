# Smart Note Extractor: MVP + RAG-Hazir Plan

## 1. Urun Hedefi

Sunlari yapabilen bir AI not cikarma uygulamasi gelistirmek:

1. Dokuman yukleme (`pdf`, `txt`, daha sonra `docx`)
2. Ozet uretimi (`short`, `medium`, `long`)
3. Madde madde not uretimi
4. Anahtar kelime cikarma
5. Cekirdek pipeline'i yeniden yazmadan RAG tabanli Soru-Cevap sistemine genisleyebilme

## 2. Algoritma Karari (MVP)

V1 icin deterministik puanlamaya dayali hibrit bir extractive pipeline kullan.

### 2.1 Ozet

- Birincil yontem: TF-IDF cumle puanlama + konum bonusu + top-k cumle secimi
- Opsiyonel iyilestirme: Uzun dokumanlarda TextRank ile extractive ozetleme
- Cikti: Kaynak cumlelere dayali, gercekci ve izlenebilir ozet

MVP icin bu secimin nedeni:

- Hizli ve dusuk maliyetli
- Uretimde stabil
- Debug ve degerlendirme kolay

### 2.2 Anahtar Kelimeler

- Birincil yontem: Cok dilli embedding ile `KeyBERT`
- Fallback: TF-IDF n-gram (mevcut kod stiline uyumlu)
- Cikti: En iyi anahtar kelime ve anahtar ifade listesi

MVP icin bu secimin nedeni:

- Sadece TF-IDF'e gore daha kaliteli phrase ciktisi
- Modelin calismadigi durumlarda fallback yolunu korur

### 2.3 Notlar

- Aday havuzu: Ozet puanlayicisindan gelen yuksek skorlu cumleler
- Secim stratejisi: Kapsami artirip tekrar oranini dusurme (MMR benzeri secim)
- Cikti: 3-10 arasi madde not listesi

### 2.4 Dil Stratejisi

- On-isleme sirasinda dil tespiti (`tr`, `en`)
- Turkce tokenizer kalitesi dusukse regex fallback cumle bolucu kullan

## 3. RAG Kullanmali miyiz?

Kisa cevap: MVP ozetleme icin zorunlu degil, ama ikinci faz ozellikler icin cok faydali.

RAG su durumlarda kullanilmali:

- Dokumanlar buyuk ve cok sayida ise
- Kullanici yuklenen dokumanlar uzerinden soru soracaksa
- Kaynak gosterimli, takip edilebilir cevap gerekiyorsa

MVP teslimini RAG'e baglayip geciktirme.

## 4. RAG-Hazir Mimari (Simdi Tasarla, Sonra Aktif Et)

Veri modellerini simdiden RAG'e uygun tasarla ki sonra minimum refaktor ile entegre edilebilsin.

### 4.1 Pipeline Asamalari

1. `validate_file`
2. `extract_text`
3. `clean_text`
4. `segment_text` (cumleler + chunk'lar)
5. `score_sentences`
6. `generate_summary`
7. `generate_notes`
8. `extract_keywords`
9. `build_response`

### 4.2 Chunk Metadata Sozlesmesi

Her chunk su alanlari tasimali:

- `doc_id`
- `chunk_id`
- `page` (varsa)
- `start_char`
- `end_char`
- `section` (opsiyonel)
- `text`

Bu metadata, ileride vector DB indexleme ve kaynak gosterimi icin yeterlidir.

## 5. Onerilen Backend Yapisi (Sifirdan)

```text
backend/
	app/
		api/
			routes.py
		core/
			config.py
			logging.py
		pipeline/
			orchestrator.py
		services/
			file_validation.py
			text_extraction.py
			text_cleaning.py
			segmentation.py
			sentence_scoring.py
			summary_generation.py
			notes_generation.py
			keyword_extraction.py
			language_detection.py
		schemas/
			request.py
			response.py
			domain.py
		tests/
			test_api.py
			test_pipeline.py
```

## 6. API Sozlesmesi (MVP)

### 6.1 Request

`POST /analyze` (multipart form-data)

- `file`: pdf/txt
- `summary_type`: `balanced` | `keywords_first`
- `summary_length`: `short` | `medium` | `long`

### 6.2 Response

```json
{
	"summary": "...",
	"notes": ["...", "..."],
	"keywords": ["...", "..."],
	"metadata": {
		"doc_id": "uuid",
		"file_name": "lecture1.pdf",
		"language": "tr",
		"sentence_count": 120,
		"chunk_count": 18,
		"summary_type": "balanced",
		"summary_length": "medium"
	}
}
```

## 7. Iki Haftalik Gelistirme Plani

## 1. Hafta

1. Gun 1: Temiz backend klasor yapisi ve schema'lari olustur
2. Gun 2: Dosya dogrulama + text extraction (`pdf`, `txt`) gelistir
3. Gun 3: Text cleaning + segmentation + dil tespiti ekle
4. Gun 4: Cumle puanlama + ozet uretimini tamamla
5. Gun 5: Not uretimi + anahtar kelime cikarmayi ekle
6. Gun 6: `/analyze` endpoint'i ve hata yonetimini ekle
7. Gun 7: Servis unit testleri ve endpoint smoke testleri yaz

## 2. Hafta

1. Gun 8: Frontend upload akisina `/analyze` baglantisini yap
2. Gun 9: Sonuc UI kartlarini yap (ozet, notlar, anahtar kelimeler, metadata)
3. Gun 10: Loading/error/empty state'leri ekle
4. Gun 11: Performans guardrail'leri ekle (dosya boyutu, timeout, cumle limiti)
5. Gun 12: Kalite kontrolleri ve ornek regresyon dokumanlari hazirla
6. Gun 13: RAG-hazir chunk metadata persistence arayuzunu hazirla
7. Gun 14: Son refaktor + dokumantasyon + demo script

## 8. RAG Faz-2 (MVP Sonrasi)

MVP stabil oldugunda su adimlari ekle:

1. Chunk embedding uretimi
2. Vector DB (`Chroma` lokal MVP icin, `Qdrant` olceklenebilir secenek icin)
3. Retrieval katmani (top-k + re-ranking)
4. Yeni endpoint: `POST /ask` (kaynak gosterimli)

`/ask` cikti formati su alanlari icermeli:

- `answer`
- `sources` (chunk id ve sayfa referanslari)

## 9. Tamamlanma Kriteri (MVP)

MVP su kosullar saglandiginda tamam sayilir:

1. Kullanici pdf/txt yukler ve summary, notes, keywords alir
2. Kucuk dokumanlarda uctan uca yanit suresi kabul edilebilir seviyededir
3. Hata mesajlari acik ve aksiyona donuktur
4. Cekirdek pipeline icin en az temel test kapsami vardir
5. Gelecekteki RAG icin chunk metadata response yolunda veya ic modelde mevcuttur

