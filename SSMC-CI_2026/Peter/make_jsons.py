from FoSpy.blocks.synthesis import Synthesis


mysyn = Synthesis.fromFile("example/synthesis/start_synthesis.fos")
mysyn.add_calc_routine("materials.add_weight_pcts")

fullDict = mysyn.serialize(clean=False)

mysyn.save("SSMC-CI_2026/Peter/synthesis_clean.json")

with open("SSMC-CI_2026/Peter/synthesis_full.json", "w") as f:
    import json
    json.dump(fullDict, f, indent=4)

