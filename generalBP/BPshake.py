# -*- coding: utf-8 -*-
import sys
import os

sys.path.append("../")
from blueprintBase import CBlueprintBase, make_Video
import outputDesc

class CBPShake(CBlueprintBase):

    # input: https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4
    # output: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-8529-014172.mp4
    def __init__(self, user_element, videoDuration, configDict=dict()):
        super(CBPShake, self).__init__("Shake")
        self._width = configDict.get('width', 720)
        self._height = configDict.get('height', 1280)
        self._user_element = user_element
        self._element_duration = videoDuration
        self._element_type = self.get_elementType_fromValue(user_element)

    def init_outputDesc(self):
        outputLocation = "*"
        outputAlphaLocation = ".avi"
        fps = 25.0
        duration = self._element_duration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(self._width, self._height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "shake"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_shake_Func
        configDict['newelement_func'] = self.newelement_shake_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_shake_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, self._element_duration)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "track": "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/duopai/track/t9.txt"
        }
        kwargs = {
            'element': configDict['elementNames']
        }
        level = self.create_level_from_action(baseActionDict, configDict, times, **kwargs)
        return level

    def newelement_shake_Func(self, configDict):
        names = configDict['elementNames']
        for i, name in enumerate(names):
            element = {
                'name': name,
                'source': 'designer',
                'type': self._element_type,
                'value': self._user_element
            }
            self._elements.append(element)


def test_effect():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4"
    videoDuration = 10000

    rotateVideo = make_Video(CBPShake, userVideo, videoDuration)
    print(rotateVideo)


if __name__ == "__main__":
    test_effect()
