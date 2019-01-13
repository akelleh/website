import tornado.web
from util import Event


class WritingHandler(tornado.web.RequestHandler):
    def get(self):
        event = Event(self, page_id=0, event_type='pageview')
        event.log()

        items = [
                    {
                     'title': 'If Correlation Doesn\'t Imply Causation, Then What Does?',
                     'description': 'A conceptual introduction to causal graphs.',
                     'thumbnail': 'static/0_72hZybkt6KZntsp5.png',
                     'url': 'https://medium.com/causal-data-science/if-correlation-doesnt-imply-causation-then-what-does-c74f20d26438',
                     'id_': 0
                     },
                     {
                       'title': 'Understanding Bias: A Pre-requisite For Trustworthy Results',
                       'description': 'Why do we need causal inference? What\'s wrong with just plotting X vs. Y and reading the answer?',
                       'thumbnail': 'static/1.png',
                       'url': 'https://medium.com/causal-data-science/understanding-bias-a-pre-requisite-for-trustworthy-results-ee590b75b1be',
                       'id_': 1
                     },
                     {
                       'title': 'A Technical Primer On Causality',
                       'description': 'A brief introduction to Pearlian causality and the back-door criterion',
                       'thumbnail': 'static/2.png',
                       'url': 'https://medium.com/@akelleh/a-technical-primer-on-causality-181db2575e41',
                       'id_': 2
                     },
                     {
                       'title': 'Speed vs. Accuracy: When is Correlation Enough? When Do You Need Causation?',
                       'description': 'What are the tradeoffs when you do causal instead of correlative analysis? Is causal inference practical on a deadline?',
                       'thumbnail': 'static/3.png',
                       'url': 'https://medium.com/@akelleh/speed-vs-accuracy-when-is-correlation-enough-when-do-you-need-causation-708c8ca93753',
                       'id_': 3
                     },
                     {
                       'title': 'What do AB tests actually measure?',
                       'description': 'We can use the tools we\'ve developed to look at our standard approaches in data science, and realize sometimes we\'re not measuring what we think we\'re measuring!',
                       'thumbnail': 'static/0_1zQt9lT_BwOv8y3H2.png',
                       'url': 'https://medium.com/@akelleh/what-do-ab-tests-actually-measure-e89ebd63a73e',
                       'id_': 4
                     },
                     {
                       'title': 'Causal Inference With pandas.DataFrames',
                       'description': 'How can we do observational causal inference in the usual data science workflow?',
                       'thumbnail': 'static/4.png',
                       'url': 'https://medium.com/@akelleh/causal-inference-with-pandas-dataframes-fc3e64fce5d',
                       'id_': 5
                     },

                ]

        projects = [
                {
                 'title': 'Causality',
                 'description': 'A python package implementing methods for causal inference, including propensity score matching, weighting, and g-formula approaches. See the documentation for more details!',
                 'thumbnail': 'https://cdn-images-1.medium.com/max/600/0*1zQt9lT_BwOv8y3H.png',
                 'url': 'https://github.com/akelleh/causality'
                },
                {
                 'title': 'Causal Data Science (blog)',
                 'description': 'A blog sharing techniques and intuition around causal inference in data science in a business context. Many of these articles are linked to by the writing portion of this site!',
                 'thumbnail': 'https://cdn-images-1.medium.com/max/800/1*3CPKsitAG2R6Qbj_bg1Kxg.png',
                 'url': 'https://medium.com/causal-data-science/causal-data-science-721ed63a4027'
                },
                {
                 'title': 'Traffic Dashboard',
                 'description': 'See how many visitors come to this site! Updated every 15 minutes',
                 'thumbnail': 'static/traffic.png',
                 'url': 'http://adamkelleher.com:8051/'
                }
                ]

        self.render("../html/writing.html", title="Writing", items=items, projects=projects)
