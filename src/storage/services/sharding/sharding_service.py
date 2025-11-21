import os
import secrets
import uuid
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class ShardingService:
    def shard_media(self, local_file_path: str):
        # Read file
        file_bytes = Path(local_file_path).read_bytes()
        shard_size = 256 * 1024  # 256kb
        shards = []

        # Split file
        for i in range(0, len(file_bytes), shard_size):
            chunk = file_bytes[i:i + shard_size]
            shards.append(chunk)

        # Generate one master key for entire video
        master_key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(master_key)

        # Scramble and encrypt shard
        shard_metadata = []
        for index, shard in enumerate(shards):
            scrambled_shard, mask = self.scramble_shard(shard)

            nonce = secrets.token_bytes(12)

            encrypted_shard = aesgcm.encrypt(nonce=nonce, data=scrambled_shard, associated_data=None)
            shared_name = self.shard_name(index)

            self.upload_shard(encrypted_shard, shared_name)

            shard_metadata.append({
                'nonce': nonce,
                'shard': shared_name,
                'mask': mask.hex(),
            })

    def scramble_shard(self, shard, index: int) -> tuple[bytes, bytes]:
        print(type(shard))
        mask = os.urandom(1)  # 1 byte mask
        scrambled = bytearray()

        mask_bit = index
        while mask_bit > 7:
            digits = list(map(int, str(mask_bit)))
            sum_digit = 0
            for digit in digits:
                sum_digit += digit

            if mask_bit == sum_digit:
                sum_digit = sum_digit - 1

            mask_bit = sum_digit

        for byte in shard:
            result = byte ^ mask[mask_bit]  # XOR
            result = ((result << 3) | (result >> 5)) & 0xFF  # Rotate left 3 bits
            scrambled.append(result)

        return (bytes(scrambled), mask)

    def upload_shard(self, encrypted_shard, shared_name: str):
        print(type(encrypted_shard))

    def shard_name(self, index: int) -> str:
        name = str(uuid.uuid4())
        name = name[0:12] + str(index) + name[13:]
        name = f'{name}.dar.io'
        return name
