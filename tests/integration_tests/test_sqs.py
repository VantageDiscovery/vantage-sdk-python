#!/usr/bin/env python
from vantage_sdk.client import VantageClient


""" Integration tests for semantic query suggestions endpoints."""


class TestSemanticQuerySuggestions:
    def test_list_semantic_query_suggestions_configurations(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        collection_id = "sqs-collection"

        # When
        sqs_configurations = (
            client.list_semantic_query_suggestions_configurations(
                collection_id=collection_id
            )
        )

        # Then
        assert len(sqs_configurations) == 3
        for config in sqs_configurations:
            assert config.account_id == test_account_id
            assert config.collection_id == collection_id

    def test_get_semantic_query_suggestions_configuration(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        collection_id = "sqs-collection"
        test_sqs_id = "test-sqs-id"

        # When
        sqs_configuration = (
            client.get_semantic_query_suggestions_configuration(
                sqs_configuration_id=test_sqs_id,
                collection_id=collection_id,
            )
        )

        # Then
        assert sqs_configuration.account_id == test_account_id
        assert sqs_configuration.semantic_query_suggestions_id == test_sqs_id

    def test_create_semantic_query_suggestions_configuration(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        collection_id = "sqs-collection"
        external_account_id = "test-external-account-id"
        llm_model_name = "text-embeddings-ada-002"
        system_prompt_id = "1234"
        suggestions_per_document = 3

        # When
        sqs_configuration = (
            client.create_semantic_query_suggestions_configuration(
                external_account_id=external_account_id,
                llm_model_name=llm_model_name,
                system_prompt_id=system_prompt_id,
                suggestions_per_document=suggestions_per_document,
                collection_id=collection_id,
            )
        )

        # Then
        assert sqs_configuration.account_id == test_account_id
        assert sqs_configuration.semantic_query_suggestions_id is not None
        assert sqs_configuration.system_prompt_id == system_prompt_id
        assert (
            sqs_configuration.suggestions_per_document
            == suggestions_per_document
        )
        assert sqs_configuration.external_account_id == external_account_id
        assert sqs_configuration.llm_model_name == llm_model_name

    def test_delete_semantic_query_suggestions_configuration(
        self, client: VantageClient
    ) -> None:
        # Given
        test_sqs_id = "test-sqs-id"
        collection_id = "sqs-collection"

        # When
        client.delete_semantic_query_suggestions_configuration(
            sqs_configuration_id=test_sqs_id,
            collection_id=collection_id,
        )

        # Then
        # Success, no error occurs
        assert 1 == 1
