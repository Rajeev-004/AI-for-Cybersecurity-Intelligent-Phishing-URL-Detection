

This project presents an AI-based phishing URL detection system built using a 
realistic dataset called PILU-90K. The system focuses on detecting phishing 
attempts through login-page URL analysis and addresses the limitations found in 
traditional detection methods and outdated datasets.

# OBJECTIVES
- Understand challenges in phishing URL detection
- Build an AI-driven system with high accuracy
- Analyze URLs using TF-IDF, CNN, GRU, and handcrafted features
- Evaluate model performance over different years (temporal analysis)
- Identify attacker trends using domain frequency analysis
- Use a realistic login-page-oriented dataset (PILU-90K)

# DATASET OVERVIEW (PILU-90K)
- 30,000 phishing URLs
- 30,000 legitimate login URLs
- 30,000 legitimate homepage URLs
- Total: 90,000 URLs
- Designed to represent real login-page phishing scenarios

# TECHNICAL APPROACH

1. Handcrafted Feature Pipeline
   - Uses 38 lexical, structural, and host-based URL features
   - Trained using multiple supervised ML classifiers

2. TF-IDF + Machine/Deep Learning Models
   - Character-level N-gram TF-IDF extraction
   - Models used: Logistic Regression, GRU
   - Best accuracy achieved: 96.50% (TF-IDF + Logistic Regression)

3. Character-Level CNN
   - Learns URL structural patterns
   - Useful for detecting adversarial and obfuscated URLs

# TEMPORAL ROBUSTNESS ANALYSIS
- Model trained on URLs from 2016
- Evaluated on datasets from 2017 to 2020
- Results show a drop in accuracy over time
- Confirms that phishing techniques evolve rapidly
- Suggests the need for frequent dataset updates

# PHISHING DOMAIN FREQUENCY ANALYSIS
- Analysis reveals six main phishing domain categories
- Shows attacker hosting and infrastructure patterns
- Helps understand modern phishing campaigns

# ADVANTAGES OF THE PROPOSED SYSTEM
- Real login-based phishing detection
- High accuracy (96.50%)
- Handles modern phishing techniques
- Uses realistic dataset instead of outdated ones
- Strong ML/DL pipelines (LR, GRU, CNN)
- Works without third-party services like WHOIS

# SUMMARY
This project delivers an AI-driven phishing URL detection framework using a 
realistic login-based dataset. By combining TF-IDF, CNN, GRU models, handcrafted 
features, and temporal evaluation, the system provides a reliable and adaptive 
solution for detecting modern phishing attacks. PILU-90K and the analysis 
methods make this system relevant for cybersecurity research and SOC operations.
