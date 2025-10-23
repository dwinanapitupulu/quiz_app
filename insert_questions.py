from database import get_db

questions = [
    {
        "question": "Apa tujuan utama dari Artificial Intelligence (AI)?",
        "option1": "Menggantikan sistem operasi komputer",
        "option2": "Membuat mesin mampu berpikir dan belajar seperti manusia",
        "option3": "Mempercepat koneksi internet",
        "option4": "Membuat animasi 3D",
        "answer": "Membuat mesin mampu berpikir dan belajar seperti manusia"
    },
    {
        "question": "Apa itu Machine Learning dalam Python?",
        "option1": "Bahasa baru dalam Python",
        "option2": "Metode agar mesin belajar dari data",
        "option3": "Teknik menggambar digital",
        "option4": "Fitur membuat game",
        "answer": "Metode agar mesin belajar dari data"
    },
    {
        "question": "Library Python apa yang digunakan untuk komputasi numerik dalam AI?",
        "option1": "TensorFlow",
        "option2": "NumPy",
        "option3": "Flask",
        "option4": "Requests",
        "answer": "NumPy"
    },
    {
        "question": "Apa fungsi dari model supervised learning?",
        "option1": "Menganalisis data tanpa label",
        "option2": "Memprediksi output berdasarkan data berlabel",
        "option3": "Menyimpan data dalam database",
        "option4": "Menghapus file duplikat",
        "answer": "Memprediksi output berdasarkan data berlabel"
    },
    {
        "question": "Apa fungsi utama TensorFlow dan PyTorch?",
        "option1": "Pemrosesan gambar",
        "option2": "Framework untuk deep learning",
        "option3": "Membuat aplikasi web",
        "option4": "Membuat animasi komputer",
        "answer": "Framework untuk deep learning"
    },
    {
        "question": "Apa itu dataset dalam Machine Learning?",
        "option1": "Kumpulan file program",
        "option2": "Kumpulan data yang digunakan untuk melatih model",
        "option3": "Bahasa pemrograman baru",
        "option4": "Aplikasi AI",
        "answer": "Kumpulan data yang digunakan untuk melatih model"
    },
    {
        "question": "Apa fungsi activation function dalam neural network?",
        "option1": "Menghapus error dari model",
        "option2": "Membantu model belajar dari database",
        "option3": "Memberikan non-linearitas agar jaringan bisa belajar pola kompleks",
        "option4": "Menambah jumlah neuron",
        "answer": "Memberikan non-linearitas agar jaringan bisa belajar pola kompleks"
    },
    {
        "question": "Contoh algoritma classification adalah...",
        "option1": "K-Means",
        "option2": "Linear Regression",
        "option3": "Decision Tree",
        "option4": "Gradient Descent",
        "answer": "Decision Tree"
    }
]

db = get_db()
for q in questions:
    db.execute("""
        INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (q["question"], q["option1"], q["option2"], q["option3"], q["option4"], q["answer"]))
db.commit()
print("✅ 8 soal berhasil dimasukkan!")
