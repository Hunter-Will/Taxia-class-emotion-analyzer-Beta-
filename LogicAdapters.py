from chatterbot import filters
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.trainers import ListTrainer
from preprocessor import *
from Sentiment import SentiCmp, SentimentVec
import ResponseSelection
import random


class BasicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.excluded_words = kwargs.get('excluded_words', [])

        with open("./Data/default_resp.dat", "r") as f:
            self.__default_resp = f.readlines()

        self.__list_trainer = ListTrainer(chatbot)

    @staticmethod
    def upconfidence(statement1, statement2):
        score, weight = SentiCmp(statement1, statement2)
        return (1 - weight) * statement2.confidence + weight * score

    def get_default_response(self, input_statement):
        return Statement(random.choice(self.__default_resp).strip('\n'))

    def process(self, input_statement, additional_response_selection_parameters=None):
        vec = SentimentVec(cleanstop(chprocess(input_statement.text)))
        ResponseSelection.update(vec)

        search_results = self.search_algorithm.search(input_statement)

        closet = next(search_results, input_statement)
        # closet.confidence=self.upconfidence(input_statement,res)
        for res in search_results:
            res.confidence = self.upconfidence(input_statement, res)
            if res.confidence < self.maximum_similarity_threshold:
                continue
            if res.confidence >= closet.confidence:
                closet = res

        recent = filters.get_recent_repeated_responses(
            self.chatbot, input_statement.conversation)
        res_selc = {
            'search_in_response_to': closet.search_text,
            'exclude_text': recent,
            'exclude_text_words': self.excluded_words
        }
        resps = list(self.chatbot.storage.filter(**res_selc))

        if resps:
            resp = self.select_response(input_statement, resps)
            resp.confidence = (resp.confidence+closet.confidence)/2
        else:
            resp = self.get_default_response(input_statement)

        if resp.confidence >= 0.9:
            self.__list_trainer.train([input_statement, resp.text])
        else:
            self.__default_resp.append(resp.text)
        return resp
