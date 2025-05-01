# data.py

# 产品数据，可以用来进行搜索
products = [
    {
        "name": "Aspirin",
        "type": "medicine",
        "info": "An analgesic used to reduce pain, fever, or inflammation, and also an antiplatelet agent for preventing heart attacks."
    },
    {
        "name": "Benzoyl Peroxide",
        "type": "skincare",
        "info": "An over-the-counter medication and topical treatment for acne vulgaris, reduces bacteria and has a mild drying effect."
    },
    {
        "name": "Cetaphil Cleanser",
        "type": "skincare",
        "info": "A mild, non-irritating skin cleanser suitable for daily use on all skin types, including sensitive skin."
    },
    {
        "name": "Ibuprofen",
        "type": "medicine",
        "info": "A nonsteroidal anti-inflammatory drug (NSAID) used to reduce fever and treat pain or inflammation from various conditions."
    },
    {
        "name": "Acyclovir",
        "type": "antiviral",
        "info": "An antiviral medication used to treat infections caused by herpes viruses, including genital herpes, cold sores, shingles, and chickenpox."
    },
    {
        "name": "Oseltamivir",
        "type": "antiviral",
        "info": "An antiviral medication used to treat and prevent influenza A and B, it works by inhibiting the neuraminidase enzyme."
    },
    {
        "name": "Remdesivir",
        "type": "antiviral",
        "info": "Originally developed for hepatitis C, it's now used to treat COVID-19 infections by inhibiting viral RNA polymerase."
    },
    {
        "name": "Zidovudine",
        "type": "antiviral",
        "info": "Also known as AZT, it's used in the treatment of HIV/AIDS by inhibiting the virus's reverse transcriptase."
    },
    {
        "name": "Ritonavir",
        "type": "antiviral",
        "info": "An antiretroviral drug used to boost the effect of protease inhibitors in the treatment of HIV/AIDS."
    },
    {
        "name": "Lopinavir",
        "type": "antiviral",
        "info": "Used in combination with Ritonavir, it acts as a protease inhibitor for the treatment of HIV/AIDS."
    },
    {
        "name": "Paracetamol",
        "type": "medicine",
        "info": "Commonly used for the relief of fever and mild to moderate pain. Known as acetaminophen."
    },
    {
        "name": "Hydroxychloroquine",
        "type": "antimalarial",
        "info": "Used to prevent and treat malaria, also used for treating rheumatoid arthritis and lupus."
    },
    {
        "name": "Amoxicillin",
        "type": "antibiotic",
        "info": "A penicillin antibiotic used to treat a number of bacterial infections."
    },
    {
        "name": "Clindamycin",
        "type": "antibiotic",
        "info": "An antibiotic used for treating a variety of bacterial infections, often used for anaerobic bacteria and protozoal infections."
    },
    {
        "name": "Fluconazole",
        "type": "antifungal",
        "info": "An antifungal medication used to treat infections caused by fungus, including yeast infections."
    }
]

# 问答数据，用于实现聊天功能
questions = {
    "What is aspirin?": "Aspirin is used to reduce pain, fever, or inflammation, and is also used as an antiplatelet for heart attack prevention.",
    "What does benzoyl peroxide do?": "Benzoyl Peroxide is commonly used for acne treatment, working by reducing bacteria and skin inflammation.",
    "Tell me about cetaphil cleanser": "Cetaphil Cleanser is a gentle, non-irritating cleanser suitable for everyday use, for all skin types.",
    "How does ibuprofen work?": "Ibuprofen is an NSAID that reduces hormones which cause inflammation and pain in the body.",
    "What is acyclovir used for?": "Acyclovir is used in the treatment of herpes virus infections such as cold sores and shingles.",
    "How does oseltamivir function?": "Oseltamivir works as a neuraminidase inhibitor to treat and prevent influenza.",
    "What is remdesivir?": "Remdesivir is an antiviral medication used for treating COVID-19 by inhibiting viral replication.",
    "Usage of zidovudine?": "Zidovudine, or AZT, is used in HIV/AIDS management by blocking reverse transcriptase.",
    "Function of ritonavir?": "Ritonavir boosts the effectiveness of other protease inhibitors in HIV treatment.",
    "What is paracetamol?": "Paracetamol is used to treat fever and mild to moderate pain, also known as acetaminophen.",
    "Explain hydroxychloroquine": "Hydroxychloroquine is used in malaria prevention and treatment, and also for autoimmune diseases like lupus and arthritis.",
    "Usage of amoxicillin": "Amoxicillin treats bacterial infections and is a type of penicillin antibiotic.",
    "What is clindamycin good for?": "Clindamycin is used for treating serious bacterial infections, including skin and respiratory infections.",
    "How does fluconazole work?": "Fluconazole treats fungal infections like candidiasis by inhibiting the growth of fungi."
}
