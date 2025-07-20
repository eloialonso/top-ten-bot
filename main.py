import os
import sys
import random
import openai

# List of fun AI player names
AI_NAME_POOL = [
    "TurboBot", "FunkyBot", "RoboClown", "ChattyAI", "MisterGiggles", "DrLudique", "PixelPirate", "Écho", "Galacto", "Zigzag"
]


def clear_screen():
    """Clear console screen for privacy between reveals"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_ai_suggestion(theme, number, previous_suggestions):
    """
    Calls the ChatGPT API to generate a suggestion for the given theme and intensity number (1–10),
    adapting length/style to previous suggestions.
    Suggestions are in French and playful.
    """
    avg_length = 0
    if previous_suggestions:
        avg_length = sum(len(text) for _, text in previous_suggestions) / len(previous_suggestions)
    style_instruction = (
        "Reste succinct et direct." if avg_length < 30 else "Fournis un peu plus de détails et de couleur."
    )
    messages = [
        {"role": "system", "content": (
            "You are a playful Top Ten AI player. "
            "Players propose items for a French theme, each with an intensity number from 1 (mildest) to 10 (wildest). "
            "Adapt the length of your answer: " + style_instruction + " "
            "Generate fun, imaginative suggestions matching your intensity. Respond in French."
        )},
        {"role": "user", "content": (
            f"Thème : {theme}\n"
            f"Votre intensité (1–10) : {number}\n"
            "Suggestions précédentes :\n" +
            "\n".join(f"{num} : {text}" for num, text in previous_suggestions)
        )}
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            max_tokens=80
        )
        suggestion = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur API ChatGPT : {e}", file=sys.stderr)
        suggestion = "[IA indisponible — erreur]"
    return suggestion


def play_round(players, round_number):
    """Play a single round with rotating captain."""
    total_players = len(players)
    captain_idx = round_number % total_players
    captain = players[captain_idx]
    others = [p for p in players if p != captain]

    print(f"\n=== Manche {round_number + 1} — Capitaine : {captain['name']} ===")
    theme = input("Entrez le thème de la manche (en français) : ")

    intensities = random.sample(range(1, 11), k=len(others))
    random.shuffle(others)
    turn_order = [{"name": p['name'], "kind": p['kind'], "number": num}
                  for p, num in zip(others, intensities)]

    # Reveal numbers privately with computer pass
    for p in turn_order:
        if p['kind'] == 'human':
            clear_screen()
            print(f"C'est au tour de {p['name']} de prendre l'ordinateur pour voir son intensité.")
            input("Appuyez sur Entrée quand vous êtes prêt...")
            print(f"Votre intensité est {p['number']}")
            input("Notez-la puis appuyez sur Entrée pour continuer, et assurez-vous que personne d'autre ne regarde.")
    clear_screen()

    print("\n--- Ordre de passage ---")
    for idx, p in enumerate(turn_order, start=1):
        print(f"Position {idx} : {p['name']}")

    print("\n--- Début des propositions ---")
    suggestions = []
    for p in turn_order:
        if p['kind'] == 'human':
            text = input(f"{p['name']} (votre intensité) : votre proposition : ")
        else:
            text = get_ai_suggestion(theme, p['number'], sorted(suggestions, key=lambda x: x[0]))
            print(f"{p['name']} propose : {text}")
        suggestions.append((p['number'], text))

    # Captain makes guess
    print(f"\n{captain['name']}, entrez l'ordre des intensités (séparées par espaces) : ")
    guess_input = input().strip()
    guessed_order = guess_input.split()
    print(f"Vous avez deviné : {' '.join(guessed_order)}")

    print("\n--- Propositions finales (ordre par intensité) ---")
    for num, text in sorted(suggestions, key=lambda x: x[0]):
        print(f"{num} : {text}")
    print(f"\n{captain['name']}, comparez votre ordre à la réalité.")


def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("Erreur : définissez OPENAI_API_KEY.")
        return

    num_humans = int(input("Nombre de joueurs humains : "))
    human_names = [input(f"Prénom du joueur humain #{i+1} : ") for i in range(num_humans)]
    num_ai = int(input("Nombre de joueurs IA : "))
    ai_names = random.sample(AI_NAME_POOL, k=num_ai)
    players = [{"name": n, "kind": "human"} for n in human_names] + \
              [{"name": n, "kind": "ai"} for n in ai_names]

    round_number = 0
    while True:
        play_round(players, round_number)
        round_number += 1
        cont = input("\nLancer une nouvelle manche ? (o/n) : ")
        if cont.lower() != 'o':
            print("Fin de la partie. Merci d'avoir joué !")
            break

if __name__ == "__main__":
    main()

