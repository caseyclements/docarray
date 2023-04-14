import numpy as np
import pytest

from docarray import BaseDoc, DocList
from docarray.documents import ImageDoc, TextDoc
from docarray.typing import NdArray


@pytest.mark.proto
def test_simple_proto():
    class CustomDoc(BaseDoc):
        text: str
        tensor: NdArray

    da = DocList(
        [CustomDoc(text='hello', tensor=np.zeros((3, 224, 224))) for _ in range(10)]
    )

    new_da = DocList[CustomDoc].from_protobuf(da.to_protobuf())

    for doc1, doc2 in zip(da, new_da):
        assert doc1.text == doc2.text
        assert (doc1.tensor == doc2.tensor).all()


@pytest.mark.proto
def test_nested_proto():
    class CustomDocument(BaseDoc):
        text: TextDoc
        image: ImageDoc

    da = DocList[CustomDocument](
        [
            CustomDocument(
                text=TextDoc(text='hello'),
                image=ImageDoc(tensor=np.zeros((3, 224, 224))),
            )
            for _ in range(10)
        ]
    )

    DocList[CustomDocument].from_protobuf(da.to_protobuf())


@pytest.mark.proto
def test_nested_proto_any_doc():
    class CustomDocument(BaseDoc):
        text: TextDoc
        image: ImageDoc

    da = DocList[CustomDocument](
        [
            CustomDocument(
                text=TextDoc(text='hello'),
                image=ImageDoc(tensor=np.zeros((3, 224, 224))),
            )
            for _ in range(10)
        ]
    )

    DocList.from_protobuf(da.to_protobuf())