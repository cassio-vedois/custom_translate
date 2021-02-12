# -*- coding: utf-8 -*-

__doc__ = """
Class responsible for the translation and recording of messages in the requested languages.
- Receive the message to be translated together with the input and output languages, or just the message
- If there are no known languages, obtain from the json file in the 'DEFAULT' key - (input and output)
- Get the message in the json file by the output language as registered
- If there is no translation in the output language, use googletrans to search for a translation on
  the web and register it in the json file
- Returns the translated message

Note: The version used for googletrans is 4.0.0rc1
To install use 'pip install googltrans == 4.0.0rc1'

Settings.json file structure:
{
    "DEFAULT": {"input": "en", "output": "pt"},
    "LANGUAGE": {"en": "English language input message": {
                        "pt": "Output message translated into Portuguese",
                        "es": "Output message translated into Spanish"
                        ...
                        }
                ...
                }
}
"""

import os, json
from googletrans import Translator

# from core.logger import Logger


def gettext(message, input_language=None, output_language=None):
    return CustomTranslator().translate(message, input_language, output_language)


class CustomTranslator:
    """
        Class responsible for the translation and recording of messages in the requested languages.
    """
    def __init__(self):

        self.translations = {}
        self.lang_default = {}
        self.path_settings = os.path.join(os.getcwd(), 'translations/') + 'settings.json'

    def __get_settings(self):
        """ Read the message archive """
        try:
            with open(self.path_settings) as jfile:
                self.translations = json.load(jfile)
                jfile.close()
        except Exception as e:
            print(str(e))
            # Logger.error(str(e))

    def __set_settings(self, jdata):
        """ Set a new incoming message with your corresponding translation """
        try:
            with open(self.path_settings, 'w') as jfile:
                json.dump(jdata, jfile, indent=4)
                jfile.close()
        except Exception as e:
            print(str(e))
            # Logger.error(str(e))

    @staticmethod
    def get_translation(message, lang):
        """
            Use Googletrans to translate the message
        """
        try:
            ret = Translator().translate(message, lang)
        except:
            return message

        return ret.text

    def translate(self, message, input_language=None, output_language=None):
        """
            Receive the message and return the translation as configured in the .json file.
            If not found, translate it and insert it in the file for later use.
        """

        self.__get_settings()

        input_lang = input_language if input_language else self.translations['DEFAULT'].get('input')
        output_lang = output_language if output_language else self.translations['DEFAULT'].get('output')

        if not output_lang:
            return message

        # Creates the default dictionary if there is no data in the json file
        has_update = False
        if not self.translations or not self.translations.get('LANGUAGE'):
            self.translations['LANGUAGE'] = {
                input_lang: {
                    message: {
                        output_lang: self.get_translation(
                            message=message, lang=output_lang)
                    }
                }
            }
            has_update = True
        elif not self.translations['LANGUAGE'].get(input_lang):
            self.translations['LANGUAGE'].update({
                input_lang: {
                    message: {
                        output_lang: self.get_translation(message=message, lang=output_lang)
                    }
                }
            })
            has_update = True
        elif not self.translations['LANGUAGE'][input_lang].get(message):
            self.translations['LANGUAGE'][input_lang].update({
                message: {
                    output_lang: self.get_translation(message=message, lang=output_lang)
                }
            })
            has_update = True
        elif not self.translations['LANGUAGE'][input_lang][message].get(output_lang):
            self.translations['LANGUAGE'][input_lang][message].update({
                output_lang: self.get_translation(message=message, lang=output_lang)
            })
            has_update = True

        if has_update:
            self.__set_settings(self.translations)

        # If there is a message for the output language, get it, otherwise it returns the original
        try:
            translations = self.translations['LANGUAGE']
            output_message = translations[input_lang][message][output_lang]
        except Exception as e:
            print(str(e))
            # Logger.error(str(e))
            output_message = message

        return output_message
