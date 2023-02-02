import pyttsx3
import openai
import speech_recognition as sr
import os

from dotenv import load_dotenv

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

openai.api_key = os.getenv("API_KEY")


class ChatBot:

    def __init__(self):
        return

    def __get_raw_response(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=2048
        )
        return response

    def __get_moderation_assessment(self, prompt):
        moderation = openai.Moderation.create(
            model="text-moderation-stable",
            input=prompt
        )
        return moderation

    def get_response(self, prompt):
        response = self.__get_raw_response(prompt)
        moderation = self.__get_moderation_assessment(prompt)
        if not moderation.results[0].flagged:
            response = response.choices[0].text.replace('\n\n', '\n')
            if response == '\n':
                response = response.choices[0].text[1:]
            return response
        return "The given prompt does not comply to the moderation policy.\nPlease revise the statement!"


class Senses:

    def __init__(self):
        return

    def speak(self, prompt, engine='sapi5', voice=1):
        """
        voice [0] => Male
        voice [1] => Female (default)
        """
        engine = pyttsx3.init(engine)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice].id)
        engine.say(prompt)
        engine.runAndWait()

    def hear_me(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(
                source=source,
                timeout=10,
                phrase_time_limit=7
            )
        try:
            command = r.recognize_google(audio)

        except sr.UnknownValueError:
            self.speak('Sorry! I didn\'t get that!')
            self.speak('Try Typing the command.')
            command = str(input('User: '))
        return command


def run_bot():
    senses = Senses()
    while True:
        print("User:")
        usr_input = semses.hear_me()
        if usr_input == "exit" or usr_input == "qw":
            print("GPT:\n Bye Bye!!")
            break
        response = ChatBot().get_response(prompt=str(usr_input))

        print_response = response.replace('\n\n', '\n')

        if print_response == '\n':
            print_response = print_response[1:]

        print("GPT:", print_response)
        print("========================================")
        senses.speak(response)
        print("")


if __name__ == '__main__':
    run_bot()
