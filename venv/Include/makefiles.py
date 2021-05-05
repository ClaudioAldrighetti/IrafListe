# Files maker
import os.path as opt
from operator import attrgetter

from utility import *

# STAR SESSION


def make_Pulizia0(ws_path):
    print("Creating pulizia0.txt file...")
    file_path = opt.join(ws_path, "pulizia0.txt")
    with open(file_path, "w") as new_file:
        new_file.write(
            "mkdir 00_originali\n"
            "cp *.fit 00_originali\n"
            "cd 00_originali\n"
            "!gzip *\n"
            "cd ..\n")
    new_file.close()
    return


def make_CreaDarkati(ws_path, star_list, list_dim):
    print("Creating crea_darkati.txt file...")
    file_path = opt.join(ws_path, "crea_darkati.txt")
    with open(file_path, "w") as new_file:

        # new_file.write(
        #     "imarith @lista_generale.txt - master_bias.fit @lista_biassati.txt calctyp=real pixtype=real\n")

        min_dark = min(star_list, key=attrgetter('dark_time')).dark_time

        for i in range(0, list_dim):
            star_info = star_list[i]

            for pose in range(1, star_info.pose + 1):
                new_file.write(
                    "imarith " + star_info.name + "-" + str(pose) + "_b.fit - "
                    "master_dark_" + str(star_info.dark_time) + ".fit "
                    + star_info.name + "-" + str(pose) + "_bd.fit calctyp=real pixtype=real\n")

            for i_flat in range(1, star_info.flat + 1):
                new_file.write(
                    "imarith FLAT_" + star_info.name + "-" + str(i_flat) + "_b.fit - "
                    "master_dark_" + str(min_dark) + ".fit "
                    "FLAT_" + star_info.name + "-" + str(i_flat) + "_bd.fit calctyp=real pixtype=real\n")

            for i_neon in range(1, star_info.neon + 1):
                new_file.write(
                    "imarith NEON_" + star_info.name + "-" + str(i_neon) + "_b.fit - "
                    "master_dark_" + str(min_dark) + ".fit "
                    "NEON_" + star_info.name + "-" + str(i_neon) + "_bd.fit calctyp=real pixtype=real\n")

    new_file.close()
    return


def make_ListaGenerale(ws_path, star_list, list_dim):
    print("Creating lista_generale.txt file...")
    file_path = opt.join(ws_path, "lista_generale.txt")
    new_file = open(file_path, "w")

    for i in range(0, list_dim):
        star_info = star_list[i]

        for i_pose in range(1, star_info.pose + 1):
            new_file.write(star_info.name + "-" + str(i_pose) + ".fit\n")

        for i_flat in range(1, star_info.flat + 1):
            new_file.write("FLAT_" + star_info.name + "-" + str(i_flat) + ".fit\n")

        for i_neon in range(1, star_info.neon + 1):
            new_file.write("NEON_" + star_info.name + "-" + str(i_neon) + ".fit\n")

    new_file.close()
    return


def make_ListaBiassati(ws_path, star_list, list_dim):
    print("Creating lista_biassati.txt file...")
    file_path = opt.join(ws_path, "lista_biassati.txt")
    new_file = open(file_path, "w")

    for i in range(0, list_dim):
        star_info = star_list[i]

        for i_pose in range(1, star_info.pose + 1):
            new_file.write(star_info.name + "-" + str(i_pose) + "_b.fit\n")

        for i_flat in range(1, star_info.flat + 1):
            new_file.write("FLAT_" + star_info.name + "-" + str(i_flat) + "_b.fit\n")

        for i_neon in range(1, star_info.neon + 1):
            new_file.write("NEON_" + star_info.name + "-" + str(i_neon) + "_b.fit\n")

    new_file.close()
    return


def make_FLAT(ws_path, star_list, list_dim):
    print("Creating FLAT files...")
    for i in range(0, list_dim):
        star_info = star_list[i]

        file_name = "FLAT_" + star_info.name + ".txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:
            for i_flat in range(1, star_info.flat + 1):
                new_file.write("FLAT_" + star_info.name + "-" + str(i_flat) + "_bd.fit\n")

        new_file.close()
    return


