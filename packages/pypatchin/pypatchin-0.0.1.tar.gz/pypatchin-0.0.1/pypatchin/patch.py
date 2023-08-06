from diff_match_patch import diff_match_patch
import os

# Patch files


# DIFF FOR STRINGS
def compute_diff_from_strings(old_value, new_value):
    # Create diff string
    dmp = diff_match_patch()
    patches = dmp.patch_make(old_value, new_value)
    diff = dmp.patch_toText(patches)
    # print("DIFF \n######################")
    # print(diff)
    return diff


def apply_diff_to_string(string_to_patch, diff):
    # Apply diff
    dmp = diff_match_patch()
    patches = dmp.patch_fromText(diff)
    new_text, _ = dmp.patch_apply(patches, string_to_patch)
    # print(new_text)
    return new_text


def read_file_to_text(file_path):
    file = open(file_path, "r")
    s = ''
    for line in file:
        s = s + line
    return s


# DIFF FOR FILES
def compute_and_save_patch_from_file(original_dir, original_file, latest_dir, latest_file, patch_dir, patch_file):
    # Create diff string

    # Should automatically add extension .patch to patch_file

    original_path = original_dir + original_file
    latest_path = latest_dir + latest_file

    patch_path = patch_dir + patch_file + ".patch"

    original_text = read_file_to_text(original_path)
    latest_text = read_file_to_text(latest_path)

    diff = compute_diff_from_strings(original_text, latest_text)

    # Check directory structure exists otherwise it creates the path
    os.makedirs(os.path.dirname(patch_path), exist_ok=True)

    with open(patch_path, "w") as open_file:
        open_file.write(diff)


def apply_patch_to_file(dir_to_patch, file_to_patch, patch_dir, patch_file, patched_file_dir, patched_file):
    # Apply diff saved into patch_file!

    # Should automatically add extension .patch to patch_file

    patch_path = patch_dir + patch_file + ".patch"
    with open(patch_path, "r") as open_file:
        diff_to_apply = open_file.read()

    path_to_patch = dir_to_patch + file_to_patch
    old_text = read_file_to_text(path_to_patch)

    new_text = apply_diff_to_string(old_text, diff_to_apply)

    patched_file_path = patched_file_dir + patched_file

    # Check directory structure exists otherwise it creates the path
    os.makedirs(os.path.dirname(patched_file_path), exist_ok=True)

    with open(patched_file_path, "w") as open_file:
        open_file.write(new_text)


def compute_and_save_patches_for_list_of_files(list_of_files, original_dir, latest_dir, patches_dir):
    # Search a list of file inside original_dir and latest_dir,
    # compute patches and save them with the same names inside patched_file_dir

    # CHECK DIRECTORIES EXIST INSIDE patches_dir, OTHERWISE CREATE THEM
    for f in list_of_files:
        compute_and_save_patch_from_file(original_dir, f, latest_dir, f, patches_dir, f)


def apply_all_patches_to_files(list_of_files, patches_dir, original_dir, generated_dir):
    # Search all patches of list_of_files inside patched_files_dir and apply them to original_dir,
    # save all generated files inside generated_dir with the same names (and paths)

    for f in list_of_files:
        apply_patch_to_file(original_dir, f, patches_dir, f, generated_dir, f)
