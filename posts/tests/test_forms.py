from posts.forms import Feedback_form

class TestFeedbackForm:
    # Check whether Feedback form is accepting blank data
     def test_blank(self):
         form = Feedback_form(data={})
         assert form.is_valid() is False, 'Feedback form should be invalid if no data is given'

    # Check whether Feedback form is accepting valid data
     def test_with_data(self):
         data = {'email': 'test@gmail.com', "name" : "Sample Name", "message" : "Sample Message"}
         form = Feedback_form(data=data)
         assert form.is_valid() is True, 'Feedback form should be valid when data is given'
