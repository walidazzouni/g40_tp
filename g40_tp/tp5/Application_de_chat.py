import socket
import sys
import time
from struct import pack

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        if i + 1 < len(msg):
            w = (msg[i] << 8) + msg[i + 1]
        else:
            w = msg[i] << 8
        s += w
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xFFFF
    return s

def create_ip_header(ip_source, ip_dest):
    ip_version   = 4
    ip_ihl       = 5
    ip_tos       = 0
    ip_total_len = 0
    ip_id        = 54321
    ip_frag_off  = 0
    ip_ttl       = 255
    ip_proto     = socket.IPPROTO_TCP
    ip_check     = 0
    ip_saddr     = socket.inet_aton(ip_source)
    ip_daddr     = socket.inet_aton(ip_dest)
    ip_ihl_ver   = (ip_version << 4) + ip_ihl
    ip_header    = pack('!BBHHHBBH4s4s',
                        ip_ihl_ver, ip_tos, ip_total_len, ip_id,
                        ip_frag_off, ip_ttl, ip_proto, ip_check,
                        ip_saddr, ip_daddr)
    return ip_header

def create_tcp_header(message, ip_source, ip_dest):
    tcp_source     = 1234
    tcp_dest       = 80
    tcp_seq        = 454
    tcp_ack_seq    = 0
    tcp_doff       = 5
    tcp_fin        = 0
    tcp_syn        = 1
    tcp_rst        = 0
    tcp_psh        = 0
    tcp_ack        = 0
    tcp_urg        = 0
    tcp_window     = socket.htons(5840)
    tcp_check      = 0
    tcp_urg_ptr    = 0
    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags      = (tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) +
                      (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5))
    tcp_header     = pack('!HHLLBBH',
                          tcp_source, tcp_dest, tcp_seq, tcp_ack_seq,
                          tcp_offset_res, tcp_flags, tcp_window)
    source_address = socket.inet_aton(ip_source)
    dest_address   = socket.inet_aton(ip_dest)
    placeholder    = 0
    protocol       = socket.IPPROTO_TCP
    tcp_length     = len(tcp_header) + len(message)
    psh            = pack('!4s4sBBH',
                          source_address, dest_address,
                          placeholder, protocol, tcp_length)
    tcp_check      = checksum(psh + tcp_header + message.encode('utf-8'))
    tcp_header     = (pack('!HHLLBBH',
                           tcp_source, tcp_dest, tcp_seq, tcp_ack_seq,
                           tcp_offset_res, tcp_flags, tcp_window) +
                      pack('H', tcp_check) +
                      pack('!H', tcp_urg_ptr))
    return tcp_header

def create_packet(ip_header, tcp_header, message):
    return ip_header + tcp_header + message.encode('utf-8')

if __name__ == '__main__':
    ip_source  = '127.0.0.1'
    ip_dest    = '127.0.0.1'
    message    = 'Hello, how are you'
    s          = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    ip_header  = create_ip_header(ip_source, ip_dest)
    tcp_header = create_tcp_header(message, ip_source, ip_dest)
    packet     = create_packet(ip_header, tcp_header, message)
    print(f"Entête IP    : {len(ip_header)} bytes")
    print(f"Entête TCP   : {len(tcp_header)} bytes")
    print(f"Paquet total : {len(packet)} bytes")
    s.sendto(packet, (ip_dest, 0))
    print("Paquet envoyé avec succès !")
    s.close()