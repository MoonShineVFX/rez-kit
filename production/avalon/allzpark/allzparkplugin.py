
import os
from allzpark import plugin
from allzpark.vendor.Qt import QtCore, QtGui, QtWidgets
from avalon.tools import widgets as avalon_widgets
from avalon.tools import models as avalon_models
from avalon.vendor import qtawesome
from avalon import io, style


def patch():
    # patch it so AssetModel won't connecting db on init
    def __init__(self, parent=None):
        avalon_models.TreeModel.__init__(self, parent=parent)
    setattr(avalon_models.AssetModel, "__init__", __init__)


patch()

avalon_icon = "{root}/payload/res/icons/ico/avalon.ico".format(
    root=os.environ["REZ_AVALON_ROOT"])


class AvalonLauncher(plugin.EnvPluginBase):
    """Avalon asset/task selector"""

    name = "Avalon"

    def __init__(self, parent=None):
        self.icon = QtGui.QIcon(avalon_icon)
        super(AvalonLauncher, self).__init__(parent)

        widgets = {
            "asset": avalon_widgets.AssetWidget(),
            "task": TaskList(),
        }

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widgets["asset"], stretch=True)
        layout.addWidget(widgets["task"])

        # init
        widgets["task"].set_asset(None)

        # signals
        widgets["asset"].selection_changed.connect(self.on_asset_changed)
        widgets["task"].currentTextChanged.connect(self.on_task_changed)

        self._widgets = widgets
        self._env = dict()

    def on_profile_changed(self, package):
        # TODO: should not be touching os.environ
        os.environ["AVALON_PROJECT"] = package.name
        io.uninstall()
        io.install()
        self._widgets["task"].get_task_icons()
        self._widgets["asset"].refresh()
        self._env.clear()
        self.clear_env()
        self.reveal()

    def on_asset_changed(self):
        env = self._env
        asset = self._widgets["asset"].get_active_asset_document()
        if asset:
            env["AVALON_SILO"] = asset["silo"]
            env["AVALON_ASSET"] = asset["name"]
        else:
            env.clear()

        self._widgets["task"].set_asset(asset)

    def on_task_changed(self, task):
        env = self._env
        if task == TaskList.NoTask:
            env.pop("AVALON_TASK", None)
        else:
            env["AVALON_TASK"] = task

        self.set_env(env)


class TaskList(QtWidgets.QComboBox):
    NoTask = "No task"

    def __init__(self, parent=None):
        super(TaskList, self).__init__(parent=parent)
        self._icons = {
            "__default__": qtawesome.icon("fa.male",
                                          color=style.colors.default),
            "__no_task__": qtawesome.icon("fa.exclamation-circle",
                                          color="darkred")
        }

    def get_task_icons(self):
        # Get the project configured icons from database
        project = io.find_one({"type": "project"})
        tasks = project["config"].get("tasks", [])
        for task in tasks:
            icon_name = task.get("icon", None)
            if icon_name:
                icon = qtawesome.icon("fa.{}".format(icon_name),
                                      color=style.colors.default)
                self._icons[task["name"]] = icon

    def set_asset(self, asset_doc=None):
        if asset_doc:
            tasks = asset_doc.get("data", {}).get("tasks", [])
        else:
            tasks = []

        self.clear()

        if not tasks:
            no_task_icon = self._icons["__no_task__"]
            self.addItem(no_task_icon, self.NoTask)

        else:
            default_icon = self._icons["__default__"]

            for task in sorted(tasks):
                icon = self._icons.get(task, default_icon)
                self.addItem(icon, task)
