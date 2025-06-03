<h1 align="center">Tugas Besar 3 IF2211 Strategi Algoritma</h1>
<h2 align="center">Semester II tahun 2024/2025</h2>
<h2 align="center">Pemanfaatan Pattern Matching untuk Membangun Sistem ATS (Applicant Tracking System) Berbasis CV Digital
</h2>

<p align="center">
  <img src="doc/img/main.jpg" alt="main"/>
</p>

## Table of Contents

- [Description](#description)
- [Requirements & Installation](#requirements--installation)
- [How to Run](#how-to-run)
- [Author](#author)

## Description

### Problem Solving Steps with KMP (Knuth-Morris-Pratt)

### Problem Solving Steps with BM (Boyer-Moore)

## Built With

## Requirements & Installation

**1.Create a virtual environment using the following command:**
```bash
python -m venv .venv
```

**2.Activate the environment**

**For Windows:**
```bash
.venv\Scripts\activate
```
**For MacOS/Linux:**
```bash
source .venv/bin/activate
```

**3. Install the required dependencies for the program by running:**
```bash
pip install -r requirements.txt
```

**4. Create database (open terminal and run this command)**
```bash
mysql -u root -p < src/database/schema.sql
```

**5. Jalanin main.py (oiya janlup db password nya yg di AppConfg disesuaiin)**
```bash
python -m src.main
```

**6. Buat Seeder**
```bash
python -m src.database.Seeder
```

## Author

| **NIM**  | **Nama Anggota**     | **Github**                              |
| -------- | -------------------- | --------------------------------------- |
| 13523029 | Bryan Ho             | [bry-ho](https://github.com/bry-ho)     |
| 13523033 | Alvin Christopher Santausa | [Incheon21](https://github.com/Incheon21) |
| 13523091 | Carlo Angkisan       | [carllix](https://github.com/carllix)   |