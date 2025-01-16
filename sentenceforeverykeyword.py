from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Încarcă modelul și tokenizerul GPT-2
model_name = "gpt2"  # Poți schimba la un model mai mic sau alt model pre-antrenat dacă e disponibil
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Setează modelul pe CPU
device = 'cpu'
model.to(device)

# Cuvinte cheie pentru tema pisici în limba engleză
keywords = [
    "cats",
    "cat behavior",
    "cats are playful",
    "cat care",
    "cats and health",
    "pedigree cats",
    "kitten",
    "feeding cats",
    "cats and their comfort",
    "cats in the house"
]

def generate_sentence_with_keyword(keyword, max_length=60):
    # Construirea promptului în limba engleză
    prompt = f"Generate a sentence in English with the keyword: {keyword}"

    inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)
    
    # Generează propoziția
    output = model.generate(
        inputs, 
        max_length=max_length, 
        do_sample=True, 
        temperature=0.3,  # Reglează temperatura pentru diversitate
        top_p=0.9,  # Parametru pentru nucleu de probabilitate
        num_return_sequences=1,  # Numărul de propoziții generate
        pad_token_id=50256  # Id-ul pentru tokenul de padding
    )
    
    # Decodează și returnează propoziția generată
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Generarea propozițiilor pentru fiecare cuvânt cheie
for keyword in keywords:
    generated_sentence = generate_sentence_with_keyword(keyword)
    print(f"{keyword} - {generated_sentence}")
