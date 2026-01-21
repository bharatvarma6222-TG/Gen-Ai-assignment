# Gen AI Internship Assignment – Synlabs

## Overview
This repository contains solutions for a Gen AI internship assignment consisting of three tasks:
1. AI Video Generation Tool
2. AI-Based SEO Blog Creation Tool
3. High-Level to Low-Level Architecture Automation Tool

Each task is implemented as a working prototype focusing on feasibility, clarity, and real-world applicability.

---

## Task 1: AI Video Generation Tool
**Objective:**  
Generate a 30–60 second news video by scraping trending news, generating a script, and creating a video with text overlays and topic-based images.

**Key Features:**
- Scrapes trending news using Google News RSS
- Cleans and processes article content
- Generates a short news script automatically
- Extracts topic-accurate images using article OpenGraph metadata
- Adds text overlays and transitions
- Produces an MP4 video output

**Tech Stack:**  
Python, MoviePy, Pillow, BeautifulSoup

---

## Task 2: AI-Based SEO Blog Creation Tool
**Objective:**  
Automatically generate SEO-optimized blog content for trending products.

**Key Features:**
- Scrapes trending products from an e-commerce website
- Automatically researches 3–4 SEO keywords using Google Autocomplete
- Generates a 150–200 word SEO blog post
- Outputs content in Markdown format for publishing

**Tech Stack:**  
Python, BeautifulSoup, Google Search Autocomplete

---

## Task 3: High-Level to Low-Level Architecture Tool
**Objective:**  
Convert high-level business requirements into low-level technical specifications.

**Key Features:**
- Accepts free-text business requirements
- Generates system modules, APIs, database schema, and pseudocode
- Domain-aware with generic fallback logic
- Outputs structured architecture data

**Tech Stack:**  
Python

---

## How to Run
Each task is located in its own folder:
```bash
cd task-folder
python app.py
```

---

## Author
[S Bharat Kumar varma]
