import nibabel as nib
import sys
sys.path.insert(0, "xnat_downloader")
import xnat_downloader.cli.run as run
import os
import argparse
from pyxnat import Interface


def get_PUP_timecourse_object(testSub, ses_of_interest):
    assessors_obj = testSub.ses_dict[ses_of_interest].assessors().get('')
    for assessor_obj in assessors_obj:
        if assessor_obj.id() is not None:
            if "PUPTIMECOURSE" in assessor_obj.id():
                puptimecourse_obj = assessor_obj
                return puptimecourse_obj
        else:
            return None


def convert_analyze_to_nii(img_path, hdr_path):
    img = nib.load(img_path)
    nii_path = img_path.replace('.img', '.nii.gz')
    nib.save(img, nii_path)

    os.remove(img_path)
    os.remove(hdr_path)


def get_image_and_header(assessor_puptimecourse_obj,
                         orig_img_path,
                         orig_hdr_path,
                         new_img_path,
                         new_hdr_path):
    try:
        # if header is missing, it is because the other file is an info file or some other type
        # that doesn't need to be converted to nifti
        assessor_puptimecourse_obj.resource(
            'DATA').file(orig_img_path).get(new_img_path)
        if orig_hdr_path is not None and new_hdr_path is not None:
            assessor_puptimecourse_obj.resource(
                'DATA').file(orig_hdr_path).get(new_hdr_path)
            convert_analyze_to_nii(new_img_path, new_hdr_path)
    except:
        print("Could not find the requested file")


def get_t1w_image(puptimecourse_obj,
                  ses_dir,
                  sub,
                  ses):
    orig_img_path = os.path.join("pet_proc", "T1001.4dfp.img")
    orig_hdr_path = os.path.join("pet_proc", "T1001.4dfp.hdr")
    new_img_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_T1w.img")
    new_hdr_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_T1w.hdr")
    if not os.path.exists(new_img_path.replace('.img', '.nii.gz')):
        get_image_and_header(puptimecourse_obj, orig_img_path,
                             orig_hdr_path, new_img_path, new_hdr_path)
    else:
        print("Found a T1w file for " + sub + " at " + ses)


def get_orig_pet_image(puptimecourse_obj,
                       ses_dir,
                       sub,
                       ses):
    filename_prefix = sub + "_" + ses + "_pib.4dfp"
    orig_img_path = os.path.join("pet_proc", filename_prefix + ".img")
    orig_hdr_path = os.path.join("pet_proc", filename_prefix + ".hdr")
    new_img_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_task-rest_acq-pib_pet.img")
    new_hdr_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_task-rest_acq-pib_pet.hdr")
    if not os.path.exists(new_img_path.replace('.img', '.nii.gz')):
        get_image_and_header(puptimecourse_obj, orig_img_path,
                             orig_hdr_path, new_img_path, new_hdr_path)
    else:
        print("Found a raw PET image for " + sub + " at " + ses)


def get_orig_pet_info_file(puptimecourse_obj,
                           ses_dir,
                           sub,
                           ses):
    orig_img_path = os.path.join("pet_proc", sub + "_" + ses + "_pib.info")
    new_img_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_task-rest_acq-pib_pet.info")
    if not os.path.exists(new_img_path):
        get_image_and_header(
            puptimecourse_obj, orig_img_path, None, new_img_path, None)
    else:
        print("Found a raw PET info file for" + sub + " at " + ses)


def get_dkt_t1w_space_image(puptimecourse_obj,
                            ses_dir,
                            sub,
                            ses):
    orig_img_path = os.path.join("pet_proc", "wmparc001.4dfp.img")
    orig_hdr_path = os.path.join("pet_proc", "wmparc001.4dfp.hdr")
    new_img_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_parcellation-DKT_space-T1w.img")
    new_hdr_path = os.path.join(
        ses_dir, "sub-" + sub + "_ses-" + ses + "_parcellation-DKT_space-T1w.hdr")
    if not os.path.exists(new_img_path.replace('.img', '.nii.gz')):
        get_image_and_header(puptimecourse_obj, orig_img_path,
                             orig_hdr_path, new_img_path, new_hdr_path)
    else:
        print("Found an atlas in native space file for " + sub + " at " + ses)


