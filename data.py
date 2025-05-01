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
    },
    {
        "name": "Metformin",
        "type": "medicine",
        "info": "A medication used for the treatment of type 2 diabetes. It helps control blood sugar levels."
    },
    {
        "name": "Lisinopril",
        "type": "medicine",
        "info": "An ACE inhibitor used to treat high blood pressure and heart failure, and to improve survival after a heart attack."
    },
    {
        "name": "Simvastatin",
        "type": "medicine",
        "info": "A medication used to control hypercholesterolemia (high cholesterol) and to prevent cardiovascular disease."
    }
]

# 问答数据，用于实现聊天功能
questions = {
    "What is aspirin?": (
        "Aspirin, also known as acetylsalicylic acid, is commonly used to reduce pain, fever, or inflammation. "
        "Additionally, it is widely used as an antiplatelet agent for preventing heart attacks and strokes among individuals "
        "at high risk. Aspirin works by blocking the production of prostaglandins, which are chemicals that promote inflammation, "
        "pain, and fever. By inhibiting the enzyme cyclooxygenase (COX), aspirin reduces the production of thromboxane, thereby "
        "lowering the risk of blood clots forming. This mechanism makes it beneficial not just for managing minor pains, but "
        "also for cardiovascular protection. However, long-term use should always be under medical supervision due to potential "
        "side effects such as gastric ulcers and bleeding."
    ),
    "What does benzoyl peroxide do?": (
        "Benzoyl peroxide is a popular treatment for acne, found in various over-the-counter skincare products. It helps achieve "
        "clearer skin by reducing the amount of acne-causing bacteria on the skin, due to its antibacterial properties. Furthermore, "
        "it acts as a peeling agent, which increases skin turnover and clears pores, thus reducing inflammation and preventing "
        "new breakouts. This dual action makes it effective for treating mild to moderate acne. Users should be aware of its drying "
        "effect, often leading to skin irritation, especially if used excessively. Therefore, it's recommended to start with a lower "
        "concentration and gradually increase usage as the skin adapts."
    ),
    "Tell me about cetaphil cleanser": (
        "Cetaphil Cleanser is a sensitive-skin-friendly facial and body wash designed for everyday use. It's known for its non-irritating "
        "formula, which makes it ideal for individuals with sensitive or dry skin conditions such as eczema or rosacea. The product is soap-free, "
        "which means it cleanses the skin without stripping it of its natural protective oils and emollients. Dermatologically tested and recommended, "
        "Cetaphil Cleanser effectively removes dirt, surface oils, and makeup without clogging pores, maintaining the skin's pH balance. It provides "
        "a gentle yet thorough cleansing experience that does not leave residue, allowing for healthier, smoother skin."
    ),
    "How does ibuprofen work?": (
        "Ibuprofen, a member of the nonsteroidal anti-inflammatory drug (NSAID) family, is widely used for alleviating pain, reducing inflammation, and "
        "lowering fever. It works by inhibiting the activity of cyclooxygenase (COX) enzymes, specifically COX-1 and COX-2, which are responsible for the "
        "formation of prostaglandins, compounds that mediate inflammation and pain sensations throughout the body. By blocking these enzymes, ibuprofen "
        "effectively reduces the symptoms associated with inflammation, including swelling, redness, and pain, making it useful for treating conditions "
        "like arthritis, menstrual cramps, headaches, and more. Although effective, improper or prolonged use of ibuprofen can lead to side effects such "
        "as gastrointestinal issues, cardiovascular risks, and kidney damage, so it should be used as directed by a physician."
    ),
    "What is acyclovir used for?": (
        "Acyclovir is an antiviral drug primarily used to manage infections caused by the herpes simplex virus, including genital herpes, cold sores, and "
        "herpes zoster (shingles). It operates by inhibiting the replication of viral DNA, thereby slowing down the spread and number of outbreaks. Acyclovir "
        "is often prescribed to reduce pain and accelerate the healing of sores or blisters. Regular use as prescribed can also help decrease the intensity and "
        "frequency of future episodes. While acyclovir does not cure herpes, nor does it prevent transmission of the virus to others, it acts as an effective "
        "management tool for reducing the discomfort and social stigma associated with the condition."
    ),
    "How does oseltamivir function?": (
        "Oseltamivir, known by its brand name Tamiflu, is an antiviral medication used to treat and prevent influenza types A and B. It belongs to a class of drugs "
        "called neuraminidase inhibitors that target the neuraminidase enzyme on the surface of the influenza virus, which is essential for the virus’s replication. "
        "By blocking this enzyme, oseltamivir prevents new viral particles from being released from infected cells, thereby limiting the spread of infection within the "
        "body. When taken within 48 hours of the first flu symptoms, oseltamivir can reduce the severity and duration of the illness. It's often recommended for people at "
        "high risk of flu complications, such as the elderly and those with certain chronic conditions."
    ),
    "What is remdesivir?": (
        "Remdesivir is a broad-spectrum antiviral agent initially developed for treating infections with the Ebola virus. More recently, it gained attention for its emergency "
        "use in managing COVID-19. Remdesivir works by inhibiting RNA-dependent RNA polymerase, an enzyme the virus uses to replicate its genetic material. This interference "
        "slows down viral multiplication, helping to control the infection. Clinical trials have demonstrated that remdesivir can shorten recovery time in hospitalized patients "
        "with severe COVID-19 symptoms. Despite being a promising treatment, it is not a cure, and its administration should be strictly supervised by healthcare professionals. "
        "Safety and efficacy continue to be evaluated as more data becomes available."
    ),
    "Usage of zidovudine?": (
        "Zidovudine, often recognized by its acronym AZT, is used in the treatment and management of HIV/AIDS. It was the first notable antiretroviral drug approved for the "
        "disease and works by inhibiting the replication of HIV in the body. Specifically, zidovudine targets reverse transcriptase, an enzyme that HIV needs to convert its RNA "
        "into DNA and reproduce within the host's cells. By blocking this process, zidovudine reduces the viral load in the patient’s body, bolstering the immune system and helping "
        "to prevent opportunistic infections. It's commonly used in combination with other antiretroviral medications for maximal efficacy."
    ),
    "Function of ritonavir?": (
        "Ritonavir is an antiretroviral drug, part of the protease inhibitor class, used primarily to treat HIV/AIDS. As a significant enhancement therapy, it 'boosts' the effect of "
        "other protease inhibitors by inhibiting cytochrome P450-3A4 (CYP3A4), an enzyme responsible for metabolizing many HIV protease inhibitors. By doing so, ritonavir increases "
        "the blood levels and permanence of these drugs, enhancing their effectiveness. Although not often used alone due to gastrointestinal side effects, ritonavir's role in "
        "combination therapy has made it invaluable, especially in highly active antiretroviral therapy (HAART) regimens that aim to keep the HIV virus in check."
    ),
    "What is paracetamol?": (
        "Paracetamol, also known as acetaminophen, is a widely used over-the-counter medication for relieving pain and reducing fever. It is utilized in the management of headaches, "
        "muscle aches, arthritis, backaches, toothaches, colds, and fevers. Although the exact mechanism isn't completely understood, it's believed to work by inhibiting the COX enzymes "
        "in the brain, thereby decreasing the production of prostaglandins, which play a key role in pain and fever. Unlike NSAIDs, paracetamol does not have an anti-inflammatory effect, "
        "making it a preferred option for patients with stomach sensitivity. However, large doses can lead to severe liver damage, highlighting the need for cautious use especially in people "
        "with existing liver conditions or those consuming alcohol regularly."
    ),
    "Explain hydroxychloroquine": (
        "Hydroxychloroquine is a medication with multiple uses, primarily known for treating and preventing malaria. Additionally, it is successfully utilized in managing auto-immune conditions "
        "such as rheumatoid arthritis and lupus erythematosus. It functions by modulating the immune system and reducing inflammation. Although it gained attention during the COVID-19 pandemic as "
        "a potential therapeutic, the extent of its efficacy remains to be conclusively proven. Routine usage requires careful monitoring due to its possible side effects, which range from retinal "
        "toxicity to arrhythmic conditions, necessitating medical supervision to ensure patient safety."
    ),
    "Usage of amoxicillin": (
        "Amoxicillin is a penicillin antibiotic that treats a broad spectrum of bacterial infections by inhibiting the growth of bacteria that cause infections in different parts of the body, "
        "including the ear, nose, throat, and urinary tract. This drug works by disrupting the bacterial cell wall synthesis, effectively killing the bacteria. It's renowned for its high absorption "
        "rate when taken orally, and is considered safe for use in children and adults alike. However, inappropriate use may result in antibiotic resistance, making it important to adhere to "
        "prescription guidelines."
    ),
    "What is clindamycin good for?": (
        "Clindamycin is a powerful antibiotic primarily used to treat severe bacterial infections such as sepsis, intra-abdominal infections, lower respiratory tract infections, and skin and soft "
        "tissue infections. It works by inhibiting bacterial protein synthesis, which is essential for bacteria growth and reproduction. Clindamycin is effective against certain protozoal infections "
        "and is an alternative for people allergic to penicillin. Despite its effectiveness, clindamycin usage can lead to side effects such as gastrointestinal distress and an increased risk of "
        "Clostridioides difficile infection caused by the disruption of normal gut flora, emphasizing the importance of using it judiciously and under medical guidance."
    ),
    "How does fluconazole work?": (
        "Fluconazole is an antifungal medication that treats infections caused by fungi by inhibiting the enzyme lanosterol 14-alpha-demethylase. This action disrupts the formation of ergosterol, "
        "a critical component of the fungal cell membrane, leading to weakened cell walls and subsequent cell death. Fluconazole is effective in the treatment of candidiasis, including vaginal yeast "
        "infections, thrush, and systemic infections caused by Candida species. It is also used to treat cryptococcal meningitis. While generally well-tolerated, monitoring for potential liver damage "
        "is essential due to rare reports of hepatotoxicity associated with its use."
    ),
    "What is metformin used for?": (
        "Metformin is a first-line medication for the treatment of type 2 diabetes, particularly in overweight and obese individuals. It functions by lowering blood glucose levels and improving insulin "
        "sensitivity. Metformin decreases hepatic glucose production, reduces intestinal absorption of glucose, and enhances peripheral glucose uptake, collectively resulting in better blood sugar control. "
        "Metformin is also associated with a modest amount of weight loss and positively impacts lipid profiles. It's generally well-tolerated but can cause gastrointestinal side effects such as nausea, "
        "bloating, and diarrhea. Regular kidney function monitoring is recommended as metformin can accumulate in patients with renal impairment, potentially leading to lactic acidosis, a rare but serious "
        "complication."
    ),
    "Explain the use of lisinopril": (
        "Lisinopril is an angiotensin-converting enzyme (ACE) inhibitor commonly prescribed to treat high blood pressure and heart failure. It can also be used to improve survival rates after a heart attack. "
        "Lisinopril works by relaxing blood vessels, allowing blood to flow more smoothly and the heart to pump more efficiently. This action helps lower blood pressure and reduce strain on the heart. In addition, "
        "it decreases the risk of stroke and heart attack in individuals with cardiovascular risk factors. Some patients may experience side effects such as cough, dizziness, or hyperkalemia, which a healthcare provider "
        "can discuss during counseling."
    ),
    "What is simvastatin used for?": (
        "Simvastatin is a statin medication used to control hypercholesterolemia (high cholesterol levels) and lower the risk of cardiovascular disease. It works by inhibiting HMG-CoA reductase, an enzyme involved in "
        "cholesterol synthesis, consequently reducing the levels of bad cholesterol (LDL) and triglycerides while increasing the levels of good cholesterol (HDL) in the bloodstream. An improvement in the cholesterol "
        "profile helps decrease the risk of heart attack, stroke, and related health problems. While simvastatin is generally safe, it may cause muscle pain, digestive problems, and in rare cases, liver damage, so patients "
        "should undergo regular monitoring during treatment."
    )
}
