class FileManagerInterface:
    """FileManagerInterface defines interface for handling read/write
    files to its asset/meta storage inside tintin's projects
    """

    def list(self, prefix: str) -> [str]:
        """list: list all elements (including files and dirs) under the prefix

        Args:
            prefix (str): prefix

        Returns:
            [str]:
        """
        pass

    def upload(self, prefix: str, local_dir: str):
        """upload: upload all files under $local_dir to its desitnation
        $prefix.

        For example, if the given $prefix is '/testupload' and $local_dir is '/testdata'
        , then the destination would be `/testupload/testdata/...`


        Args:
            prefix (str): prefix
            local_dir (str): local_dir
        """
        pass

    def download(self, dst: str, filepaths: [str], recursive: bool = False):
        """download: download the files defined in $filepaths to local with
        path $dst.
        Use recursive = True if you want to fetch all subfiles inside a dir.

        For example, if the given dst is `/tmp` and filepaths is
        `['/testupload/testdata']` with recursive = `True`
        , then the `testdata` folder will be downloaded to `/tmp/testupload/testdata`

        Args:
            dst (str): dst
            filepaths ([str]): filepaths
            recursive (bool): recursive
        """
 

