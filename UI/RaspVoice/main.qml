import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Layouts 1.12

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Smart Home IoT Station")

    Column{
        anchors.fill: parent
        Rectangle{
            id: appBar
            color: "#04C9FF"
            width: parent.width
            height: 50
            RowLayout{
                anchors.fill: parent

                Text {
                    id: dashboardTitle
                    width: parent.width
                    height: 15
                    Layout.alignment: Qt.AlignLeft
                    Layout.leftMargin: 5
                    text: qsTr("Voice Dashboard")
                    color: "white"
                    font.pointSize: 15
                    font.family: "Open Sans"
                    font.bold: true
                }

                // Button{
                //     id: recordButton
                //     width: 100
                //     height: 40
                //     Layout.alignment: Qt.AlignRight
                //     Layout.rightMargin: 20
                //     title: "Record"
                //     buttonColor: "#009CC7"
                //     stage1: "Record"
                //     stage2: "Stop"
                // }
            }
        }

        Row{
            width: parent.width
            height: parent.height
            spacing: 5
            Rectangle{
                id: tabBar
                width: (parent.width * 0.25 > 200) ? 200 : parent.width * 0.25
                height: parent.height
                color: "#00789A"
                Column{
                    height: parent.height
                    width: parent.width
                    topPadding: 10
                    bottomPadding: 10
                    spacing: 5
                    Row{
                        id: lightSection
                        height: 50
                        width: parent.width
                        anchors.horizontalCenter: parent.horizontalCenter 
                        spacing: 5
                        Image {
                            id: image1
                            source: "images/idea.png"
                            width: 30
                            height: 30
                        }
                        DeviceButton{
                            id: light
                            width: 100
                            height: 40
                            deviceName: "LIGHT"
                            buttonColor: "#009CC7"
                            stage1: "ON"
                            stage2: "OFF"
                        }
                    }
                    Row{
                        id: diffuserSection
                        height: 50
                        width: parent.width
                        anchors.horizontalCenter: parent.horizontalCenter 
                        spacing: 5
                        Image {
                            id: image2
                            source: "images/diffuser.png"
                            width: 30
                            height: 30
                        }
                        DeviceButton{
                            id: diffuser
                            width: 100
                            height: 40
                            deviceName: "DIFFUSER"
                            buttonColor: "#009CC7"
                            stage1: "ON"
                            stage2: "OFF"
                        }
                    }
                    Row{
                        id: socketSection
                        height: 50
                        width: parent.width
                        anchors.horizontalCenter: parent.horizontalCenter 
                        spacing: 5
                        Image {
                            id: image3
                            source: "images/socket.png"
                            width: 30
                            height: 30
                        }
                        DeviceButton{
                            id: socket
                            width: 100
                            height: 40
                            deviceName: "SOCKET"
                            buttonColor: "#009CC7"
                            stage1: "ON"
                            stage2: "OFF"
                        }
                    }
                    Row{
                        id: fanSection
                        height: 50
                        width: parent.width
                        anchors.horizontalCenter: parent.horizontalCenter 
                        spacing: 5
                        Image {
                            id: image4
                            source: "images/fan.png"
                            width: 30
                            height: 30
                        }
                        Slider {
                            property double backend: 0
                            width: 100
                            height: 40
                            maximum:  10
                            value:    backend
                            minimum: -10
                        }
                    }
                }
            }

            Column{
                height: parent.height
                width: parent.width - tabBar.width
                topPadding: 5
                bottomPadding: 5
                spacing: 5
                Item {
                    id: listViewContainer
                    height: parent.height * 0.75
                    width: parent.width
                    ListView{
                        anchors.fill: parent
                        spacing: 5
                        topMargin: 5
                        leftMargin: 5
                        rightMargin: 5
                        clip: true
                        model: dataModel.model
                        delegate: Component{
                            ListItem{
                                cmdName: mcmdName
                                cmdValue: mcmdValue
                                width: parent.width
                                height: 70
                            }
                        }
                    }
                }
                
                Rectangle{
                    id: spectrumView
                    radius: 5
                    width: parent.width
                    height: parent.height - listViewContainer.height
                    color: "#ABEDFF"
                }
            }
        }
    }
}
