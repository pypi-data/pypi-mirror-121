from django.test import TestCase

from brainutils import models
from brainutils import messages

class MessagesTestCase(TestCase):
    
    def setUp(self):
        self.language = models.Language.objects.create(name='English',title='English', default=True)
        
    def test_create_message(self):
        """Se prueba crear un mensaje"""
        msg = messages.get_message('msg.first', language=self.language, default='Hello Everyone')
        self.assertEqual(msg, 'Hello Everyone')
