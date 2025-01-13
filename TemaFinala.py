# Punctul doi:
# Citiți o descriere în limbaj natural a unei pisici,
# extrageți atributele relevante și identificați rasa.

import spacy
import pandas as pd
from laborator10 import get_synonyms, get_antonyms, get_hypernyms

# AVETI NEVOIE DE
# pip install spacy
# python -m spacy download en_core_web_sm

data = pd.read_excel('Data cat personality and predation Cordonnier et al.xlsx')

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

nlp = spacy.load("en_core_web_sm")


# Options for all values present in the database

def all_options(word):
    options = get_hypernyms(word) + get_synonyms(word) + get_antonyms(word)
    return list(set(options))


# Sexe variable

male_options = all_options("male")
male_options.extend(["male"])
male_options = [item.lower() for item in male_options]

female_options = all_options("female")
female_options.extend(["female"])
female_options = [item.lower() for item in female_options]

sexe_options = male_options + female_options

# Age variable cant find other words and numbers are enough

valid_age = [0]

valid_age.extend(range(1, 30))

# number of cats in the household does not need more options

# Longement variable

apartment_options = all_options("apartment")
house_options = all_options("house")
balcony = all_options("balcony")
subdivision_options = all_options("subdivision")

longement_options = apartment_options + house_options + subdivision_options

# Zone variable

urban_options = all_options("urban")
periurban_options = all_options("periurban")
rural_options = all_options("rural")

valid_zone = urban_options + periurban_options + rural_options

# Time spent outside variable AND for time spent with human variable

none = all_options("none")
limited = all_options("limited")
moderate = all_options("moderate")
long = all_options("long")
all_the_time = all_options("all the time")

time_spent = none + limited + moderate + long + all_the_time

# abundance of natural areas

low = all_options("low")
# we already have moderate
high = all_options("high")
dont_know = all_options("dont know")

abondance_options = low + moderate + high + dont_know

#for frequency of catching birds or small mammals

never = all_options("never")
rarely = all_options("rarely")
sometimes = all_options("sometimes")
often = all_options("often")
very_often = all_options("very often")


def extract_attributes(description):
    doc = nlp(description)
    print(doc)
    attributes = {
        "Sexe": None,
        "Age": None,
        "Logement": None,
        "Zone": None,
        "Ext": None,
        "Obs": None,
        "Abondance": None,
        "PredOiseau": None,
        "PredMamm": None,
    }

    for token in doc:

        if token.text.lower() in sexe_options:
            attributes["Sexe"] = "M" if token.text.lower() in male_options else "F"
        if token.text.lower() in valid_age:
            attributes["Age"] = token.text.lower()
        if token.text.lower() in longement_options:
            if token.text.lower() in apartment_options:
                if token.text.lower() in balcony:
                    attributes["Longement"] = "ABS"
                else:
                    attributes["Longement"] = "AAB"
            else:
                if token.text.lower() in subdivision_options:
                    attributes["Longement"] = "ML"
                else:
                    attributes["Longement"] = "MI"
        if token.text.lower() in valid_zone:
            if token.text.lower() in urban_options:
                attributes["Zone"] = "U"
            elif token.text.lower() in periurban_options:
                attributes["Zone"] = "PU"
            else:
                attributes["Zone"] = "R"
    # a way to differenciate between time spent outdoors and time
    # spent with the cat in the context of the description?
        if token.text.lower() in time_spent:
            if token.text.lower() in none:
                attributes["Ext"] = "1"
            elif token.text.lower() in limited:
                attributes["Ext"] = "2"
            elif token.text.lower() in moderate:
                attributes["Ext"] = "3"
            elif token.text.lower() in long:
                attributes["Ext"] = "4"
            else:
                attributes["Ext"] = "5"
        if token.text.lower() in time_spent:
            if token.text.lower() in none:
                attributes["Obs"] = "1"
            elif token.text.lower() in limited:
                attributes["Obs"] = "2"
            elif token.text.lower() in moderate:
                attributes["Obs"] = "3"
            else:
                attributes["Obs"] = "4"

        # a way to differenciate between catching birds frequency
        # and catching small mammals frequency
        # in the context of the description?

    return attributes


def dominant_race(data, race_col, attribute_col, attribute_value):
    """
    Identify the race with the highest percentage for a specific attribute value.

    Args:
    - data: DataFrame containing the dataset.
    - race_col: Name of the column representing the race.
    - attribute_col: Name of the column representing the attribute.
    - attribute_value: Value of the attribute to filter.

    Returns:
    - The race with the highest percentage or None if no match.
    """
    filtered_data = data[data[attribute_col] == attribute_value]
    if filtered_data.empty:
        return None

    race_counts = filtered_data[race_col].value_counts(normalize=True) * 100
    dominant_race_code = race_counts.idxmax()
    return race_dict.get(dominant_race_code, "Unknown")


def predict_race(description, data, race_col="Race", attributes=None):
    if attributes is None:
        attributes = ["Sexe", "Age", "Logement", "Zone", "Ext", "Obs", "Abondance", "PredOiseau", "PredMamm"]

    extracted_attributes = extract_attributes(description)
    race_scores = {}

    for attribute in attributes:
        attribute_value = extracted_attributes.get(attribute)
        if attribute_value:
            dominant = dominant_race(data, race_col, attribute, attribute_value)
            if dominant:
                race_scores[dominant] = race_scores.get(dominant, 0) + 1

    if race_scores:
        predicted_race = max(race_scores, key=race_scores.get)
        return predicted_race

    return "Unknown"


description = "A male cat that is 2-10 years old, lives in an apartment, and is medium-sized with spotted orange fur."
predicted_breed = predict_race(description, data)
print(f"The predicted breed is: {predicted_breed}")
