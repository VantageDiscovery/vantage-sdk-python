from vantage_sdk.model.document import (
    MetadataItem,
    VantageDocument,
    Variant,
    VariantItem,
)


# Integration tests for Vantage documents


class TestDocuments:
    def test_create_vantage_document(self):
        # Given
        metadata_items = [
            MetadataItem(key="meta1", value="meta1"),
            MetadataItem(key="meta2", value="meta2"),
            MetadataItem(key="meta3", value="meta3"),
        ]
        variants = [
            Variant(
                id="var1",
                items=[VariantItem(key="var_key1", value="var_value1")],
            ),
            Variant(
                id="var2",
                items=[VariantItem(key="var_key2", value="var_value2")],
            ),
        ]

        # When
        document = VantageDocument(
            id="doc1", metadata=metadata_items, variants=variants
        )

        # Then
        assert len(document.metadata) == 3
        assert len(document.variants) == 2
        for metadata_item in document.metadata:
            assert metadata_item.key.startswith("meta")
            assert metadata_item.value.startswith("meta")
        for variant in document.variants:
            assert variant.id.startswith("var")
            assert len(variant.items) == 1
            assert variant.items[0].key.startswith("var_key")
            assert variant.items[0].value.startswith("var_value")
