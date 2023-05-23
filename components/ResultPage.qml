import QtQuick 2.14
import QtQuick.Controls 2.12

Item {
    id: result_page
    implicitHeight: 510; implicitWidth: 200
    //height: 510; width: 200

    QtObject {
        id: internal
        // check availability of database and populate screen

        property bool name: value
    }

    BusyIndicator {
        id: busy
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        running: false
        // animate running between true and false
        // animate height to zero when db Ready
    }

    ListView {
        id: listView
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: busy.bottom
        anchors.bottom: parent.bottom

        anchors.margins: 3
        model: ListModel {
            /*ListElement {
                name: "Grey"
                colorCode: "grey"
            }*/
        }
        delegate: Item {
            x: 5
            //width: 80
            height: 40

            Row {
                id: row1
                Rectangle {
                    width: 50
                    height: 40
                    color: colorCode
                }

                Text {
                    text: name
                    anchors.verticalCenter: parent.verticalCenter
                    font.bold: true
                }
                spacing: 10
            }
        }
    }
}
