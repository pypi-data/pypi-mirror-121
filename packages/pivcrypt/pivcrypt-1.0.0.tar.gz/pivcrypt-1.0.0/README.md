# PivCrypt - File encryption package using PIV Applet

## Installation
`pip install --upgrade pivcrypt`

## Prerequisities
1. Security key or card with PIV Applet installed.
2. RSA2048 key+certificate in PIV slot
    * Generated selfsigned RSA2048 certificate in PIV applet using PIV Manager. This is recommended for 1 key scenario.
    * or Offcard generated private key and public certificate injected in PIV slot. Offcard keys can be backuped and restore to new security keys or cloned in multiple PIV applets, so many users can share the decryption key.

## Usage
```
$ py -m pivcrypt
Usage: python -m pivcrypt [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  decrypt      Decrypt file
  encrypt      Encrypt file
  export-cert  Export certificate used for future encryption
  serve        Encryption/decryption service
```
Default PIV slot for all operations is `9D`

### Export public certificate from PIV slot
```
$ py -m pivcrypt export-cert --help
Usage: python -m pivcrypt export-cert [OPTIONS] CERT

  Export certificate used for future encryption

Options:
  -r, --reader TEXT  When using NFC reader, set it's device name,
                     default="Crayonic KeyVault"
  -s, --slot TEXT    PIV slot to be used for file encryption, default=9D
  --help             Show this message and exit.
```
Export certificate to `cert.crt`
```
$ py -m pivcrypt export-cert cert.crt
Available smartcard readers: Crayonic KeyVault 0
Selected reader: Crayonic KeyVault 0
Exported cert from slot 9D stored as cert.crt
```

### Use cert file to encrypt desired file
```
$ py -m pivcrypt encrypt --help
Usage: python -m pivcrypt encrypt [OPTIONS] FILE

  Encrypt file

Options:
  -c, --cert TEXT         Certificate with public key  [required]
  -ext, --extension TEXT  Extension for encrypted file, default="kvef"
  --delete                Deletes original file after succesful encryption
  --help                  Show this message and exit.
```
Encrypt file `cat.jpg` with public key from cert `cert.crt`
```
$ py -m pivcrypt encrypt cat.jpg -c cert.crt
* Encrypting cat.jpg to cat.jpg.kvef

```

### Decrypt file with PIV
```
$ py -m pivcrypt decrypt --help
Usage: python -m pivcrypt decrypt [OPTIONS] FILE

  Decrypt file

Options:
  -r, --reader TEXT       When using NFC reader, set it's device name,
                          default="Crayonic KeyVault"
  -ext, --extension TEXT  Extension for encrypted file, default="kvef"
  -s, --slot TEXT         PIV slot to be used for file encryption, default=9D
  --pin-mode TEXT         CMD -commandline mode, GUI -graphical window
                          (default)
  --help                  Show this message and exit.
```
Decrypt file `cat.jpg`
```
$ py -m pivcrypt decrypt cat.jpg
Available smartcard readers: Crayonic KeyVault 0
Selected reader: Crayonic KeyVault 0
Waiting for PIN input
* Decrypting file cat.jpg
* Decrypted file cat.jpg
```

### Service mode for continus encryption/decryption
```
$ py -m pivcrypt serve --help
Usage: python -m pivcrypt serve [OPTIONS] FILE

  Encryption/decryption service

Options:
  -r, --reader TEXT       When using NFC reader, set it's device name,
                          default="Crayonic KeyVault"
  -c, --cert TEXT         Certificate with public key  [required]
  -ext, --extension TEXT  Extension for encrypted file, default="kvef"
  -s, --slot TEXT         PIV slot to be used for file encryption, default=9D
  --pin-mode TEXT         CMD -commandline mode, GUI -graphical window
                          (default)
  --help                  Show this message and exit.
```

Encrypt file `cat.jpg` when Crayonic KeyVault is disconnected and decrypt it back after KeyVault is connected and correct PIN is entered. This is intented to run as a service on PC to keep contents of given file secret.
```
py -m pivcrypt serve cat.jpg -c cert.crt -r "Crayonic KeyVault"
Available smartcard readers: Crayonic KeyVault 0
Selected reader: Crayonic KeyVault 0
Waiting for PIN input
* Decrypting file cat.jpg
* Decrypted file cat.jpg
Available smartcard readers:
* Encrypting file cat.jpg
* Encrypted file cat.jpg
Available smartcard readers: Crayonic KeyVault 0
Selected reader: Crayonic KeyVault 0
Waiting for PIN input
* Decrypting file cat.jpg
* Decrypted file cat.jpg
* Encrypting file cat.jpg
* Encrypted file cat.jpg
```