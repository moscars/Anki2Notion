# anki2notion

Turn [Anki](https://apps.ankiweb.net) flashcards into [Notion](https://www.notion.so) toggle blocks.

![results](https://media.giphy.com/media/zFW24gju13s7O1NhP7/giphy.gif)

## Usage

Install [notion-py](https://github.com/jamalex/notion-py) (requires Python 3.5 or greater) by running:

`pip install notion`

Install [progress](https://github.com/verigak/progress) by running:

`pip install progress`

* Clone this repo.
* Export the deck you want to import to Notion from Anki by using these options:
![exportoptions](https://i.imgur.com/StkX2KC.png)
* Add the .txt file to the repository
* If you have images in your Anki deck, add an asset folder with them in the repository.

Open main.py and edit these variables: <br>
```Python
# Insert the URL of the page you want to edit (Open Notion is browser)
page_url = "Insert url"
# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
tok_v2 = "Insert token v2"
asset_folder = "images"
# Export deck as 'Cards as Plain Text' with 'Include HTML and media references' ticked
textfile = "test.txt"
```

Finally, run the program: <br>
`python3 main.py`
