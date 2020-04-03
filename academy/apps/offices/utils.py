from .models import Setting, SettingSerializer


def get_settings(serializer=False):
    sett = Setting.get_data()
    if serializer:
        return SettingSerializer(sett).data
    return sett
