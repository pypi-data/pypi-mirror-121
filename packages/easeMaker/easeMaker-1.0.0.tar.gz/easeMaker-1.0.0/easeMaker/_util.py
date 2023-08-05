class ByteEngine:
    def str_to_hex(self,str,decoding="utf-8"):
        import binascii
        str_val = str.encode('utf-8')
        hex_val = binascii.hexlify(str_val).decode(decoding)
        return hex_val 
    def hex_to_str(self,hex_val,decoding="utf-8"):
        return bytes.fromhex(hex_val).decode(decoding)   
    def to_hexadecimal(self,str_value,decoding="utf-8"):
        import binascii
        str_val = str_value.encode('utf-8')
        hex_val = binascii.hexlify(str_val).decode(decoding)   
        return hex_val
    def to_bytes(self,string):
        import binascii
        from binascii import unhexlify
        str_val = string.encode('utf-8')
        hex_val = binascii.hexlify(str_val).decode('utf-8')
        return unhexlify(hex_val)
 
         