def get_suvr_t1w_space_image(puptimecourse_obj,
                             ses_dir,
                             sub,
                             ses,
                             radiotracer):
    filename_prefix = sub + "_" + ses + "_pibn_msum_on_roi.4dfp"
    orig_img_path = os.path.join("pet_proc", filename_prefix + ".img")
    orig_hdr_path = os.path.join("pet_proc", filename_prefix + ".hdr")
    new_img_path = os.path.join(ses_dir,
                                "sub-" + sub + "_ses-" + ses + "_acq-" + radiotracer + "_space-T1w_coregistered_pet.img")
    new_hdr_path = os.path.join(ses_dir,
                                "sub-" + sub + "_ses-" + ses + "_acq-" + radiotracer + "_space-T1w_coregistered_pet.hdr")
    if not os.path.exists(new_img_path.replace('.img', '.nii.gz')):
        get_image_and_header(puptimecourse_obj, orig_img_path,
                             orig_hdr_path, new_img_path, new_hdr_path)
    else:
        print("Found an SUVR file in native space for " + sub + " at " + ses)
        
        
def get_suvr_t1w_space_image(puptimecourse_obj,
                             ses_dir,
                             sub,
                             ses,
                             radiotracer):
    filename_prefix = sub + "_" + ses + "_pibn_msum_on_roi.4dfp"
    orig_img_path = os.path.join("pet_proc", filename_prefix + ".img")
    orig_hdr_path = os.path.join("pet_proc", filename_prefix + ".hdr")
    new_img_path = os.path.join(ses_dir,
                                "sub-" + sub + "_ses-" + ses + "_acq-" + radiotracer + "_space-T1w_coregistered_pet.img")
    new_hdr_path = os.path.join(ses_dir,
                                "sub-" + sub + "_ses-" + ses + "_acq-" + radiotracer + "_space-T1w_coregistered_pet.hdr")
    if not os.path.exists(new_img_path.replace('.img', '.nii.gz')):
        get_image_and_header(puptimecourse_obj, orig_img_path,
                             orig_hdr_path, new_img_path, new_hdr_path)
    else:
        print("Found an SUVR file in native space for " + sub + " at " + ses)

def get_moco_image(puptimecourse_obj,
                   ses_dir,
                   sub,
                   ses,
                   radiotracer):
    filename_prefix = sub + "_" + radiotracer + "_" + ses + "n_moco.4dfp"
    orig_img_path = os.path.join("pet_proc", filename_prefix + ".img")
    orig_hdr_path = os.path.join("pet_proc", filename_prefix + ".hdr")
    new_img_path = os.path.join(ses_dir,
                                "sub-" + sub + "_ses-" + ses + "_acq-" + radiotracer + "_moco_pet.img")
    new_hdr_path = os.path.join(ses_dir,
                                "sub-" + sub + "_ses-" + ses + "_acq-" + radiotracer + "_moco_pet.hdr")
    if not os.path.exists(new_img_path.replace('.img', '.nii.gz')):
        get_image_and_header(puptimecourse_obj, orig_img_path,
                             orig_hdr_path, new_img_path, new_hdr_path)
    else:
        print("Found a MOCO file in PET space for " + sub + " at " + ses)



