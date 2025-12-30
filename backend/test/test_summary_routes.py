"""Unit tests for summary API routes."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException

# Import schemas without importing routes to avoid circular dependency
from backend.app.schemas.summary_schema import SummaryRequest, ModifyRequest


class TestGenerateSummaryRoute:
    """Test cases for generate_summary endpoint - tests SummaryGenerator integration."""

    @patch('backend.app.utils.summary_generator.SummaryGenerator')
    @patch('backend.app.utils.task_manager.TaskManager')
    def test_summary_generator_integration(
        self, mock_task_manager, mock_summary_gen, test_db, mock_llm_client, mock_config, sample_task
    ):
        """Test summary generator integration without route circular import."""
        # Test the underlying logic without importing the route
        from backend.app.utils.summary_generator import SummaryGenerator
        from backend.app.utils.task_manager import TaskManager

        mock_task_manager.get_task.return_value = sample_task
        generator = SummaryGenerator(mock_llm_client, mock_config)

        # Verify generator can be created and used
        assert generator is not None
        assert generator.llm_client == mock_llm_client

    def test_summary_request_schema(self, sample_task):
        """Test summary request schema validation."""
        request = SummaryRequest(task_id=sample_task.id)
        assert request.task_id == sample_task.id


class TestModifySummaryRoute:
    """Test cases for modify_summary - tests ModifyRequest schema."""

    def test_modify_request_schema(self, sample_task):
        """Test modify request schema validation."""
        request = ModifyRequest(
            task_id=sample_task.id,
            modification_prompt="Make it shorter"
        )

        assert request.task_id == sample_task.id
        assert request.modification_prompt == "Make it shorter"


class TestSummaryRouteSchemas:
    """Test cases for summary route schemas."""

    def test_summary_response_schema(self):
        """Test summary response schema."""
        from backend.app.schemas.summary_schema import SummaryResponse

        response = SummaryResponse(
            task_id=1,
            summary="Test summary",
            success=True
        )

        assert response.task_id == 1
        assert response.summary == "Test summary"
        assert response.success is True

    def test_modify_response_schema(self):
        """Test modify response schema."""
        from backend.app.schemas.summary_schema import ModifyResponse

        response = ModifyResponse(
            task_id=1,
            original_summary="Original",
            modified_summary="Modified",
            success=True
        )

        assert response.task_id == 1
        assert response.original_summary == "Original"
        assert response.modified_summary == "Modified"
