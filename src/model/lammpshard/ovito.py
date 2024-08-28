from ovito.io import import_file
from ovito.vis import TextLabelOverlay, Viewport
from ovito.modifiers import ExpressionSelectionModifier
from ovito.modifiers import ColorCodingModifier,CreateBondsModifier
from ovito.modifiers import SliceModifier
import warnings

def ovito(dump):
    warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')

    # Import a simulation dataset and select some atoms based on their potential energy:
    pipeline = import_file(dump, multiple_frames = True)

    pipeline.add_to_scene()
    pipeline.modifiers.append(ColorCodingModifier(property='Particle Type'))
    # dont show bonds
    pipeline.modifiers.append(CreateBondsModifier(enabled=False))
    #pipeline.modifiers.append(ExpressionSelectionModifier(expression="peatom > -4.2"))
    #pipeline.modifiers.append(SliceModifier(normal=(0,0,1), distance=0))

    # Create the overlay. Note that the text string contains a reference
    # to an output attribute of the ExpressionSelectionModifier.
    overlay = TextLabelOverlay(text="Number of selected atoms: [ExpressionSelection.count]")
    # Specify the source of dynamically computed attributes.
    overlay.source_pipeline = pipeline

    # Attach overlay to a newly created viewport:
    viewport = Viewport(type=Viewport.Type.Front)
    viewport.overlays.append(overlay)
    return viewport


    # shoew 
    
# now I want see the last frame
