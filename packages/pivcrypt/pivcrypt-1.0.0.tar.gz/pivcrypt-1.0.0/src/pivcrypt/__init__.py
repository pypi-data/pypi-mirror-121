import smartcard
import os
import hmac
import hashlib
from time import sleep
from pprint import pprint
import click
import tkinter as tk
from tkinter import simpledialog
from getpass import getpass

from binascii import hexlify, unhexlify
from base64 import urlsafe_b64decode, urlsafe_b64encode

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from .fido_applet import PivApplet

ROOT = tk.Tk()
ROOT.withdraw()

def ask_for_pin(prompt, mode='GUI'): 
    if mode == 'GUI':
        ROOT.update_idletasks()
        ROOT.overrideredirect(True)
        ROOT.lift()
        ROOT.focus_force()
        return simpledialog.askstring(
            title="Enter PIN",
            prompt=prompt,
            show="⚫"
        )
    else: # mode 'CMD'
        return getpass(f"{prompt}: ")


backend = default_backend()

SLOT_TAGS = {
    0x9E: PivApplet.TAG_CERT_9E,
    0x9A: PivApplet.TAG_CERT_9A,
    0x9C: PivApplet.TAG_CERT_9C,
    0x9D: PivApplet.TAG_CERT_9D,
}

def uniform_slot(slot):
    if isinstance(slot, int):
        return slot
    elif isinstance(slot, str):
        return int.from_bytes(unhexlify(slot), byteorder='big')
    else:
        raise Exception(f"Slot should be int or str, but is {type(slot)} = {slot}")

def slot_to_tag(slot):
    return SLOT_TAGS[uniform_slot(slot)]

def get_applet(reader_name):
    try:
        readers = smartcard.System.readers()
        print("Available smartcard readers:", ", ".join(str(r) for r in readers))
        for reader in readers:
            if reader_name in str(reader):
                connection = reader.createConnection()
                connection.connect()
                atr = connection.getATR()
                SELECT_PIV = [
                    0x00, 0xA4, 0x04, 0x00, 0x0B, 
                    0xA0, 0x00, 0x00, 0x03, 0x08, 0x00, 0x00, 0x10, 0x00, 0x01, 0x00]
                data, *sw = connection.transmit(SELECT_PIV)
                assert sw == [0x90, 0x00]
                print("Selected reader:", reader)
                # print(reader, hexlify(bytes(atr)).decode().upper())
                return PivApplet(connection, debug=False)
        else:
            return None
    except smartcard.Exceptions.SmartcardException as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None

def wait_for_reader_change(readers_fingerprint):
    readers = None
    while True:
        try:
            readers = smartcard.System.readers()
        except Exception as e:
            print(e)
            readers = readers_fingerprint
        if readers_fingerprint == str(readers):
            sleep(1)
            continue
        else:
            return str(readers)

def encrypt_file(filename: str, enc_filename: str, encrypted_key: bytes, key: bytes):
    # print("key", len(key), hexlify(key))
    f = Fernet(urlsafe_b64encode(key))
    with open(filename, "rb") as file:
        with open(enc_filename, "wb") as encrypted_file:
            encrypted_file.write(b"KVEF")
            encrypted_file.write(b'\x01') # version
            encrypted_file.write(len(encrypted_key).to_bytes(byteorder='big', length=2))
            encrypted_file.write(encrypted_key)
            encrypted_file.write(urlsafe_b64decode(f.encrypt(file.read())))


def decrypt_file(filename: str, enc_filename: str, decrypt_key_callback):
    with open(enc_filename, "rb") as encrypted_file:
        assert encrypted_file.read(4) == b"KVEF"
        version = encrypted_file.read(1)
        if version == b'\x01':
            encrypted_key_length = int.from_bytes(encrypted_file.read(2), byteorder="big")
            encrypted_key = encrypted_file.read(encrypted_key_length)
            # print("encrypted_key", hexlify(encrypted_key))
            key = decrypt_key_callback(encrypted_key)
            # print("key", key, hexlify(urlsafe_b64decode(key)), len(urlsafe_b64decode(key)))
            f = Fernet(key)
            decrypted_file_data = f.decrypt(urlsafe_b64encode(encrypted_file.read()))
            with open(filename, "wb") as file:
                file.write(decrypted_file_data)
        else: 
            raise Exception(f"Unsupported KVEF version {version}")



def encryption_service(
        filename, 
        public_key,
        slot,
        encrypted_extension="kvef", 
        reader_name="Crayonic KeyVault",
        pin_mode='cmd'
    ):
    enc_filename = f"{filename}.{encrypted_extension}"
    applet = None
    readers_fingerprint = None

    def do_encryption():
        nonlocal public_key
        key = urlsafe_b64decode(Fernet.generate_key())
        encrypted_key = public_key.encrypt(key, padding.PKCS1v15())

        # encrypt file
        try:
            print(f"* Encrypting file {filename}")
            encrypt_file(filename, enc_filename, encrypted_key, key)
            print(f"* Encrypted file {filename}")
            if filename != enc_filename:
                os.remove(filename)
        except FileNotFoundError:
            print(f"* File {filename} do not exist, assuming it is already encrypted")

    def do_decryption():
        nonlocal applet
        try:
            def decrypt_key(encrypted_key: bytes):
                return urlsafe_b64encode(applet.genAuth(
                    PivApplet.PIV_ALG_RSA2048, 
                    slot, 
                    unhexlify("7c820106820081820100") + encrypted_key
                ).body[-32:])
            
            # decrypt file
            # applet.authPin('123456')
            click.echo("Waiting for PIN input")
            applet.authPin(
                ask_for_pin(prompt=f"Enter PIN to decrypt {filename}", mode=pin_mode)
            )
            print(f"* Decrypting file {filename}")
            decrypt_file(filename, enc_filename, decrypt_key)
            print(f"* Decrypted file {filename}")
        except Exception as e:
            print(e)

    # Encryption/decryption loop
    while True:
        try:
            readers_fingerprint = wait_for_reader_change(readers_fingerprint)
            applet = get_applet(reader_name)
            sleep(1) # TODO some race condition after kv inserted in USB
            if applet is None:
                do_encryption()
            else:
                do_decryption()
        except KeyboardInterrupt:
            do_encryption()
            exit()


