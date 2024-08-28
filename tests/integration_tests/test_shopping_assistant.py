#!/usr/bin/env python
from vantage_sdk.client import VantageClient


""" Integration tests for shopping assistant endpoints."""


class TestShoppingAssistant:
    def test_list_shopping_assistants(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]

        # When
        shopping_assistants_result = client.list_shopping_assistants()

        # Then
        assert len(shopping_assistants_result) == 3
        for assistant in shopping_assistants_result:
            assert assistant.account_id == test_account_id
            assert assistant.groups is not None

    def test_get_shopping_assistant(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        test_shopping_assistant_id = "test-shopping-assistant-id"

        # When
        shopping_assistant = client.get_shopping_assistant(
            test_shopping_assistant_id
        )

        # Then
        assert shopping_assistant.account_id == test_account_id
        assert (
            shopping_assistant.shopping_assistant_id
            == test_shopping_assistant_id
        )

    def test_create_shopping_assistant(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        name = "test-assistant"
        groups = ["group 1", "group 2", "group 3"]
        external_account_id = "test-external-account-id"
        llm_model_name = "text-embeddings-ada-002"

        # When
        shopping_assistant = client.create_shopping_assistant(
            name=name,
            groups=groups,
            external_account_id=external_account_id,
            llm_model_name=llm_model_name,
        )

        # Then
        assert shopping_assistant.account_id == test_account_id
        assert shopping_assistant.shopping_assistant_id is not None
        assert shopping_assistant.name == name
        assert shopping_assistant.groups == groups
        assert shopping_assistant.external_account_id == external_account_id
        assert shopping_assistant.llm_model_name == llm_model_name

    def test_delete_shopping_assistant(self, client: VantageClient) -> None:
        # Given
        test_shopping_assistant_id = "test-shopping-assistant-id"

        # When
        client.delete_shopping_assistant(test_shopping_assistant_id)

        # Then
        # Success, no error occurs
        assert 1 == 1
