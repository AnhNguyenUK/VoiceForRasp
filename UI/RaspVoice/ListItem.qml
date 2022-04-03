import QtQuick 2.12

Item {
    property color cmdcolor: "Red"
    property string cmdName
    property string cmdValue

    Rectangle{
        id: text_container
        height: parent.height
        width: parent.width
        radius: 5
        color: "#FEF3FF"

        Row{
            anchors.fill: parent
            padding: 5
            Column{
                height: parent.height
                width: 0.75 * parent.width
                padding: 5
                Text {
                    font.pointSize: 15
                    font.family: "Futura"
                    text: cmdName
                }
                Text {
                    font.pointSize: 13
                    font.family: "Open Sans"
                    text: cmdValue
                }
            }
            Text{
                id: statusText
                height: parent.height
                width: 0.25 * parent.width
                horizontalAlignment: Text.AlignRight
                rightPadding: 25
                text: "..."
                font.pointSize: 10
            }
        }
    }

    // Connection{
    //     target: client
    //     onSentStatus: {
    //         statusText.text = sentStatus   
    //     }
    // }

    ListModel{
        id: testModel
        ListElement{
            mcmdName: "Fans"
            mcmdValue: "1232153"
        }
        ListElement{
            mcmdName: "Diffuser"
            mcmdValue: "1232153"
        }
        ListElement{
            mcmdName: "Light"
            mcmdValue: "1232153"                    
        }
    }
}
