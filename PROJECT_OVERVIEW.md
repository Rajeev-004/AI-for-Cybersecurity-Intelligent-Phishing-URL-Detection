# AI for Cybersecurity: From Adversarial Anomaly Detection to Intelligent Network Security Systems (Phishing URL)
This system builds an AI-driven phishing URL detection model focused on real
login-page URLs using the PILU-90K dataset. It evaluates multiple pipelines
(handcrafted features, TF-IDF + ML/DL, CNN) and includes temporal testing and
domain frequency analysis to ensure long-term robustness.

# DATASET: PILU-90K
- Total: 90,000 URLs
  - 30,000 phishing URLs
  - 30,000 legitimate login URLs
  - 30,000 legitimate homepage URLs
- Purpose: provide realistic login-page training data for phishing detection.

# PIPELINE STRUCTURE / TECHNICAL APPROACH

## 1) Handcrafted Features + Machine Learning
- Uses 38 lexical, structural, and host-based features:
  - URL length
  - digit count
  - special characters
  - presence of IP address
  - subdomain count
  - TLD patterns
- Models used:
  - SVM, Random Forest, Decision Tree, Naive Bayes, Logistic Regression
- Purpose: baseline evaluation and feature interpretability.

## 2) TF-IDF (Character N-gram) + ML/DL Models
- Extracts character-level n-gram patterns via TF-IDF.
- Captures common phishing indicators (login, secure, verify, cgi-bin, .php).
- Models:
  - Logistic Regression (best performance)
  - GRU (RNN-based)
- Accuracy:
  - TF-IDF + Logistic Regression ≈ **96.50%**
- Advantages:
  - fast, lightweight, scalable
  - works well on large, text-heavy datasets.

## 3) Character-Level CNN
- Input: raw URL characters → embeddings → convolution filters.
- Capable of detecting:
  - obfuscation attacks
  - character substitution (e.g., paypa1 vs paypal)
  - random character injection
- Useful against adversarial URL manipulation.

# TEMPORAL ROBUSTNESS TESTING
- Training set: URLs collected in 2016
- Testing sets: URLs from 2017, 2018, 2019, 2020
- Observation:
  - Models lose accuracy on newer URLs.
- Conclusion:
  - phishing techniques evolve rapidly
  - datasets must be updated regularly
  - detection systems require periodic retraining.

# PHISHING DOMAIN FREQUENCY & PATTERN ANALYSIS
- Examined attacker domain behavior:
  - free hosting services
  - rapid domain rotation (fast-flux)
  - disposable TLDs (.xyz, .top, .online)
  - clones of popular brand login pages
- Found six major domain categories used by attackers.
- Helps improve threat intelligence and blacklist automation.

# SYSTEM WORKFLOW

1. Raw URL collection  
2. Labeling (phishing vs legitimate)  
3. URL preprocessing and normalization  
4. Feature extraction (handcrafted, TF-IDF, CNN inputs)  
5. Train ML/DL models  
6. Test on both random and time-separated datasets  
7. Perform phishing domain frequency analysis  
8. Select best model (TF-IDF + LR)  
9. Deploy detection model + monitoring pipeline  

# KEY ADVANTAGES

- Realistic login-page representation  
- High accuracy (96.50%)  
- Independent from external tools (WHOIS, PageRank)  
- Robust model evaluation using temporal datasets  
- Strong ML/DL mix (LR, GRU, CNN)  
- Scalable and production-ready  
- Effective against obfuscated URLs  

# LIMITATIONS & MITIGATION

- Dataset aging → solved via periodic retraining.  
- Obfuscation attacks → mitigated using CNN and TF-IDF n-grams.  
- Large-scale URL changes → enhanced via domain intelligence analysis.  

# DEPLOYMENT RECOMMENDATION 

- Preprocessing pipeline → clean URLs and vectorize with TF-IDF  
- Model server → expose REST API returning phishing probability  
- SOC integration → alert generation, SIEM ingestion, URL filtering  
- Monitoring → drift detection and dataset update triggers  

# CONCLUSION

The proposed system introduces an accurate, robust, and login-focused phishing
detection architecture using the PILU-90K dataset. By combining TF-IDF, LR, GRU,
and CNN models—and validating performance across multiple years—the system
provides a strong foundation for intelligent cybersecurity automation and
real-world phishing defense.
