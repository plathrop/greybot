import pinhook.plugin
from oxford_dictionaries_api import DictionaryEntriesApi, LemmatronApi
from oxford_dictionaries_api.rest import ApiException
import bcp47
import os

APP_ID = os.getenv("OXFORD_APP_ID")
APP_KEY = os.getenv("OXFORD_APP_KEY")

if not any(v is None for v in [APP_ID, APP_KEY]):
    @pinhook.plugin.command("define", "Get the definition of a word.")
    def define(message):
        entries = DictionaryEntriesApi()
        lemmas = LemmatronApi()
        source_lang = bcp47.languages["English"]

        words = message.arg.split()
        if len(words) != 1:
            reply = "Sorry {}, I can only define one word at a time!".format(message.nick)
            return pinhook.plugin.message(reply)

        try:
            response = lemmas.inflections_source_lang_word_id_filters_get(source_lang=source_lang,
                                                                          app_id=APP_ID,
                                                                          app_key=APP_KEY,
                                                                          word_id=words[0])
            headword = [item for item in response.results if item.type == "headword"][0]

            response = entries.entries_source_lang_word_id_filters_get(source_lang=source_lang,
                                                                       app_id=APP_ID,
                                                                       app_key=APP_KEY,
                                                                       filters=["definitions"],
                                                                       word_id=headword)

            definition = response.results.lexical_entries.entries.senses.definitions[0]
            reply = "{}: *{}* - {}".format(message.nick, headword, definition)
            return pinhook.plugin.message(reply)

        except ApiException:
            reply = "Sorry {}, I got an error from the dictionary service and cannot define {} for you.".format(message.nick, words[0])
            return pinhook.plugin.message(reply)

        except Exception as e:
            reply = "Sorry {}, I ran into an unexpected error. Please tell greytalyn about it!".format(message.nick)
            message.logger.exception("Error while executing 'define' command: {}", e)
            return pinhook.plugin.message(reply)
