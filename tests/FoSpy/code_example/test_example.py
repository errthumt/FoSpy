

def test_example_match(example_frozen, example_finished, example_relpaths, subtests):
    for rel_path in example_relpaths:
        with subtests.test(msg=f"Checking {rel_path}"):
            frozen_path = example_frozen / rel_path
            finished_path = example_finished / rel_path

            frozen_lines = frozen_path.read_text().splitlines()
            finished_lines = finished_path.read_text().splitlines()

            assert frozen_lines == finished_lines