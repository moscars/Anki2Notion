from notion.client import NotionClient
from notion.block import *
from progress.bar import Bar

# Insert the URL of the page you want to edit (Open Notion is browser)
page_url = "Insert url"
# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
tok_v2 = "Insert token v2"
asset_folder = "images"
# Export deck as 'Cards as Plain Text' with 'Include HTML and media references' ticked
textfile = "test.txt"

print("Preparing data")
#Split the input file into questions and answers
list_ = open(textfile).read().split('\n')
questions = []
answers = []
for complete in list_:
    qans = complete.split('\t')
    if len(qans) == 2:
        questions.append(qans[0])
        answers.append(qans[1])

def remove_leading_quotes(list_):
    for i in range(0, len(list_)):
        l = list_[i]
        if l[0] == "\"":
            l = l[1: len(l) - 1]
            list_[i] = l

def remove_trailing_space(list_):
    for i in range(0, len(list_)):
        list_[i] = list_[i].strip()

def remove_multiple_quotes(list_):
    for i in range(0, len(list_)):
        l = list_[i]
        list_[i] = l.replace("\"\"", "\"")

def remove_subclass_info(list_):
    for i in range(0, len(list_)):
        l = list_[i]
        subclassinfo, quest = l.split(":</br> </div>  ")
        list_[i] = quest
    
def split_into_mult_on_image(list_):
    for i in range(0, len(list_)):
        l = list_[i]
        parts = l.split("<img ")
        totlist = []
        for j in range(0, len(parts)):
            ll = parts[j]
            subparts = ll.split("\">")
            for p in subparts:
                totlist.append(p)
        list_[i] = totlist

def remove_br_and_div(list_):
    for i in range(0, len(list_)):
        sublist = list_[i]
        acc = []
        for j in range(0, len(sublist)):
            subpart = sublist[j]
            subpart = subpart.replace("<div>", "")
            subpart = subpart.replace("</div>", "")
            subpart = subpart.replace("<br>", "")
            acc.append(subpart)
        list_[i] = acc

def remove_empty_sublist(list_):
    for i in range(0, len(list_)):
        sublist = list_[i]
        acc = []
        for j in range(0, len(sublist)):
            if sublist[j] != "":
                acc.append(sublist[j])
        list_[i] = acc

remove_leading_quotes(questions)
remove_trailing_space(questions)
remove_multiple_quotes(questions)
remove_subclass_info(questions)
split_into_mult_on_image(questions)
remove_br_and_div(questions)
remove_empty_sublist(questions)

remove_leading_quotes(answers)
remove_trailing_space(answers)
remove_multiple_quotes(answers)
split_into_mult_on_image(answers)
remove_br_and_div(answers)
remove_empty_sublist(answers)

print("Connecting to Notion")
 # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2=tok_v2)

# Replace this URL with the URL of the page you want to edit
page = client.get_block(page_url)
# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
page.title = "Imported From Anki"

bar = Bar('Importing to Notion', max=len(questions))

for i in range(len(questions)):

    current_q = questions[i]
    current_a = answers[i]
    image_question = False
    image_pos = {}
    question_string = ""
    image_missing_shown = False

#Insert question
    for i in range(0, len(current_q)):
        if current_q[i].startswith("src=\""):
            image_pos[i] = True
            image_question = True
        else:
            image_pos[i] = False
            question_string += current_q[i]
        
    togglechild = page.children.add_new(ToggleBlock, title = question_string)
    
    if image_question:
        for i in range(0, len(image_pos)):
            if image_pos[i]:
                try:
                    imagechild = togglechild.children.add_new(EmbedOrUploadBlock)
                    imagechild.upload_file(asset_folder + "/" + current_q[i][5 : len(current_q[i])])
                except:
                    if not image_missing_shown:
                        togglechild.title = togglechild.title + " (Missing image)"
                        image_missing_shown = True
        togglechild = togglechild.children.add_new(ToggleBlock, title = "Answer")
#Insert answer
    for i in range(0, len(current_a)):
        if current_a[i].startswith("src=\""):
            try:
                imagechild = togglechild.children.add_new(EmbedOrUploadBlock)
                imagechild.upload_file(asset_folder + "/" + current_a[i][5 : len(current_a[i])])
            except:
                if not image_missing_shown:
                    togglechild.title = togglechild.title + " (Missing image)"
                    image_missing_shown = True
        else:
            textchild = togglechild.children.add_new(TextBlock, title = current_a[i])
    
    bar.next()
bar.finish()
