import pytest

from build_mime_types import _to_enum_name

class TestBuildMimeTypes:
    @pytest.mark.parametrize(
        "template,expected_name",
        [
            ('application/1d-interleaved-parityfec', 'APPLICATION_1D_INTERLEAVED_PARITYFEC'),
            ('multipart/form-data', 'MULTIPART_FORM_DATA'),
            ('model/vnd.flatland.3dml', 'MODEL_VND_FLATLAND_3DML'),
            ('application/EmergencyCallData.SubscriberInfo+xml', 'APPLICATION_EMERGENCYCALLDATA_SUBSCRIBERINFO_XML'),
            ('multipart/vnd.bint.med-plus','MULTIPART_VND_BINT_MED_PLUS'),
            ('audio/amr-wb+', 'AUDIO_AMR_WB_PLUS'),
            ('text/*+json', 'TEXT_ANY_JSON'),
        ]
    )
    def test__to_enum_name(self, template: str, expected_name: str):
        assert _to_enum_name(template=template) == expected_name




