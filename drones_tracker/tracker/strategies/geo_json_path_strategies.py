from abc import ABC, abstractmethod


class GeoJSONPathStrategy(ABC):
    @abstractmethod
    def get_path(self, logs):
        pass


class PointsGeoJsonPath(GeoJSONPathStrategy):
    def get_path(self, logs):
        try:
            features = []
            for log in logs:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [log.payload['longitude'], log.payload['latitude']]
                    },
                    "properties": {
                        "height": log.payload['height'],
                        "horizontal_speed": log.payload['horizontal_speed'],
                        "timestamp": log.timestamp
                    }
                })

            return {
                "type": "FeatureCollection",
                "features": features
            }
        except Exception as e:
            raise e


class LinesGeoJsonPath(GeoJSONPathStrategy):
    def get_path(self, logs):
        try:
            coordinates = []
            for log in logs:
                coordinates.append(
                    [log.payload['longitude'], log.payload['latitude']])

            return {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "coordinates": coordinates,
                            "type": "LineString"
                        }
                    }
                ]
            }
        except Exception as e:
            raise e


class GeoJSONPathContext:
    def __init__(self, path_strategy):
        self.path_strategy = path_strategy

    def set_path_strategy(self, path_strategy):
        self.path_strategy = path_strategy

    def get_path(self, logs):
        return self.path_strategy.get_path(logs)


class GeoJSONStrategyFactory:
    @staticmethod
    def create_strategy(strategy):
        if strategy == 'points':
            return PointsGeoJsonPath()
        elif strategy == 'lines':
            return LinesGeoJsonPath()
        else:
            raise ValueError("Invalid GeoJSON path type")
