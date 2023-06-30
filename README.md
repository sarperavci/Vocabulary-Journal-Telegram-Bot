# Vocabulary Journal Telegram Bot

The Vocabulary Journal Telegram Bot is a bot designed to help English learners improve their vocabulary. It allows users to search for the definitions, forms, synonyms, example sentences, and collocations of English words. Users can add words to their personal vocabulary journal and generate a PDF document containing their vocabulary entries.

## Getting Started

To use the Vocabulary Journal Telegram Bot, follow these steps:

1. Install the necessary dependencies:
   - `telegram` (Python Telegram API)
   - `openai` (OpenAI Python API)
   - `requests` (HTTP library for sending requests)

2. Obtain a Telegram Bot API token:
   - Create a new bot on Telegram by talking to the [BotFather](https://core.telegram.org/bots#botfather).
   - Retrieve the API token provided by the BotFather.

3. Set up OpenAI API credentials:
   - Sign up for an account on the [OpenAI platform](https://platform.openai.com/).
   - Generate an OpenAI API key.

4. Clone or download the Vocabulary Journal Telegram Bot project files.

5. Replace the placeholders in the code with your Telegram Bot API token and OpenAI API key:
   - Replace `TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'` with your Telegram Bot API token.
   - Replace `openai.api_key = 'YOUR_OPENAI_API_KEY'` with your OpenAI API key.

6. Run the bot:
   - Execute the Python script containing the bot code.
   - The bot will start listening for incoming messages and commands.

## Usage

Once the bot is up and running, you can interact with it in a Telegram chat. Here are the available commands:

- **/read**: Generate a PDF document containing the vocabulary entries in your journal.
- **/remove _word_**: Remove a specific word from your vocabulary journal. Replace `_word_` with the word you want to remove.
- **/list**: List all the words in your vocabulary journal.

To search for the definition, forms, synonyms, example sentence, and collocations of a word, simply send the word as a message to the bot. The bot will provide you with the requested information and add the word to your vocabulary journal.

## Data Storage

The Vocabulary Journal Telegram Bot uses a text file (`database.txt`) to store the vocabulary entries. Each entry follows the format: `word:base64(json_data)`. The JSON data contains the definition, forms, synonyms, example sentence, and collocations of the word.

The `add` function is responsible for adding new entries to the database, while the `query` function retrieves the data for a given word. The encoded data is decoded using the `base64` module.

## PDF Generation

The bot can generate a PDF document containing the vocabulary entries in your journal. It converts the entries from Markdown format to PDF using an external service called `md-to-pdf.fly.dev`. The generated PDF file is then sent to you through the Telegram chat.

The `convert_markdown_to_pdf` function sends a POST request to the `md-to-pdf.fly.dev` service with the Markdown content, and the response is saved as a PDF file.

## Removing Words

You can remove specific words from your vocabulary journal using the `/remove` command followed by the word you want to remove. The `remove_words` function reads the database file, removes the specified words, and updates the file with the remaining entries. The function returns a list of the removed words.

## Listing Words

You can use the `/list` command to display all the words in your vocabulary journal. The function reads the database file, extracts the words, and sends the list in multiple messages (if necessary) to prevent exceeding Telegram's message length limit.



## Contributions

Contributions to the Vocabulary Journal Telegram Bot are welcome. If you find any issues or have suggestions for improvements, feel free to submit a pull request or open an issue on the project's repository.

## Disclaimer

The Vocabulary Journal Telegram Bot uses the OpenAI API for generating responses. While efforts have been made to ensure accurate and useful information, the bot's responses may not always be perfect. It is recommended to double-check any definitions, forms, synonyms, example sentences, or collocations provided by the bot through reliable sources.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