def make_Pulizia1(ws_path):
    print("Creating pulizia1.txt file...")
    file_path = opt.join(ws_path, "pulizia1.txt")
    with open(file_path, "w") as new_file:
        new_file.write(
            "mkdir 01_biassati\n"
            "cd 01_biassati\n"
            "mv ../*_b.fit .\n"
            "!gzip *\n"
            "cd ..\n"
            "mkdir 02_darkati\n"
            "mv *_bd.fit 02_darkati\n"
            "!rm -f *.fit\n"
            "cd 02_darkati\n"
            "cp * ../\n"
            "!gzip *\n"
            "cd ..\n"
            "mkdir 03_flat\n"
            "mv FLAT_* 03_flat\n")
    new_file.close()
    return


def make_GeneraMasterFlat(ws_path, star_list, list_dim, min_h_pixel, max_h_pixel, h_image, l_row):
    print("Creating genera_master_flat.txt file...")
    file_path = opt.join(ws_path, "genera_master_flat.txt")
    with open(file_path, "w") as new_file:
        new_file.write("cd 03_flat\n")

        for i in range(0, list_dim):
            star_info = star_list[i]
            new_file.write(
                "imcombine @FLAT_" + star_info.name + ".txt "
                "medflat_" + star_info.name + ".fit combine=average reject=none\n"
                "blkavg medflat_" + star_info.name + ".fit"
                "[*," + str(min_h_pixel) + ":" + str(max_h_pixel) + "] "
                "avcol_in_" + star_info.name + ".fit 1 " + str(l_row) + "\n"
                "blkrep avcol_in_" + star_info.name + ".fit "
                "avcol_out_" + star_info.name + ".fit 1 " + str(h_image) + "\n"
                "imarith medflat_" + star_info.name + ".fit / "
                "avcol_out_" + star_info.name + ".fit "
                "master_flat_" + star_info.name + ".fit calctyp=real pixtype=real\n")

        new_file.write(
            "cp master_flat_* ../\n"
            "!gzip *\n"
            "cd ..\n")

    new_file.close()
    return


def make_ListaFlattati(ws_path, star_list, list_dim):
    print("Creating lista_flattati.txt file...")
    file_path = opt.join(ws_path, "lista_flattati.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(
                    "imarith " + star_info.name + "-" + str(i_pose) + "_bd.fit / "
                    "master_flat_" + star_info.name + ".fit " +
                    star_info.name + "-" + str(i_pose) + "_f.fit calctyp=real pixtype=real\n")

            for i_neon in range(1, star_info.neon + 1):
                new_file.write(
                    "imarith NEON_" + star_info.name + "-" + str(i_neon) + "_bd.fit / "
                    "master_flat_" + star_info.name + ".fit "
                    "NEON_" + star_info.name + "-" + str(i_neon) + "_f.fit calctyp=real pixtype=real\n")

    new_file.close()
    return


