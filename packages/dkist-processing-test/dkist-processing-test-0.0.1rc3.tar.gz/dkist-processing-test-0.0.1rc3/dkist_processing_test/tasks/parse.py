from typing import List
from typing import TypeVar

from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.tasks import ParseL0InputData

S = TypeVar("S", bound=Stem)


class ParseL0TestInputData(ParseL0InputData):
    @property
    def fits_parsing_class(self):
        return L0FitsAccess

    @property
    def tag_flowers(self) -> List[S]:
        return super().tag_flowers + [
            SingleValueSingleKeyFlower(
                tag_stem_name=StemName.task.value, metadata_key="ip_task_type"
            ),
        ]
