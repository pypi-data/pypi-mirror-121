"""
The Extra assets widget.

The widget is a chunk of Qt embedded in Nuke's properties panel.
"""
import json
import nuke
import re
import os
from PySide2 import QtWidgets, QtGui, QtCore
from cionuke.components.conductor_knob import ConductorKnob
from ciopath.gpath_list import PathList


NODE_BLACKLIST = ["Write", "DeepWrite"]

TOKENS = (
    r"#+"  # image.####.exr - hash
    , r"%0\d+d"  # image.%04d.exr - percent
)

TOKEN_RX = re.compile("|".join(TOKENS), re.IGNORECASE)

class ExtraAssetsKnob(ConductorKnob):

    def __init__(self, submitter):
        """Set up the UI.

        UI consists of a Header row containing buttons, and list widget for the files.
        """

        super(ExtraAssetsKnob, self).__init__(submitter)

        self.button_layout = QtWidgets.QHBoxLayout()

        # Buttons
        for button in [
            {"label": "Clear", "func": self.clear},
            {"label": "Remove selected", "func": self.remove_selected},
            {"label": "Browse files", "func": self.browse_files},
            {"label": "Browse directory", "func": self.browse_dir},
        ]:

            btn = QtWidgets.QPushButton(button["label"])
            btn.setAutoDefault(False)
            btn.clicked.connect(button["func"])
            self.button_layout.addWidget(btn)

        self.content_layout.addLayout(self.button_layout)

        # List
        self.list_component = QtWidgets.QListWidget()
        self.list_component.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_component.setMaximumHeight(100)

        self.content_layout.addWidget(self.list_component)

    def updateValue(self):
        """
        Populate the UI from the hidden storage knob.

        Called automatically by Nuke when needed.
        """
        self.list_component.clear()
        try:
            assets = json.loads(self.submitter.knob(
                "cio_extra_assets").getText())
        except ValueError:
            assets = []
        self.list_component.addItems(assets)

    def entries(self):
        """Return the text of each entry."""
        result = []
        for i in range(self.list_component.count()):
            result.append(self.list_component.item(i).text())
        return result

    def on_edited(self):
        """
        Update the JSON in the hidden storage knob.
        """
        payload = json.dumps(self.entries())
        self.submitter.knob("cio_extra_assets").setValue(payload)

    def add_paths(self, *paths):
        """
        Add path items to the UI and update the stporage knob.

        Paths are deduplicated.
        """
        path_list = PathList(*self.entries())
        path_list.add(*paths)
        self.list_component.clear()
        self.list_component.addItems([p.fslash() for p in path_list])
        self.on_edited()

    def clear(self):
        """Clear the UI and update the storage knob."""
        self.list_component.clear()
        self.on_edited()

    def remove_selected(self):
        """Remove selected items and update the storage knob."""
        model = self.list_component.model()
        for row in sorted([index.row() for index in self.list_component.selectionModel().selectedIndexes()], reverse=True):
            model.removeRow(row)
        self.on_edited()

    def browse_files(self):
        """Browse for files to add."""
        result = QtWidgets.QFileDialog.getOpenFileNames(
            parent=None, caption="Select files to upload")
        if len(result) and len(result[0]):
            self.add_paths(*result[0])

    def browse_dir(self):
        """Browse for a folder to add."""
        result = QtWidgets.QFileDialog.getExistingDirectory(
            parent=None, caption="Select a directory to upload")
        if result:
            self.add_paths(result)


def build(submitter):
    """
    Build custom UI knob and a string knob for storage.

    The storage knob contains JSON.
    """
    cmd = "assets.ExtraAssetsKnob(nuke.thisNode())"

    k = nuke.String_Knob("cio_extra_assets", "Extra Assets Raw", "")
    submitter.addKnob(k)
    k.setVisible(False)

    k = nuke.PyCustom_Knob(
        "cio_extra_assets_ui", "Extra Assets",  cmd)
    k.setFlag(nuke.STARTLINE)
    submitter.addKnob(k)


def resolve(submitter, **kwargs):
    """
    Resolve the part of the payload that is handled by this component.
    """

    should_scrape_assets = kwargs.get("should_scrape_assets")
    extra_assets = json.loads(submitter.knob("cio_extra_assets").getText() or "[]")

    scraped_assets = scrape_assets(submitter) if should_scrape_assets else []
    path_list = PathList()
    path_list.add(*extra_assets)
    path_list.add(*scraped_assets)
    path_list.add(nuke.Root().knob("name").getValue()) 
    path_list.remove_missing()
    path_list.glob()
    return {"upload_paths": sorted([p.fslash() for p in path_list])}

def scrape_assets(submitter):
    node_names=set()
    get_node_dependencies(submitter.fullName(), node_names)
    paths = set()
    for node_name in node_names:
        node = nuke.toNode(node_name)
        if node.Class() in NODE_BLACKLIST:
            continue
        knobs = [k for k in node.allKnobs() if k.Class() == "File_Knob"]
        for knob in knobs:
            value = knob.value().replace("'", "\\'")
            if value:
                value = nuke.runIn(knob.node().fullName(), f"nuke.tcl('return {value}')")
                if not os.path.isabs(value):
                    value = os.path.join(nuke.script_directory(), value)
                value = TOKEN_RX.sub("*", value)
                paths.add(value)
    return paths

def get_node_dependencies(node_name, visited=set()):
    """
    Collect nodes by name.
    """
    visited.add(node_name)
    node = nuke.toNode(node_name)
    node_names = set(filter(None,[_full_node_name(n) for n in node.dependencies()]))
    if node.Class() in ["Group", "LiveGroup"]:
        node_names |= set(filter(None,[_full_node_name(n) for n in node.nodes()]))
    for node_name in node_names:
        if node_name not in visited: # prevent loop
            get_node_dependencies(node_name, visited)


 
def _full_node_name(rhs):
    # Unexpectedly, either  node.dependencies() or node.nodes() produces something
    # that might not be a node. It might be a knob. The example was
    # despillToColor2.falloff, so presumably it could have been:
    # grp1.grp2.despillToColor2.falloff.x
    # We want the full node if it exists, so we rpartition in a loop and test until we find it.
    name  = rhs.fullName()
    while 1:
        if not name:
            return None
        node =  nuke.toNode(name)
        if node:
            return name
        name = name.rpartition(".")[0]

def affector_knobs():
    return [
        "cio_extra_assets"
    ]