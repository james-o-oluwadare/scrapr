import QtQuick 2.14
import QtQuick.Window 2.14
import QtQuick.Controls 2.14
import "./components"

Window {
    id: mainwindow
    width: 800
    height: 540
    visible: true
    color: "#00000000"
    title: qsTr("Searchr")
    flags: "FramelessWindowHint"


    Rectangle {
        id: bgwindow
        //opacity: 0
        color: "#282846"
        radius: 10
        border.color: "#33334c"
        border.width: 3
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        AppBar {
            id: appbar
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right

            onExitClicked: Qt.quit()

            DragHandler { onActiveChanged: if(active){
                                               mainwindow.startSystemMove()}}

        }

        Item {
            id: mainframe
            anchors {
                top: appbar.bottom; bottom: parent.bottom
                left: parent.left; right: parent.right
            }

            Item {
                id: menuframe
                property bool opened: false
                state: "closed"

                anchors {
                    left: mainframe.left
                    top: mainframe.top; bottom: mainframe.bottom
                }
                Rectangle {
                    id: menu_bg
                    anchors.fill: parent
                }

                Button {
                    id: menu_btn

                    width: 50; height: 30
                    anchors {
                        left: parent.left; leftMargin:5
                        top: parent.top; topMargin: 10
                    }

                    icon {
                        source: "./png/hamburger.svg"
                    }
                    display: AbstractButton.IconOnly
                    background: Rectangle {
                        width: parent.width
                        height: parent.height
                        color: menu_btn.down?"#202050":"transparent"
                    }

                    onClicked: {
                        menuframe.state = (menuframe.state=="opened"?"closed":"opened")
                    }
                }
                states:[
                    State {
                        name: "closed"
                        PropertyChanges {
                            target: menuframe
                            width: 60
                        }
                        PropertyChanges {
                            target: menu_bg
                            color: "transparent"
                        }
                    },
                    State {
                        name: "opened"
                        PropertyChanges {
                            target: menuframe
                            width: 150
                        }
                        PropertyChanges {
                            target: menu_bg
                            color: "#303090"
                        }
                    }
                ]
                transitions: [
                    Transition {
                        to:"*"
                        NumberAnimation {
                            target: menuframe
                            property: "width"
                            duration: 500
                            easing.type: Easing.Linear
                        }

                        ColorAnimation {
                            duration: 500
                            target: menu_bg
                            property: "color"
                        }
                    }
                ]
            }

            Item {
                id: leftframe
                width:250
                anchors {
                    left: menuframe.right
                    top: mainframe.top; bottom: mainframe.bottom
                }
                Loader {
                    source: "./components/SearchPage.qml"
                }
            }
            Item {
                id: rightframe
                anchors {
                    left: leftframe.right; right: mainframe.right
                    top: mainframe.top; bottom: mainframe.bottom
                }
                Loader {
                    source: "./components/ResultPage.qml"
                }
            }
        }
    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.33}
}
##^##*/
