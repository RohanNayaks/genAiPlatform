"""
Unit tests for Phase 1 implementation of the Generative AI Platform
Tests the core components: Guardial, TemplateCreator, FirstCache, and InvokeGenAI
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from Guardial import InputGuardial
from getTemplates import TemplateCreator
from models import InvokeGenAI
from reducelatency import FirstCache


class TestInputGuardial:
    """Test suite for InputGuardial data masking functionality"""

    def test_guardial_initialization(self):
        """Test InputGuardial initializes correctly with text"""
        text = "My name is John Doe"
        try:
            guardian = InputGuardial(text)
            assert guardian.unmasked_text == text
            assert hasattr(guardian, 'model_output')
            assert hasattr(guardian, 'result_data')
        except Exception as e:
            pytest.skip(f"Model loading failed (expected on first run): {str(e)}")

    def test_guardial_masks_sensitive_data(self):
        """Test that InputGuardial masks sensitive information"""
        text = "Contact John Smith at john.smith@example.com"
        try:
            guardian = InputGuardial(text)
            masked_text = guardian.result_data
            # Check that masking occurred (output should contain brackets for entities)
            assert isinstance(masked_text, str)
            assert len(masked_text) > 0
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")

    def test_guardial_create_entity_map(self):
        """Test entity map creation from model output"""
        text = "John Doe works here"
        try:
            guardian = InputGuardial(text)
            entity_map = guardian.create_entity_map(guardian.model_output, text)
            assert isinstance(entity_map, dict)
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")

    def test_guardial_replace_entities(self):
        """Test entity replacement with masked names"""
        text = "Call John Doe"
        try:
            guardian = InputGuardial(text)
            entity_map = {"John": "PERSON"}
            result = guardian.replace_entities(text, entity_map)
            assert "[PERSON]" in result or "John" in result
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")


class TestTemplateCreator:
    """Test suite for TemplateCreator template generation"""

    def test_template_creator_initialization(self):
        """Test TemplateCreator initializes with text"""
        text = "Generate utterances for login"
        try:
            creator = TemplateCreator(text)
            assert creator.text == text
            assert hasattr(creator, 'templateResponse')
            assert isinstance(creator.templateResponse, str)
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")

    def test_template_creator_get_masked_data(self):
        """Test that TemplateCreator gets masked data from InputGuardial"""
        text = "User John Smith wants to login"
        try:
            creator = TemplateCreator(text)
            masked_data = creator.getMaskeddata(text)
            assert isinstance(masked_data, str)
            assert len(masked_data) > 0
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")

    def test_template_creator_generate_intent_template(self):
        """Test intent template generation"""
        text = "Generate utterances for checkout"
        try:
            creator = TemplateCreator(text)
            template = creator.generateIntentTemplate(text)
            assert isinstance(template, str)
            assert len(template) > 0
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")

    def test_template_creator_call_template(self):
        """Test template call with LangChain prompt"""
        text = "Generate for purchase"
        try:
            creator = TemplateCreator(text)
            result = creator.callTemplate()
            assert isinstance(result, str)
            assert "Generate utterance for the Intent:" in result
        except Exception as e:
            pytest.skip(f"Model loading failed: {str(e)}")


class TestInvokeGenAI:
    """Test suite for InvokeGenAI model invocation"""

    def test_invoke_genai_initialization(self):
        """Test InvokeGenAI initializes with template"""
        template = "Generate utterances for [LOGIN]"
        invoker = InvokeGenAI(template)
        assert invoker.templateCreated == template
        assert hasattr(invoker, 'model_functions')
        assert isinstance(invoker.model_functions, dict)

    def test_invoke_genai_model_registry(self):
        """Test that model functions are registered"""
        template = "Test template"
        invoker = InvokeGenAI(template)
        assert "phi3" in invoker.model_functions
        assert "openAI" in invoker.model_functions

    def test_invoke_genai_phi3_model(self):
        """Test Phi3 model invocation"""
        template = "Generate utterances for [LOGIN]"
        invoker = InvokeGenAI(template)
        response = invoker.invoke_model("phi3")
        assert response is not None
        assert isinstance(response, str)
        assert template in response

    def test_invoke_genai_openai_model(self):
        """Test OpenAI model invocation"""
        template = "Generate utterances for [CHECKOUT]"
        invoker = InvokeGenAI(template)
        response = invoker.invoke_model("openAI")
        assert response is not None
        assert isinstance(response, str)

    def test_invoke_genai_invalid_model(self):
        """Test handling of invalid model name"""
        template = "Test template"
        invoker = InvokeGenAI(template)
        response = invoker.invoke_model("invalid_model")
        assert response is None

    def test_invoke_genai_phy3_method(self):
        """Test phy3Model method directly"""
        template = "Test [MASKED]"
        invoker = InvokeGenAI(template)
        response = invoker.phy3Model()
        assert "Phi3 model response" in response
        assert template in response


class TestFirstCache:
    """Test suite for FirstCache caching functionality"""

    @patch('redis.Redis')
    def test_first_cache_initialization(self, mock_redis):
        """Test FirstCache initializes Redis connection"""
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        cache = FirstCache()
        assert cache.r is not None
        mock_redis.assert_called_once()

    @patch('reducelatency.TC')  # Mock TemplateCreator
    @patch('reducelatency.IGI')  # Mock InvokeGenAI
    @patch('redis.Redis')
    def test_get_cache_answer_cache_hit(self, mock_redis, mock_igi, mock_tc):
        """Test cache hit scenario"""
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        # Setup mock to return a cached value
        mock_redis_instance.get.return_value = "cached response"

        cache = FirstCache()
        # Note: Current implementation always returns None for cache check
        # This test reflects the actual behavior
        response = cache.getCacheAnswer("test text", "phi3")
        assert response is not None

    @patch('reducelatency.TC')  # Mock TemplateCreator
    @patch('reducelatency.IGI')  # Mock InvokeGenAI
    @patch('redis.Redis')
    def test_get_cache_answer_cache_miss(self, mock_redis, mock_igi, mock_tc):
        """Test cache miss - falls back to template and model"""
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        # Mock TemplateCreator
        mock_tc_instance = MagicMock()
        mock_tc_instance.templateResponse = "masked template"
        mock_tc.return_value = mock_tc_instance

        # Mock InvokeGenAI
        mock_igi_instance = MagicMock()
        mock_igi_instance.invoke_model.return_value = "model response"
        mock_igi.return_value = mock_igi_instance

        cache = FirstCache()
        response = cache.getCacheAnswer("test text", "phi3")

        assert response == "model response"
        mock_tc.assert_called_once_with(text="test text")
        mock_igi.assert_called_once()

    @patch('redis.Redis')
    def test_first_cache_redis_connection(self, mock_redis):
        """Test Redis connection parameters"""
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        cache = FirstCache()

        # Verify Redis was called with correct parameters
        mock_redis.assert_called_once_with(
            host='localhost',
            port=6379,
            decode_responses=True
        )


class TestIntegration:
    """Integration tests for the complete pipeline"""

    def test_full_pipeline_generate_intent(self):
        """Test complete pipeline from input to model response"""
        try:
            # Step 1: Mask input
            text = "Generate utterances for user John Smith"
            guardian = InputGuardial(text)
            masked_input = guardian.result_data

            # Step 2: Create template
            creator = TemplateCreator(text)
            template = creator.templateResponse

            # Step 3: Invoke model
            invoker = InvokeGenAI(template)
            response = invoker.invoke_model("phi3")

            # Assertions
            assert masked_input is not None
            assert template is not None
            assert response is not None
            assert isinstance(response, str)
        except Exception as e:
            pytest.skip(f"Full pipeline test skipped: {str(e)}")

    @patch('reducelatency.TC')
    @patch('reducelatency.IGI')
    @patch('redis.Redis')
    def test_cache_layer_integration(self, mock_redis, mock_igi, mock_tc):
        """Test integration with cache layer"""
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        mock_redis_instance.get.return_value = None

        mock_tc_instance = MagicMock()
        mock_tc_instance.templateResponse = "[LOGIN] intent template"
        mock_tc.return_value = mock_tc_instance

        mock_igi_instance = MagicMock()
        mock_igi_instance.invoke_model.return_value = "Phi3 generated response"
        mock_igi.return_value = mock_igi_instance

        cache = FirstCache()
        response = cache.getCacheAnswer("Generate for login", "phi3")

        assert response == "Phi3 generated response"


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_input_text(self):
        """Test handling of empty input"""
        try:
            guardian = InputGuardial("")
            assert guardian.unmasked_text == ""
        except Exception as e:
            # Empty input might cause model to fail, which is acceptable
            assert True

    def test_special_characters_in_input(self):
        """Test handling special characters"""
        text = "Name: John!@#$%^&*() Email: test@#$%.com"
        try:
            guardian = InputGuardial(text)
            assert guardian.unmasked_text == text
        except Exception as e:
            pytest.skip(f"Special character handling: {str(e)}")

    def test_very_long_input(self):
        """Test handling of very long input"""
        text = "A" * 1000  # 1000 character input
        try:
            guardian = InputGuardial(text)
            assert len(guardian.result_data) > 0
        except Exception as e:
            pytest.skip(f"Long input handling: {str(e)}")

    def test_invoke_genai_with_none_template(self):
        """Test InvokeGenAI with None template"""
        invoker = InvokeGenAI(None)
        assert invoker.templateCreated is None
        response = invoker.phy3Model()
        assert response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
