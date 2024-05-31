import json
import re
import string
from json.decoder import JSONDecodeError
from typing import Any, Optional

import pyarrow.parquet as parquet
import tiktoken

from vantage_sdk.model.validation import (
    CollectionType,
    ErrorMessage,
    ValidationError,
)


_MAX_ID_LENGTH = 256
_MAX_SEQUENCE_LENGTH = 8191
_VALID_OPERATIONS = ["add", "delete", "update"]
_VALID_META_NAME_CHARACTERS = set(
    string.ascii_lowercase + string.ascii_uppercase + string.digits + '-' + '_'
)
_VALID_META_PRIMITIVE_VALUES = (int, float, str)
_NUMBERS = (int, float)
_LIST = list


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


def _check_for_duplicate(
    document_id: Optional[str],
    encountered: set[str],
) -> Optional[ErrorMessage]:
    if document_id is None:
        return None

    if document_id not in encountered:
        return None

    return ErrorMessage(
        field_name="id",
        error_message="Duplicate encountered.",
    )


def _validate_text(
    document: dict[str, Any],
    model: str = None,
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

    if not model:
        return None

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
            error_message=f"Unsupported operation: '{operation}'.",
        )

    return None


def _is_valid_meta_name(name: str) -> bool:
    split = name.split("_", 1)

    if len(split) == 1:
        return False

    suffix = split[1]
    return set(suffix) <= _VALID_META_NAME_CHARACTERS


def _validate_meta_value(key: str, value: Any) -> ErrorMessage:
    # Value of "meta_ordered" field must be a number.
    if key.startswith("meta_ordered"):
        if not isinstance(value, _NUMBERS):
            return ErrorMessage(
                field_name=key,
                error_message="Value must be a number.",
            )
        else:
            return None

    if isinstance(value, _VALID_META_PRIMITIVE_VALUES):
        return None

    # If meta field is a list/array, check if all items are
    # either a number or a string.
    if hasattr(value, '__iter__'):
        if len(value) == 0:
            return None

        is_string_list = isinstance(value[0], str)
        for item in value:
            if not isinstance(item, _VALID_META_PRIMITIVE_VALUES):
                return ErrorMessage(
                    field_name=key,
                    error_message="Meta arrays can contain only "
                    "[str, float, int] values.",
                )
            if is_string_list:
                if not isinstance(item, str):
                    return ErrorMessage(
                        field_name=key,
                        error_message="Meta arrays cannot contain mixed values.",
                    )
            else:
                if not isinstance(item, _NUMBERS):
                    return ErrorMessage(
                        field_name=key,
                        error_message="Meta arrays cannot contain mixed values.",
                    )
        return None

    return ErrorMessage(
        field_name=key,
        error_message="Value must be either [int, str, float], or an "
        "array of one of those types.",
    )


def _validate_meta_fields(document: dict[str, Any]) -> list[ErrorMessage]:
    errors = []
    meta_fields = {
        name: value
        for name, value in document.items()
        if name == "meta" or name.startswith("meta_")
    }

    if not any(meta_fields):
        return []

    for meta_field in meta_fields.items():
        name, value = meta_field
        if not _is_valid_meta_name(name):
            errors.append(
                ErrorMessage(
                    field_name=name,
                    error_message="Field has invalid name. "
                    "May contain only [a-zA-Z0-9-_] characters.",
                )
            )
            continue

        meta_error = _validate_meta_value(name, value)
        if meta_error is not None:
            errors.append(meta_error)

    return errors


