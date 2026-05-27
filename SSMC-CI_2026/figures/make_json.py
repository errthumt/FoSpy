from FoSpy.blocks.synthesis import Synthesis

mySyn = Synthesis.fromFile("SSMC-CI_2026/start_synthesis.fos")

with open("SSMC-CI_2026/figures/synthesis_dict.json", "w") as f:
    import json
    json.dump(mySyn.serialize(clean=True), f, indent=4)