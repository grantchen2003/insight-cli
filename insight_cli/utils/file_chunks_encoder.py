import base64


class FileChucksEncoder:
    @staticmethod
    def utf8_encode(file_content_chunks: list[bytes]) -> list[dict]:
        return [
            {
                "content": base64.b64encode(file_content_chunk).decode("utf-8"),
                "size_bytes": len(file_content_chunk),
                "chunk_index": i,
                "num_total_chunks": len(file_content_chunks),
            }
            for i, file_content_chunk in enumerate(file_content_chunks)
        ]
