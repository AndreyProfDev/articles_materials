


from pathlib import Path
import shutil
import tempfile
import unittest

from src.utils.monitoring.monitoring_service import CompletionEventRegistry, EmbeddingCreatedEvent, EmbeddingEventRegistry, TextCompletionEvent


class EmbeddingMonitoringServiceTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)
        self.monitoring_service = EmbeddingEventRegistry(cache_path=self.temp_dir_path)
    
    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_embedding_monitoring_is_empty(self):

        self.assertTrue(self.monitoring_service.is_empty())

    def test_embedding_monitoring_register_embedding(self):

        info = EmbeddingCreatedEvent(id='test test',
                            text='test test', 
                            embedding=[1, 2, 3],
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)
        self.assertFalse(self.monitoring_service.is_empty())

    def test_embedding_monitoring_retrieve_embedding_info(self):

        text = 'test test'
        info = EmbeddingCreatedEvent(id='test test',
                            text='test test', 
                            embedding=[1, 2, 3],
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)

        embedding_info = self.monitoring_service.get_event(text)
        self.assertEqual(embedding_info.text, text)

    def test_embedding_monitoring_retrieve_embedding_info_not_found(self):

        with self.assertRaises(ValueError):
            self.monitoring_service.get_event('test test')

    def test_embedding_monitoring_caching(self):

        text = 'test test'
        info = EmbeddingCreatedEvent(id='test test',
                            text='test test', 
                            embedding=[1, 2, 3],
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)

        monitoring_service_2 = EmbeddingEventRegistry(cache_path=self.temp_dir_path)
        embedding_info = monitoring_service_2.get_event(text)
        self.assertEqual(embedding_info.text, text)

    def test_embedding_monitoring_total_cost_calculation(self):

        info = EmbeddingCreatedEvent(id='test test',
                            text='test test', 
                            embedding=[1, 2, 3],
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)

        info2 = EmbeddingCreatedEvent(id='test test',
                            text='test test 2', 
                            embedding=[1, 2, 3],
                            cost=3,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info2)

        self.assertEqual(self.monitoring_service.get_total_cost(), 5)

class CompletionMonitoringServiceTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)
        self.monitoring_service = CompletionEventRegistry(cache_path=self.temp_dir_path)
    
    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_embedding_monitoring_register_embedding(self):

        info = TextCompletionEvent(id='test test',
                            text='test test', 
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)
        self.assertFalse(self.monitoring_service.is_empty())

    def test_embedding_monitoring_retrieve_embedding_info(self):

        text = 'test test'
        info = TextCompletionEvent(id=text,
                            text=text, 
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)

        embedding_info = self.monitoring_service.get_event(text)
        self.assertEqual(embedding_info.text, text)

    def test_embedding_monitoring_total_cost_calculation(self):

        info = TextCompletionEvent(id='test test',
                            text='test test', 
                            cost=2,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info)

        info2 = TextCompletionEvent(id='test test',
                            text='test test 2', 
                            cost=3,
                            model_name='GPT_4O')
        
        self.monitoring_service.register_event(info2)

        self.assertEqual(self.monitoring_service.get_total_cost(), 5)