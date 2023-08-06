from src.proto_formatter import format_str

proto_str = """
    /*
    * *
                 *Person balabala
        **         asdas
        
*/
/* I'am a comment */
    message Person {
       string locale            = 3 [(validate.rules).string.pattern = "^[a-z]{2}-[A-Z]{2}$"];   // ISO 639-2 language code & ISO 3166-1 country code. e.g. en-US, en-GB
}
"""
formatted_proto_str = format_str(proto_str, align_by_equal_sign=True, comment_max_length=120)
print(formatted_proto_str)