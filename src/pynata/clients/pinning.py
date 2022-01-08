from pathlib import Path

from pynata.clients.base import PinataClient
from pynata.response import PinataResponse


class PinningClient(PinataClient):
    def pin_file(self, file_path: Path) -> PinataResponse:
        """
        Add and pin any file, or directory, to Pinata's IPFS nodes.

        Args:
            file_path (pathlib.Path): The path to the file to pin.

        Returns:
            :class:`~pynata.response.PinataResponse`
        """
        paths = [f for f in file_path.iterdir()] if file_path.is_dir() else [file_path]
        files = (
            [("file", (str(path), open(path, "rb"))) for path in paths]
            if file_path.is_dir()
            else [("file", open(path, "rb")) for path in paths]
        )
        return self.session.post("pinning/pinFileToIPFS", files=files)

    def unpin(self, content_hash: str) -> PinataResponse:
        """
        Unpin content they previously uploaded to Pinata's IPFS nodes.

        Args:
            content_hash (str): The hash of the content to stop pinning.

        Returns:
            :class:`~pynata.response.PinataResponse`
        """
        url = f"/pinning/unpin/{content_hash}"
        return self.session.delete(url)


__all__ = ["PinningClient"]
