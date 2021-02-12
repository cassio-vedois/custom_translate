# custom_translate
Class responsible for the translation and recording of messages in the request languages

Routine message translation for use in small multilingual applications. The messages involved in the '_ ()' function are first translated on the web on free sites and recorded in the settings.json file.
That way there will be no need to constantly access the web to make translations since the system messages are usually fixed and, once registered in settings.json, they will be available always decreasing the network flow.

Example of use:
>from translations.translate import gettex as _

>print(_("Message to be translated.", input_language="en", output_language="pt"))

>Mensagem a ser traduzida.

Json file:
{
  "LANGUAGES": {
    "en": {
      "Message to be translated.": {
          "pt": "Mensagem a ser traduzida."
      }
    }
  }
}

>print(_("Message to be translated.", input_language="en", output_language="it"))

>Messaggio da tradurre.

Json file:
{
  "LANGUAGES": {
    "en": {
      "Message to be translated.": {
          "pt": "Mensagem a ser traduzida."
          "it": "Messaggio da tradurre."
      }
    }
  }
}

If you do not enter the input and output languages, the class uses the default settings.

Example:

Json file:
{
    "DEFAULT": {
        "input": "pt", # Default input portuguese
        "output": "en" # Default output english
    },
}

>print(_("Mensagem a ser traduzida."))

>Message to be translated.

Json file:
{
  "DEFAULT": {
    "input": "pt",
    "output": "en"
  },
  "LANGUAGES": {
    "en": {
      "Message to be translated.": {
          "pt": "Mensagem a ser traduzida."
          "it": "Messaggio da tradurre."
      }
    },
    "pt": {
        "Mensagem a ser traduzida.": {
            "en": "Message to be translated."
        }
    }
  }
}

You can vary by entering a specific input / output language if you do not want to use the standard. However, if there is no default in the settings and an input or output language is not informed, the same input message will be returned.

In this way, the system will periodically record messages and systematically reduce the use of the web.
THAT SIMPLE!
