# Persistent toolbars support for FreeCAD
# Copyright (C) 2016  triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA


def persistentToolbars():
    """
    Persistent toolbars support for FreeCAD.
    """
    import operator
    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide import QtCore
    from PySide import QtGui

    global startToolbar
    startToolbar = False
    startToolbars = []
    conectedToolbars = []

    paramGet = App.ParamGet("User parameter:BaseApp/PersistentToolbars")

    def pythonToolbars():
        """
        Manage Python based toolbars in Arch and Draft workbench.
        """
        active = Gui.activeWorkbench().MenuText

        if active == "Draft" or active == "Arch":
            if hasattr(Gui, "draftToolBar"):
                Gui.draftToolBar.Activated()
            if hasattr(Gui, "Snapper"):
                Gui.Snapper.show()
        else:
            pass

    def onDefault():
        """
        Default sorting for toolbars.
        """
        toolbars = {}

        for i in mw.findChildren(QtGui.QToolBar):

            isConnected(i)

            if i.objectName() and i.isVisible() and not i.isFloating():
                toolbars[i.objectName()] = i
            else:
                pass

        sort = ["Workbench",
                "File",
                "Macro",
                "True",
                "View"]

        for i in sort:
            if i == "True":
                mw.addToolBarBreak(QtCore.Qt.TopToolBarArea)
            elif i in toolbars:
                mw.addToolBar(QtCore.Qt.TopToolBarArea, toolbars[i])
                del toolbars[i]
            else:
                pass

        for i in toolbars:
            mw.addToolBar(QtCore.Qt.TopToolBarArea, toolbars[i])

    def onSave():
        """
        Save current workbench toolbars position.
        """
        active = Gui.activeWorkbench().MenuText
        group = paramGet.GetGroup(active)

        top = []
        left = []
        right = []
        bottom = []

        for i in mw.findChildren(QtGui.QToolBar):
            if i.objectName() and i.isVisible() and not i.isFloating():

                area = mw.toolBarArea(i)

                x = i.geometry().x()
                y = i.geometry().y()
                b = mw.toolBarBreak(i)
                n = i.objectName().encode("UTF-8")

                if area == QtCore.Qt.ToolBarArea.TopToolBarArea:
                    top.append([x, y, b, n])
                elif area == QtCore.Qt.ToolBarArea.LeftToolBarArea:
                    left.append([x, y, b, n])
                elif area == QtCore.Qt.ToolBarArea.RightToolBarArea:
                    right.append([-x, y, b, n])
                elif area == QtCore.Qt.ToolBarArea.BottomToolBarArea:
                    bottom.append([x, -y, b, n])
                else:
                    pass
            else:
                pass

        top = sorted(top, key=operator.itemgetter(1, 0))
        left = sorted(left, key=operator.itemgetter(0, 1))
        right = sorted(right, key=operator.itemgetter(0, 1))
        bottom = sorted(bottom, key=operator.itemgetter(1, 0))

        topSave = []
        leftSave = []
        rightSave = []
        bottomSave = []

        for i in top:
            if i[2]:
                topSave.append("True")
                topSave.append(i[3])
            else:
                topSave.append(i[3])

        for i in left:
            if i[2]:
                leftSave.append("True")
                leftSave.append(i[3])
            else:
                leftSave.append(i[3])

        for i in right:
            if i[2]:
                rightSave.append("True")
                rightSave.append(i[3])
            else:
                rightSave.append(i[3])

        for i in bottom:
            if i[2]:
                bottomSave.append("True")
                bottomSave.append(i[3])
            else:
                bottomSave.append(i[3])

        group.SetBool("Saved", 1)
        group.SetString("Top", ".,.".join(topSave))
        group.SetString("Left", ".,.".join(leftSave))
        group.SetString("Right", ".,.".join(rightSave))
        group.SetString("Bottom", ".,.".join(bottomSave))

    def isConnected(i):
        """
        Connect toolbar (if not already connected) to onSave function.
        """
        if i.objectName():
            if i.objectName() in conectedToolbars:
                pass
            else:
                conectedToolbars.append(i.objectName())
                i.topLevelChanged.connect(onSave)
        else:
            pass

    def onRestore():
        """
        Restore current workbench toolbars position.
        """
        active = Gui.activeWorkbench().MenuText
        group = paramGet.GetGroup(active)

        toolbars = {}

        for i in mw.findChildren(QtGui.QToolBar):

            isConnected(i)

            if i.objectName() and i.isVisible() and not i.isFloating():
                toolbars[i.objectName().encode("UTF-8")] = i
            else:
                pass

        if group.GetBool("Saved"):
            topRestore = group.GetString("Top").split(".,.")
            leftRestore = group.GetString("Left").split(".,.")
            rightRestore = group.GetString("Right").split(".,.")
            bottomRestore = group.GetString("Bottom").split(".,.")

            for i in topRestore:
                if i == "True":
                    mw.addToolBarBreak(QtCore.Qt.TopToolBarArea)
                elif i in toolbars:
                    mw.addToolBar(QtCore.Qt.TopToolBarArea, toolbars[i])
                else:
                    pass

            for i in leftRestore:
                if i == "True":
                    mw.addToolBarBreak(QtCore.Qt.LeftToolBarArea)
                elif i in toolbars:
                    mw.addToolBar(QtCore.Qt.LeftToolBarArea, toolbars[i])
                else:
                    pass

            for i in rightRestore:
                if i == "True":
                    mw.addToolBarBreak(QtCore.Qt.RightToolBarArea)
                elif i in toolbars:
                    mw.addToolBar(QtCore.Qt.RightToolBarArea, toolbars[i])
                else:
                    pass

            for i in bottomRestore:
                if i == "True":
                    mw.addToolBarBreak(QtCore.Qt.BottomToolBarArea)
                elif i in toolbars:
                    mw.addToolBar(QtCore.Qt.BottomToolBarArea, toolbars[i])
                else:
                    pass
        else:
            onDefault()

    def onWorkbencActivated():
        """
        When workbench gets activated restore toolbar position.
        """
        try:
            active = Gui.activeWorkbench().MenuText
        except AttributeError:
            active = False

        if active:
            pythonToolbars()
            onRestore()
        else:
            pass

    def onVisibilityChanged(i):
        """
        When (first) toolbar is made visible restore toolbar position
        in (default) workbench. After restore toolbars when workbench
        is activated.
        """
        global startToolbar

        if i:
            for a in startToolbars:
                if a.isVisible():
                    a.visibilityChanged.disconnect(onVisibilityChanged)
                    startToolbars.remove(a)
                else:
                    pass

            onWorkbencActivated()

            if startToolbar:
                pass
            else:
                mw.workbenchActivated.disconnect(onStart)
                mw.workbenchActivated.connect(onWorkbencActivated)

            startToolbar = True
        else:
            pass

    def onStart():
        """
        Detect default workbench toolbars visibility change.
        """
        for i in mw.findChildren(QtGui.QToolBar):
            if i in startToolbars:
                pass
            else:
                startToolbars.append(i)
                i.visibilityChanged.connect(onVisibilityChanged)

    mw = Gui.getMainWindow()
    mw.workbenchActivated.connect(onStart)

persistentToolbars()
