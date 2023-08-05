import nuke
from ciocore import data as coredata
from cionuke import const as k

def build(submitter):
    """Build knobs to specify project."""
    knob = nuke.Enumeration_Knob("cio_project", "Project", [k.NOT_CONNECTED])
    knob.setTooltip('Choose a Conductor project.')
    submitter.addKnob(knob)

def rebuild_menu(submitter, projects):
    submitter.knob("cio_project").setValues( projects or [k.NOT_CONNECTED])

 
def resolve(submitter, **kwargs):
    if (not coredata.valid()) or  submitter.knob("cio_project").value() == k.NOT_CONNECTED:
        return {"project": k.INVALID}
    return {"project": submitter.knob("cio_project").value()}


def affector_knobs():
    return [
        "cio_project"
    ]