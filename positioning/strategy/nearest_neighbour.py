from scipy.spatial.distance import euclidean

from models import APData
from positioning import chains
from positioning.strategy.abstract_location_strategy import AbstractLocationStrategy
from positioning.vectorisation.by_mac_and_rssi import VectorisationByMacAndRssi


class NearestNeighbourStrategy(AbstractLocationStrategy):
    CHAINS = {
        'averages': chains.Averages,
        'permutations': chains.PermutationsChain,
        'consecutive': chains.ConsecutiveChain
    }

    def __init__(self, chain, **kwargs):
        self.vectorisation = self.create_vectorisation(**kwargs)
        if chain not in self.CHAINS.keys():
            raise ValueError("Incompatible chain: {}".format(chain))
        self.chain = self.CHAINS[chain](vectorisation=self.vectorisation, **kwargs)
        self.fingerprint_data = self.stats = None

    def initialise(self, **kwargs):
        result = self.chain.calculate(**kwargs)
        self.fingerprint_data = result["fingerprint_data"]
        self.stats = result["fingerprint_stats"]

    def locate(self, measures):
        measures_vector = self.vectorisation.vectorise(measures)
        distances = self.fingerprint_data.map(euclidean, measures_vector)
        return self.fingerprint_data.location(distances.argmin())

    @staticmethod
    def create_vectorisation(access_point_dao, **kwargs):
        macs_order = [ap.mac.mac for ap in access_point_dao.active()]
        rssis_order = APData.RSSIS_KEYS
        return VectorisationByMacAndRssi(macs_order, rssis_order)
