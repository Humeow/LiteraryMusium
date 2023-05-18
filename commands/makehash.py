import hashlib

hashmake_repeat = 2

class hash_funcs:
    @staticmethod
    def hash_make(text, hash_count=hashmake_repeat):
        global hashmake_repeat

        for x in range(hash_count):
            result = hashlib.sha256(text.encode())
            text = result.hexdigest()

        return text

    @staticmethod
    def hash_compare(text, hash_text, hash_count=hashmake_repeat):
        global hashmake_repeat

        for x in range(hash_count):
            result = hashlib.sha256(text.encode())
            text = result.hexdigest()

        if text == hash_text:
            return True

        return False