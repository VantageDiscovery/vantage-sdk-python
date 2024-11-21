#!/usr/bin/env python
from vantage_sdk.client import VantageClient
from vantage_sdk.model.keys import OpenAIKey


""" Integration tests for Vantage vibe endpoints."""


class TestVantageVibe:
    def test_list_vibe_configurations(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]

        # When
        vibes_result = client.list_vibe_configurations()

        # Then
        assert len(vibes_result) == 3
        for vibe in vibes_result:
            assert vibe.account_id == test_account_id

    def test_get_vibe_configuration(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        test_vibe_id = "test-vibe-id"

        # When
        vibe = client.get_vibe_configuration(test_vibe_id)

        # Then
        assert vibe.account_id == test_account_id
        assert vibe.id == test_vibe_id

    def test_create_vibe_configuration(
        self, client: VantageClient, account_params: dict
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        name = "test-vibe"
        llm_model_name = "text-embeddings-ada-002"
        external_key = OpenAIKey(external_key_id="test-external-account-id")

        # When
        vibe = client.create_vibe_configuration(
            name=name,
            external_key=external_key,
            llm_model_name=llm_model_name,
        )

        # Then
        assert vibe.account_id == test_account_id
        assert vibe.id is not None
        assert vibe.name == name
        assert vibe.external_account_id == external_key.external_key_id
        assert vibe.llm_model_name == llm_model_name

    def test_delete_vibe_configuration(self, client: VantageClient) -> None:
        # Given
        test_vibe_id = "test-vibe-id"

        # When
        client.delete_vibe_configuration(test_vibe_id)

        # Then
        # Success, no error occurs
        assert 1 == 1
