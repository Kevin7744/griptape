from typing import Literal

import pytest
from unittest.mock import Mock
from griptape.drivers import AzureOpenAiDalleImageGenerationDriver


class TestAzureOpenAiDalleImageGenerationDriver:
    @pytest.fixture
    def driver(self):
        return AzureOpenAiDalleImageGenerationDriver(
            model="dall-e-3",
            client=Mock(),
            azure_endpoint="https://dalle.example.com",
            azure_deployment="dalle-deployment",
            image_size="512x512",
        )

    def test_init(self, driver):
        assert driver

    def test_init_requires_endpoint(self):
        with pytest.raises(TypeError):
            AzureOpenAiDalleImageGenerationDriver(
                model="dall-e-3", client=Mock(), azure_deployment="dalle-deployment", image_size="512x512"
            )

    def test_init_requires_deployment(self):
        with pytest.raises(TypeError):
            AzureOpenAiDalleImageGenerationDriver(
                model="dall-e-3", client=Mock(), azure_endpoint="https://dalle.example.com", image_size="512x512"
            )

    def test_generate_image(self, driver):
        driver.client.images.generate.return_value = Mock(data=[Mock(b64_json=b"aW1hZ2UgZGF0YQ==")])

        image_artifact = driver.generate_image(prompts=["test prompt"])

        assert image_artifact.value == b"image data"
        assert image_artifact.mime_type == "image/png"
        assert image_artifact.width == 512
        assert image_artifact.height == 512
        assert image_artifact.model == "dall-e-3"
        assert image_artifact.prompt == "test prompt"
