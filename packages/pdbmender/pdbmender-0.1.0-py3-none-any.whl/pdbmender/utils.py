import os
import subprocess
from pdbmender.formats import read_pdb_line, new_pdb_line
from pdbmender.constants import (
    PROTEIN_RESIDUES,
    TITRATABLE_RESIDUES,
    RESIDUE_REFSTATE,
    RENAME_ATOMS,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def mend_pdb(pdb_to_clean, pdb_cleaned, ff, ffout, logfile="LOG_pdb2pqr", hopt=True):
    try:
        # TODO: Port pdb2pqr to py3 and import it as a module
        cmd = (
            "python2 {0}/pdb2pqr/pdb2pqr.py {1} {2} "
            "--ff {3} --ffout {4} --drop-water -v --chain {6} > {5} 2>&1 ".format(
                SCRIPT_DIR,
                pdb_to_clean,
                pdb_cleaned,
                ff,
                ffout,
                logfile,
                "" if hopt else "--noopt",
            )
        )
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            "pdb2pqr did not run successfully\nMessage: {}".format(
                e.stderr.decode("ascii")
            )
        )


def add_tautomers(pdb_in, sites_addHtaut, ff_family, outputpqr, logfile="LOG_addHtaut"):
    try:
        # TODO rewrite addHtaut as python module
        cmd = "{}/addHtaut {} {} {} > {}".format(
            SCRIPT_DIR,
            pdb_in,
            ff_family,
            sites_addHtaut,
            outputpqr,
            logfile,
        )
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            "addHtaut did not run successfully\nMessage: {}".format(
                e.stderr.decode("ascii")
            )
        )


def correct_names(resnumb, resname, aname, titrating_sites, termini):
    # TODO: some of these are no longer used as it is done by pdb2pqr
    def change_aname(aname, restype):
        not_correct_names = list(restype.keys())
        for not_corrected in not_correct_names:
            if aname == not_corrected:
                aname = restype[not_corrected]
        return aname

    NTR_numb, CTR_numb = termini
    restype = None
    if resnumb == CTR_numb:
        restype = "CTR"

    elif resnumb == NTR_numb:
        restype = "NTR"

    if restype and restype in list(RENAME_ATOMS.keys()):
        aname = change_aname(aname, RENAME_ATOMS[restype])

    if resnumb in titrating_sites:
        if resname not in PROTEIN_RESIDUES:
            for tit_res in TITRATABLE_RESIDUES:
                if tit_res[:2] == resname[:2]:
                    restype, resname = tit_res, tit_res

        if resname in list(RENAME_ATOMS.keys()):
            aname = change_aname(aname, RENAME_ATOMS[resname])

    if resname in list(RESIDUE_REFSTATE.keys()):
        resname = RESIDUE_REFSTATE[resname]

    return aname, resname


# pdb_out -> cleaned.pqr
def prepare_for_addHtaut(
    pdb_in, pdb_out, sites, termini, to_exclude, terminal_offset=5000
):
    with open(pdb_in) as f:
        content = f.readlines()

    new_pdb_text = ""
    removed_pdb_lines = []
    resnumb_max = 0
    chains = sites.keys()
    for line in content:
        if line.startswith("ATOM"):
            termini_trigger = False
            aname, anumb, resname, chain, resnumb, x, y, z = read_pdb_line(line)

            if chain in chains:
                resnumb_max = resnumb
                sites_numbs = sites[chain]
                aname, resname = correct_names(
                    resnumb, resname, aname, sites_numbs, termini[chain]
                )

                if resnumb in termini[chain]:
                    termini_trigger = True

            if resname == "CYS":
                change_atoms = {"1CB": "CB", "1SG": "SG"}
                if aname in change_atoms.keys():
                    aname = change_atoms[aname]
            if (
                aname in ("O1", "O2", "OT1", "OT2", "H1", "H2", "H3")
                and not termini_trigger
                and resname in PROTEIN_RESIDUES
            ):
                if aname == "O1":
                    aname = "O"
                elif aname == "H1":
                    aname = "H"
                else:
                    continue

            if line[26] != " ":
                resnumb += terminal_offset

            new_line = new_pdb_line(
                anumb,
                aname,
                resname,
                resnumb,
                x,
                y,
                z,
                chain=chain,
            )
            if chain in chains:
                new_pdb_text += new_line
            elif (
                aname not in ("O1", "O2", "OT1", "OT2", "H1", "H2", "H3")
                or resname in to_exclude
            ):
                removed_pdb_lines.append(new_line)

    with open(pdb_out, "w") as f_new:
        f_new.write(new_pdb_text)

    resnumb_old = resnumb_max + 1
    removed_pdb_text = ""
    for line in removed_pdb_lines:
        (aname, anumb_old, resname, chain, resnumb, x, y, z) = read_pdb_line(line)
        anumb += 1
        resnumb += resnumb_old
        while resnumb < resnumb_max:
            resnumb += resnumb_old
        removed_pdb_text += new_pdb_line(
            anumb, aname, resname, resnumb, x, y, z, chain=chain
        )
        resnumb_max = resnumb

    with open("removed.pqr", "w") as f_new:
        f_new.write(removed_pdb_text)
    return removed_pdb_text