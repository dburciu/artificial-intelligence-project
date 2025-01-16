Integrarea în fluxul de execuție
while not valid:
    option = input(f"\nCum doriti sa inserati textul? [Consola/Fisier]\n")

    if option.lower() == "consola":
        valid = True
        text = input("\nIntroduceti textul: ")
        print(f"\nTextul este: {text}\n")

        # Detectarea limbii
        lang = detectare_limba(text)

        # Generarea informațiilor stilometrice
        informatii_stilometrice(text, lang)

        # Extragem cuvintele cheie
        keywords = extract_keywords(text)
        print("\nCuvinte cheie extrase:", keywords)

        # Generăm propoziții pentru fiecare cuvânt cheie
        sentences = generate_sentences_with_context(keywords, text)
        for sentence in sentences:
            print(sentence)

    elif option.lower() == "fisier":
        valid = True
        file_path = input("\nIntroduceti calea catre fisier: ")
        print(f"\nCalea primita: {file_path}\n")

        # Citirea textului din fișier
        text = citire_fisier(file_path)

        # Detectarea limbii
        lang = detectare_limba(text)

        # Generarea informațiilor stilometrice
        informatii_stilometrice(text, lang)

        # Extragem cuvintele cheie
        keywords = extract_keywords(text)
        print("\nCuvinte cheie extrase:", keywords)

        # Generăm propoziții pentru fiecare cuvânt cheie
        sentences = generate_sentences_with_context(keywords, text)
        for sentence in sentences:
            print(sentence)

    else:
        print("\noptiune invalida!")
        valid = False
        continue