def _validate_embeddings(
    document: dict[str, Any],
    embeddings_dimension: Optional[int],
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

    # Embeddings must be iterable (array/list)
    if not hasattr(embeddings, '__iter__'):
        return ErrorMessage(
            field_name="embeddings",
            error_message="Embeddings must be a list of float numbers.",
        )

    if not embeddings_dimension:
        return None

    actual_size = len(embeddings)
    if actual_size != embeddings_dimension:
        return ErrorMessage(
            field_name="embeddings",
            error_message="Mismatch in embeddings dimension: "
            f"found {actual_size},"
            f" expected {embeddings_dimension}",
        )

    for item in embeddings:
        if not isinstance(item, _NUMBERS):
            return ErrorMessage(
                field_name="embeddings",
                error_message="Embeddings must not contain non-number values.",
            )

    return None


def _create_json_parsing_error(
    exception: JSONDecodeError,
    line_number: int,
) -> ValidationError:
    message = f"JSON decoder error: {exception.msg}"

    return ValidationError(
        document_id=None,
        line_number=line_number,
        errors=[
            ErrorMessage(
                field_name=None,
                error_message=message,
            )
        ],
    )


class DocumentValidator:
    """Component for validating documents."""

    _encountered_ids: set[str] = set()

    def _validate_document(
        self,
        document: dict[str, Any],
        line_number: int,
        collection_type: CollectionType,
        embeddings_dimension: Optional[int] = None,
        model: Optional[str] = None,
    ) -> Optional[ValidationError]:
        document_id = document.get("id")
        error_messages = []

        id_error = _validate_id(document)
        if id_error is not None:
            error_messages.append(id_error)

        duplicate_document_error = _check_for_duplicate(
            document_id=document_id,
            encountered=self._encountered_ids,
        )
        if duplicate_document_error is not None:
            error_messages.append(duplicate_document_error)

        operation_error = _validate_operation(document)
        if operation_error is not None:
            error_messages.append(operation_error)

        text_error = _validate_text(
            document=document,
            model=model,
            mandatory=(
                collection_type == CollectionType.USER_PROVIDED_EMBEDDINGS
            ),
        )
        if text_error is not None:
            error_messages.append(text_error)

        meta_errors = _validate_meta_fields(document)
        if any(meta_errors):
            error_messages.extend(meta_errors)

        embeddings_error = _validate_embeddings(
            document=document,
            embeddings_dimension=embeddings_dimension,
            mandatory=(
                collection_type == CollectionType.USER_PROVIDED_EMBEDDINGS
            ),
        )
        if embeddings_error is not None:
            error_messages.append(embeddings_error)

        if document_id is not None:
            self._encountered_ids.add(document_id)

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
        collection_type: CollectionType,
        model: Optional[str] = None,
        embeddings_dimension: Optional[int] = None,
    ) -> list[ValidationError]:
        """Validates documents from a JSONL file.

        Parameters
        ----------
        file_path : str
            Path of the JSONL file in the filesystem.
        collection_type : CollectionType
            For what kind of collection are documents from this file intended.
        model : Optional[str] = None
            Which model should be used to generate embeddings (if any).
        embeddings_dimension : Optional[int] = None
            Dimension of embeddings (if provided in file).

        Raises
        ------
        FileNotFoundError
            If specified file is not found.

        Returns
        -------
        List of encountered errors. If file is valid, the list will be empty.
        """
        errors = []
        line_number = 0
        with open(file_path, 'r') as file:
            document = None
            line = None
            while True:
                line = file.readline()
                if not line:
                    # Reached end of file.
                    break

                document = None
                try:
                    document = json.loads(line)
                except JSONDecodeError as exception:
                    errors.append(
                        _create_json_parsing_error(
                            exception,
                            line_number,
                        )
                    )
                    continue

                error = self._validate_document(
                    document=document,
                    line_number=line_number,
                    model=model,
                    collection_type=collection_type,
                    embeddings_dimension=embeddings_dimension,
                )
                if error is not None:
                    errors.append(error)
                line_number += 1

        return errors

    """
    Validates documents from a Parquet file.

    Parameters
    ----------
    file_path : str
        Path of the Parquet file in the filesystem.
    collection_type : CollectionType
        For what kind of collection are documents from this file intended.
    model : Optional[str] = None
        Which model should be used to generate embeddings (if any).
    embeddings_dimension : Optional[int] = None
        Dimension of embeddings (if provided in file).

    Raises
    ------
    FileNotFoundError
        If specified file is not found.

    Returns
    -------
    List of encountered errors. If file is valid, the list will be empty.
    """

    def validate_parquet(
        self,
        file_path: str,
        collection_type: CollectionType,
        model: Optional[str] = None,
        embeddings_dimension: Optional[int] = None,
    ) -> list[ValidationError]:
        parquet_file = parquet.ParquetFile(file_path)
        batches = parquet_file.iter_batches(batch_size=4096)
        line_number = 0
        errors = []

        for batch in batches:
            items = batch.to_pandas().to_dict(orient="records")
            for document in items:
                error = self._validate_document(
                    document=document,
                    line_number=line_number,
                    model=model,
                    collection_type=collection_type,
                    embeddings_dimension=embeddings_dimension,
                )
                if error is not None:
                    errors.append(error)
                line_number += 1

        return errors


VALIDATOR = DocumentValidator()