def main():
    parser = argparse.ArgumentParser(
        description='Script to download PET Unified Pipeline derivatives from XNAT server.')
    parser.add_argument("--server",
                        help="Specify the XNAT server of interest")
    parser.add_argument("--user",
                        help="Specify the XNAT server username")
    parser.add_argument("--password",
                        help="Specify the associated password")
    parser.add_argument("--project",
                        help="Specify the project/data collection, e.g. DIANDF11")
    parser.add_argument("--ses", nargs="+",
                        help="Specify the visit labels or sessions to download, e.g. v00")
    parser.add_argument("--subjects", action="append",
                        help="Specify a subject or list of subjects for which to download images")
    parser.add_argument("--radiotracer",
                        help="Specify the radiotracer, e.g. pib or fdg")
    parser.add_argument("--output_dir",
                        help="Specify the directory where to write the outputs")

    args = parser.parse_args()
    sessions = args.ses
    radiotracer = args.radiotracer
    output_dir = args.output_dir
    server = args.server
    user = args.user
    password = args.password
    project = args.project
    subjects = args.subjects

    central = Interface(server=server, user=user, password=password)
    
    if not central.select.projects().get():
        msg = "You have no access to any projects in the server, " \
          "please check your url, username, and password."
        raise RuntimeError(msg)
    
    proj_obj = central.select.project(project)

    if subjects is None:
        sub_objs = proj_obj.subjects()
        sub_objs._id_header = 'label'
        subjects = sub_objs.get()

    for sub in subjects:
        print(sub)
        testSub = run.Subject(proj_obj, sub)
        testSub.get_sessions()
        if project == "DIANDF12":
            for ses in sessions:
                ses_of_interest = sub + "_" + ses + "_" + radiotracer
                if ses_of_interest in testSub.ses_dict.keys():
                    puptimecourse_obj = get_PUP_timecourse_object(
                        testSub, ses_of_interest)
                    if puptimecourse_obj is not None:
                        sub_dir = os.path.join(output_dir, "sub-" + sub)
                        ses_dir = os.path.join(sub_dir, "ses-" + ses)
                        if not os.path.exists(sub_dir):
                            os.mkdir(sub_dir)
                            os.mkdir(ses_dir)
                        else:
                            if not os.path.exists(ses_dir):
                                os.mkdir(ses_dir)
                        get_t1w_image(puptimecourse_obj, ses_dir, sub, ses)
                        get_dkt_t1w_space_image(
                            puptimecourse_obj, ses_dir, sub, ses)
                        get_suvr_t1w_space_image(
                            puptimecourse_obj, ses_dir, sub, ses, radiotracer)
                        get_orig_pet_image(puptimecourse_obj, ses_dir, sub, ses)
                        get_orig_pet_info_file(
                            puptimecourse_obj, ses_dir, sub, ses)
    
                        print("Finished downloading images for: " + ses_of_interest)
                    else:
                        print("No PUP timecourse available for: " + ses_of_interest)
                else:
                    print(sub + " does not have a " + ses + " session")
        elif project == "OASIS3":
            for ses in testSub.ses_dict.keys():
                if radiotracer == ses.split("_")[1]
                    puptimecourse_obj = get_PUP_timecourse_object(
                        testSub, ses_of_interest)
                    if puptimecourse_obj is not None:
                        sub_dir = os.path.join(output_dir, "sub-" + sub)
                        ses_dir = os.path.join(sub_dir, "ses-" + ses)
                        if not os.path.exists(sub_dir):
                            os.mkdir(sub_dir)
                            os.mkdir(ses_dir)
                        else:
                            if not os.path.exists(ses_dir):
                                os.mkdir(ses_dir)
                        get_t1w_image(puptimecourse_obj, ses_dir, sub, ses)
                        get_dkt_t1w_space_image(
                            puptimecourse_obj, ses_dir, sub, ses)
                        if project == "DIAN":
                            get_suvr_t1w_space_image(
                                puptimecourse_obj, ses_dir, sub, ses, radiotracer)
                        elif project == "OASIS3":
                            
                        get_orig_pet_image(puptimecourse_obj, ses_dir, sub, ses)
                        get_orig_pet_info_file(
                            puptimecourse_obj, ses_dir, sub, ses)
    
                        print("Finished downloading images for: " + ses_of_interest)
                    else:
                        print("No PUP timecourse available for: " + ses_of_interest)
                else:
                    print(sub + " does not have a " + ses + " session")


if __name__ == "__main__":
    main()
