# pypatchin

Do you want a fast and clean solution to patch your files and repositories? Use me, a Python **pypatchin** package!

I can patch your text, your files and your entire repositories. To do so, I rely on the high performance patching library [diff-match-patch](https://github.com/google/diff-match-patch), making it accessible via Python code.

## How to use

This project requires the diff-match-patch package:

```
pip install diff-match-patch
```


There are 2 main methods provided:
```
from pypatchin import patch

patch.compute_and_save_patches_for_list_of_files(all_files_to_patch, original_dir_name, latest_dir_name, patch_dir_name)
patch.apply_all_patches_to_files(all_files_to_patch, patch_dir_name, original_dir_name, patched_file_dir_name)
```

To compute patches for a list of files and to apply these patches to the same list of files.

Also, a method for checking the working is provided:
```
from pypatchin import compare

result = compare.compare_latest_vs_generated_list_of_files(all_files_to_patch, latest_dir_name, generated_dir_name)
```


## Examples

See ``try_me.py`` and ``check_me.py`` scripts inside the example directory. They work on the sample repository inside original and latest directories.

## Extras

Patch a text:

```
tmp_diff = compute_diff_from_strings("Test old text.", "Test new text.")
apply_diff_to_string("Text ole text", tmp_diff)
```

Patch a single file:

```
compute_and_save_patch_from_file(original_dir_name, original_file_name, latest_dir_name, latest_file_name, patch_dir_name, patch_file_name)
apply_patch_to_file(original_dir_name, original_file_name, patch_dir_name, patch_file_name, patched_file_dir_name, patched_file_name)
```

## Tests
No tests present for now.

## Contribute
Pull Requests are welcome.

Ensure the PR description clearly describes the problem and solution. It should include:

* Name of the module modified
* Reasons for modification
