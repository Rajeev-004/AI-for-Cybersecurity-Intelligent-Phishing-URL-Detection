┌──────────────────────────────────────────────────────────────────────────────┐
│                              PROJECT OVERVIEW                                │
└──────────────────────────────────────────────────────────────────────────────┘

Phishing remains one of the most dangerous cyber threats, with attackers creating
fake login pages to steal user credentials. Traditional detection systems rely on
outdated datasets and homepage URLs, causing high false positives and weak 
performance against modern phishing attacks.

To address this, we introduce **PILU-90K (Phishing Index Login URL)**—a realistic,
modern dataset containing:

   • 30,000 Phishing URLs
   • 30,000 Legitimate Login URLs
   • 30,000 Legitimate Homepage URLs
   • Total: 90,000 URLs

Unlike older datasets, PILU-90K focuses on real login-page scenarios where users
are most vulnerable.

───────────────────────────────────────────────────────────────────────────────
  MACHINE LEARNING & DEEP LEARNING PIPELINES
───────────────────────────────────────────────────────────────────────────────

We evaluate several detection approaches:

   • Handcrafted URL feature descriptors + ML classifiers
   • TF-IDF (character N-gram) + Logistic Regression (Achieves **96.50% accuracy**)
   • TF-IDF + GRU model
   • Character-level CNN for pattern extraction

TF-IDF + Logistic Regression provides the best results on the new dataset.

───────────────────────────────────────────────────────────────────────────────
  TEMPORAL ROBUSTNESS & PHISHING EVOLUTION
───────────────────────────────────────────────────────────────────────────────

Models trained on 2016 datasets lose accuracy when tested on URLs from 2017–2020,
proving that phishing techniques evolve rapidly. Domain frequency analysis reveals
six major attacker domain categories based on hosting infrastructure.

───────────────────────────────────────────────────────────────────────────────
  SUMMARY
───────────────────────────────────────────────────────────────────────────────

This project delivers a realistic, AI-driven phishing detection framework using:

   ✓ Real login-page URLs  
   ✓ Multiple ML/DL pipelines  
   ✓ Temporal performance evaluation  
   ✓ Modern domain-level phishing behavior analysis  

The system is designed to be **intelligent, adaptive, and effective** against
current phishing threats—providing a strong foundation for modern cybersecurity
solutions.
