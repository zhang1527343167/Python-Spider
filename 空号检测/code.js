var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
function base64encode(a) {
    var c, i, h, _, g, v;
    for (h = a.length,
    i = 0,
    c = ""; h > i; ) {
        if (_ = 255 & a.charCodeAt(i++),
        i == h) {
            c += base64EncodeChars.charAt(_ >> 2),
            c += base64EncodeChars.charAt((3 & _) << 4),
            c += "==";
            break
        }
        if (g = a.charCodeAt(i++),
        i == h) {
            c += base64EncodeChars.charAt(_ >> 2),
            c += base64EncodeChars.charAt((3 & _) << 4 | (240 & g) >> 4),
            c += base64EncodeChars.charAt((15 & g) << 2),
            c += "=";
            break
        }
        v = a.charCodeAt(i++),
        c += base64EncodeChars.charAt(_ >> 2),
        c += base64EncodeChars.charAt((3 & _) << 4 | (240 & g) >> 4),
        c += base64EncodeChars.charAt((15 & g) << 2 | (192 & v) >> 6),
        c += base64EncodeChars.charAt(63 & v)
    }
    return c
}




function GetCode(phone) {
    code = base64encode(phone);
    return code
}