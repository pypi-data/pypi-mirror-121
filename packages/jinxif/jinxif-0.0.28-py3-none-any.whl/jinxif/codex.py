############
# title: codex.py
#
# langue: Python3
# date: 2021-09-16
# license: GPL>=v3
# author: Jenny, bue
#
# description:
#     functions to fork codex output into our pipeline.
############


# library
from jinxif import basic
from jinxif import config
import os
import shutil

# developemnt
#import importlib
#importlib.reload()

def trafo(
        es_sample,
        b_symlink = True,
        # filesystem
        s_codexdir = config.d_nconv['s_codexdir'],  #'./CodexImages/'
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'./SubtractedRegisteredImages/'
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  # {}{}/  s_afsubdir, slide_scene
    ):
    '''
    version: 2021-09-16

    input:
        es_sample: set of sample ids ak folders under s_codexdir,
            which should be transformated to be jinxif s_afsubdir compatible.
        b_symlink: if false then the original codex files are copied.
            if true, then the original codex tiff files are just symbolicaly linked not copied.
            this is faster and does not consume any additionl disk space.
            default setting is true.
        s_codexdir: standard codex platform output directory, which has the following
            for us relevant subfolder structure: sample/processed_YYYY-MM-DD/stitched/regNNN/
        s_afsubdir: auto fluorescent subtracted registrated image directory
        s_format_afsubdir: s_afsubdir subfolder structur where for each slide_scene the afsubtracted files are stored.

    output:
        for each slide_scene a directory and tiff files (either real or just symbolically linked) under s_afsubdir.

    description:
        symbolic link or copy the codex processed stitched tiff images for jinxif processing into s_afsubdir.
        the genrate symbolic link or file name will be totally jinxif nameing convention compatible.
    '''
    for s_sample in sorted(es_sample):
        print(f'jinxif.codex.trafo : processing data from sample {s_sample} ...')
        s_path_root = s_codexdir + s_sample + '/'
        for s_dir_processed in os.listdir(s_path_root):
            if os.path.isdir(s_path_root + s_dir_processed) and s_dir_processed.startswith('processed_'):
                s_path_stitched = s_path_root + s_dir_processed + '/stitched/'
                s_slide = f"{s_sample.replace('_','-')}-{s_dir_processed.split('_')[-1].replace('-','')}"
                for s_dir_reg in os.listdir(s_path_stitched):
                    if os.path.isdir(s_path_stitched + s_dir_reg) and s_dir_reg.startswith('reg'):
                        print(f'detected: {s_slide} {s_dir_reg}')
                        s_path_reg = s_path_stitched + s_dir_reg + '/'
                        df_codex = basic.parse_tiff_codex(s_path_reg)
                        # update with new columns
                        df_codex['slide'] = s_slide
                        df_codex['slide_scene'] = df_codex['slide'] + '_' + df_codex['scene']
                        df_codex['imagetype'] = 'SubCodexORG'
                        # translate color string
                        df_codex['color'] = [config.d_nconv['ls_color_order_jinxif'][config.d_nconv['ls_color_order_codex'].index(s_color)]for s_color in df_codex.color]
                        # translate round string
                        df_codex['round'] = [s_round.replace(config.d_nconv['s_round_codex'], config.d_nconv['s_round_jinxif']) for s_round in df_codex.loc[:,'round']]
                        #print(df_codex.info())

                        # for each file
                        for s_file in df_codex.index:

                            # get src
                            s_src_pathfile = df_codex.index.name + s_file

                            # get dst
                            s_dst_path = s_format_afsubdir.format(s_afsubdir, df_codex.loc[s_file, 'slide_scene'])
                            os.makedirs(s_dst_path, exist_ok=True)
                            ds_dst = {}
                            for s_dst, i_dst in config.d_nconv['di_regex_tiff_reg'].items():
                                ds_dst.update({i_dst: df_codex.loc[s_file, s_dst]})
                            s_dst_file = config.d_nconv['s_format_tiff_reg'].format(ds_dst[1], ds_dst[2], ds_dst[3], ds_dst[4], ds_dst[5], ds_dst[6], ds_dst[7])
                            s_dst_pathfile = s_dst_path + s_dst_file

                            # make symbolic links or copy
                            if (b_symlink):
                                print(f'symlink:\n{s_src_pathfile}\n{s_dst_pathfile}')
                                if os.path.islink(s_dst_pathfile):
                                   os.remove(s_dst_pathfile)
                                s_dst_relative = '../' * (s_dst_pathfile.count('/') - 1)
                                s_src_pathfile_symlink = s_dst_relative + s_src_pathfile
                                os.symlink(s_src_pathfile_symlink, s_dst_pathfile)
                            else:
                                print(f'copy:\n{s_src_pathfile}\n{s_dst_pathfile}')
                                shutil.copyfile(s_src_pathfile, s_dst_pathfile)
                        #break
                #break
        #break
