# 🛒 Divar AI Smart Listing Assistant

An AI-powered pipeline for classifieds listings (Divar-style). A user uploads a photo of an item, adds a short description and a few extra details, and the system automatically:

1. **Recognizes the product category** from the photo,
2. **Assesses the item's condition** from the description,
3. **Estimates an approximate price** in Toman.

The system is built from **three specialized models** working together.

---

## 📑 Table of Contents

- [How It Works](#-how-it-works)
- [Use Cases](#-use-cases)
- [Supported Categories](#-supported-categories)
- [Model 1: Image Classification](#-model-1-image-classification)
- [Model 2: Text Condition Classification](#-model-2-text-condition-classification)
- [Model 3: Price Regression](#-model-3-price-regression)
- [Evaluation Metrics Explained](#-evaluation-metrics-explained)
- [Supported Image Formats](#-supported-image-formats)

---

## 🔄 How It Works

```
 ┌────────────────┐     ┌──────────────────────┐
 │  Upload photo  │────▶│ Model 1: Image       │──▶ Product category
 └────────────────┘     │ Classification       │
                        └──────────────────────┘

 ┌────────────────────────────┐   press "Processing"
 │ Description + extra info   │───────────────┐
 │ (brand, age, appearance,   │               │
 │  city)                     │               ▼
 └────────────────────────────┘     ┌──────────────────────┐
              │                      │ Model 2: Text        │──▶ Item condition
              │ description          │ Classification       │
              └─────────────────────▶└──────────────────────┘
              │
              │ extra info (brand, age, appearance, city)
              ▼
        ┌──────────────────────┐
        │ Model 3: Price       │──▶ Estimated price (Toman)
        │ Regression           │
        └──────────────────────┘
```

**Step by step:**

1. The user uploads a photo using the **Upload** button.
2. **Model 1** identifies which category the photo belongs to.
3. The user writes a description and fills in the extra details:
   - **Brand**
   - **Age of the item**
   - **Visual condition:** `Poor` · `Fair` · `Good` · `Like New`
   - **City**
4. The user presses the **Processing** button.
5. The description is sent to **Model 2**, which determines the item's condition.
6. The extra details are sent to **Model 3**, which estimates the approximate price.

---

## 🎯 Use Cases

| Use Case | Description | Model Used |
|----------|-------------|------------|
| **Automatic categorization** | The seller only uploads a photo; the product category (refrigerator, bicycle, sofa, TV or laptop) is detected automatically, so no manual category selection is needed. | Image Classification |
| **Condition assessment** | The seller's free-text description is analyzed to decide whether the item is *healthy and usable*, *needs repair*, or *suitable for parts*. Buyers can filter listings by condition. | Text Classification |
| **Price suggestion** | Brand, age, visual condition (poor / fair / good / like new) and city are used to suggest a realistic price, helping sellers avoid over- or under-pricing. | Price Regression |
| **Faster listing creation** | One upload plus one description and a few details produce category, condition and price in a single **Processing** step. | All three models |
| **Better buyer experience** | Buyers get consistent, trustworthy categories, condition labels and fair price references across listings. | All three models |
| **Repair and parts marketplace** | Items labeled *needs repair* or *suitable for parts* can be routed to repair shops or buyers looking for spare parts. | Text Classification |

---

## 📦 Supported Categories

| # | Category | Example |
|---|----------|---------|
| 1 | 🧊 Refrigerator | ![Refrigerator](assets/refrigerator.svg) |
| 2 | 🚲 Bicycle | ![Bicycle](assets/bicycle.svg) |
| 3 | 🛋️ Sofa | ![Sofa](assets/sofa.svg) |
| 4 | 📺 TV | ![TV](assets/tv.svg) |
| 5 | 💻 Laptop | ![Laptop](assets/laptop.svg) |

---

## 🖼️ Model 1: Image Classification

Classifies an uploaded photo into one of five product categories: **Refrigerator, Bicycle, Sofa, TV, Laptop**.

### Evaluation Setup

The model was tested on **5 different images per class** (25 images in total).

### Results

| Class | Precision |
|-------|:---------:|
| Refrigerator | **100%** |
| Bicycle | **100%** |
| Sofa | **100%** |
| TV | **100%** |
| Laptop | **100%** |

| Overall Metric | Value |
|----------------|:-----:|
| **Accuracy** | **100%** |

### Confusion Matrix

![Confusion matrix of the image classification model (5×5)](assets/confusion_matrix_image_model.png)

All 5 test images of every class were classified correctly, so every value off the diagonal is zero.

---

## 📝 Model 2: Text Condition Classification

Reads the user's description and predicts the item's condition as one of three classes:

| Class | Meaning |
|-------|---------|
| 1 | ✅ Healthy and usable |
| 2 | 🔧 Needs repair |
| 3 | 🧩 Suitable for parts |

### Results

| Metric | Value |
|--------|:-----:|
| **Precision** | **100%** |
| **Accuracy** | **100%** |

### Confusion Matrix

![Confusion matrix of the text classification model (3×3)](assets/confusion_matrix_text_model.png)

The matrix is perfectly diagonal: 342, 343 and 315 samples were correctly assigned to classes 1, 2 and 3 respectively, with no misclassifications.

---

## 💰 Model 3: Price Regression

Estimates the approximate price of the item (in **Toman**) from the extra information provided by the user (brand, age, visual condition, city) together with the product category.

### Results

| Metric | Full Name | Value | Unit |
|--------|-----------|------:|:----:|
| **RMSE** ⭐ | Root Mean Squared Error | **± 5,804,331** | Toman |
| **MAE** | Mean Absolute Error | ± 4,580,710 | Toman |
| **MSE** | Mean Squared Error | ± 33,690,263,219,430 | Toman² |

> ⭐ **RMSE is the primary metric** for this model. In plain terms: the model's typical price estimate is off by roughly **5.8 million Toman**.

---

## 📐 Evaluation Metrics Explained

Let **yᵢ** be the true price, **ŷᵢ** the predicted price, and **n** the number of samples.

### 1. RMSE — Root Mean Squared Error ⭐ (primary metric)

$$
\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2}
$$

**What it tells you:**

- It measures the typical size of the prediction error **in the same unit as the target** (Toman), which makes it easy to interpret.
- Because errors are squared before averaging, **large mistakes are penalized more heavily** than small ones. This matters for price estimation, where a few badly wrong estimates (e.g., a laptop priced as a sofa) hurt users the most.
- Lower is better; `0` would mean perfect predictions.

**In this project:** RMSE = **± 5,804,331 Toman**. Since RMSE is larger than MAE, a small number of larger errors are present, and RMSE highlights them. It is the number to watch when comparing model versions.

### 2. MAE — Mean Absolute Error

$$
\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}\left|y_i - \hat{y}_i\right|
$$

**What it tells you:**

- The average absolute gap between predicted and true price, in Toman.
- Every error counts proportionally, so it is **less sensitive to outliers** than RMSE.
- Useful as an "average miss" figure that is easy to explain to non-technical readers.

**In this project:** MAE = **± 4,580,710 Toman**.

### 3. MSE — Mean Squared Error

$$
\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2
$$

**What it tells you:**

- The average of the squared errors. It is the quantity most training procedures minimize because it is smooth and easy to differentiate.
- Its unit is **Toman²**, so it is not directly interpretable. This is why RMSE (its square root) is preferred for reporting.

**In this project:** MSE = **± 33,690,263,219,430 Toman²**, and √MSE gives the RMSE above.

### Quick Comparison

| Metric | Unit | Outlier Sensitivity | Best Used For |
|--------|:----:|:-------------------:|---------------|
| **RMSE** ⭐ | Toman | High | Main reporting metric; penalizing big mistakes |
| **MAE** | Toman | Low | Simple "average error" explanation |
| **MSE** | Toman² | High | Training / optimization |

### Classification Metrics (Models 1 & 2)

- **Accuracy** = (correct predictions) ÷ (all predictions)
- **Precision** (per class) = TP ÷ (TP + FP), the share of items predicted as a class that truly belong to it
- **Confusion matrix:** a table of true classes (rows) vs. predicted classes (columns). A perfectly diagonal matrix means no mistakes.

---

## 🖼️ Supported Image Formats

The image classifier can read **all common image formats** (e.g., JPG/JPEG, PNG, BMP, TIFF) **except WEBP and GIF**.

| Format | Supported |
|--------|:---------:|
| JPG / JPEG | ✅ |
| PNG | ✅ |
| BMP | ✅ |
| TIFF | ✅ |
| **WEBP** | ❌ |
| **GIF** | ❌ |

> If you have a `.webp` or `.gif` image, convert it to JPG or PNG before uploading.

---

## 📁 Repository Assets

```
.
├── README.md
└── assets/
    ├── confusion_matrix_image_model.png   # 5×5, image classification model
    ├── confusion_matrix_text_model.png    # 3×3, text classification model
    ├── refrigerator.svg                   # example illustration
    ├── bicycle.svg                        # example illustration
    ├── sofa.svg                           # example illustration
    ├── tv.svg                             # example illustration
    └── laptop.svg                         # example illustration
```
