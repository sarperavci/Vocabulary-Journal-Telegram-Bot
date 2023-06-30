from telegram.ext import Updater, CommandHandler, MessageHandler,Filters
import openai,base64,telegram,json,  requests,os,time


def enc(message):return base64.b64encode(message.encode('ascii')).decode('ascii')
def dec(key):return base64.b64decode(key.encode('ascii')).decode('ascii')

DATABASE_FILE = "database.txt"
TOKEN = '' #TELEGRAM BOT TOKEN
openai.api_key = 'sk-'

def convert_json_to_markdown(json_data,id,word):
    # Extract data from JSON
    definition = json_data.get("definition")
    forms = json_data.get("forms", [])
    synonyms = json_data.get("synonyms", [])
    sentence = json_data.get("sentence")
    collocations = json_data.get("collocations", [])

    # Create Markdown content
    markdown = f"## {id}- {word}\n\n"
    markdown += f"**Definition:** {definition}\n\n"

    if forms:
        markdown += "**Forms:**\n"
        for form in forms:
            markdown += f"- {form}\n"
        markdown += "\n"

    if synonyms:
        markdown += "**Synonyms:**\n"
        for synonym in synonyms:
            markdown += f"- {synonym}\n"
        markdown += "\n"

    if sentence:
        markdown += f"**Sentence:** {sentence}\n\n"

    if collocations:
        markdown += "**Collocations:**\n"
        for collocation in collocations:
            markdown += f"- {collocation}\n"

    return markdown

def add(a, b):
    b = enc(b)
    data = f"{a.lower()}:{b}\n"
    with open(DATABASE_FILE, "a") as file:
        file.write(data)

def query(a):
    with open(DATABASE_FILE, "r") as file:
        for line in file:
            key, value = line.strip().split(":")
            if key.lower() == a.lower():
                return dec(value)
    return False


def create(word):
  q = query(word)
  print(q)
  if q == False:

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[

              {"role": "user", "content": f"""
I will give you a word.
Define the word in a few basic sentence.
Give the word's other forms.
Give a few synonyms of the word.
Give a sentence using the word.
Give collocations of the word.

Here is the word: {word}
The response HAVE TO BE in JSON format.
keys: definition, forms (in a list), synonyms  (in a list), sentence, collocations  (in a list)"""},
          ]
  )

    result = ''
    for choice in response.choices:
        result += choice.message.content
    add(word,result)
    print(result)
    return result
  else: return q


def process_message(update, context):
    user_id = update.effective_chat.id
    word = update.message.text
    response = create(word)
    json_data = json.loads(response)
    response =convert_json_to_markdown(json_data,,word)
    context.bot.send_message(chat_id=user_id, text=response
                ,  parse_mode=telegram.ParseMode.MARKDOWN)

def read_command(update, context):
    user_id = update.effective_chat.id
    text = ""
    x = 1
    with open(DATABASE_FILE, "r") as file:
        for line in file:
            key, value = line.strip().split(":")

            text += convert_json_to_markdown(json.loads(dec(value)),x,key) + "\n"
            x += 1

    output_file = "vocabulary.pdf"
    convert_markdown_to_pdf(text, output_file)

    # Send the PDF document
    with open(output_file, "rb") as pdf_file:
        context.bot.send_document(chat_id=user_id, document=pdf_file)

    # Delete the temporary PDF file
    os.remove(output_file)

    # Send a message confirming the PDF has been sent
    context.bot.send_message(chat_id=user_id, text="PDF file has been sent.")


def convert_markdown_to_pdf(markdown_content, output_file):
    url = 'https://md-to-pdf.fly.dev'
    data = {
        'markdown': markdown_content
    }
    response = requests.post(url, data=data, stream=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"PDF file saved as {output_file}")
    else:
        print("Conversion failed. Status code:", response.status_code)

def remove_words(phrases):
    with open(DATABASE_FILE, "r") as file:
        lines = file.readlines()

    removed = []
    with open(DATABASE_FILE, "w") as file:
        for line in lines:
            key, _ = line.strip().split(":")
            if key.lower() not in phrases:
                file.write(line)
            else:
                removed.append(key)

    return removed

def remove_command(update, context):
    user_id = update.effective_chat.id
    phrase = " ".join(context.args)

    if not phrase:
        context.bot.send_message(chat_id=user_id, text="Please provide phrases to remove.")
        return

    removed_phrases = remove_words([phrase])

    if removed_phrases:
        removed_text = "\n".join(removed_phrases)
        response_text = f"The following phrases have been removed:\n{removed_text}"
    else:
        response_text = "No matching phrases found in the database."

    context.bot.send_message(chat_id=user_id, text=response_text)

def list_command(update, context):
    user_id = update.effective_chat.id

    with open(DATABASE_FILE, "r") as file:
        lines = file.readlines()

    words = [line.strip().split(":")[0] for line in lines]

    if not words:
        context.bot.send_message(chat_id=user_id, text="The database is empty.")
        return

    response_text = "Words in the database:\n"
    for i, word in enumerate(words, start=1):
        response_text += f"{i}. {word}\n"
        if i % 10 == 0 or i == len(words):
            time.sleep(0.1)
            context.bot.send_message(chat_id=user_id, text=response_text)
            response_text = ""



def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))
    # Add command handler for /read
    dispatcher.add_handler(CommandHandler("read", read_command))
    dispatcher.add_handler(CommandHandler("remove", remove_command))
    dispatcher.add_handler(CommandHandler("list", list_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
