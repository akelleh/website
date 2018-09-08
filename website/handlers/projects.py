import tornado.web
import uuid
import time


class ProjectHandler(tornado.web.RequestHandler):
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
        page_id = 1
        print(user_id)
        items = [
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
                ]

        self.render("../html/projects.html", title="Projects", items=items)
