"""collection of serializer classes"""
from datetime import datetime
from json import loads
from uuid import UUID

from timeslime.model import Setting, Timespan


class TimespanSerializer:
    """serializer for a timespan object"""

    @classmethod
    def deserialize(cls, json_string: str) -> Timespan:
        """deserialize a json string into a Timespan object
        :param json_string: defines json string"""
        if isinstance(json_string, str):
            timespan_object = loads(json_string)
        else:
            timespan_object = json_string

        timespan = Timespan()

        if 'id' in timespan_object:
            timespan.id = UUID(timespan_object['id'])

        if timespan_object["start_time"] == "None":
            raise KeyError

        timespan.start_time = datetime.strptime(
            timespan_object["start_time"], "%Y-%m-%d %H:%M:%S.%f"
        )

        if 'stop_time' in timespan_object:
            if timespan_object['stop_time'] == 'None':
                return timespan
            timespan.stop_time = datetime.strptime(
                timespan_object["stop_time"], "%Y-%m-%d %H:%M:%S.%f"
            )
        return timespan

    @classmethod
    def serialize(cls, timespan: Timespan):
        """serialize a Timespan object into a string
        :param timespan: defines Timespan object"""
        return {
            "id": str(timespan.id),
            "start_time": str(timespan.start_time),
            "stop_time": str(timespan.stop_time),
        }


class SettingSerializer:
    """serializer for a setting object"""

    @classmethod
    def deserialize(cls, json_string: str) -> Setting:
        """deserialize a json string into a Setting object
        :param json_string: defines json string"""
        if isinstance(json_string, str):
            setting_object = loads(json_string)
        else:
            setting_object = json_string

        setting = Setting()

        if "id" in setting_object:
            setting.id = UUID(setting_object["id"])

        if setting_object["key"] == "None" or setting_object["key"] is None:
            raise KeyError

        setting.key = setting_object["key"]

        if "value" in setting_object:
            if setting_object["value"] == "None":
                return setting
            setting.value = setting_object["value"]
        return setting

    @classmethod
    def serialize(cls, setting: Setting):
        """serialize a Setting object into a string
        :param setting: defines Setting object"""
        return {
            "id": str(setting.id),
            "key": setting.key,
            "value": setting.value,
        }

    def serialize_list(self, settings: list):
        """serialize a Setting object into a string
        :param settings: defines a list of Setting object"""
        settings_json = []
        for setting in settings:
            settings_json.append(self.serialize(setting))

        return settings_json
