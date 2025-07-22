# Top Ten AI bot

This repo contains a Python implementation of [**Top Ten**](https://www.cocktailgames.com/jeu/top-ten/), enhanced with AI players via the OpenAI API. 

## Quick Rules

* **Goal**: Each non-captain player gets a secret intensity number (1 = mildest, 10 = wildest) and must propose exactly one answer matching that intensity to a given theme. The captain then guesses the ascending order of proposals.
* **Rounds**: The **captain** rotates each round; each human player privately sees their intensity.
* **AI players**: Generate one concise suggestion per intensity, adapting to previous answers.

## Setup Steps

1. **Clone the repo**

   ```bash
   git clone https://github.com/eloialonso/top-ten-bot.git
   cd top-ten-bot
   ```
2. **Install uv**

Follow the uv doc: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

3. **OpenAI API key**

   * Create an API key at [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
   * Copy the key
     
4. **.env file**

   * At project root, create `.env`:

     ```bash
     OPENAI_API_KEY=sk-...  # paste the key here
     ```

## Running the Game

```bash
cd top-ten-bot
uv run --env-file .env main.py
```

* Enter number of human and AI players, player names, and themes as prompted.
* The script handles private intensity reveals, AI suggestions, captain rotation, and guess input.
* After each round you can choose to play another or exit.

## Notes

* **Privacy**: Human players view their intensity by temporarily taking control of the terminal; screen is cleared afterwards.
* **Captain rotation**: Automatically rotates each round.
* **Terminal colors**: Uses `colorama` if supported.
