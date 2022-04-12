import QtQuick 2.0
import QtQuick.Controls 2.5

Item {
    id: root
   
// public
    property double maximum: 10
    property double value:    0
    property double minimum:  0

    Slider{
        id: fanSlider
        width: parent.width
        height: parent.height
        from: minimum
        to: maximum
        stepSize: 10/3
        snapMode: Slider.SnapOnRelease
        onPressedChanged:{
            var pos = fanSlider.visualPosition
            const fanSpeedMode = ["off","low","medium","high"]
            var posIdx = pos*3
            if (!fanSlider.pressed) {
                console.log(fanSlider.valueAt(pos));
                console.log(fanSpeedMode[posIdx]);
                client.sendData('FAN',fanSpeedMode[posIdx])
            }
        }
    }
}