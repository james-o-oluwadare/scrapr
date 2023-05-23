import QtQuick 2.14
import QtQuick.Controls 2.12

Item {
    id: search_page
    implicitHeight: 510; implicitWidth: 250
    //height: 510; width: 250

    Label {
        id: search_label
        text: "Search"
        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.top: parent.top
        font.pointSize: 14
        anchors.topMargin: 30
    }
    TextField {
        id: search_field
        height: 30
        width: 210
        anchors.top: search_label.bottom
        anchors.horizontalCenter: parent.horizontalCenter

        font.pointSize: 16
        bottomPadding: 5
        topPadding: 5
        placeholderText: "Enter article name"

        background: Rectangle{
            id: t_bg
            color: "#783232ff"
            radius: 3
            clip: true
            height: parent.height
            width: parent.width

            Rectangle {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: 2
                border.width: 0
                color: "#222299"
            }
        }

        Button {
            id: search_btn
            width: 20; height: 20
            icon.source: "../png/search.svg"
            display: AbstractButton.IconOnly
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            padding: 0
            background: Rectangle {
                color: search_btn.down? "#3030ff":"transparent"
                anchors.fill: parent
            }
        }
    }
}


