import json
import re
import string
from typing import Any, Optional

import tiktoken

from vantage_sdk.model.validation import ErrorMessage, ValidationError


_MAX_ID_LENGTH = 256
_MAX_SEQUENCE_LENGTH = 8191
_VALID_OPERATIONS = ["add", "delete", "update"]
_VALID_META_NAME_CHARACTERS = set(
    string.ascii_lowercase + string.ascii_uppercase + string.digits + '-' + '_'
)
_VALID_META_ALL_VALUES = (int, float, str)
_VALID_META_NUMBER_VALUES = (int, float)


def _validate_id(document: dict[str, Any]) -> Optional[ErrorMessage]:
    if "id" not in document.keys():
        return ErrorMessage(
            field_name="id", error_message="Field must be present."
        )

    document_id = document["id"]

    if not isinstance(document_id, str):
        return ErrorMessage(
            field_name="id", error_message="Field content must be string."
        )

    if len(document_id) > _MAX_ID_LENGTH:
        return ErrorMessage(
            field_name="id",
            error_message=f"Maximum content length is {_MAX_ID_LENGTH}",
        )

    if re.search(r"[\x00-\x1F\x7F-\x9F]", document_id) is not None:
        return ErrorMessage(
            field_name="id",
            error_message="Field contains unsupported characters.",
        )

    return None


def _validate_text(
    document: dict[str, Any],
    model: str,
    mandatory: bool = True,
) -> Optional[ErrorMessage]:
    if "text" not in document.keys():
        if mandatory:
            return ErrorMessage(
                field_name="text", error_message="Field missing."
            )
        else:
            return None

    if not isinstance(document["text"], str):
        return ErrorMessage(
            field_name="text", error_message="Field content must be string."
        )

    encoding = tiktoken.encoding_for_model(model)

    if len(encoding.encode(document["text"])) > _MAX_SEQUENCE_LENGTH:
        return ErrorMessage(
            field_name="text",
            error_message="Content length exceeds maximum sequence length.",
        )

    return None


def _validate_operation(document: dict[str, Any]) -> Optional[ErrorMessage]:
    if "operation" not in document.keys():
        return None

    operation = document["operation"]

    if not isinstance(operation, str):
        return ErrorMessage(
            field_name="operation",
            error_message="Operation value must be string.",
        )

    if operation not in _VALID_OPERATIONS:
        return ErrorMessage(
            field_name="operation",
            error_message=f"Unsupported operation {operation}.",
        )

    return None


def _is_valid_meta_name(name: str) -> bool:
    split = name.split("_", 1)

    if len(split) == 1:
        return False

    suffix = split[1]
    return set(suffix) <= _VALID_META_NAME_CHARACTERS


def _validate_meta_value(key: str, value: Any) -> ErrorMessage:
    if key.startswith("meta_ordered") and not isinstance(value, float):
        return ErrorMessage(
            field_name=key,
            error_message="Value must be a float number.",
        )

    # If meta_ is a list, validate if all items are
    # either a number or a string.
    if isinstance(value, list):
        first_item_type = type(value[0])
        for item in value:
            if not isinstance(item, _VALID_META_ALL_VALUES):
                return ErrorMessage(
                    field_name=key,
                    error_message="Meta arrays can contain only "
                    "[str, float, int] values.",
                )
            current_item_type = type(item)
            if first_item_type != current_item_type:
                if isinstance(
                    first_item_type,
                    _VALID_META_NUMBER_VALUES,
                ) and isinstance(
                    current_item_type,
                    _VALID_META_NUMBER_VALUES,
                ):
                    continue

                return ErrorMessage(
                    field_name=key,
                    error_message="Meta arrays cannot contain mixed values.",
                )

    if not isinstance(value, _VALID_META_ALL_VALUES):
        return ErrorMessage(
            field_name=key,
            error_message="Value must be either [int, str, float], or an "
            "array of one of those types.",
        )


def _validate_meta_fields(document: dict[str, Any]) -> list[ErrorMessage]:
    errors = []
    meta_fields = {
        key: value
        for key, value in document.items()
        if key == "meta" or key.startswith("meta_")
    }

    if not any(meta_fields):
        return None

    for meta_field in meta_fields.items():
        key, value = meta_field
        if not _is_valid_meta_name(key):
            errors.append(
                ErrorMessage(
                    field_name=meta_field,
                    error_message="Field has invalid suffix. May contain only [a-zA-Z0-9-_] characters.",
                )
            )
            continue

        meta_error = _validate_meta_value(key, value)
        if meta_error is not None:
            errors.append(meta_error)

    return errors


def _validate_embeddings(
    document: dict[str, Any],
    embeddings_dimension: int,
    mandatory=False,
) -> Optional[ErrorMessage]:
    if "embeddings" not in document.keys():
        if mandatory:
            return ErrorMessage(
                field_name="embeddings",
                error_message="Field must be present.",
            )
        else:
            return None

    embeddings = document["embeddings"]

    if not isinstance(embeddings, list):
        return ErrorMessage(
            field_name="embeddings",
            error_message="Embeddings must be a list of float numbers",
        )

    actual_size = len(embeddings)
    if actual_size != embeddings_dimension:
        return ErrorMessage(
            field_name="embeddings",
            error_message="Mismatch in embeddings dimension: "
            f"found {actual_size},"
            f" expected {embeddings_dimension}",
        )

    return None


class DocumentValidator:
    _encountered_ids: list[str]

    def _validate_document(
        self,
        document: dict[str, Any],
        line_number: int,
        model: str,
        is_upe: bool = False,
        embeddings_dimension=None,
    ) -> Optional[ValidationError]:
        document_id = None
        error_messages = []

        id_error = _validate_id(document)
        if id_error is not None:
            error_messages.append(id_error)
        else:
            document_id = None

        operation_error = _validate_operation(document)
        if operation_error is not None:
            error_messages.errors.append(operation_error)

        text_error = _validate_text(
            document=document,
            model=model,
            mandatory=(not is_upe),
        )
        if text_error is not None:
            error_messages.append(text_error)

        meta_errors = _validate_meta_fields(document)
        if any(meta_errors):
            error_messages.extend(meta_errors)

        embeddings_error = _validate_embeddings(
            document=document,
            embeddings_dimension=embeddings_dimension,
            mandatory=is_upe,
        )
        if embeddings_error is not None:
            error_messages.append(embeddings_error)

        if not any(error_messages):
            return None

        return ValidationError(
            document_id=document_id,
            line_number=line_number,
            errors=error_messages,
        )

    def validate_jsonl(
        self,
        file_path: str,
        model: str,
        is_upe: bool = False,
        embeddings_dimension=None,
    ) -> list[ValidationError]:
        errors = []
        line_number = 0
        with open(file_path, 'r') as file:
            document = None
            line = None
            while True:
                try:
                    line = file.readline()
                except Exception as exception:
                    raise exception

                if not line:
                    return errors

                try:
                    document = json.loads(line)
                except Exception as exception:
                    raise exception

                error = self._validate_document(
                    document=document,
                    line_number=line_number,
                    is_upe=is_upe,
                    embeddings_dimension=embeddings_dimension,
                    model=model,
                )
                if error is not None:
                    errors.append(error)
                line_number += 1
