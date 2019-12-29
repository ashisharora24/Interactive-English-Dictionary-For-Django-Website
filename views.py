from django.shortcuts import render
from .forms import DictionaryQueryModelForms
from .models import DictionaryQuery
from django.conf import settings

# Create your views here.
'''
    this is am interactive english dictionary
    where the user will search for meanings for the english word

    when the user provides the input
    the user will get the meeting of the word
    if the word doesnot exist, then closest words will be suggested to the user
'''

def home_page(request):
    '''
        we have model form
        we are creating the model form an taking input from user
        and we are also saving every search made by the user

        if the user is authenticated user, then user name will be saved,
        if the user is not authenticated blank will be saved
    '''
    template_name = "interactive_english_dictionary/home_page.html"
    context = {}

    # since we are using module form
    # model form is avaialable in forms.py
    form = DictionaryQueryModelForms(request.POST or None)

    # check is form is valid or not
    if form.is_valid():
        # we do not want to make changes in the database, so we stopping it here
        form.save(commit=False)

        # getting user entered value
        word = form.cleaned_data.get("word")

        # passing the word to html page
        context['word']=word

        # incase the user is not logged in the reach history will be saved in
        # as None
        user = None
        if word:
            # if user is logged in then search history will be in his\her name
            if request.user.is_authenticated:
                user = request.user

            # check for the meaning
            meaning = word_to_meaning(word)

            # if word doesnt exist in our dictionary
            result="not_exist"

            if meaning:
                result="exist"

                # passing meanings to html page
                context['meaning'] = meaning

            else:
                # if word doesnt exist then we will check for the close matching words
                if get_close_matches(word):
                    # passing the html page
                    context['suggested_word']=get_close_matches(word)
                else:
                    # no close matches found
                    context["no_words"]=True

            # updating the search query record
            DictionaryQuery.objects.create(user=user, word=word,result=result)

        form = DictionaryQueryModelForms()
    # passing the model form to the html page
    context['form']=form

    return render(request, template_name, context)

def import_json_file():
    '''
        imports the json file
        and sends back the data in dictionary format
    '''
    import json
    import os
    data_json = os.path.join(settings.BASE_DIR,'interactive_english_dictionary','data.json')
    return json.load(open(data_json))

def word_to_meaning(word):
    '''
        we will check if the word exist
        if the word doesnot exist, then return None
    '''
    data = import_json_file()
    w = word.lower()
    if w in data:
        return data[w]
    else:
        return

def get_close_matches(words):
    '''
        this will get the closes words which are related.
        example : ashish . closets will be oasis, dashi, basis
        the closest will be picked from the dictionary only
    '''
    import difflib
    from difflib import get_close_matches

    # import_json_file()
    #    --> returns the complete dictionary in the dtictionary datatype format
    # once the dictionary is received, we take only key values
    # import_json_file().keys()
    list_of_words = import_json_file().keys()

    # get_close_matches(word, [list of word])
    # this function wil return the closest words from the [list of words]
    return get_close_matches(words.lower(),list_of_words)


def confirmed_words_to_meaning(request,word):
    '''
        when we suggest the user to check the suggested words
        that time we are 100% sure the word already exist in the dictionary,
        so we show the meaning to those words in the link format
        the word is received in the url format
    '''
    template_name = "interactive_english_dictionary/home_page.html"
    context = {}
    context['word']=word
    # passing the model form to html page
    context['form']=DictionaryQueryModelForms()
    context['meaning'] = word_to_meaning(word)
    return render(request, template_name, context)
