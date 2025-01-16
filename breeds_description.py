import pandas as pd
from transformers import pipeline
from transformers import FlaxGPT2LMHeadModel, GPT2Tokenizer
import jax
import jax.numpy as jnp

# Folosim GPT-2 care este disponibil in Flax

model_name = "gpt2"
model = FlaxGPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

race_dict = {
    "BEN": "Bengal",
    "SBI": "Birman",
    "BRI": "British Shorthair",
    "CHA": "Chartreux",
    "EUR": "European",
    "MCO": "Maine coon",
    "PER": "Persian",
    "RAG": "Ragdoll",
    "SPH": "Sphynx",
    "SAV": "Savannah",  #nu exista mentionata SVA
    "ORI": "Sphynx",
    "TUV": "Turkish angora",
    "Autre": "No Breed/ Other",
    "NSP": "Unkown"
}


def generate_breed_description(breed_code):
    if breed_code not in race_dict:
        return "Rasa de pisică nu este recunoscută."

    breed_name = race_dict[breed_code]

    # Alcatuim promptul care va genera raspunsul 

    prompt = f"Tell me the most important traits of {breed_name} cats."

    # Impartim promptul in tokeni

    inputs = tokenizer(prompt, return_tensors="jax", padding=True, truncation=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Generam textul

    outputs = model.generate(input_ids,
                             attention_mask=attention_mask,
                             max_length=150,  # Limitam lungimea la 150 de tokenuri
                             pad_token_id=tokenizer.pad_token_id,
                             do_sample=True,  # Permitem generarea aleatorie a textului
                             temperature=0.5,  # Temperatura mai scazuta pentru mai putina aleatorizare
                             top_p=0.85,  # top_p mai scazut pentru a reduce diversitatea extreme
                             top_k=50,  # Setam top_k pentru limitarea alegerii
                             num_return_sequences=1)  # Doar o secventa generata

    # accesam secventa pe care am generat-o

    generated_tokens = outputs.sequences[0]

    # Traduce tokenii in text

    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # Avem grija sa nu afisam si prompt-ul in output

    description = generated_text.replace(prompt, "").strip()

    return description

#print(generate_breed_description("PER"))