def load_public_key(cert):
    with open(cert, 'rb') as certfile:
        cert_x509 = cryptography.x509.load_der_x509_certificate(certfile.read())
        # click.echo(cert_x509.serial_number)
        # click.echo(cert_x509.subject)
        # click.echo(cert_x509.issuer)
        # click.echo(cert_x509.not_valid_before, cert_x509.not_valid_after)
        # click.echo(cert_x509.extensions)
        public_key = cert_x509.public_key()
        return public_key

option_slot = click.option(
    '--slot', '-s', 
    default='9D', 
    help='PIV slot to be used for file encryption, default=9D',
    callback=lambda ctx,self,value: uniform_slot(value)
)
option_reader = click.option('--reader', '-r', default='Crayonic KeyVault', help='When using NFC reader, set it\'s device name, default="Crayonic KeyVault"')
option_extension = click.option('--extension', '-ext', default='kvef', help='Extension for encrypted file, default="kvef"')
option_cert = click.option('--cert', '-c', required=True, help='Certificate with public key')
option_pin_mode = click.option('--pin-mode', default='GUI', help='CMD -commandline mode, GUI -graphical window (default)')
arg_file = click.argument('file')
arg_cert = click.argument('cert')

@click.group()
# @click.option('--verbose', '-v', is_flag=True)
def cli():
    pass
    # if verbose:
    #     click.echo('Verbose mode on')

@cli.command(help="Encryption/decryption service")
@option_reader
@option_cert
@option_extension
@option_slot
@option_pin_mode
@arg_file
def serve(reader, extension, slot, file, cert, pin_mode):
    
    with open(cert, 'rb') as certfile:
        cert = cryptography.x509.load_der_x509_certificate(certfile.read())
        public_key = cert.public_key()

    encryption_service(
        file, 
        public_key,
        slot,
        encrypted_extension=extension, 
        reader_name=reader,
        pin_mode=pin_mode
    )

@cli.command(help="Export certificate used for future encryption")
@option_reader
@arg_cert
@option_slot
def export_cert(reader, slot, cert):
    applet = get_applet(reader)
    response = applet.getData(slot_to_tag(slot))
    # print("CERT:", hexlify(response.body))

    cert_bytes = response.body[8:-5]
    # print("CERT bytes:", hexlify(cert_bytes))

    cert_x509 = cryptography.x509.load_der_x509_certificate(cert_bytes)
    # click.echo(cert_x509.serial_number)
    # click.echo(cert_x509.subject)
    # click.echo(cert_x509.issuer)
    # click.echo(cert_x509.not_valid_before, cert_x509.not_valid_after)
    # click.echo(cert_x509.extensions)
    public_key = cert_x509.public_key()
    with open(cert, 'wb') as certout:
        certout.write(cert_bytes)
    # print(public_key)
    click.echo(f"Exported cert from slot {slot:X} storead as {cert}")

@cli.command(help="Encrypt file")
@option_cert
@option_extension
@arg_file
@click.option('--delete', is_flag=True, help="Deletes original file after succesful encryption")
def encrypt(file, cert, extension, delete):
    encrypted_file = f'{file}.{extension}'
    public_key = load_public_key(cert)
    key = urlsafe_b64decode(Fernet.generate_key())
    encrypted_key = public_key.encrypt(key, padding.PKCS1v15())
    click.echo(f"* Encrypting {file} to {encrypted_file}")
    encrypt_file(file, encrypted_file, encrypted_key, key)
    if delete and file != encrypted_file:
        click.echo(f"Deleting {file}")
        os.remove(file)

@cli.command(help="Decrypt file")
@option_reader
@option_extension
@option_slot
@option_pin_mode
@arg_file
def decrypt(reader, slot, file, extension, pin_mode):
    applet = get_applet(reader)
    if file.endswith(extension):
        encrypted_file = file
        file = encrypted_file.rstrip(f'.{extension}')
    else:
        encrypted_file = f'{file}.{extension}'

    def decrypt_key(encrypted_key: bytes):
        return urlsafe_b64encode(applet.genAuth(
            PivApplet.PIV_ALG_RSA2048, 
            slot,
            unhexlify("7c820106820081820100") + encrypted_key
        ).body[-32:])
    
    try:
        # decrypt file
        click.echo("Waiting for PIN input")
        applet.authPin(ask_for_pin(F"Enter PIN", mode=pin_mode))
        click.echo(f"* Decrypting file {file}")
        decrypt_file(file, encrypted_file, decrypt_key)
        click.echo(f"* Decrypted file {file}")
    except cryptography.fernet.InvalidToken as e:
        click.echo("Decryption error {e}.")


if __name__ == "__main__":
    cli()
    # encryption_service("cat.webp")