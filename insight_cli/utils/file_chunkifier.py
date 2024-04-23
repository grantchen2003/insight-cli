class FileChunkifier:
    @staticmethod
    def chunkify_file_content(
        file_content: bytes, chunk_size_bytes: int, first_chunk_size_bytes: int = 0
    ) -> list[bytes]:
        if first_chunk_size_bytes == 0:
            first_chunk_size_bytes = chunk_size_bytes

        file_size_bytes = len(file_content)
        file_content_chunks = []
        left, right = 0, first_chunk_size_bytes

        while left < file_size_bytes:
            right = min(right, file_size_bytes)
            file_content_chunks.append(file_content[left:right])
            left, right = right, right + chunk_size_bytes

        return file_content_chunks
