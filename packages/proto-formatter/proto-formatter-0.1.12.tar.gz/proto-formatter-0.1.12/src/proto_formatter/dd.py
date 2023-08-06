from src.proto_formatter import format_str

proto_str = """
message DeviceInfo {
    /*
    **    A characteristic string that lets servers and network peers identify the application, operating system, vendor, and/or version of the requesting
    **    example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
    **    This field can be empty.
    */
    string user_agent             = 1 [(validate.rules).any.required = true];
    common.DeviceType device_type = 2 [(validate.rules).message.required = true];   // The type of device, e.g. desktop, tablet, mobile
    string user_ip_address        = 3;                                             // Ip address for user's device
}
"""
formatted_proto_str = format_str(proto_str, align_by_equal_sign=True, comment_max_length=120, indents=4)
print(formatted_proto_str)