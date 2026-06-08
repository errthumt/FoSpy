from fos_site.run_example import extract_and_run

if __name__ == "__main__":
    from FoSpy.blocks import attachments
    attachments._debug.on = True
    extract_and_run(figures=True)
    pass #debugging break point