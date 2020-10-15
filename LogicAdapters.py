from chatterbot.logic import LogicAdapter
from chatterbot import filters
from Sentiment import SentiCmp
from chatterbot.conversation import Statement

class BasicAdapter(LogicAdapter):
    def __init__(self,chatbot,**kwargs):
        super().__init__(chatbot,**kwargs)
        self.excluded_words = kwargs.get('excluded_words')
        
    def upconfidence(self,statement1,statement2):
        score,weight=SentiCmp(statement1,statement2)
        return (1-weight)*statement2.confidence+weight*score

    def get_default_response(self,input_statement):
        with open("./Data/default_resp.dat","r") as f:
            from random import choice
            resp=Statement(choice(f.readlines()).strip('\n'))
        resp.confidence=0
        return resp
    
    def process(self,input_statement,additional_response_selection_parameters=None):
        search_results=self.search_algorithm.search(input_statement)
        closet=next(search_results,input_statement)
        #closet.confidence=self.upconfidence(input_statement,res)
        for res in search_results:
            res.confidence=self.upconfidence(input_statement,res)
            if res.confidence<self.maximum_similarity_threshold:
                continue
            if res.confidence>=closet.confidence:
                closet=res
        recent=filters.get_recent_repeated_responses(self.chatbot,input_statement.conversation)
        res_selc={
            'search_in_response_to':closet.search_text,
            'exclude_text':recent,
            'exclude_text_words':self.excluded_words
            }
        resps=list(self.chatbot.storage.filter(**res_selc))
        if resps:
            resp=self.select_response(input_statement,resps)
            resp.confidence=(resp.confidence+closet.confidence)/2
        else:
            resp=self.get_default_response(input_statement)
        return resp
        

    