def make_ListaTracciamoStelle(ws_path, star_list, list_dim):
    print("Creating lista_tracciamo_stelle.txt file...")
    file_path = opt.join(ws_path, "lista_tracciamo_stelle.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]

            for i_pose in range(1, star_info.pose + 1):
                new_file.write("apall " + star_info.name + "-" + str(i_pose) + "_f.fit\n")

    new_file.close()
    return


def make_Pulizia2(ws_path):
    print("Creating pulizia2.txt file...")
    file_path = opt.join(ws_path, "pulizia2.txt")
    with open(file_path, "w") as new_file:
        new_file.write(
            "mkdir 04_flattati\n"
            "cp *_f.fit 04_flattati\n"
            "!rm -f *_bd.fit\n"
            "mkdir 05_neon\n"
            "mv NEON_* 05_neon\n")
    new_file.close()
    return


def make_NEON(ws_path, star_list, list_dim):
    print("Creating NEON files...")
    for i in range(0, list_dim):
        star_info = star_list[i]

        file_name = "NEON_" + star_info.name + ".txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:
            for i_neon in range(1, star_info.neon + 1):
                new_file.write("NEON_" + star_info.name + "-" + str(i_neon) + "_f.fit\n")

        new_file.close()
    return


def make_GeneraMasterNeon(ws_path, star_list, list_dim):
    print("Creating genera_master_neon.txt file...")
    file_path = opt.join(ws_path, "genera_master_neon.txt")
    with open(file_path, "w") as new_file:
        new_file.write("cd 05_neon\n")

        for i in range(0, list_dim):
            star_info = star_list[i]
            new_file.write(
                "imcombine @NEON_" + star_info.name + ".txt "
                "master_neon_" + star_info.name + ".fit combine=average reject=none\n")

        new_file.write(
            "cp master_neon_* ../\n"
            "!gzip *\n"
            "cd ..\n")

    new_file.close()
    return


def make_ListaApallNe(ws_path, star_list, list_dim):
    print("Creating lista_apall_Ne.txt file...")
    file_path = opt.join(ws_path, "lista_apall_Ne.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(
                    "apall master_neon_" + star_info.name + ".fit "
                    "output=" + star_info.name + "-" + str(i_pose) + "_Ne.fit "
                    "referen=" + star_info.name + "-" + str(i_pose) + "_f.fit "
                    "profile=" + star_info.name + "-" + str(i_pose) + "_f.fit\n")

    new_file.close()
    return


def make_ListaReidentify(ws_path, star_list, list_dim, ref_name, ref_pose):
    print("Creating lista_reidentify.txt file...")
    file_path = opt.join(ws_path, "lista_reidentify.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]

            for i_pose in range(1, star_info.pose + 1):
                if (star_info.name != ref_name) or (i_pose != ref_pose):
                    new_file.write(
                        "reidentify images=" + star_info.name + "-" + str(i_pose) + "_Ne.0001.fits "
                        "referenc=" + ref_name + "-" + str(ref_pose) + "_Ne.0001.fits\n")

    new_file.close()
    return


def make_ListaChiConChi(ws_path, star_list, list_dim):
    print("Creating lista_chi_con_chi.txt file...")
    file_path = opt.join(ws_path, "lista_chi_con_chi.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(
                    "hedit " + star_info.name + "-" + str(i_pose) + "_f.ms.fits "
                    "refspec1 " + star_info.name + "-" + str(i_pose) + "_Ne.0001 add+ ver-\n")

    new_file.close()
    return


def make_ListaCalibraLambda(ws_path, star_list, list_dim):
    print("Creating lista_calibra_lambda.txt file...")
    file_path = opt.join(ws_path, "lista_calibra_lambda.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(
                    "dispcor " + star_info.name + "-" + str(i_pose) + "_f.ms.fits " +
                    star_info.name + "-" + str(i_pose) + "_fw.fits linearize=no\n")

    new_file.close()
    return


def make_STANDARD(ws_path, star_list, list_dim):
    print("Creating STANDARD files...")
    for i in range(0, list_dim):
        star_info = star_list[i]
        if not is_standard(star_info.name):
            continue

        file_name = "STANDARD_" + star_info.name + ".txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:
            star_n = star_info.name[2:]

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(
                    "standard " + star_info.name + "-" + str(i_pose) + "_fw.fits "
                    "star_nam=hr_" + star_n + "\n")

        new_file.close()
    return


def make_DaFlussare(ws_path, star_list, list_dim):
    print("Creating FLUSSARE files...")
    for i in range(0, list_dim):
        star_info = star_list[i]
        if is_standard(star_info.name):
            continue

        file_name = star_info.name + "_da_flussare.txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(star_info.name + "-" + str(i_pose) + "_fw.fits\n")

            for i_pose in range(1, star_info.std_pose + 1):
                new_file.write(star_info.standard + "-" + str(i_pose) + "_fw.fits\n")

        new_file.close()
    return


def make_Flussati(ws_path, star_list, list_dim):
    print("Creating FLUSSATI files...")
    for i in range(0, list_dim):
        star_info = star_list[i]
        if is_standard(star_info.name):
            continue

        file_name = star_info.name + "_flussati.txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(star_info.name + "-" + str(i_pose) + "_fwx.fits\n")

            for i_pose in range(1, star_info.std_pose + 1):
                new_file.write(star_info.standard + "-" + str(i_pose) + "_fwx.fits\n")

        new_file.close()
    return


def make_HelioRename(ws_path, star_list, list_dim):
    print("Creating HELIO files...")
    for i in range(0, list_dim):
        star_info = star_list[i]
        if is_standard(star_info.name):
            continue

        file_name = star_info.name + "_helio_rename.txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(
                    "cp " + star_info.name + "-" + str(i_pose) + "_fwx.fits " +
                    star_info.name + "-" + str(i_pose) + "_hv.fits\n")

            for i_pose in range(1, star_info.std_pose + 1):
                new_file.write(
                    "cp " + star_info.standard + "-" + str(i_pose) + "_fwx.fits " +
                    star_info.standard + "-" + str(i_pose) + "_hv.fits\n")

        new_file.close()
    return


def make_RvCorrected(ws_path, star_list, list_dim):
    print("Creating RV_CORRECTED files...")
    for i in range(0, list_dim):
        star_info = star_list[i]
        if is_standard(star_info.name):
            continue

        file_name = star_info.name + "_rv_corrected.txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(star_info.name + "-" + str(i_pose) + "_hv.fits\n")

            for i_pose in range(1, star_info.std_pose + 1):
                new_file.write(star_info.standard + "-" + str(i_pose) + "_hv.fits\n")

        new_file.close()
    return


def make_PreparoHelio(ws_path, star_list, list_dim):
    print("Creating PREPARO_HELIO files...")
    for i in range(0, list_dim):
        star_info = star_list[i]
        if is_standard(star_info.name):
            continue

        file_name = star_info.name + "_preparo_helio.txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:
            new_file.write(
                "hedit @" + star_info.name + "_rv_corrected.txt "
                "field=observat value=OMB add+ update+\n"
                "setjd @" + star_info.name + "_rv_corrected.txt\n"
                "setairmass @" + star_info.name + "_rv_corrected.txt\n"
                "hedit @" + star_info.name + "_rv_corrected.txt\n"
                "fields=DATE-OBS value=. > lista_date.txt\n"
                "!more lista_date.txt\n")

        new_file.close()
    return


def make_Mediana(ws_path, star_list, list_dim):
    print("Creating MEDIANA files...")
    for i in range(0, list_dim):
        star_info = star_list[i]

        file_name = star_info.name + "_mediana.txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:

            for i_pose in range(1, star_info.pose + 1):
                new_file.write(star_info.name + "-" + str(i_pose) + "_hv.fits\n")

        new_file.close()
    return


def make_Pulizia3(ws_path, star_list, list_dim):
    print("Creating pulizia3.txt file...")
    file_path = opt.join(ws_path, "pulizia3.txt")
    with open(file_path, "w") as new_file:

        for i in range(0, list_dim):
            star_info = star_list[i]
            if is_standard(star_info.name):
                continue

            new_file.write(
                "mkdir " + star_info.name + "\n"
                "mv " + star_info.name + "-* " + star_info.name + "\n"
                "mv " + star_info.name + "_da_flussare.txt " + star_info.name + "\n"
                "mv " + star_info.name + "_flussati.txt " + star_info.name + "\n"
                "mv " + star_info.name + "_helio_rename.txt " + star_info.name + "\n"
                "mv " + star_info.name + "_rv_corrected.txt " + star_info.name + "\n"
                "mv " + star_info.name + "_preparo_helio.txt " + star_info.name + "\n"
                "mv " + star_info.name + "_mediana.txt " + star_info.name + "\n"
                "cp " + star_info.standard + "-* " + star_info.name + "\n"
                "cp STANDARD_" + star_info.standard + ".txt " + star_info.name + "\n")

    new_file.close()
    return


def make_Pulizia4(ws_path):
    print("Creating pulizia4.txt file...")
    file_path = opt.join(ws_path, "pulizia4.txt")
    with open(file_path, "w") as new_file:
        new_file.write(
            "mkdir 06_standard\n"
            "mv *.fits 06_standard\n"
            "mv *.fit 06_standard\n"
            "cd 06_standard\n"
            "!gzip *\n"
            "cd ..\n"
            "mkdir 07_liste\n"
            "mv *.txt 07_liste\n")
    new_file.close()
    return


def make_ListaInizio(ws_path, dark_flag):
    print("Creating lista_inizio.txt file...")
    file_path = opt.join(ws_path, "lista_inizio.txt")
    with open(file_path, "w") as new_file:
        new_file.write(
            "cl < pulizia0.txt\n")
        if dark_flag:
            new_file.write(
                "cl < crea_master_db.txt\n")
        new_file.write(
            "imarith @lista_generale.txt - master_bias.fit @lista_biassati.txt calctyp=real pixtype=real\n"
            "cl < crea_darkati.txt\n"
            "cl < pulizia1.txt\n"
            "cl < genera_master_flat.txt\n"
            "cl < lista_flattati.txt\n"
            "cl < pulizia2.txt\n"
            "cl < genera_master_neon.txt\n")
    new_file.close()
    return


# GEN MASTER


def make_DARK(ws_path, master_list, list_dim):
    print("Creating LISTA DARK files...")
    for i in range(0, list_dim):
        if master_list[i].master_type == BIAS:
            continue

        dark_poses = master_list[i].master_poses
        dark_time = master_list[i].master_time

        file_name = "lista_dark_" + str(dark_time) + ".txt"
        file_path = opt.join(ws_path, file_name)
        with open(file_path, "w") as new_file:

            for i_pose in range(1, dark_poses + 1):
                new_file.write("DARK_" + str(dark_time) + "-" + str(i_pose) + ".fit\n")

        new_file.close()
    return


def make_ListaBias(ws_path, bias_poses):
    print("Creating lista_bias.txt files...")
    file_path = opt.join(ws_path, "lista_bias.txt")
    with open(file_path, "w") as new_file:

        for i_pose in range(1, bias_poses + 1):
            new_file.write("BIAS" + "-" + str(i_pose) + ".fit\n")

    new_file.close()
    return


def make_CreaMasterDb(ws_path, master_list, list_dim):
    print("Creating crea_master_db.txt file...")
    file_path = opt.join(ws_path, "crea_master_db.txt")
    with open(file_path, "w") as new_file:
        new_file.write(
            "mkdir bias\n"
            "mv BIAS-* bias\n"
            "cp lista_bias.txt bias\n"
            "cd bias\n"
            "imcombine @lista_bias.txt master_bias.fit "
            "combine=average reject=minmax nlow=1 nhigh=1\n"
            "cp master_bias.fit ../\n"
            "!gzip *\n"
            "cd ..\n"
            "mkdir dark\n"
            "mv DARK* dark\n"
            "cp lista_dark* dark\n"
            "cd dark\n"
            "cp ../master_bias.fit .\n")

        for i in range(0, list_dim):
            if master_list[i].master_type == BIAS:
                continue

            master_time = master_list[i].master_time
            new_file.write(
                "imcombine @lista_dark_" + str(master_time) + ".txt "
                "dark_no_bias_" + str(master_time) + ".fit "
                "combine=average reject=minmax nlow=1 nhigh=1\n"
                "imarith dark_no_bias_" + str(master_time) + ".fit - "
                "master_bias.fit master_dark_" + str(master_time) + ".fit\n")

        new_file.write(
            "cp master_dark* ../\n"
            "!gzip *\n"
            "cd ..\n")

    new_file.close()
    return
