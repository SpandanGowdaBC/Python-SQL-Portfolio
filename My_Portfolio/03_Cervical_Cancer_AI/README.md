# 🔬 Cervical Cancer Detection System (Computer Vision)

### **Project Overview**
This project automates the classification of Pap smear cells into 7 categories (dysplastic vs normal) to assist medical diagnosis using Deep Learning.

---

### **⚠️ Dataset Information**
**Note:** Due to the large size of the medical imaging dataset (Herlev Pap Smear Dataset), the raw images are not hosted in this repository.
* **Data Source:** Search in kaggle for the dataset and the the dataset balacing and augmentation code is already given in the file.
* **Preprocessing:** The dataset was balanced using data augmentation (rotation, zoom, flips) to ~1,800 images per class.

---

### **Key Results**
I trained and benchmarked three architectures. The **Vision Transformer (ViT)** achieved the highest accuracy.

| Model Architecture | Framework | Test Accuracy |
| :--- | :--- | :--- |
| **Vision Transformer (ViT)** | PyTorch | **98.68%** 🏆 |
| **Custom CNN** | TensorFlow | 97.85% |
| **EfficientNetB0** | TensorFlow | 96.67% |

### **File in this Repository**
* `analysis_notebook.ipynb`: The Python code for the CNN, EfficientNet, and ViT models.
The full training and evaluation pipeline.

### ** Technologies Used**
* **Deep Learning:** PyTorch, TensorFlow, Keras, Transformers (HuggingFace)
* **Explainable AI:** GradCAM (for heatmap visualization)
* **Processing:** OpenCV, NumPy, Pandas

### ** visualizations**
GRADCAM1 IMAGE
<img width="640" height="467" alt="image" src="https://github.com/user-attachments/assets/7215d814-b72c-40a8-8595-5f9264e89cec" />

GRADCAM2 IMAGE
<img width="627" height="658" alt="image" src="https://github.com/user-attachments/assets/6999e97a-5a2c-48dc-bd28-52b122544b1e" />

