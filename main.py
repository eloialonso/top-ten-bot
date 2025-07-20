import os
import sys
import random
import openai
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# List of fun AI player names
AI_NAME_POOL = [
    "TurboBot", "FunkyBot", "RoboClown", "ChattyAI", "MisterGiggles", "DrLudique", "PixelPirate", "Écho", "Galacto", "Zigzag"
]

# Available colors for players
COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]


def clear_screen():
    """Clear console screen for privacy between reveals"""
    os.system('cls' if os.name == 'nt' else 'clear')


def assign_colors(players):
    """Assign a unique color to each player, cycling through COLORS"""
    return {p['name']: COLORS[i % len(COLORS)] for i, p in enumerate(players)}


def get_ai_suggestion(theme, number, previous_suggestions):
    """
    Calls ChatGPT to generate exactly one suggestion (not a list) matching the theme and intensity.
    Always respond with a single concise item, no enumeration. Use previous_suggestions to adjust tone.
    """
    messages = [
        {"role": "system", "content": (
            "You are an AI player in Top Ten. "
            "Given a French theme and a unique intensity from 1 (très léger) to 10 (très fort), "
            "you must propose exactly one suggestion that fits this intensity. "
            "Do not list multiple items or numbers—just one. "
            "Keep it brief (one short sentence). For example, if theme is 'Un animal pour convaincre un enfant de venir au zoo', a good answer for intensity 1 would be 'une huitre', a good intensity 5 would be 'un chat sauvage', and a good intensity 10 would be 'un t-rex'. Also, keep in mind that you have to guess yourself the intensity of previous players and try and adapt your proposition to be in the right range of intensity (because the captain of the game will try and guess the different ranks once all propositions have been submitted)."
        )},
        {"role": "user", "content": (
            f"Thème : {theme}\n"
            f"Intensité assignée : {number}\n"
            "Écoutez bien les propositions déjà faites, et adaptez la vôtre :\n" +
            "\n".join(f"Player {num} : {text}" for num, (_, text) in enumerate(previous_suggestions))
        )}
    ]
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=40
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"ChatGPT API error: {e}", file=sys.stderr)
        return "[IA indisponible]"


def play_round(players, colors, round_number):
    total = len(players)
    cap_idx = round_number % total
    captain = players[cap_idx]
    others = [p for p in players if p != captain]

    clr_cap = colors[captain['name']]
    print(f"\n=== Manche {round_number+1} — Capitaine : {clr_cap}{captain['name']}{Style.RESET_ALL} ===")
    theme = input("Entrez le thème (en français) : ")

    intensities = random.sample(range(1, 11), k=len(others))
    random.shuffle(others)
    order = [{"name": p['name'], "kind": p['kind'], "number": i}
             for p, i in zip(others, intensities)]

    for p in order:
        if p['kind']=='human':
            clr = colors[p['name']]
            clear_screen()
            print(f"À {clr}{p['name']}{Style.RESET_ALL}, prendre l'ordi.")
            input("Prêt ?")
            print(f"Votre intensité : {clr}{p['number']}{Style.RESET_ALL}")
            input("Notez et passer.")
    clear_screen()

    print("\n--- Thème ---")
    print(theme)

    print("\n--- Ordre de passage ---")
    for idx, p in enumerate(order,1): clr=colors[p['name']]; print(f"{idx}. {clr}{p['name']}{Style.RESET_ALL}")
    print()

    print("--- Propositions ---")
    prev=[]
    for p in order:
        clr=colors[p['name']]
        if p['kind']=='human':
            text=input(f"{clr}{p['name']}{Style.RESET_ALL} : ")
        else:
            text=get_ai_suggestion(theme, p['number'], prev)
            print(f"{clr}{p['name']}{Style.RESET_ALL}: {text}")
        prev.append((p['number'],text))
        print()

    #print(f"{clr_cap}{captain['name']}{Style.RESET_ALL}, devinez l'ordre (ex: 3 1 2 ...):")
    #guess=input().strip()
    #print("Vous avez deviné :",guess)

    input("\n--- Résultats (par intensité) ---")
    for n,t in sorted(prev): print(f"{n}: {t}")


def main():
    openai.api_key=os.getenv("OPENAI_API_KEY")
    if not openai.api_key: print("Définir OPENAI_API_KEY");return
    nh=int(input("Nb humains: "))
    humans=[input(f"Prénom #{i+1}: ") for i in range(nh)]
    nai=int(input("Nb IA: "))
    ais=random.sample(AI_NAME_POOL,k=nai)
    players=[{'name':n,'kind':'human'} for n in humans]+[{'name':n,'kind':'ai'} for n in ais]
    colors=assign_colors(players)
    r=0
    while True:
        play_round(players,colors,r)
        r+=1
        if input("Encore ? (o/n):").lower()!='o':break

if __name__=='__main__': main()

