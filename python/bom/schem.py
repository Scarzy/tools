"""Routines for extracting information from schematics"""
import eagle, geda, parts_db, re

EAGLE = 0
GSCHEM = 1
UNKNOWN = 2

def schem_type(fname):
    """Returns the type of file.
    At the moment it'll return EAGLE or UNKNOWN."""
    f = open( fname, "r" )

    if eagle.file_is_eagle(f):
        return EAGLE
    else:
        return GSCHEM

    return UNKNOWN

def open_schem(fname):
    s = schem_type(fname)
    if s == EAGLE:
        schem = eagle.EagleSchem(fname)
    elif s == GSCHEM:
        schem = geda.GSchem(fname)
    else:
        raise "We don't yet support exporting BOMs from non-EAGLE or gschem things"

    # New items to add to the schematic
    new_items = {}
    # Items to remove from the schematic
    rem_keys = []

    # Expand all assemblies into their component parts:
    for des, srcode in schem.iteritems():
        num = 1

        if srcode[0:len("sr-asm-")] == "sr-asm-":
            # TODO: Don't parse the Db again!
            db = parts_db.get_db()

            desc = db[srcode]["description"]

            for s in desc.split():
                if s == "+":
                    continue

                r = re.compile("([0-9]+)\(([^)]+)\)")
                m = r.match(s)
                if m:

                    quantity = int(m.group(1))
                    code = m.group(2)

                    for x in range(quantity):
                        newdes = "%s.%i" % (des,num)

                        new_items[newdes] = code
                        num = num + 1

            rem_keys.append(des)

    schem.update(new_items)
    for des in rem_keys:
        schem.pop(des)

    return schem
