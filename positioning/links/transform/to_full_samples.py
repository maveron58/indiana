from collections import defaultdict

from positioning.entities import Sample
from positioning.links.base import Base


class ToFullSamples(Base):
    def __init__(self, ap_data_dao, **kwargs):
        self.ap_data_dao = ap_data_dao

    def to_sample(self, stamp):
        ap_datas = self.ap_data_dao.get_for_time_range(stamp.start_time, stamp.end_time, asc=False)
        grouped = defaultdict(list)
        for ap_data in ap_datas:
            grouped[ap_data.router_mac.mac].append(ap_data)
        return Sample(stamp, grouped)

    def calculate(self, sample_stamps, **kwargs):
        return {"samples": list(map(self.to_sample, sample_stamps))}
