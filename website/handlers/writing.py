import tornado.web
import uuid
import time


class WritingHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            user_id = self.get_cookie("user_id")
            if not user_id:
                raise Exception
        except:
            user_id = str(uuid.uuid4())
            self.set_cookie("user_id", user_id)
        event_id = str(uuid.uuid4())
        ts = time.time()
        page_id = 0
        print(user_id)
        items = [
                    {
                     'title': 'If Correlation Doesn\'t Imply Causation, Then What Does?',
                     'description': 'A conceptual introduction to causal graphs.',
                     'thumbnail': 'https://cdn-images-1.medium.com/max/600/0*1zQt9lT_BwOv8y3H.png',
                     'url': 'https://medium.com/causal-data-science/if-correlation-doesnt-imply-causation-then-what-does-c74f20d26438'
                     },
                     {
                       'title': 'Understanding Bias: A Pre-requisite For Trustworthy Results',
                       'description': 'Why do we need causal inference? What\'s wrong with just plotting X vs. Y and reading the answer?',
                       'thumbnail': 'https://cdn-images-1.medium.com/max/600/0*1zQt9lT_BwOv8y3H.png',
                       'url': 'https://medium.com/causal-data-science/understanding-bias-a-pre-requisite-for-trustworthy-results-ee590b75b1be'
                     },
                     {
                       'title': 'A Technical Primer On Causality',
                       'description': 'A brief introduction to Pearlian causality and the back-door criterion',
                       'thumbnail': 'https://cdn-images-1.medium.com/max/800/1*b31Wp5PD2_7ERqbbPta8kg.png',
                       'url': 'https://medium.com/@akelleh/a-technical-primer-on-causality-181db2575e41'
                     },
                     {
                       'title': 'Speed vs. Accuracy: When is Correlation Enough? When Do You Need Causation?',
                       'description': 'What are the tradeoffs when you do causal instead of correlative analysis? Is causal inference practical on a deadline?',
                       'thumbnail': 'https://cdn-images-1.medium.com/max/600/0*1zQt9lT_BwOv8y3H.png',
                       'url': 'https://medium.com/@akelleh/speed-vs-accuracy-when-is-correlation-enough-when-do-you-need-causation-708c8ca93753'
                     },
                     {
                       'title': 'What do AB tests actually measure?',
                       'description': 'We can use the tools we\'ve developed to look at our standard approaches in data science, and realize sometimes we\'re not measuring what we think we\'re measuring!',
                       'thumbnail': 'https://cdn-images-1.medium.com/max/600/0*1zQt9lT_BwOv8y3H.png',
                       'url': 'https://medium.com/@akelleh/what-do-ab-tests-actually-measure-e89ebd63a73e'
                     },
                  {
                    'title': 'Causal Inference With pandas.DataFrames',
                    'description': 'How can we do observational causal inference in the usual data science workflow?',
                    'thumbnail': 'https://cdn-images-1.medium.com/max/600/0*1zQt9lT_BwOv8y3H.png',
                    'url': 'https://medium.com/@akelleh/causal-inference-with-pandas-dataframes-fc3e64fce5d'
                  },

                ]

        self.render("../html/writing.html", title="Writing", items=items)
