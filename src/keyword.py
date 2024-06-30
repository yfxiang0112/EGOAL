from keybert import KeyBERT

doc = "Treatment protocol: BES carbon paper electrodes from continuous BES operation were dipped in Qiagen RNA-protect and frozen at -80°C until total RNA extraction. Growth protocol: Cells were grown anaerobically at 30°C in a contiuous bioelectrochemical system (BES) with defined medium (modified M4) and 20 mM lactate. The BES anode was the only electron acceptor."

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(doc)

print(keywords)
