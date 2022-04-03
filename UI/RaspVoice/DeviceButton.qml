import QtQuick 2.0

Item {
    property string defaultStatus: "OFF"
    property string deviceName
    property color buttonColor
    property int buttonState: 0
    property string stage1
    property string stage2
    Rectangle{
        anchors.fill: parent
        color: buttonColor
        radius: 5
        Text {
            id: buttonText
            text: defaultStatus
            color: "white"
            anchors.centerIn: parent
        }
        MouseArea{
            anchors.fill: parent
            property bool isSendSuccessfull: true
            onClicked: {
                if(buttonState == 0){
                    console.log(stage1.toLowerCase())
                    buttonState = 1
                    buttonText.text = stage2
                    client.sendData(deviceName, stage1.toLowerCase())
                }else{
                    console.log(stage2.toLowerCase())
                    buttonState = 0
                    buttonText.text = stage1
                    client.sendData(deviceName, stage2.toLowerCase())
                }
            }
        }
    }
}
